# Inspect country control DOM + test-click it to see if dropdown opens
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

# the country label leaf and its clickable ancestor chain
lab = js("""
(() => {
  const l=[...document.querySelectorAll('*')].filter(e=>e.offsetParent!==null&&(e.textContent||'').trim().startsWith('Country of origin')&&e.children.length===0)[0];
  if(!l) return 'none';
  const chain=[]; let n=l;
  for(let i=0;i<6 && n;i++,n=n.parentElement){
    const r=n.getBoundingClientRect();
    chain.push({tag:n.tagName, role:n.getAttribute&&n.getAttribute('role'), tab:(n.getAttribute&&n.getAttribute('tabindex')), ce:(n.getAttribute&&n.getAttribute('contenteditable')), x:Math.round(r.x),y:Math.round(r.y),w:Math.round(r.width),h:Math.round(r.height), cls:(n.className||'').toString().slice(0,40)});
  }
  return JSON.stringify(chain);
})()
""")
print("country label + ancestors:", lab)

# snapshot count of role=dialog/scrollable forms before click
print("before click, forms/lists:", js("[...document.querySelectorAll('form,ul,[role=listbox],[role=dialog]')].filter(e=>e.offsetParent!==null).length"))

# where is 'Country of origin (required)' leaf -> click its parent
xy = js("""
(() => {
  const l=[...document.querySelectorAll('*')].filter(e=>e.offsetParent!==null&&(e.textContent||'').trim().startsWith('Country of origin')&&e.children.length===0)[0];
  const t=l.closest('[role=button],[tabindex]')||l.parentElement;
  const r=t.getBoundingClientRect();
  return JSON.stringify({x:r.x+r.width/2,y:r.y+r.height/2});
})()
""")
print("click target:", xy)
p=json.loads(xy); trusted(p['x'],p['y']); time.sleep(3)
print("after click, forms/lists:", js("[...document.querySelectorAll('form,ul,[role=listbox],[role=dialog]')].filter(e=>e.offsetParent!==null).length"))
print("Åland Islands now:", js("(document.body.innerText||'').includes('Åland Islands')"))
print("body tail:", repr(js("(document.body.innerText||'').slice(-350)")))
# list rows visible
print("rows:", js("[...document.querySelectorAll('li,[role=option]')].filter(e=>e.offsetParent!==null).map(e=>{const r=e.getBoundingClientRect();return {t:(e.textContent||'').trim().slice(0,20),x:Math.round(r.x),y:Math.round(r.y)}}).slice(0,12)"))
WS.close()