import sys, time, json
pkg=r'C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package'
sys.path.insert(0,pkg)
import cdp_harness as C
C.goto_url('https://www.facebook.com/marketplace/inbox')
time.sleep(10)
# text-range based point for the string
pt=C.js("""(() => {
  const w=window, d=document;
  const txt='iamPatrick';
  const it=d.createTreeWalker(d.body, NodeFilter.SHOW_TEXT);
  let n; 
  while(n=it.nextNode()){ if(n.data && n.data.includes(txt)){ break; } }
  if(!n) return 'nf';
  const r=document.createRange(); r.selectNodeContents(n);
  const b=r.getBoundingClientRect();
  return JSON.stringify({x:(b.x+b.width/2)|0, y:(b.y+b.height/2)|0});
})()""")
print('char point:', pt)
