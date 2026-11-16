import sys, time, json
pkg=r'C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package'
sys.path.insert(0,pkg)
import cdp_harness as C
C.goto_url('https://www.facebook.com/marketplace/inbox')
time.sleep(10)
print('URL:', C.js("location.href"))
print('has Patrick:', C.js("document.body.innerText.includes('iamPatrick')"))
r=C.js("""(() => {
  const as=[...document.querySelectorAll('a')].filter(a=>a.offsetParent!==null && a.href && a.href.includes('messages'));
  return JSON.stringify(as.map(a=>({h:a.href.slice(0,60), t:(a.innerText||'').replace(/\n/g,'|').slice(0,50)})).slice(0,30));
})()""")
print('msg links:', r[:1500])
print('body near Patrick:', C.js("(() => {const t=document.body.innerText; const i=t.indexOf('iamPatrick'); return i>=0? t.slice(Math.max(0,i-100), i+120):'nf';})()"))
