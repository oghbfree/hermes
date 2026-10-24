"""Open buyer thread via synthetic click (proven recipe 22/10/26) and dump conversation tail (READ-ONLY)."""
import sys, json, time
sys.path.insert(0, r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package")
import cdp_harness as C

kw = sys.argv[1].lower()

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
time.sleep(3)

u = C.js("location.href") or ""
print("URL PRE:", u[:110])

# ensure we're at inbox list first
if "/marketplace/inbox" not in u:
    C.goto_url("https://www.facebook.com/marketplace/inbox")
    time.sleep(8)

r = C.js("""(() => {
  const kw=%s;
  const els=[].slice.call(document.querySelectorAll('[role=button]')).filter(e=>e.offsetParent!==null);
  const hits=els.filter(e=>{const t=(e.textContent||'').replace(/\\s+/g,' ').trim();
    return t.toLowerCase().startsWith(kw) && t.includes('·') && t.length<300;});
  if(!hits.length) return 'NO_ROW';
  const el=hits.sort((a,b)=>b.getBoundingClientRect().width-a.getBoundingClientRect().width)[0];
  const ME=t=>new MouseEvent(t,{bubbles:true,cancelable:true,view:window});
  ['mousedown','mouseup','click'].forEach(t=>el.dispatchEvent(ME(t)));
  el.click && el.click();
  return 'DISPATCHED:' + el.textContent.replace(/\\s+/g,' ').trim().slice(0,80);
})()""" % json.dumps(kw))
print("CLICK:", r)
time.sleep(9)

state = C.js("""(() => {
  const conv=[...document.querySelectorAll('[aria-label]')].filter(e=>e.offsetParent!==null && /conversation titled/i.test(e.getAttribute('aria-label')||'')).map(e=>e.getAttribute('aria-label'));
  const t=document.body.innerText||'';
  return JSON.stringify({url: location.href.slice(0,140), conv: conv.slice(0,3), tail: t.slice(-3000)});
})()""")
print("STATE:", state[:3500])
