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
r=_send("Page.captureScreenshot",format="png")
data=r["result"]["data"]
out=r"C:/Users/User/.hermes/workspace/Vault/business/2real/2real-agent/channel_upload_package/_wa_state.png"
with open(out.replace("C:/","C:\\").replace("/","\\"),"wb") as f:
    f.write(base64.b64decode(data))
print("saved", out, len(data), "bytes")
# viewport
v=_send("Runtime.evaluate",expression="JSON.stringify({w:innerWidth,h:innerHeight,dpr:devicePixelRatio})",returnByValue=True)["result"]["result"]["value"]
print("viewport:",v)