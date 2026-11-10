# Check viewport height, scroll country control into view, then click and verify dropdown
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
    if "exceptionDetails" in r.get("result",{}): return "EXC:"+json.dumps(r["result"]["exceptionDetails"].get("exception",{}))[:200]
    return r.get("result",{}).get("result",{}).get("value")
def cdp(m,**p): return _send(m,**p)
def trusted(x,y):
    cdp('Input.dispatchMouseEvent',type='mousePressed',x=int(x),y=int(y),button='left',clickCount=1)
    cdp('Input.dispatchMouseEvent',type='mouseReleased',x=int(x),y=int(y),button='left',clickCount=1)

print("innerHeight:", js("window.innerHeight"), "innerWidth:", js("window.innerWidth"))
# find the drawer's scroll container and country control
print("country control rect (before scroll):", js("[...document.querySelectorAll('*')].filter(e=>e.offsetParent!==null&&(e.textContent||'').trim().startsWith('Country of origin')&&e.children.length===0).map(e=>{const r=e.getBoundingClientRect();return {x:Math.round(r.x),y:Math.round(r.y)}})"))
# scrollIntoView the country control
print("scroll result:", js("""(() => { const l=[...document.querySelectorAll('*')].filter(e=>e.offsetParent!==null&&(e.textContent||'').trim().startsWith('Country of origin')&&e.children.length===0)[0]; const t=l.closest('[role=button],[tabindex]')||l.parentElement; t.scrollIntoView({block:'center',behavior:'instant'}); return 'ok'; })()"""))
time.sleep(1)
print("country control rect (after scroll):", js("[...document.querySelectorAll('*')].filter(e=>e.offsetParent!==null&&(e.textContent||'').trim().startsWith('Country of origin')&&e.children.length===0).map(e=>{const r=e.getBoundingClientRect();return {x:Math.round(r.x),y:Math.round(r.y)}})"))
# click it now
p=js("""(() => { const l=[...document.querySelectorAll('*')].filter(e=>e.offsetParent!==null&&(e.textContent||'').trim().startsWith('Country of origin')&&e.children.length===0)[0]; const t=l.closest('[role=button],[tabindex]')||l.parentElement; const r=t.getBoundingClientRect(); return JSON.stringify({x:r.x+r.width/2,y:r.y+r.height/2}); })()""")
pp=json.loads(p); print("click target now:", pp); trusted(pp['x'],pp['y']); time.sleep(3)
print("Åland Islands:", js("(document.body.innerText||'').includes('Åland Islands')"))
print("rows visible:", js("[...document.querySelectorAll('li,[role=option]')].filter(e=>e.offsetParent!==null&&(e.textContent||'').trim()).map(e=>{const r=e.getBoundingClientRect();return {t:(e.textContent||'').trim().slice(0,18),y:Math.round(r.y)}}).slice(0,15)"))
WS.close()