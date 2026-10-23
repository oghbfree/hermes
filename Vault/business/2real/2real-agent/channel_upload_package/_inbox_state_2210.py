import sys, json, time
sys.path.insert(0, r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package")
import cdp_harness as C

tabs = C.list_tabs()
inbox = [t for t in tabs if "inbox" in t.get("url","").lower() or "marketplace" in t.get("url","").lower()]
C._ws = inbox[0]["webSocketDebuggerUrl"]; C._conn = None
time.sleep(2)

info = C.js(r"""(() => {
  const t = document.body.innerText || '';
  const idxType = t.indexOf('Type a message');
  const eds=[...document.querySelectorAll('[contenteditable=true]')].filter(e=>e.offsetParent!==null);
  // find any elements that look like send affordances
  const sendish=[...document.querySelectorAll('[aria-label],[role=button],button')].filter(e=>e.offsetParent!==null && /send/i.test((e.getAttribute('aria-label')||'')+(e.textContent||''))).slice(0,8).map(e=>({tag:e.tagName, aria:e.getAttribute('aria-label'), txt:(e.textContent||'').trim().slice(0,20)}));
  return JSON.stringify({
    url: location.href.slice(0,140),
    bodylen: t.length,
    has_type_msg: idxType,
    eds: eds.length,
    ed_html: eds.length? eds[0].outerHTML.slice(0,200):'',
    around_type: idxType>-1? t.slice(Math.max(0,idxType-700), idxType+80):'(none)',
    sendish,
    has_anakwa_header: /Anakwa/i.test(t.slice(0,2500))
  });
})()""")
print(info)
