import sys, json, time
sys.path.insert(0, r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package")
import cdp_harness as C

time.sleep(1)
info = C.js(r"""(() => {
  try {
    const kw='black decker electric power drill';
    const els=[].slice.call(document.querySelectorAll('div,span,a')).filter(function(e){ return e.offsetParent!==null; });
    const hits=els.filter(function(e){
      const t=(e.innerText||e.textContent||'').replace(/\s+/g,' ').trim().toLowerCase();
      return t.startsWith(kw) && t.length < 200;
    });
    if(!hits.length) return 'NO_HITS';
    const el = hits[hits.length-1];
    const chain=[]; let n=el;
    for(let i=0;i<8 && n && n!==document.body;i++,n=n.parentElement){
      chain.push({tag:n.tagName, role:(n.getAttribute?n.getAttribute('role'):''), href:(n.getAttribute?n.getAttribute('href')||'':'').slice(0,90),
        cls:(typeof n.className==='string'?n.className:'').slice(0,45),
        txt:(n.innerText||n.textContent||'').replace(/\s+/g,' ').slice(0,55)});
    }
    const card = chain[chain.length-1];
    const btns = card ? [].slice.call(card.querySelectorAll('[role=button],button')).map(function(b){ return (b.innerText||b.getAttribute('aria-label')||'').trim().slice(0,30); }).slice(0,10) : [];
    return JSON.stringify({hits: hits.length, chain: chain, btns: btns});
  } catch (err) { return 'JSERR: ' + err.message; }
})()""")
print(info)
