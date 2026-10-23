import sys, json, time
sys.path.insert(0, r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package")
import cdp_harness as C

time.sleep(1)
info = C.js(r"""(() => {
  const kw='black decker electric power drill 520w';
  const els=[].slice.call(document.querySelectorAll('div,span,a')).filter(e=>e.offsetParent!==null);
  const leaf=els.filter(e=>{
    const t=(e.innerText||e.textContent||'').replace(/\s+/g,' ').trim().toLowerCase();
    return t===kw;
  }).pop();
  if(!leaf) return 'NO_LEAF';
  const chain=[]; let n=leaf;
  for(let i=0;i<6 && n && n!==document.body;i++,n=n.parentElement){
    chain.push({tag:n.tagName, role:n.getAttribute&&n.getAttribute('role'), href:(n.getAttribute&&n.getAttribute('href')||'').slice(0,80),
      cls:(typeof n.className==='string'?n.className:'').slice(0,40),
      txt:(n.innerText||n.textContent||'').replace(/\s+/g,' ').slice(0,60)});
  }
  // buttons inside the card (up to 2 levels up from leaf)
  const card = chain[chain.length-1];
  const btns = card ? [].slice.call(card.querySelectorAll('[role=button],button')).map(b=>({t:(b.innerText||b.getAttribute('aria-label')||'').trim().slice(0,30), aria:b.getAttribute('aria-label')||''})).slice(0,8) : [];
  return JSON.stringify({chain, btns});
})()""")
print(info)
