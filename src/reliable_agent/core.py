from enum import Enum
from pydantic import BaseModel,Field
from typing import Any
from concurrent.futures import ThreadPoolExecutor,as_completed
class Status(str,Enum):
 PLANNED="planned";APPROVAL="approval";EXECUTING="executing";UNKNOWN="unknown";SUCCEEDED="succeeded";FAILED="failed";HUMAN_REVIEW="human_review"
class Call(BaseModel):
 tool:str;args:dict[str,Any]=Field(default_factory=dict);idempotency_key:str|None=None;consequential:bool=False
class State(BaseModel):
 run_id:str;call:Call;status:Status=Status.PLANNED;attempts:int=0;max_attempts:int=3;approved:bool=False;verified:bool=False;result:Any=None;errors:list[str]=Field(default_factory=list);trace:list[dict]=Field(default_factory=list)
class AmbiguousOutcome(Exception):pass
def event(s,name,**d):s.trace.append({"event":name,**d})
def execute(s,tool,verify):
 if s.call.consequential and not s.approved:s.status=Status.APPROVAL;event(s,"approval_required");return s
 s.attempts+=1;s.status=Status.EXECUTING;event(s,"tool_started",attempt=s.attempts)
 try:s.result=tool(**s.call.args)
 except AmbiguousOutcome as e:s.status=Status.UNKNOWN;s.errors.append(str(e));event(s,"ambiguous_outcome")
 except Exception as e:
  s.errors.append(str(e));s.status=Status.FAILED if s.attempts>=s.max_attempts else Status.PLANNED;return s
 s.verified=bool(verify(s.call,s.result))
 if s.verified:s.status=Status.SUCCEEDED;event(s,"effect_verified")
 elif s.call.consequential or s.attempts>=s.max_attempts:s.status=Status.HUMAN_REVIEW;event(s,"human_review")
 else:s.status=Status.PLANNED;event(s,"safe_retry")
 return s
def run(s,tool,verify):
 while s.status in (Status.PLANNED,Status.UNKNOWN) and s.attempts<s.max_attempts:
  execute(s,tool,verify)
  if s.status in (Status.SUCCEEDED,Status.HUMAN_REVIEW,Status.APPROVAL,Status.FAILED):break
 return s
def approve(s,actor):s.approved=True;event(s,"approved",actor=actor);return s
class Checkpoints:
 def __init__(self):self.d={}
 def save(self,s):self.d[s.run_id]=s.model_dump_json()
 def load(self,k):return State.model_validate_json(self.d[k])
class Idempotency:
 def __init__(self):self.d={}
 def seen(self,k):return k in self.d
 def put(self,k,v):self.d.setdefault(k,v)
def project(ctx,keys):return {k:ctx[k] for k in keys if k in ctx}
def workers(spec,ctx):
 out={};err={}
 with ThreadPoolExecutor(max_workers=4) as ex:
  fs={ex.submit(fn,project(ctx,keys)):name for name,(fn,keys) in spec.items()}
  for f in as_completed(fs):
   try:out[fs[f]]=f.result()
   except Exception as e:err[fs[f]]=str(e)
 return {"results":out,"errors":err,"ok":not err}
def stale(start,current):return start!=current
def token_reduction(base,opt):return round((base-opt)/base*100,2) if base else 0
def outcome_score(s):return 1.0 if s.status==Status.SUCCEEDED and s.verified else 0.0
def trajectory_score(actual,expected):
 return sum(a==b for a,b in zip(actual,expected))/max(1,max(len(actual),len(expected)))
