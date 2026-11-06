# Reconcile: harvest the LIVE WhatsApp catalogue titles for verification.
import json, time, sys, urllib.request, websocket

CDP_HTTP = "http://127.0.0.1:9222"

def list_tabs():
    with urllib.request.urlopen(CDP_HTTP + "/json", timeout=10) as r:
        return json.load(r)

cands = [t for t in list_tabs()
         if t.get("type") == "page" and t.get("url", "").startswith("https://web.whatsapp.com")]
if not cands:
    print("[CRON_FAILURE] no web.whatsapp.com tab found"); sys.exit(1)
for t in cands:
    if "WhatsApp" in t.get("title", ""):
        TAB = t; break
else:
    TAB = cands[0]
WS = websocket.create_connection(TAB["webSocketDebuggerUrl"].replace("localhost", "127.0.0.1"),
                                 timeout=120, suppress_origin=True)
_seq = [0]
def _send(method, **params):
    _seq[0] += 1
    WS.send(json.dumps({"id": _seq[0], "method": method, "params": params}))
    deadline = time.time() + 110
    while time.time() < deadline:
        msg = json.loads(WS.recv())
        if msg.get("id") == _seq[0]:
            return msg
    raise TimeoutError(method)
def js(expr):
    r = _send("Runtime.evaluate", expression=expr, returnByValue=True, awaitPromise=True, timeout=90000)
    res = r.get("result", {})
    if "exceptionDetails" in res:
        return "EXC:" + str(res["exceptionDetails"].get("exception", {}).get("description", ""))[:200]
    return res.get("result", {}).get("value")

print("TAB:", TAB["title"][:60])

def open_tools_catalogue():
    js(WA_OPEN_TOOLS); time.sleep(3)
    js(WA_OPEN_CATALOGUE); time.sleep(3)
    # open the 'All' items view: find a leaf labelled 'All items' / 'All'
    r = js("""(() => {
      const c=[...document.querySelectorAll('*')].filter(e=>e.offsetParent!==null&&(e.textContent||'').trim()==='All items'&&e.children.length===0)[0];
      if(!c) return 'noAll';
      const t=c.closest('[role=button],[role=radio],[tabindex],li')||c.parentElement;
      const rc=t.getBoundingClientRect();
      const ME=ev=>new MouseEvent(ev,{bubbles:true,cancelable:true,view:window,clientX:rc.x+rc.width/2,clientY:rc.y+rc.height/2});
      ['mousedown','mouseup','click'].forEach(ev=>t.dispatchEvent(ME(ev)));
      return 'ok';
    })()""")
    time.sleep(3)
    return r

WA_OPEN_TOOLS = """(() => {
  const t=[...document.querySelectorAll('[aria-label=Tools],[title=Tools]')].filter(e=>e.offsetParent!==null)[0];
  if(!t) return 'noTools';
  const rc=t.getBoundingClientRect();
  const ME=ev=>new MouseEvent(ev,{bubbles:true,cancelable:true,view:window,clientX:rc.x+rc.width/2,clientY:rc.y+rc.height/2});
  ['mousedown','mouseup','click'].forEach(ev=>t.dispatchEvent(ME(ev)));
  return 'ok';
})()"""
WA_OPEN_CATALOGUE = """(() => {
  const c=[...document.querySelectorAll('*')].filter(e=>e.offsetParent!==null&&(e.textContent||'').trim()==='Catalogue'&&e.children.length===0)[0];
  if(!c) return 'noCat';
  const t=c.closest('[role=button],[tabindex],li')||c.parentElement;
  const rc=t.getBoundingClientRect();
  const ME=ev=>new MouseEvent(ev,{bubbles:true,cancelable:true,view:window,clientX:rc.x+rc.width/2,clientY:rc.y+rc.height/2});
  ['mousedown','mouseup','click'].forEach(ev=>t.dispatchEvent(ME(ev)));
  return 'ok';
})()"""

op = open_tools_catalogue()
print("open All:", op)
head = (js("(document.body.innerText||'')") or "")[:200]
print("head:", head.replace(chr(10), " "))

# Sweep the big scroll container collecting leaf texts
sweep = """(() => {
  const sw=[...document.querySelectorAll('div')].filter(e=>e.offsetParent!==null&&e.scrollHeight>e.clientHeight+20&&e.clientWidth>400&&e.getBoundingClientRect().x<200)[0];
  if(!sw) return 'noContainer';
  const out=[];
  const step=Math.max(280, Math.round(sw.clientHeight*0.5));
  for(let y=0;y<=sw.scrollHeight;y+=step){
    sw.scrollTop=y;
    // wait handled by caller between sweeps? we do micro wait via sync js impossible; collect each
    out.push([y, [...document.querySelectorAll('*')].filter(e=>e.offsetParent!==null&&e.children.length===0&&/gh(s|c|)$/i.test((e.textContent||'').trim().slice(-3))).map(e=>e.textContent.trim())]);
  }
  sw.scrollTop=0;
  return JSON.stringify({container: sw.scrollHeight+'x'+sw.clientHeight, out});
})()"""
print("SCAN", sweep)