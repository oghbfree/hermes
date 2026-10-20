import json, time, urllib.request, websocket
D='http://127.0.0.1:9222'
tabs=[t for t in json.load(urllib.request.urlopen(D+'/json')) if t['type']=='page' and 'facebook.com' in t['url']]
conn=websocket.create_connection(tabs[0]['webSocketDebuggerUrl'],timeout=90,suppress_origin=True)
mid=[0]
def send(m,**p):
    mid[0]+=1; i=mid[0]
    conn.send(json.dumps({'id':i,'method':m,'params':p}))
    while True:
        msg=json.loads(conn.recv())
        if msg.get('id')==i: return msg.get('result',{})
def js(e):
    r=send('Runtime.evaluate',expression=e,returnByValue=True,awaitPromise=False)
    if r.get('exceptionDetails'): return 'ERR: '+json.dumps(r['exceptionDetails'])[:400]
    return r.get('result',{}).get('value')
# Reload inbox fresh, then JS-click the John thread button
js("location.reload()"); time.sleep(9)
r = js(r"""(() => {
  // find the element/button whose accessible name mentions Open chat ... Loudspeakers / Thumbs
  const all=[...document.querySelectorAll('a,div[role=button],div[role=link]')].filter(e=>e.offsetParent);
  const cand=all.find(e=>{
    const t=(e.getAttribute && (e.getAttribute('aria-label')||'')) || (e.textContent||'');
    return t.includes('Loudspeakers') && t.includes('John');
  });
  if(!cand) return 'NO_CAND';
  const r=cand.getBoundingClientRect();
  // prefer the most specific (smaller area) matching node
  return JSON.stringify({x:r.x+r.width/2,y:r.y+r.height/2,w:r.width,h:r.height,tag:cand.tagName,label:(cand.getAttribute('aria-label')||cand.textContent||'').replace(/\s+/g,' ').slice(0,70)});
})()""")
print("CAND:", r)
try:
    c=json.loads(r)
    # JS click via mouse events on the element itself located by text
    js(r"""(() => {
      const all=[...document.querySelectorAll('a,div[role=button],div[role=link]')].filter(e=>e.offsetParent);
      const cand=all.find(e=>{const t=(e.getAttribute&&e.getAttribute('aria-label'))||''; return t.includes('Loudspeakers')&&t.includes('John');});
      if(!cand) return 'none';
      const ME=t=>new MouseEvent(t,{bubbles:true,cancelable:true,view:window});
      ['mousedown','mouseup','click'].forEach(t=>cand.dispatchEvent(ME(t)));
      return 'clicked '+cand.tagName;
    })()""")
    time.sleep(7)
except Exception as e:
    print("err",e)
print("URL:", js("location.href"))
# Check the conversation area - is the visible chat now about Sony?
vis = js(r"""(() => {
  const main=document.querySelector('[role=main]');
  const t=main?main.innerText:'';
  // find the textbox placeholder / conversation
  const tb=document.querySelector('div[role=textbox]');
  const ph = tb ? (tb.getAttribute('aria-label')||tb.getAttribute('placeholder')||'') : '';
  return JSON.stringify({ph, hasSonyInMain: t.includes('Sony 2 Long Loudspeakers'), tail:t.slice(-400)});
})()""")
print("VIS:", vis)
