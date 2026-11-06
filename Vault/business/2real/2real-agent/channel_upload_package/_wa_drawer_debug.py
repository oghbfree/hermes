import json, time, sys, urllib.request, websocket
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
def js(expr,awaitP=True):
    r=_send("Runtime.evaluate",expression=expr,returnByValue=True,awaitPromise=awaitP,timeout=60000)
    res=r.get("result",{})
    if "exceptionDetails" in res: return "EXC:"+str(res["exceptionDetails"].get("exception",{}).get("description",""))[:250]
    return res.get("result",{}).get("value")
def cdp(m,**p):
    return _send(m,**p)
def trusted_click(x,y):
    cdp("Input.dispatchMouseEvent",type="mousePressed",x=int(x),y=int(y),button="left",clickCount=1)
    cdp("Input.dispatchMouseEvent",type="mouseReleased",x=int(x),y=int(y),button="left",clickCount=1)

WA_OPEN_TOOLS = ('(() => {'
 "  const t=[...document.querySelectorAll('[aria-label=Tools],[title=Tools]')].filter(e=>e.offsetParent!==null)[0];"
 "  if(!t) return 'noTools';"
 "  const rc=t.getBoundingClientRect();"
 "  const ME=ev=>new MouseEvent(ev,{bubbles:true,cancelable:true,view:window,clientX:rc.x+rc.width/2,clientY:rc.y+rc.height/2});"
 "  ['mousedown','mouseup','click'].forEach(ev=>t.dispatchEvent(ME(ev)));"
 "  return 'ok rect='+JSON.stringify({x:rc.x,y:rc.y,w:rc.width,h:rc.height});})()")
WA_OPEN_CATALOGUE = ('(() => {'
 "  const c=[...document.querySelectorAll('*')].filter(e=>e.offsetParent!==null&&(e.textContent||'').trim()==='Catalogue'&&e.children.length===0)[0];"
 "  if(!c) return 'noCat';"
 "  const t=c.closest('[role=button],[tabindex],li')||c.parentElement;"
 "  const rc=t.getBoundingClientRect();"
 "  const ME=ev=>new MouseEvent(ev,{bubbles:true,cancelable:true,view:window,clientX:rc.x+rc.width/2,clientY:rc.y+rc.height/2});"
 "  ['mousedown','mouseup','click'].forEach(ev=>t.dispatchEvent(ME(ev)));"
 "  return 'ok rect='+JSON.stringify({x:rc.x,y:rc.y,w:rc.width,h:rc.height});})()")
WA_ADD_ITEM_CARD = ('(() => {'
 "  const leaf=[...document.querySelectorAll('*')].filter(e=>e.offsetParent!==null&&(e.textContent||'').trim()==='Add new item'&&e.children.length===0);"
 "  const gc=(leaf[0]||{}).closest?leaf[0].closest('[role=gridcell]'):null;"
 "  if(!gc) return 'gone';"
 "  let el=gc;"
 "  for(let i=0;i<10;i++){ el=el.parentElement||el;"
 "    if(el.scrollTop!==undefined && el.scrollHeight>el.clientHeight+20 && el.clientWidth>250){ el.scrollTop=0; } }"
 "  const rc=gc.getBoundingClientRect();"
 "  const vis=[...document.querySelectorAll('[role=gridcell]')].filter(e=>e.offsetParent!==null&&(e.textContent||'').trim()==='Add new item'&&e.children.length===0)"
 "    .map(e=>{const r=e.getBoundingClientRect();return{x:r.x+r.width/2,y:r.y+r.height/2,vis:r.x>40&&r.y>40&&r.y<innerHeight-40};})"
 "    .find(o=>o.vis);"
 "  return JSON.stringify(vis||{x:rc.x+rc.width/2,y:rc.y+rc.height/2});"
 "})()")

print("STEP1 tools:", js(WA_OPEN_TOOLS)); time.sleep(4)
print("STEP2 catalogue:", js(WA_OPEN_CATALOGUE)); time.sleep(4)
print("STEP3 add-card coords:", js(WA_ADD_ITEM_CARD))
p=json.loads(js(WA_ADD_ITEM_CARD))
print("STEP4 trusted click at", p)
trusted_click(p["x"],p["y"]); time.sleep(4)
print("STEP5 drawer open (Add images):", js("(document.body.innerText||'').includes('Add images')"))
print("  title present:", js("document.querySelectorAll('div[contenteditable=true][aria-label=Name]').length"))
print("  head:", (js("(document.body.innerText||'')") or "").replace(chr(10),' | ')[-250:])