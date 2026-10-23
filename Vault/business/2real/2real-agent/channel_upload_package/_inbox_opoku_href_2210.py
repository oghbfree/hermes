import sys, json, time
sys.path.insert(0, r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package")
import cdp_harness as C

tabs = C.list_tabs()
inbox = [t for t in tabs if "inbox" in t.get("url","").lower()]
C._ws = inbox[0]["webSocketDebuggerUrl"]; C._conn = None
time.sleep(1)

href = C.js("""(() => {
  const kw='opoku';
  const anchors=[].slice.call(document.querySelectorAll('a[href]')).filter(e=>e.offsetParent!==null);
  const hit=anchors.filter(e=>{const t=(e.textContent||'').replace(/\\s+/g,' ').trim();
    return t.toLowerCase().startsWith(kw) && t.includes('·') && t.length<300 && /marketplace/i.test(e.getAttribute('href')||'');}).sort((a,b)=>b.getBoundingClientRect().width-a.getBoundingClientRect().width)[0];
  return hit ? hit.getAttribute('href') : 'NO_HREF';
})()""")
print("HREF:", href)
