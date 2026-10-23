import sys, json, time
sys.path.insert(0, r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package")
import cdp_harness as C

tabs = C.list_tabs()
inbox = [t for t in tabs if "inbox" in t.get("url","").lower()]
C._ws = inbox[0]["webSocketDebuggerUrl"]; C._conn = None
time.sleep(1)

r = C.js("""(() => {
  const kw='opoku';
  const els=[].slice.call(document.querySelectorAll('[role=button]')).filter(e=>e.offsetParent!==null);
  const hits=els.filter(e=>{const t=(e.textContent||'').replace(/\\s+/g,' ').trim();
    return t.toLowerCase().startsWith(kw) && t.includes('·') && t.length<300;});
  if(!hits.length) return 'NO_ROW';
  const el=hits.sort((a,b)=>b.getBoundingClientRect().width-a.getBoundingClientRect().width)[0];
  // synthetic mousedown/mouseup/click directly on the element
  const ME=t=>new MouseEvent(t,{bubbles:true,cancelable:true,view:window});
  ['mousedown','mouseup','click'].forEach(t=>el.dispatchEvent(ME(t)));
  el.click && el.click();
  return 'DISPATCHED';
})()""")
print("CLICK:", r)
time.sleep(7)

state = C.js("""(() => {
  const conv=[...document.querySelectorAll('[aria-label]')].filter(e=>e.offsetParent!==null && /conversation titled/i.test(e.getAttribute('aria-label')||'')).map(e=>e.getAttribute('aria-label'));
  const t=document.body.innerText||'';
  return JSON.stringify({conv: conv.slice(0,3), tail: t.slice(-500)});
})()""")
print("STATE:", state[:1200])
