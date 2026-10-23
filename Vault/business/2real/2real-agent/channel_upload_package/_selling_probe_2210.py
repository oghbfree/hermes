import sys, json, time
sys.path.insert(0, r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package")
import cdp_harness as C

time.sleep(2)
try:
    print("URL:", C.js("location.href") or "None")
    print("TITLE:", C.js("document.title") or "None")
    n = C.js("document.querySelectorAll('a').length")
    print("ANCHOR COUNT:", n)
except Exception as e:
    print("EXC:", repr(e))
