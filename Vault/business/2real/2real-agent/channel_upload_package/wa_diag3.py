# Deep-inspect country field DOM + try clicking different sub-elements
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

# What is the whole country field region? Get the containing div with text
html = js("""
(() => {
  const l=[...document.querySelectorAll('*')].filter(e=>e.offsetParent!==null&&(e.textContent||'').trim().startsWith('Country of origin')&&e.children.length===0)[0];
  if(!l) return 'none';
  let n=l;
  for(let i=0;i<5 && n;i++,n=n.parentElement){
    if((n.textContent||'').match(/Ghana|origin/i)){
      const r=n.getBoundingClientRect();
      return {tag:n.tagName, cls:(n.className||'').toString().slice(0,60), x:Math.round(r.x),y:Math.round(r.y),w:Math.round(r.width),h:Math.round(r.height), html:(n.outerHTML||'').slice(0,600)};
    }
  }
  return 'none2';
})()
""")
print("field region:", html)

# enumerate clickable descendants in the country field div span
print("desc potential click targets:")
print(js("""
(() => {
  const l=[...document.querySelectorAll('*')].filter(e=>e.offsetParent!==null&&(e.textContent||'').trim().startsWith('Country of origin')&&e.children.length===0)[0];
  let n=l;
  for(let i=0;i<5 && n;i++,n=n.parentElement){
    if((n.textContent||'').includes('Ghana')||n.textContent.trim().startsWith('Country')){
      const els=[...n.querySelectorAll('[role=button],[role=combobox],label,div,span')].filter(e=>e.offsetParent!==null&&e.children.length===0&&(e.textContent||'').trim());
      return JSON.stringify(els.map(e=>{const r=e.getBoundingClientRect();return {t:(e.textContent||'').trim().slice(0,25),role:e.getAttribute('role'),x:Math.round(r.x),y:Math.round(r.y),w:Math.round(r.width),h:Math.round(r.height)}}).slice(0,15));
    }
  }
  return 'none';
})()
""", ))
WS.close()