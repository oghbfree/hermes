import json, time, base64, urllib.request, websocket
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
    r=_send("Runtime.evaluate",expression=expr,returnByValue=True,awaitPromise=True)
    res=r.get("result",{})
    if "exceptionDetails" in res: return "EXC:"+str(res["exceptionDetails"].get("exception",{}).get("description",""))[:200]
    return res.get("result",{}).get("value")
# click add-item card at (315,112)
x,y=315,112
_send("Input.dispatchMouseEvent",type="mousePressed",x=x,y=y,button="left",clickCount=1)
_send("Input.dispatchMouseEvent",type="mouseReleased",x=x,y=y,button="left",clickCount=1)
print("clicked",x,y)
time.sleep(5)
print("drawer:", js("(document.body.innerText||'').includes('Add images')"))
print("name field:", js("document.querySelectorAll('div[contenteditable=true][aria-label=Name]').length"))
print("menu overflow:", js("[...document.querySelectorAll('[role=menu]')].filter(e=>e.offsetParent!==null).length"))
r=_send("Page.captureScreenshot",format="png")
open(r"C:/Users/User/.hermes/workspace/Vault/business/2real/2real-agent/channel_upload_package/_wa_after_click.png","wb").write(base64.b64decode(r["result"]["data"]))
print("shot saved")