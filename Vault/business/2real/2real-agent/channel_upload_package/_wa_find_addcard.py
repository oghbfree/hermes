import json, time, urllib.request, websocket
CDP_HTTP = "http://127.0.0.1:9222"
def list_tabs():
    with urllib.request.urlopen(CDP_HTTP + "/json", timeout=10) as r:
        return json.load(r)
cands = [t for t in list_tabs() if t.get("type")=="page" and t.get("url","").startswith("https://web.whatsapp.com")]
for t in cands:
    if "WhatsApp" in t.get("title",""): TAB=t; break
else: TAB=cands[0]
print("TAB:",TAB["title"][:50])
WS=websocket.create_connection(TAB["webSocketDebuggerUrl"].replace("localhost","127.0.0.1"),timeout=60,suppress_origin=True)
_seq=[0]
def _send(m,**p):
    _seq[0]+=1; WS.send(json.dumps({"id":_seq[0],"method":m,"params":p}))
    while True:
        msg=json.loads(WS.recv())
        if msg.get("id")==_seq[0]: return msg
r=_send("Runtime.evaluate",expression="""(() => {
  const nodes=[...document.querySelectorAll('*')].filter(e=>(e.textContent||'').trim()==='Add new item'&&e.children.length===0)
    .map(e=>{const r=e.getBoundingClientRect();return{x:Math.round(r.x+r.width/2),y:Math.round(r.y+r.height/2),x0:Math.round(r.x),y0:Math.round(r.y),w:Math.round(r.width),h:Math.round(r.height),tag:e.tagName,role:e.getAttribute('role'),vis:e.offsetParent!==null};});
  return JSON.stringify(nodes);
})()""",returnByValue=True)["result"]["result"]["value"]
print("add-item nodes:",r)