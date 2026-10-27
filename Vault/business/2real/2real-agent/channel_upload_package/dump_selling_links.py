import time, sys
sys.path.insert(0, r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package")
import fb_share_groups as sg

C = sg.C
C.connect(substr='facebook.com', exclude_substr='marketplace/create')
C.goto_url('https://www.facebook.com/marketplace/you/selling')
try:
    C.wait_for_load()
except Exception:
    pass
time.sleep(8)
for _ in range(10):
    C.js("window.scrollBy(0, 1500)")
    time.sleep(1.5)
expr = """(() => { const out={}; for (const a of document.querySelectorAll('a[href*="/marketplace/item/"]')) { const m=a.href.match(/item\\/(\\d+)/); if(m && a.offsetParent!==null) out[m[1]]=(a.innerText||'').replace(/\\n/g,' | ').slice(0,100); } return out; })()"""
print(C.js(expr))
