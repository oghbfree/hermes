# Close any open Add-item drawer without saving
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

if js("(document.body.innerText||'').includes('Add images')"):
    # dismiss any open list first (Escape), then click Close at top
    js("(() => { /* Escape to close any open dropdown */ })()")
    _send('Input.dispatchKeyEvent', type='rawKeyDown', windowsVirtualKeyCode=27, key='Escape')
    _send('Input.dispatchKeyEvent', type='keyUp', windowsVirtualKeyCode=27, key='Escape')
    time.sleep(1)
    r=js("[...document.querySelectorAll('[aria-label]')].filter(e=>e.offsetParent!==null&&/^close$/i.test(e.getAttribute('aria-label').trim())).map(e=>{const rc=e.getBoundingClientRect();return {x:Math.round(rc.x+rc.width/2),y:Math.round(rc.y+rc.height/2)}})")
    # prefer the one with y<50 (drawer top)
    cands=[c for c in json.loads(json.dumps(r)) if c['y']<50]
    print("close cands:", r)
    target = cands[0] if cands else (json.loads(json.dumps(r))[0] if r else None)
    if target:
        trusted(target['x'], target['y']); time.sleep(2)
print("drawer open still:", js("(document.body.innerText||'').includes('Add images')"))
print("head:", repr(js("(document.body.innerText||'').slice(0,120)")))
WS.close()