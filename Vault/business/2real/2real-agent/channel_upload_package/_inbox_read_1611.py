import sys, time, json
pkg=r'C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package'
sys.path.insert(0,pkg)
import cdp_harness as C
C.goto_url('https://www.facebook.com/marketplace/inbox')
time.sleep(9)
txt=C.js("document.body.innerText")
# print a bounded slice
print(txt[:3500])
