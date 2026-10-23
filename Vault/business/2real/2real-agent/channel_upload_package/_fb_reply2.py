"""Guarded FB Marketplace reply: click buyer row -> header-guard -> type -> trusted Enter.
Usage: python _fb_reply2.py <buyer_keyword> <message>"""
import sys, json, time
sys.path.insert(0, r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package")
import cdp_harness as C

kw = sys.argv[1]
msg = sys.argv[2]

tabs = C.list_tabs()
inbox = [t for t in tabs if "inbox" in t.get("url","").lower()]
if not inbox:
    print("RESULT: NO_INBOX_TAB"); sys.exit(2)
C._ws = inbox[0]["webSocketDebuggerUrl"]; C._conn = None
time.sleep(1)

# click the thread row: FB renders each row as [role=button] with onClick
picked = None
for attempt in range(6):
    r = C.js("""(() => {
      const kw=%s.toLowerCase();
      const els=[].slice.call(document.querySelectorAll('[role=button]')).filter(e=>e.offsetParent!==null);
      const hits=els.filter(e=>{const t=(e.textContent||'').replace(/\\s+/g,' ').trim();
        return t.toLowerCase().startsWith(kw) && t.includes('·') && t.length<300;});
      if(!hits.length){ // fallback: any clickable containing '<kw> ·'
        const all=[].slice.call(document.querySelectorAll('div,span,a,[role=button]')).filter(e=>e.offsetParent!==null);
        const f=all.filter(e=>{const t=(e.textContent||'').replace(/\\s+/g,' ').trim();
          return t.toLowerCase().startsWith(kw) && t.includes('·') && t.length<180;}).pop();
        if(!f) return null;
        const rc2=f.getBoundingClientRect();
        return JSON.stringify({x:rc2.x+rc2.width/2,y:rc2.y+rc2.height/2});
      }
      const el=hits.sort((a,b)=>b.getBoundingClientRect().width-a.getBoundingClientRect().width)[0];
      el.scrollIntoView({block:'center'});
      const rc=el.getBoundingClientRect();
      return JSON.stringify({x:rc.x+rc.width/2,y:rc.y+rc.height/2});
    })()""" % json.dumps(kw.lower()))
    if r:
        p = json.loads(r)
        C.click_at_xy(int(p["x"]), int(p["y"]))
        picked = True
        break
    time.sleep(2)
if not picked:
    print("RESULT: SKIP no_row |", kw); sys.exit(0)
time.sleep(8)

# Guard: open conversation header must contain buyer keyword
guard = C.js("""(() => {
  const z=[...document.querySelectorAll('[aria-label]')].filter(e=>e.offsetParent!==null && /conversation titled/i.test(e.getAttribute('aria-label')||'')).map(e=>e.getAttribute('aria-label'));
  return z[0]||'';
})()""") or ""
print("HEADER:", guard[:160])
if kw.lower() not in guard.lower():
    print("RESULT: ABORT header_mismatch |", kw, "|", guard[:100]); sys.exit(3)

# Type into the active composer
typed = C.js("""(async () => {
  const ed=[...document.querySelectorAll('[contenteditable=true]')].filter(e=>e.offsetParent!==null)[0];
  if(!ed) return 'NO_ED';
  ed.focus();
  document.execCommand('insertText', false, %s);
  await new Promise(r=>setTimeout(r,700));
  return ed.innerText.trim().slice(0,40);
})()""" % json.dumps(msg))
print("TYPED:", repr(typed))
if not typed or typed in ("NO_ED",):
    print("RESULT: FAIL composer |", kw); sys.exit(4)
time.sleep(1)

# Trusted Enter via CDP input domain
try:
    C._send("Input.dispatchKeyEvent", type="keyDown", key="Enter", code="Enter",
            windowsVirtualKeyCode=13, nativeVirtualKeyCode=13)
    C._send("Input.dispatchKeyEvent", type="keyUp", key="Enter", code="Enter",
            windowsVirtualKeyCode=13, nativeVirtualKeyCode=13)
    ent = "SENT_TRUSTED"
except Exception as e:
    ent = "ENTER_ERR %r" % e
print("ENTER:", ent)
time.sleep(5)

ver = C.js("""(() => {
  const eds=[...document.querySelectorAll('[contenteditable=true]')].filter(e=>e.offsetParent!==null);
  const t=document.body.innerText||'';
  return JSON.stringify({composer: eds.length?eds[0].innerText.trim():'NO_ED', seen: t.includes(%s)});
})()""" % json.dumps(msg[:50]))
print("VERIFY:", ver)
v = json.loads(ver)
if v.get("composer") == "" and v.get("seen"):
    print("RESULT: SENT |", kw); sys.exit(0)
elif v.get("seen"):
    print("RESULT: SENT (composer retains draft) |", kw); sys.exit(0)
print("RESULT: NOT_SENT |", kw, ver); sys.exit(5)
