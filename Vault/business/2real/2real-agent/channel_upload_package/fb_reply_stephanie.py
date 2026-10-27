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
# click the Stephanie thread
r = C.js("""(() => {
  const els = [...document.querySelectorAll('a[role=link],div[role=link],div[role=button]')];
  const hit = els.find(e => (e.innerText||'').startsWith('Stephanie') && (e.innerText||'').includes('Gaggenau'));
  if (hit) { hit.click(); return 'clicked'; }
  return 'not-found';
})()""")
print("thread:", r)
time.sleep(6)
# type into the message box and send
msg = ("Hi Stephanie! Yes, the Gaggenau Industrial Deep Fryer is still available - GHS 1,000. "
       "UK Imported, Quality Checked. MoMo or cash only (no credit). "
       "Pickup Oyarifa or delivery arranged. Call/WhatsApp 0204252252")
r2 = C.js("""((msg) => {
  const box = document.querySelector('div[role=textbox][aria-label], div[role=textbox]');
  if (!box) return 'no-box';
  box.focus();
  document.execCommand('insertText', false, msg);
  return 'typed';
})""" + "(" + __import__('json').dumps(msg) + ")")
print("type:", r2)
time.sleep(2)
r3 = C.js("""(() => {
  const btns = [...document.querySelectorAll('div[role=button],button')];
  const send = btns.find(b => (b.getAttribute('aria-label')||'').toLowerCase().includes('send') || (b.innerText||'').trim().toLowerCase()==='send');
  if (send) { send.click(); return 'sent'; }
  return 'no-send-btn';
})()""")
print("send:", r3)
