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
print("TAB:", TAB["title"][:60])
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

WA_OPEN_TOOLS = ('(() => {'
 "  const t=[...document.querySelectorAll('[aria-label=Tools],[title=Tools]')].filter(e=>e.offsetParent!==null)[0];"
 "  if(!t) return 'noTools';"
 "  const rc=t.getBoundingClientRect();"
 "  const ME=ev=>new MouseEvent(ev,{bubbles:true,cancelable:true,view:window,clientX:rc.x+rc.width/2,clientY:rc.y+rc.height/2});"
 "  ['mousedown','mouseup','click'].forEach(ev=>t.dispatchEvent(ME(ev)));"
 "  return 'ok';})()")
def trusted_click(x,y):
    _send("Input.dispatchMouseEvent", type="mousePressed", x=int(x), y=int(y), button="left", clickCount=1)
    _send("Input.dispatchMouseEvent", type="mouseReleased", x=int(x), y=int(y), button="left", clickCount=1)

r=js(WA_OPEN_TOOLS); print("tools:", r); time.sleep(4)
r=js("""(() => {
  const btns=[...document.querySelectorAll('[aria-label],[title]')].filter(e=>e.offsetParent!==null);
  const c=btns.find(e=>(e.getAttribute('aria-label')||e.getAttribute('title')||'').toLowerCase().includes('catalogue'));
  if(!c) return 'noCatBtn';
  const rc=c.getBoundingClientRect();
  return JSON.stringify({x:rc.x+rc.width/2,y:rc.y+rc.height/2});
})()""")
if r.startswith("no") or r.startswith("EXC"):
    print("catalogue btn:", r)
else:
    p=json.loads(r); trusted_click(p["x"],p["y"]); print("catalogue opened")
time.sleep(4)
head=(js("(document.body.innerText||'')") or "")[:300].replace("\n"," ")
print("head:", head)

ctr=js("""(() => {
  const sw=[...document.querySelectorAll('div')].filter(e=>e.offsetParent!==null&&e.scrollHeight>e.clientHeight+40&&e.clientWidth>400&&e.getBoundingClientRect().x<200)[0];
  if(!sw) return 'noContainer';
  window.__sw=sw; return JSON.stringify({sh:sw.scrollHeight,ch:sw.clientHeight});
})()""")
print("container:", ctr)
collected=set()
if not ctr.startswith("no"):
    info=json.loads(ctr); sh=info["sh"]
    step=400
    y=0
    while y<=sh+step:
        js("window.__sw.scrollTop="+str(y))
        time.sleep(1.3)
        txt=js("""(() => {
          const out=[];
          [...document.querySelectorAll('*')].forEach(e=>{
            if(e.offsetParent===null||e.children.length) return;
            const t=(e.textContent||'').trim(); if(!t) return;
            if(/gh(s|c|)$/i.test(t)) out.push(t);
          });
          return out;
        })()""")
        if txt:
            for t in txt: collected.add(t)
        y+=step
    js("window.__sw.scrollTop=0")
print("harvested titles:", len(collected))
with open(r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package\_live_harvest.txt","w",encoding="utf-8") as f:
    for t in sorted(collected): f.write(t+"\n")
for t in sorted(collected): print(" -", t)