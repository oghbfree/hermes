import sys, time, json
pkg=r'C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package'
sys.path.insert(0,pkg)
import cdp_harness as C
# Marketplace inbox search for the thread
C.goto_url('https://www.facebook.com/marketplace/inbox')
time.sleep(8)
# use the search box to locate Nyoja's Minelab thread
C.js("document.body.innerText.includes('Nyoja')")
C.goto_url('https://www.facebook.com/marketplace/inbox')
time.sleep(3)
txt=C.js("document.body.innerText")
print("HAS NYOJA:", 'Nyoja' in txt)
# print the region around Nyoja
i=txt.find('Nyoja')
print(txt[i-200:i+200] if i>=0 else 'not found')
