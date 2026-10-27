import time, sys, json
sys.path.insert(0, r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package")
import cdp_harness as C
C.connect(substr='facebook.com', exclude_substr='marketplace/create')
C.goto_url('https://www.facebook.com/marketplace/inbox')
try:
    C.wait_for_load()
except Exception:
    pass
time.sleep(8)
txt = C.js('document.body.innerText') or ''
print(txt[:4000])
