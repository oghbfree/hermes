import sys, time, json
pkg=r'C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package'
sys.path.insert(0,pkg)
import cdp_harness as C
C.goto_url('https://www.facebook.com/marketplace/inbox')
time.sleep(9)
# find a clickable element containing 'iamPatrick'
r=C.js("""(() => {
  const out=[];
  const all=[...document.querySelectorAll('div,span,a')].filter(e=>e.offsetParent!==null && e.innerText && e.innerText.includes('iamPatrick') && e.innerText.length<400);
  all.sort((a,b)=>a.innerText.length-b.innerText.length);
  return all.slice(0,5).map(e=>({tag:e.tagName, t:e.innerText.replace(/\n/g,' | ').slice(0,90), r:(e.getBoundingClientRect().x|0)+','+(e.getBoundingClientRect().y|0)}));
})()""")
print(r)
