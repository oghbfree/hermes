import sys, json, time
sys.path.insert(0, r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package")
import cdp_harness as C

tabs = C.list_tabs()
inbox = [t for t in tabs if "inbox" in t.get("url","").lower()]
C._ws = inbox[0]["webSocketDebuggerUrl"]; C._conn = None
time.sleep(2)

needle = "0204252252"
# Confirm header + composer content
state = C.js(r"""(() => {
  const eds=[...document.querySelectorAll('[contenteditable=true]')].filter(e=>e.offsetParent!==null);
  const headerAria=[...document.querySelectorAll('[aria-label]')].filter(e=>e.offsetParent!==null && /conversation titled/i.test(e.getAttribute('aria-label')||'')).map(e=>e.getAttribute('aria-label'));
  return JSON.stringify({sel_ed: eds.length, composer: eds.length?eds[0].innerText.trim():'', headerAria: headerAria.slice(0,2)});
})()""")
print("STATE:", state[:600])
st = json.loads(state)
if st.get("composer", "").count("Wh") == 0 and "Leapfrog" not in st.get("composer", ""):
    # nothing composed: abort (do not send anything)
    print("RESULT: ABORT composer_empty")
    sys.exit(4)

# Press Enter exactly once
press = C.js(r"""(() => {
  const ed=[...document.querySelectorAll('[contenteditable=true]')].filter(e=>e.offsetParent!==null)[0];
  if(!ed) return 'NO_ED';
  ed.focus();
  const KE = new KeyboardEvent('keydown', {key:'Enter', code:'Enter', keyCode:13, which:13, bubbles:true, cancelable:true});
  const ok = ed.dispatchEvent(KE);
  ed.dispatchEvent(new KeyboardEvent('keyup', {key:'Enter', code:'Enter', keyCode:13, which:13, bubbles:true}));
  return ok?'DISPATCHED':'BLOCKED';
})()""")
print("ENTER:", press)
time.sleep(5)

ver = C.js(r"""(() => {
  const eds=[...document.querySelectorAll('[contenteditable=true]')].filter(e=>e.offsetParent!==null);
  const t=document.body.innerText||'';
  return JSON.stringify({composer: eds.length?eds[0].innerText.trim():'NO_ED', seen_in_body: t.includes(%s)});
})()""" % json.dumps("Hi Anakwa!"))
print("VERIFY:", ver)
v = json.loads(ver)
if v.get("composer") == "" and v.get("seen_in_body"):
    print("RESULT: SENT")
    sys.exit(0)
elif v.get("seen_in_body"):
    print("RESULT: SENT_BUT_COMPOSER_NOT_CLEAR", ver)
    sys.exit(0)  # text visible in conversation = delivered
else:
    print("RESULT: NOT_SENT", ver)
    sys.exit(5)
