# Close stale Add-item drawer without saving + inspect clean country field
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

print("drawer open:", js("(document.body.innerText||'').includes('Add images')"))
# enumerate close buttons
print("close buttons:", js("[...document.querySelectorAll('button[aria-label],div[aria-label],button,div[role=button]')].filter(e=>e.offsetParent!==null&&/close|back|x/i.test(e.getAttribute('aria-label')||'')).map(e=>{const r=e.getBoundingClientRect();return {t:(e.getAttribute('aria-label')||e.textContent||'').trim().slice(0,20),x:Math.round(r.x),y:Math.round(r.y)}}).slice(0,8)"))
# find visible Close/back arrow via aria-label exact
r=js("[...document.querySelectorAll('[aria-label]')].filter(e=>e.offsetParent!==null&&(e.getAttribute('aria-label').trim().toLowerCase()==='close'||e.getAttribute('aria-label').trim().toLowerCase()==='close window'||/^close/i.test(e.getAttribute('aria-label')))).map(e=>{const rc=e.getBoundingClientRect();return {t:e.getAttribute('aria-label'),x:Math.round(rc.x),y:Math.round(rc.y),w:Math.round(rc.width)}})")
print("aria close:", r)
WS.close()