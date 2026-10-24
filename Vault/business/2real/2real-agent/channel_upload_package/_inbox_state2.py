"""Verify current FB inbox conversation state: does the last message appear in the thread? Is composer empty?"""
import sys, json, time
sys.path.insert(0, r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package")
import cdp_harness as C

tabs = C.list_tabs()
inbox = [t for t in tabs if "inbox" in t.get("url", "").lower()]
if not inbox:
    print("NO_INBOX_TAB"); sys.exit(2)
C._ws = inbox[0]["webSocketDebuggerUrl"]; C._conn = None
time.sleep(3)
state = C.js("""(() => {
  const conv=[...document.querySelectorAll('[aria-label]')].filter(e=>e.offsetParent!==null && /conversation titled/i.test(e.getAttribute('aria-label')||'')).map(e=>e.getAttribute('aria-label'));
  const eds=[...document.querySelectorAll('[contenteditable=true]')].filter(e=>e.offsetParent!==null);
  const t=document.body.innerText||'';
  return JSON.stringify({conv: conv.slice(0,2), composer: eds.length?eds[0].innerText.trim().slice(0,80):'NO_ED', tail: t.slice(-2200)});
})()""")
print(state)
