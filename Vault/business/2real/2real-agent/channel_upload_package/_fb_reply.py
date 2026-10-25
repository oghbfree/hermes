"""Guarded FB Marketplace reply v4: relaxed row matcher (long message previews).
Same header-guard + trusted Enter as v3, but rows may exceed 300 chars.
Usage: python _fb_reply.py <buyer_keyword> <message>"""
import sys, json, time
sys.path.insert(0, r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package")
import cdp_harness as C

kw = sys.argv[1]
msg = sys.argv[2]

tabs = C.list_tabs()
inbox = [t for t in tabs if "inbox" in t.get("url", "").lower()]
if not inbox:
    C.goto_url("https://www.facebook.com/marketplace/inbox")
    time.sleep(8)
    tabs = C.list_tabs()
    inbox = [t for t in tabs if "inbox" in t.get("url", "").lower()]
if not inbox:
    print("RESULT: NO_INBOX_TAB"); sys.exit(2)
C._ws = inbox[0]["webSocketDebuggerUrl"]; C._conn = None
time.sleep(2)
print("URL:", (C.js("location.href") or "")[:110])

# If an old conversation pane is open, hard reload to reset (SPA keeps pane)
conv = C.js("""(() => {
  const z=[...document.querySelectorAll('[aria-label]')].filter(e=>e.offsetParent!==null && /conversation titled/i.test(e.getAttribute('aria-label')||''));
  return z.length ? z[0].getAttribute('aria-label') : '';
})()""") or ""
print("PANEBEFORE:", conv[:80])
if conv:
    try: C._send("Page.navigate", url="https://www.facebook.com/marketplace/inbox")
    except Exception: pass
    time.sleep(5)
    try: C._send("Page.reload", ignoreCache=True)
    except Exception: pass
    time.sleep(9)

# click thread row: relax length filter to 2000, still require buyer prefix + '·'
picked = None
for attempt in range(6):
    r = C.js("""(() => {
      const kw=%s.toLowerCase();
      const els=[].slice.call(document.querySelectorAll('[role=button]')).filter(e=>e.offsetParent!==null);
      const hits=els.filter(e=>{const t=(e.textContent||'').replace(/\\s+/g,' ').trim();
        return t.toLowerCase().startsWith(kw) && t.includes('·') && t.length<2000;});
      if(!hits.length) return 'NO_ROW';
      const el=hits.sort((a,b)=>b.getBoundingClientRect().width-a.getBoundingClientRect().width)[0];
      const ME=t=>new MouseEvent(t,{bubbles:true,cancelable:true,view:window});
      ['mousedown','mouseup','click'].forEach(t=>el.dispatchEvent(ME(t)));
      el.click && el.click();
      return 'DISPATCHED';
    })()""" % json.dumps(kw.lower()))
    print("CLICK:", r)
    if r == "DISPATCHED":
        picked = True
        break
    time.sleep(2)
if not picked:
    print("RESULT: SKIP no_row |", kw); sys.exit(0)
time.sleep(9)

# Guard: open conversation header must contain buyer keyword
guard = C.js("""(() => {
  const z=[...document.querySelectorAll('[aria-label]')].filter(e=>e.offsetParent!==null && /conversation titled/i.test(e.getAttribute('aria-label')||'')).map(e=>e.getAttribute('aria-label'));
  return z[0]||'';
})()""") or ""
print("HEADER:", guard[:160])
if kw.lower() not in guard.lower():
    print("RESULT: ABORT header_mismatch |", kw, "|", guard[:100]); sys.exit(3)

# Type into the active composer (retry while pane loads) — SYNC evaluate so value returns
typed = "NO_ED"
for att in range(8):
    typed = C.js("""(() => {
      const ed=[...document.querySelectorAll('[contenteditable=true]')].filter(e=>e.offsetParent!==null)[0];
      if(!ed) return 'NO_ED';
      ed.focus();
      document.execCommand('insertText', false, %s);
      return ed.innerText.trim().slice(0,40) || 'EMPTY';
    })()""" % json.dumps(msg))
    if typed not in ("NO_ED", None, "EMPTY") and typed:
        break
    time.sleep(4)
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
