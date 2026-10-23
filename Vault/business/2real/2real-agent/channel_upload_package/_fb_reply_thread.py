"""Reply to ONE FB Marketplace chat thread with recipient-header guard.

Usage: python _fb_reply_thread.py <buyer_keyword> <message>
Flow: open inbox -> click row matching buyer keyword -> verify header shows buyer
-> type into composer -> click Send -> verify composer empty + sent text present.
Skips safely (rc=SKIP/FAIL) rather than risk a wrong-thread send.
"""
import os, sys, json, time, urllib.request
sys.path.insert(0, r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package")
os.environ["FB_CDP_URL"] = "http://127.0.0.1:9222"
import cdp_harness as C

buyer_kw = sys.argv[1]
msg = sys.argv[2]

def js(expr, awaitp=True, timeout=40):
    return C.js_async(expr, timeout=timeout) if awaitp else C.js(expr)

# 1. Ensure inbox tab
tabs = C.list_tabs()
inbox_tabs = [t for t in tabs if "/marketplace/inbox" in t.get("url", "") or "marketplace/you/inbox" in t.get("url", "")]
if inbox_tabs:
    C._ws = inbox_tabs[0]["webSocketDebuggerUrl"]; C._conn = None
else:
    C.goto_url("https://www.facebook.com/marketplace/inbox")
    time.sleep(6)

# 2. Click the thread row matching buyer keyword
def click_row(kw):
    for attempt in range(6):
        r = js("""(() => {
          const kw=%s.toLowerCase();
          const els=[].slice.call(document.querySelectorAll('div,span,a')).filter(e=>e.offsetParent!==null);
          const hit=els.filter(e=>{
            const t=(e.textContent||'').replace(/\\s+/g,' ').trim();
            return t.toLowerCase().startsWith(kw) && t.includes('·') && t.length<200;
          }).pop();
          if(!hit) return null;
          hit.scrollIntoView({block:'center'});
          const rc=hit.getBoundingClientRect();
          return JSON.stringify({x:rc.x+rc.width/2,y:rc.y+rc.height/2, tag:hit.tagName});
        })()""" % json.dumps(kw.lower()), awaitp=False)
        if r:
            p = json.loads(r)
            C.click_at_xy(int(p["x"]), int(p["y"]))
            return True
        time.sleep(2)
    return False

if not click_row(buyer_kw):
    print("RESULT: SKIP no_row |", buyer_kw)
    sys.exit(0)

time.sleep(6)

# 3. Recipient guard: header of the OPEN thread must contain the buyer keyword
guard = js("""(() => {
  const t = document.body.innerText || '';
  // chat pane: texts after 'Messages' marker; take first 1800 chars containing message list
  const idx = t.indexOf('Type a message');
  const region = idx > -1 ? t.slice(Math.max(0, idx-2500), idx) : t.slice(0, 2500);
  return region;
})()""", awaitp=False) or ""
print("GUARD_REGION:", repr(guard[:400]))
if buyer_kw.lower() not in guard.lower():
    print("RESULT: ABORT header_mismatch |", buyer_kw)
    sys.exit(3)

# 4. Type into composer
typed = js("""(async () => {
  const ed=[...document.querySelectorAll('[contenteditable=true]')]
    .find(e=>e.offsetParent!==null && !/send/i.test(e.getAttribute('aria-label')||''));
  if(!ed) return 'NO_ED';
  ed.focus();
  const ok = document.execCommand('insertText', false, %s);
  return ok ? ed.innerText.slice(0, 40) : 'EXEC_FAIL';
})()""" % json.dumps(msg), timeout=30)
print("TYPED:", repr(typed))
if not typed or typed in ("NO_ED", "EXEC_FAIL"):
    print("RESULT: FAIL composer |", buyer_kw)
    sys.exit(4)
time.sleep(1.5)

# 5. Click Send (aria-label Send) — single click, no keyboard Enter
st = js("""(() => {
  const btns=[...document.querySelectorAll('[role=button]')].filter(e=>e.offsetParent!==null);
  const snd=btns.find(e=>/^send$/i.test((e.getAttribute('aria-label')||'').trim()));
  if(!snd) return 'NO_SEND';
  const ME=t=>new MouseEvent(t,{bubbles:true,cancelable:true,view:window});
  ['mousedown','mouseup','click'].forEach(t=>snd.dispatchEvent(ME(t)));
  return 'CLICKED';
})()""", awaitp=False)
print("SEND:", st)
time.sleep(4)

# 6. Verify: composer emptied + sent text visible in body
ver = js("""(() => {
  const eds=[...document.querySelectorAll('[contenteditable=true]')].filter(e=>e.offsetParent!==null);
  const bodyTxt = document.body.innerText || '';
  return JSON.stringify({composer: eds.length?eds[0].innerText.trim():'NO_ED',
                         seen: bodyTxt.includes(%s)});
})()""" % json.dumps(msg[:60]), awaitp=False)
print("VERIFY:", ver)
try:
    v = json.loads(ver)
    if v.get("composer") == "" and v.get("seen"):
        print("RESULT: SENT |", buyer_kw)
        sys.exit(0)
    print("RESULT: VERIFY_FAIL |", buyer_kw, ver)
    sys.exit(5)
except Exception as e:
    print("RESULT: VERIFY_ERR |", buyer_kw, repr(e), ver)
    sys.exit(5)
