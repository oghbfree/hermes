import sys, json, time
sys.path.insert(0, r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package")
import cdp_harness as C

time.sleep(1)
# scroll the internal list container to the bottom, in steps, then collect anchors
step = C.js("""(() => {
  const cs=[].slice.call(document.querySelectorAll('div')).filter(d=>{const s=getComputedStyle(d); return (s.overflowY==='auto'||s.overflowY==='scroll') && d.scrollHeight>d.clientHeight+50;});
  return cs.length ? cs[0] : null;
})()""")
# evaluate by directly manipulating scrollTop of every candidate container
for i in range(12):
    C.js("""(() => {
      const cs=[].slice.call(document.querySelectorAll('div')).filter(d=>{const s=getComputedStyle(d); return (s.overflowY==='auto'||s.overflowY==='scroll') && d.scrollHeight>d.clientHeight+50;});
      for (const x of cs) x.scrollTop += 800;
      return cs.length;
    })()""")
    time.sleep(1.2)

out = C.js("""(() => {
  const as=document.querySelectorAll('a[href*="/marketplace/item/"]');
  const arr=[];
  as.forEach(function(a){ arr.push((a.innerText||'').replace(/\\s+/g,' ').trim().slice(0,80) + ' || ' + a.href.split('?')[0]); });
  return JSON.stringify({n: arr.length, items: arr});
})()""")
print(out)
