import sys, json, time
sys.path.insert(0, r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package")
import cdp_harness as C

time.sleep(1)
txt = C.js("(document.body.innerText||'')") or ""
print("BODYLEN:", len(txt))
print("=" * 60)
print(txt)
