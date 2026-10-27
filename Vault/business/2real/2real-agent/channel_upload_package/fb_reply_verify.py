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
C.js("""(() => {
  const els = [...document.querySelectorAll('a[role=link],div[role=link],div[role=button]')];
  const hit = els.find(e => {
    const t = e.innerText||'';
    return t.includes('Stephanie') && t.includes('Gaggenau') && t.length < 400;
  });
  if (hit) { hit.click(); return 'clicked2'; }
  const hit2 = els.find(e => (e.innerText||'').trim().startsWith('Stephanie'));
  if (hit2) { hit2.click(); return 'clicked-any'; }
  return 'none';
})()""")
time.sleep(6)
txt = C.js('document.body.innerText') or ''
print('VERIFIED' if 'still available - Gaggenau' in txt else 'NOT FOUND')
i = txt.find('still available - Gaggenau')
print(txt[max(0,i-200):i+260].replace('\n',' | '))

# log thread in sales ops
try:
    import fb_sales_ops
    fb_sales_ops.BuyerThreads().upsert({
        'thread_id': 'gaggenau-stephanie-doh',
        'buyer': 'Stephanie (Doh Edzenyunye)',
        'item_title': 'Gaggenau Industrial Deep Fryer From UK',
        'price': 1000,
        'last_msg_from': 'us',
        'last_msg_time': '2026-10-26 22:5x',
        'note': 'Replied: available, GHS1000, MoMo/cash, pickup Oyarifa, 0204252252'
    })
    print('UPSERT OK')
except Exception as e:
    print('upsert failed:', repr(e))
