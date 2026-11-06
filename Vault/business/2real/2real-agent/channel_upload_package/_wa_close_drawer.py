import json, time, urllib.request, websocket
CDP_HTTP = "http://127.0.0.1:9222"
def list_tabs():
    with urllib.request.urlopen(CDP_HTTP + "/json", timeout=10) as r:
        return json.load(r)
cands = [t for t in list_tabs() if t.get("type")=="page" and t.get("url","").startswith("https://web.whatsapp.com")]
for t in cands:
    if "WhatsApp" in t.get("title",""): TAB=t; break
else: TAB=cands[0]
WS=websocket.create_connection(TAB["webSocketDebuggerUrl"].replace("localhost","127.0.0.1"),timeout=60,suppress_origin=True)
_seq=[0]
def _send(m,**p):
    _seq[0]+=1; WS.send(json.dumps({"id":_seq[0],"method":m,"params":p}))
    while True:
        msg=json.loads(WS.recv())
        if msg.get("id")==_seq[0]: return msg
def js(expr):
    r=_send("Runtime.evaluate",expression=expr,returnByValue=True,awaitPromise=True)
    return r.get("result",{}).get("result",{}).get("value")
def ck(x,y):
    _send("Input.dispatchMouseEvent",type="mousePressed",x=int(x),y=int(y),button="left",clickCount=1)
    _send("Input.dispatchMouseEvent",type="mouseReleased",x=int(x),y=int(y),button="left",clickCount=1)
# close button / back in the drawer
r=js("""(() => {
  const b=[...document.querySelectorAll('button[aria-label],div[role=button][aria-label],span[aria-label]')].filter(e=>e.offsetParent!==null&&/close|back/i.test(e.getAttribute('aria-label')||''));
  return JSON.stringify(b.map(e=>{const r=e.getBoundingClientRect();return{label:(e.getAttribute('aria-label')||''),x:Math.round(r.x+r.width/2),y:Math.round(r.y+r.height/2)};}));
})()""")
print("close/back buttons:", r)
if r and r!="null":
    import json as J
    for b in J.loads(r):
        print("click",b); ck(b["x"],b["y"]); time.sleep(2)
        if js("document.querySelectorAll('div[contenteditable=true][aria-label=Name]').length")==0:
            print("closed"); break
print("drawer now:", js("(document.body.innerText||'').includes('Add images')"))
print("name fields:", js("document.querySelectorAll('div[contenteditable=true][aria-label=Name]').length"))