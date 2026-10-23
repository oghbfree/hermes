import sys, json, time
sys.path.insert(0, r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package")
import cdp_harness as C

tabs = C.list_tabs()
inbox = [t for t in tabs if "inbox" in t.get("url","").lower()]
C._ws = inbox[0]["webSocketDebuggerUrl"]; C._conn = None
time.sleep(2)

info = C.js(r"""(() => {
  const nodes=[].slice.call(document.querySelectorAll('[role=link]')).filter(e=>e.offsetParent!==null);
  return JSON.stringify(nodes.map((e,i)=>({i, tag:e.tagName, txt:(e.innerText||e.textContent||'').replace(/\s+/g,' ').slice(0,110), href:(e.getAttribute('href')||'').slice(0,80)})));
})()""")
print(info[:6000])
