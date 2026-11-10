# Reload the WA tab for a clean slate
import json, time, websocket, urllib.request
CDP="http://127.0.0.1:9222"
tabs=json.load(urllib.request.urlopen(CDP+"/json",timeout=10))
cands=[t for t in tabs if t.get("type")=="page" and t.get("url","").startswith("https://web.whatsapp.com")]
tab=[t for t in cands if "WhatsApp" in t.get("title","")][0]
WS=websocket.create_connection(tab["webSocketDebuggerUrl"].replace("localhost","127.0.0.1"),timeout=60,suppress_origin=True)
seq=[0]
def _send(m,**p):
    seq[0]+=1; WS.send(json.dumps({"id":seq[0],"method":m,"params":p}))
    while True:
        x=json.loads(WS.recv())
        if x.get("id")==seq[0]: return x
_send("Page.reload", ignoreCache=True)
time.sleep(8)
_send("Runtime.evaluate", expression="(document.body.innerText||'').slice(0,60)", returnByValue=True)
print("reloaded")
WS.close()