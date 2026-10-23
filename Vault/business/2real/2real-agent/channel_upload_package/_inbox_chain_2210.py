import sys, json, time
sys.path.insert(0, r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package")
import cdp_harness as C

tabs = C.list_tabs()
inbox = [t for t in tabs if "inbox" in t.get("url","").lower()]
C._ws = inbox[0]["webSocketDebuggerUrl"]; C._conn = None
time.sleep(2)

info = C.js(r"""(() => {
  const out=[];
  for (const target of ['Anakwa','Opoku','Michael Kwesi','Richard']){
    const hits=[].slice.call(document.querySelectorAll('body *')).filter(e=>e.children.length===0 && (e.textContent||'').includes(target) && e.offsetParent!==null);
    if(!hits.length){ out.push(target+': NONE'); continue; }
    const el=hits[0];
    const chain=[];
    let n=el;
    for(let i=0;i<8 && n && n!==document.body;i++,n=n.parentElement){
      chain.push({tag:n.tagName, role:n.getAttribute&&n.getAttribute('role'), cls:(n.className||'').toString().slice(0,40), href:(n.getAttribute&&n.getAttribute('href')||'').slice(0,60), txt:(n.textContent||'').replace(/\s+/g,' ').slice(0,50)});
    }
    out.push(target+' -> '+JSON.stringify(chain));
  }
  return out.join('\n');
})()""")
print(info)
