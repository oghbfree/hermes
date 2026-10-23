import sys, json, time
sys.path.insert(0, r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package")
import cdp_harness as C

time.sleep(1)
info = C.js(r"""(() => {
  const kw='black decker electric power drill';
  const els=[].slice.call(document.querySelectorAll('div,span,a')).filter(e=>e.offsetParent!==null);
  const hits=els.filter(e=>{
    const t=(e.innerText||e.textContent||'').replace(/\s+/g,' ').trim().toLowerCase();
    return t.startsWith(kw) && t.length < 200;
  });
  if(!hits.length) return 'NO_HITS';
  const el = hits[hits.length-1];
  const chain=[]; let n=el;
  for(let i=0;i<8 && n && n!==document.body;i++,n=n.parentElement){
    chain.push({tag:n.tagName, role:n.getAttribute&&n.getAttribute('role'), href:(n.getAttribute&&n.getAttribute('href')||'').slice(0,90),
      cls:(typeof n.className==='string'?n.className:'').slice(0,45),
      txt:(n.innerText||n.textContent||'').replace(/\s+/g,' ').slice(0,55)});
  }
  const card = chain[chain.length-1];
  const btns = card ? [].slice.call(card.querySelectorAll('[role=button],button')).map(b=>({t:(b.innerText||b.getAttribute('aria-label')||'').trim().slice(0,30), aria:b.getAttribute('aria-label')||''})).slice(0,10) : [];
  const links = card ? [].slice.call(card.querySelectorAll('a[href]')).map(a=>(a.getAttribute('href')||'').slice(0,90)).slice(0,6) : [];
  return JSON.stringify({hits: hits.length, chain, btns, links});
})()""")
print(info)
