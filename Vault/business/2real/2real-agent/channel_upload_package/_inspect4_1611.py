import sys, time, json
pkg=r'C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package'
sys.path.insert(0,pkg)
import cdp_harness as C
C.goto_url('https://www.facebook.com/marketplace/inbox')
time.sleep(10)
near=C.js("(() => {const t=document.body.innerText; const i=t.indexOf('iamPatrick'); return i>=0? t.slice(Math.max(0,i-60), i+160):'nf';})()")
print('near Patrick:', near)
# find element containing Patrick and climb to clickable ancestor, get a point
pt=C.js("""(() => {
  let el=[...document.querySelectorAll('div,span,a')].find(e=>e.offsetParent!==null && e.innerText && e.innerText.includes('iamPatrick'));
  if(!el) return 'nf';
  for(let k=0;k<6&&el;k++){ if(el.onclick || el.getAttribute('role')==='button' || el.tagName==='A'){break;} el=el.parentElement; }
  const r=el.getBoundingClientRect();
  return JSON.stringify({x:(r.x+r.width/2)|0, y:(r.y+20)|0, tag:el.tagName, cls:(el.className||'').toString().slice(0,40)});
})()""")
print('click point:', pt)
