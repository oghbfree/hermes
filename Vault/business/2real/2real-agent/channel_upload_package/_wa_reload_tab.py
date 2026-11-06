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
_send("Page.reload")
print("reload sent")
time.sleep(2)
_send("Page.enable")
time.sleep(20)
# wait for whatsapp to render
head=_send("Runtime.evaluate",expression="(document.body.innerText||'').slice(0,200)",returnByValue=True)["result"].get("result",{}).get("value","")
print("after reload head:", head.replace(chr(10),' | '))