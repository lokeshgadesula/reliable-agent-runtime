from reliable_agent.core import *
from reliable_agent.adapters import langgraph_stages
def test_context_projection():assert project({"need":1,"secret":2},["need"])=={"need":1}
def test_workers():
 r=workers({"a":(lambda c:c["x"]+1,["x"]),"b":(lambda c:c["y"]*2,["y"])},{"x":1,"y":3,"unused":9});assert r["ok"] and r["results"]=={"a":2,"b":6}
def test_stale():assert stale(1,2) and not stale(2,2)
def test_token_metric():assert token_reduction(100000,52000)==48.0
def test_outcome_metric():
 s=State(run_id="x",call=Call(tool="x"),status=Status.SUCCEEDED,verified=True);assert outcome_score(s)==1
def test_graph_contract():assert langgraph_stages()[-2:] == ["checkpoint","continue_or_recover"]
