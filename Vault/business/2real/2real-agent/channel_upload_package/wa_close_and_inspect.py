# Close the stale drawer, then probe country control in a clean state
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
def js(expr):
    r=_send("Runtime.evaluate",expression=expr,returnByValue=True,awaitPromise=True,timeout=30000)
    if "exceptionDetails" in r.get("result",{}): return "EXC:"+json.dumps(r["result"]["exceptionDetails"].get("exception",{}))[:160]
    return r.get("result",{}).get("result",{}).get("value")
def cdp(m,**p): return _send(m,**p)
def trusted(x,y):
    cdp('Input.dispatchMouseEvent',type='mousePressed',x=int(x),y=int(y),button='left',clickCount=1)
    cdp('Input.dispatchMouseEvent',type='mouseReleased',x=int(x),y=int(y),button='left',clickCount=1)

# click Close button at (496,12) to dismiss stale drawer
trusted(496, 12); time.sleep(2)
print("drawer still open ('Add images'):", js("(document.body.innerText||'').includes('Add images')"))
print("body head:", repr(js("(document.body.innerText||'').slice(0,200)")))

# Now in clean catalogue state, probe country field: open Tools->Catalogue->Add new item fresh
# First check if still on catalogue. Enumerate country label current rect
print("country label:", js("[...document.querySelectorAll('*')].filter(e=>e.offsetParent!==null&&(e.textContent||'').trim().startsWith('Country of origin')&&e.children.length===0).map(e=>{const r=e.getBoundingClientRect();return {t:(e.textContent||'').trim(),x:Math.round(r.x),y:Math.round(r.y)}})"))
WS.close()