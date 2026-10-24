"""Clear the active FB composer completely and verify empty."""
import sys, json, time
sys.path.insert(0, r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package")
import cdp_harness as C

tabs = C.list_tabs()
inbox = [t for t in tabs if "inbox" in t.get("url", "").lower()]
if not inbox:
    print("NO_INBOX_TAB"); sys.exit(2)
C._ws = inbox[0]["webSocketDebuggerUrl"]; C._conn = None
time.sleep(2)

r = C.js("""(() => {
  const ed=[...document.querySelectorAll('[contenteditable=true]')].filter(e=>e.offsetParent!==null)[0];
  if(!ed) return 'NO_ED';
  ed.focus();
  document.execCommand('selectAll', false, null);
  document.execCommand('delete', false, null);
  ed.textContent='';
  ed.dispatchEvent(new InputEvent('input', {bubbles:true, inputType:'deleteContentBackward', data:null}));
  return ed.innerText.trim() || 'CLEARED';
})()""")
print("CLEAR:", repr(r))
time.sleep(1)
st = C.js("""(() => {
  const eds=[...document.querySelectorAll('[contenteditable=true]')].filter(e=>e.offsetParent!==null);
  return eds.length? JSON.stringify({text: eds[0].innerText.trim()}) : 'NO_ED';
})()""")
print("AFTER:", st)
