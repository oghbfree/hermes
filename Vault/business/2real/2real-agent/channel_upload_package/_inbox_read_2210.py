"""Read FB Marketplace inbox via CDP 9222 — dump thread rows (READ-ONLY)."""
import os, sys, json, time, re, urllib.request
sys.path.insert(0, r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package")
import cdp_harness as C

# Find a marketplace tab to reuse (avoid opening extra): prefer inbox tab if open
tabs = C.list_tabs()
print("tabs:", [(t.get("title","")[:40], t.get("url","")[:70]) for t in tabs])
inbox = [t for t in tabs if "/marketplace/inbox" in t.get("url","") or "marketplace/you/inbox" in t.get("url","")]
if inbox:
    C._ws = C._ws_for_url_filter("/marketplace/inbox")
    C._conn = None
else:
    C.goto_url("https://www.facebook.com/marketplace/inbox")

time.sleep(8)
# scroll to force lazy rows to load
for _ in range(6):
    C.js("window.scrollBy(0, 1200)")
    time.sleep(1.2)
C.js("window.scrollTo(0,0)")
time.sleep(2)

txt = C.js("document.body.innerText") or ""
print("="*50)
print("INBOX TEXT LEN:", len(txt))
print(txt[:9000])
