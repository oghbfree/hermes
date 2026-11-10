# Open Tools->Catalogue->Add new item, fill fields, click country, inspect dropdown
import json, time, websocket, urllib.request, base64
CDP="http://127.0.0.1:9222"
tabs=json.load(urllib.request.urlopen(CDP+"/json",timeout=10))
cands=[t for t in tabs if t.get("type")=="page" and t.get("url","").startswith("https://web.whatsapp.com")]
tab=[t for t in cands if "WhatsApp" in t.get("title","")][0]
WS=websocket.create_connection(tab["webSocketDebuggerUrl"].replace("localhost","127.0.0.1"),timeout=120,suppress_origin=True)
seq=[0]
def _send(m,**p):
    seq[0]+=1; WS.send(json.dumps({"id":seq[0],"method":m,"params":p}))
    while True:
        x=json.loads(WS.recv())
        if x.get("id")==seq[0]: return x
def js(expr):
    r=_send("Runtime.evaluate",expression=expr,returnByValue=True,awaitPromise=True,timeout=60000)
    if "exceptionDetails" in r.get("result",{}): return "EXC:"+json.dumps(r["result"]["exceptionDetails"].get("exception",{}))[:200]
    return r.get("result",{}).get("result",{}).get("value")
def cdp(m,**p): return _send(m,**p)
def trusted(x,y):
    cdp('Input.dispatchMouseEvent',type='mousePressed',x=int(x),y=int(y),button='left',clickCount=1)
    cdp('Input.dispatchMouseEvent',type='mouseReleased',x=int(x),y=int(y),button='left',clickCount=1)

# Reuse lib's step snippets
WA_OPEN_TOOLS = "(() => { const t=[...document.querySelectorAll('[aria-label=Tools],[title=Tools]')].filter(e=>e.offsetParent!==null)[0]; if(!t) return 'noTools'; const rc=t.getBoundingClientRect(); const ME=ev=>new MouseEvent(ev,{bubbles:true,cancelable:true,view:window,clientX:rc.x+rc.width/2,clientY:rc.y+rc.height/2}); ['mousedown','mouseup','click'].forEach(ev=>t.dispatchEvent(ME(ev))); return 'ok'; })()"
WA_OPEN_CATALOGUE = "(() => { const c=[...document.querySelectorAll('*')].filter(e=>e.offsetParent!==null&&(e.textContent||'').trim()==='Catalogue'&&e.children.length===0)[0]; if(!c) return 'noCat'; const t=c.closest('[role=button],[tabindex],li')||c.parentElement; const rc=t.getBoundingClientRect(); const ME=ev=>new MouseEvent(ev,{bubbles:true,cancelable:true,view:window,clientX:rc.x+rc.width/2,clientY:rc.y+rc.height/2}); ['mousedown','mouseup','click'].forEach(ev=>t.dispatchEvent(ME(ev))); return 'ok'; })()"
WA_ADD_ITEM_CARD = "(() => { const cand=[...document.querySelectorAll('*')].filter(e=>e.offsetParent!==null&&(e.textContent||'').trim()==='Add new item'&&e.children.length===0).map(e=>{const r=e.getBoundingClientRect();return{x:r.x+r.width/2,y:r.y+r.height/2,vis:r.x>10&&r.y>5&&r.y<innerHeight-10&&r.width>20&&r.height>10};}); const v=cand.find(o=>o.vis)||cand[0]; if(!v) return 'gone'; return JSON.stringify(v); })()"

print("open tools:", js(WA_OPEN_TOOLS)); time.sleep(3)
print("open catalogue:", js(WA_OPEN_CATALOGUE)); time.sleep(3)
r=js(WA_ADD_ITEM_CARD); print("add card:", r); time.sleep(4)
p=json.loads(r); trusted(p['x'],p['y']); time.sleep(4)
print("drawer open:", js("(document.body.innerText||'').includes('Add images')"))

# fill name + desc only, no photo needed for country probe
js("""(() => { const ed=[...document.querySelectorAll('div[contenteditable=true]')].filter(e=>e.offsetParent!==null); const name=ed.find(e=>(e.getAttribute('aria-label')||'')==='Name'); if(!name) return 'noName'; name.focus(); document.execCommand('insertText', false, 'Test Country Probe 420gh'); return 'ok'; })()""")
time.sleep(1)

# Now find country control and click, then dump state
lab=js("[...document.querySelectorAll('*')].filter(e=>e.offsetParent!==null&&(e.textContent||'').trim().startsWith('Country of origin')&&e.children.length===0).map(e=>{const r=e.getBoundingClientRect();return {t:(e.textContent||'').trim(),x:Math.round(r.x),y:Math.round(r.y),w:Math.round(r.width),h:Math.round(r.height)}})")
print("country label(s):", lab)
l2=js("""(() => { const l=[...document.querySelectorAll('*')].filter(e=>e.offsetParent!==null&&(e.textContent||'').trim().startsWith('Country of origin')&&e.children.length===0)[0]; const t=l.closest('[role=button],[tabindex]')||l.parentElement; const r=t.getBoundingClientRect(); return JSON.stringify({x:r.x+r.width/2,y:r.y+r.height/2}); })()""")
p2=json.loads(l2); print("click target:", p2)
trusted(p2['x'],p2['y']); time.sleep(3)
print("Åland Islands:", js("(document.body.innerText||'').includes('Åland Islands')"))
print("body tail after country click:", repr(js("(document.body.innerText||'').slice(-400)")))
# dump visible form/list rows
print("visible list/option rows:", js("[...document.querySelectorAll('li,[role=option],[role=listbox] *')].filter(e=>e.offsetParent!==null&&(e.textContent||'').trim()&&e.children.length===0).map(e=>{const r=e.getBoundingClientRect();return {t:(e.textContent||'').trim().slice(0,20),x:Math.round(r.x),y:Math.round(r.y)}}).slice(0,20)"))
WS.close()