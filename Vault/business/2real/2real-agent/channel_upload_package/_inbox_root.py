"""Navigate the FB inbox tab back to the marketplace inbox root (rows must be in DOM to click)."""
import sys, time
sys.path.insert(0, r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package")
import cdp_harness as C

tabs = C.list_tabs()
inbox = [t for t in tabs if "inbox" in t.get("url", "").lower()]
if not inbox:
    print("NO_INBOX_TAB")
    sys.exit(2)
C._ws = inbox[0]["webSocketDebuggerUrl"]; C._conn = None
C.goto_url("https://www.facebook.com/marketplace/inbox")
time.sleep(6)
# Hard reload to clear any open conversation pane (SPA keeps pane after nav)
try:
    C._send("Page.reload", ignoreCache=True)
except Exception as e:
    print("reload err:", e)
time.sleep(9)
print("NAVIGATED:", (C.js("location.href") or "")[:110])
