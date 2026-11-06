import json, time, sys, urllib.request, websocket
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
def js(expr):
    r=_send("Runtime.evaluate",expression=expr,returnByValue=True,awaitPromise=True,timeout=60000)
    res=r.get("result",{})
    if "exceptionDetails" in res: return "EXC:"+str(res["exceptionDetails"].get("exception",{}).get("description",""))[:250]
    return res.get("result",{}).get("value")
def trusted_click(x,y):
    _send("Input.dispatchMouseEvent",type="mousePressed",x=int(x),y=int(y),button="left",clickCount=1)
    _send("Input.dispatchMouseEvent",type="mouseReleased",x=int(x),y=int(y),button="left",clickCount=1)

# Enumerate visible labelled left-rail buttons
print("RAIL:", js("""(() => {
  const out=[...document.querySelectorAll('[aria-label],[title]')].filter(e=>e.offsetParent!==null)
    .filter(e=>{const r=e.getBoundingClientRect();return r.width>10&&r.height>10;})
    .map(e=>{const r=e.getBoundingClientRect();return {label:(e.getAttribute('aria-label')||e.getAttribute('title')||'').slice(0,30),x:Math.round(r.x+r.width/2),y:Math.round(r.y+r.height/2),x0:Math.round(r.x)};})
    .filter(o=>o.x0<250);
  return JSON.stringify(out);
})()"""))
# what does the Tools click land on, and is panel open now?
print("BODY_SNIP:", (js("(document.body.innerText||'')") or "").replace(chr(10),' | ')[-350:])