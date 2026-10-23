import sys, json, time
sys.path.insert(0, r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package")
import cdp_harness as C

tabs = C.list_tabs()
inbox = [t for t in tabs if "inbox" in t.get("url","").lower()]
C._ws = inbox[0]["webSocketDebuggerUrl"]; C._conn = None
time.sleep(1)

# click Opoku row ([role=button] starting with 'Opoku ·')
r = C.js("""(() => {
  const kw='opoku';
  const els=[].slice.call(document.querySelectorAll('[role=button]')).filter(e=>e.offsetParent!==null);
  const hits=els.filter(e=>{const t=(e.textContent||'').replace(/\\s+/g,' ').trim();
    return t.toLowerCase().startsWith(kw) && t.includes('·') && t.length<300;});
  if(!hits.length) return 'NO_ROW';
  const el=hits.sort((a,b)=>b.getBoundingClientRect().width-a.getBoundingClientRect().width)[0];
  el.scrollIntoView({block:'center'});
  const rc=el.getBoundingClientRect();
  return JSON.stringify({x:rc.x+rc.width/2,y:rc.y+rc.height/2,w:rc.width,h:rc.height, txt:(el.textContent||'').replace(/\\s+/g,' ').trim().slice(0,80)});
})()""")
print("ROW:", r)
if r and r != "NO_ROW":
    p = json.loads(r)
    C.click_at_xy(int(p["x"]), int(p["y"]))
    time.sleep(7)

state = C.js("""(() => {
  const conv=[...document.querySelectorAll('[aria-label]')].filter(e=>e.offsetParent!==null && /conversation titled/i.test(e.getAttribute('aria-label')||'')).map(e=>({aria:e.getAttribute('aria-label'), tag:e.tagName}));
  const eds=[...document.querySelectorAll('[contenteditable=true]')].filter(e=>e.offsetParent!==null);
  const t=document.body.innerText||'';
  return JSON.stringify({
    conv: conv.slice(0,5),
    eds: eds.length,
    ed_ph: eds.length? (eds[0].getAttribute('aria-placeholder')||eds[0].getAttribute('data-ph')||''):'',
    tail: t.slice(-900)
  });
})()""")
print("STATE:", state[:3000])
