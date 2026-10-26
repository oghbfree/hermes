"""FB reply v6: buyer-verified row matching for duplicate-item threads.
Matches inbox rows that contain BOTH item keyword AND buyer name, then
verifies the conversation header before typing; sends via paper-plane click
with fresh-sent verification (same mechanics as _fb_reply5.py).
Usage: python _fb_reply6.py <item_kw> <buyer_kw> <message>
"""
import sys, json, time
sys.path.insert(0, r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package")
import cdp_harness as C

item_kw = sys.argv[1].lower()
buyer_kw = sys.argv[2].lower()
msg = sys.argv[3]
probe = msg[:50]

def inbox_ws():
    tabs = C.list_tabs()
    inbox = [t for t in tabs if "inbox" in t.get("url", "").lower()]
    if not inbox:
        C.goto_url("https://www.facebook.com/marketplace/inbox")
        time.sleep(8)
        tabs = C.list_tabs()
        inbox = [t for t in tabs if "inbox" in t.get("url", "").lower()]
    if not inbox:
        return None
    return inbox[0]["webSocketDebuggerUrl"]

ws = inbox_ws()
if not ws:
    print("RESULT: NO_INBOX_TAB"); sys.exit(2)
C._ws = ws; C._conn = None
time.sleep(2)

C._send("Page.navigate", url="https://www.facebook.com/marketplace/inbox")
time.sleep(5)
C._send("Page.reload", ignoreCache=True)
time.sleep(9)
print("AFTER_RELOAD_URL:", (C.js("location.href") or "")[:100])

picked = False
for attempt in range(8):
    r = C.js("""(() => {
      const ik=%s, bk=%s;
      const els=[].slice.call(document.querySelectorAll('[role=button]')).filter(e=>e.offsetParent!==null);
      const hits=els.filter(e=>{const t=(e.textContent||'').replace(/\\s+/g,' ').toLowerCase();
        return t.includes(ik) && t.includes(bk) && t.includes('·') && t.length<2000;});
      if(!hits.length) return 'NO_ROW';
      const el=hits.sort((a,b)=>b.getBoundingClientRect().width-a.getBoundingClientRect().width)[0];
      const ME=t=>new MouseEvent(t,{bubbles:true,cancelable:true,view:window});
      ['mousedown','mouseup','click'].forEach(t=>el.dispatchEvent(ME(t)));
      el.click && el.click();
      return 'DISPATCHED';
    })()""" % (json.dumps(item_kw), json.dumps(buyer_kw)))
    print("CLICK:", r)
    if r == "DISPATCHED":
        picked = True
        break
    time.sleep(2)
if not picked:
    print("RESULT: SKIP no_row |", item_kw, buyer_kw); sys.exit(0)
time.sleep(9)

guard = C.js("""(() => {
  const z=[...document.querySelectorAll('[aria-label]')].filter(e=>e.offsetParent!==null && /conversation titled/i.test(e.getAttribute('aria-label')||'')).map(e=>e.getAttribute('aria-label'));
  return z[0]||'';
})()""") or ""
print("HEADER:", guard[:200])
if buyer_kw not in guard.lower() and buyer_kw not in (guard or "").lower():
    print("RESULT: ABORT header_mismatch |", buyer_kw, "|", guard[:120]); sys.exit(3)

before = C.js("document.body.innerText") or ""

typed = "NO_ED"
for att in range(8):
    typed = C.js("""(() => {
      const ed=[...document.querySelectorAll('[contenteditable=true]')].filter(e=>e.offsetParent!==null)[0];
      if(!ed) return 'NO_ED';
      ed.focus();
      document.execCommand('insertText', false, %s);
      return ed.innerText.trim().slice(0,50) || 'EMPTY';
    })()""" % json.dumps(msg))
    if typed not in ("NO_ED", None, "EMPTY") and typed:
        break
    time.sleep(4)
print("TYPED:", repr(typed))
if not typed or typed in ("NO_ED",):
    print("RESULT: FAIL composer |", item_kw); sys.exit(4)
time.sleep(2)

sent_click = "NO_BTN"
for att in range(6):
    sent_click = C.js("""(() => {
      const btns=[...document.querySelectorAll('div[role=button], [aria-label]')].filter(e=>e.offsetParent!==null);
      const cand=btns.filter(e=>{
        const t=(e.getAttribute('aria-label')||'').toLowerCase();
        return t.includes('send') || (e.querySelector('svg') && /send|paper.?plane/i.test(e.outerHTML.slice(0,400)));
      });
      if(!cand.length) return 'NO_BTN';
      const el=cand.sort((a,b)=>b.getBoundingClientRect().width-a.getBoundingClientRect().width)[0];
      const ME=t=>new MouseEvent(t,{bubbles:true,cancelable:true,view:window});
      ['pointerdown','mousedown','pointerup','mouseup','click'].forEach(t=>el.dispatchEvent(ME(t)));
      el.click && el.click();
      return 'SEND_CLICKED';
    })()""")
    print("SEND_BTN:", sent_click)
    if sent_click == "SEND_CLICKED":
        break
    time.sleep(2)
time.sleep(5)

after = C.js("document.body.innerText") or ""
composer = C.js("""(() => { const e=[...document.querySelectorAll('[contenteditable=true]')].filter(x=>x.offsetParent!==null)[0]; return e?e.innerText.trim():'NO_ED'; })()""") or ""
print("COMPOSER_AFTER:", repr(composer[:60]))

if probe in after and probe not in composer:
    print("RESULT: SENT |", item_kw, buyer_kw)
    sys.exit(0)
elif composer:
    print("RESULT: NOT_SENT draft_retained |", item_kw, buyer_kw)
    sys.exit(5)
else:
    print("RESULT: NOT_SENT |", item_kw, buyer_kw)
    sys.exit(5)
