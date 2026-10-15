class PostgresCheckpointAdapter:
 DDL="CREATE TABLE IF NOT EXISTS agent_checkpoints(run_id TEXT PRIMARY KEY,state JSONB NOT NULL,updated_at TIMESTAMPTZ DEFAULT now())"
class RedisIdempotencyAdapter:
 def __init__(self,client,ttl=86400):self.client=client;self.ttl=ttl
 def seen(self,k):return bool(self.client.exists("idem:"+k))
 def put(self,k,v):return self.client.set("idem:"+k,str(v),ex=self.ttl,nx=True)
class PlaywrightVerifier:
 def __init__(self,page):self.page=page
 def transition(self,selector,text):return self.page.locator(selector).is_visible() and text in self.page.locator(selector).inner_text()
 def screenshot(self,path):self.page.screenshot(path=path,full_page=True)
def langgraph_stages():return ["plan","validate","approve","execute","verify_effect","checkpoint","continue_or_recover"]
