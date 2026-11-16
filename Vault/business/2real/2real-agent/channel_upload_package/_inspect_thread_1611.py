import sys, time, json
pkg=r'C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package'
sys.path.insert(0,pkg)
import cdp_harness as C
C.goto_url('https://www.facebook.com/marketplace/inbox')
time.sleep(8)
# open first thread by clicking it
r=C.js("""(() => {
  const rows=[...document.querySelectorAll('div[role=row],[role=listitem]')].filter(e=>e.offsetParent!==null);
  return rows.length;
})()""")
print('role rows:', r)
# list all clickable conversation items
rows=C.js("""(() => {
  const els=[...document.querySelectorAll('div[role=row],[role=listitem],a[role=link]')].filter(e=>e.offsetParent!==null && e.innerText);
  return els.slice(0,20).map(e=>e.innerText.replace(/\n/g,' | ').slice(0,80));
})()""")
print('rows:', rows)
