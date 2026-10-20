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
# Scan for any element containing 'Sony 2 Long' or 'John' with a bounding box, print coords
r = js(r"""(() => {
  const out=[];
  for(const e of [...document.querySelectorAll('div,a,span')]){
    if(!e.offsetParent) continue;
    const t=e.textContent||'';
    if(!/Loudspeakers/.test(t)) continue;
    const r=e.getBoundingClientRect();
    if(r.width<10||r.height<10) continue;
    out.push({tag:e.tagName,role:e.getAttribute('role'),rect:[Math.round(r.x),Math.round(r.y),Math.round(r.width),Math.round(r.height)],txt:t.replace(/\s+/g,' ').slice(0,60)});
    if(out.length>=15) break;
  }
  return out;
})()""")
for o in (r or []): print(o)
print("=== body contains Loudspeakers?", js("document.body.innerText.includes('Loudspeakers')"))
print("body contains John?", js("document.body.innerText.includes('John')"))
