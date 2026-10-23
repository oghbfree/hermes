import sys, json, time
sys.path.insert(0, r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package")
import cdp_harness as C

tabs = C.list_tabs()
inbox = [t for t in tabs if "inbox" in t.get("url","").lower()]
C._ws = inbox[0]["webSocketDebuggerUrl"]; C._conn = None
time.sleep(1)

info = C.js("""(() => {
  const kw='opoku';
  const els=[].slice.call(document.querySelectorAll('div,span,a')).filter(e=>e.offsetParent!==null);
  const hit=els.filter(e=>{const t=(e.textContent||'').replace(/\\s+/g,' ').trim();
    return t.toLowerCase().startsWith(kw) && t.includes('·') && t.length<200;}).pop();
  if(!hit) return 'NO_HIT';
  const chain=[]; let n=hit;
  for(let i=0;i<10 && n && n!==document.body;i++,n=n.parentElement){
    chain.push({tag:n.tagName, role:n.getAttribute&&n.getAttribute('role'), href:(n.getAttribute&&n.getAttribute('href')||'').slice(0,90), cls:(typeof n.className==='string'?n.className:'').slice(0,50), txt:(n.textContent||'').replace(/\\s+/g,' ').slice(0,40)});
  }
  return JSON.stringify(chain);
})()""")
print(info)
