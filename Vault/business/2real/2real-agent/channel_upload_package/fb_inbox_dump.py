import time, sys
sys.path.insert(0, r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package")
import cdp_harness as C
C.connect(substr='facebook.com', exclude_substr='marketplace/create')
C.goto_url('https://www.facebook.com/marketplace/inbox')
try:
    C.wait_for_load()
except Exception:
    pass
time.sleep(10)
r = C.js("""(() => {
  const els = [...document.querySelectorAll('a[role=link],div[role=link],div[role=button]')];
  const hit = els.find(e => (e.innerText||'').startsWith('Stephanie') && (e.innerText||'').includes('Gaggenau'));
  if (hit) { hit.click(); return 'clicked'; }
  return 'not-found';
})()""")
print("click:", r)
time.sleep(6)
time.sleep(6)
txt = C.js('document.body.innerText') or ''
print('VERIFIED' if 'still available - Gaggenau' in txt else 'NOT FOUND')
i = txt.find('Gaggenau')
print(txt[max(0,i-100):i+900].replace('\n',' | ') if i>=0 else txt[:600].replace('\n',' | '))
