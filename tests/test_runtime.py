from reliable_agent.core import *
def S(c=False):return State(run_id="r",call=Call(tool="write",consequential=c))
def test_uncertain_write_verified_before_retry():
 s=S();external={"done":False};n={"x":0}
 def tool():n["x"]+=1;external["done"]=True;raise AmbiguousOutcome("response lost")
 run(s,tool,lambda c,r:external["done"]);assert s.status==Status.SUCCEEDED and n["x"]==1
def test_approval():
 s=S(True);execute(s,lambda:1,lambda c,r:True);assert s.status==Status.APPROVAL
 approve(s,"human");execute(s,lambda:1,lambda c,r:True);assert s.status==Status.SUCCEEDED
def test_unresolved_consequential_escalates():
 s=S(True);approve(s,"human");execute(s,lambda:1,lambda c,r:False);assert s.status==Status.HUMAN_REVIEW
def test_bounded_retries():
 s=S();s.max_attempts=2;run(s,lambda:(_ for _ in()).throw(RuntimeError("x")),lambda c,r:False);assert s.attempts==2 and s.status==Status.FAILED
def test_checkpoint_resume():
 s=S();s.attempts=1;d=Checkpoints();d.save(s);assert d.load("r").attempts==1
