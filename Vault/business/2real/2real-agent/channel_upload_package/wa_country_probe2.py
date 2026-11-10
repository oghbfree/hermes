# Inspect interactive elements in the add-item drawer + topmost element at country coord
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

print("drawer open:", js("(document.body.innerText||'').includes('Add images')"))
print("comboBox/select/drop inputs:", js("[...document.querySelectorAll('[role=combobox],select,[role=listbox],input')].filter(e=>e.offsetParent!==null).map(e=>{const r=e.getBoundingClientRect();return {tag:e.tagName,role:e.getAttribute('role'),t:(e.getAttribute('aria-label')||e.textContent||'').trim().slice(0,20),x:Math.round(r.x),y:Math.round(r.y),w:Math.round(r.width)}})"))
print("input[type=file]:", js("[...document.querySelectorAll('input[type=file]')].map(e=>e.accept).slice(0,3)"))

# country label position
lab=js("[...document.querySelectorAll('*')].filter(e=>e.offsetParent!==null&&(e.textContent||'').trim().startsWith('Country of origin')&&e.children.length===0).map(e=>{const r=e.getBoundingClientRect();return {t:(e.textContent||'').trim(),x:Math.round(r.x),y:Math.round(r.y),w:Math.round(r.width),h:Math.round(r.height)}})")
print("country label:", lab)

# topmost element at center of country field (click coords used)
top=js("(() => { const l=[...document.querySelectorAll('*')].filter(e=>e.offsetParent!==null&&(e.textContent||'').trim().startsWith('Country of origin')&&e.children.length===0)[0]; const t=l.closest('[role=button],[tabindex]')||l.parentElement; const r=t.getBoundingClientRect(); const cx=r.x+r.width/2, cy=r.y+r.height/2; const el=document.elementFromPoint(cx,cy); const out={cx:Math.round(cx),cy:Math.round(cy)}; return JSON.stringify({...out, topmost:(el?el.tagName+'.'+(el.className||'').toString().slice(0,30):'none'), aria:(el?el.getAttribute('aria-label'):null), role:(el?el.getAttribute('role'):null)}); })()")
print("topmost at click pt:", top)

# What does the field's visible text show currently? Is a country value already set?
print("field region text:", repr(js("""(() => { const l=[...document.querySelectorAll('*')].filter(e=>e.offsetParent!==null&&(e.textContent||'').trim().startsWith('Country of origin')&&e.children.length===0)[0]; let n=l; for(let i=0;i<4&&n;i++,n=n.parentElement){ if((n.textContent||'').length<120&&(n.textContent||'').includes('origin')) return n.textContent.trim(); } return 'none'; })()""")))
WS.close()