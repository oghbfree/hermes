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
    if r.get('exceptionDetails'): return 'ERR: '+json.dumps(r['exceptionDetails'])[:300]
    return r.get('result',{}).get('value')

send('Page.navigate',url='https://www.facebook.com/marketplace/inbox')
time.sleep(8)
rows=js(r"""(() => {
  const out=[];
  const divs=[...document.querySelectorAll('div')].filter(e=>e.offsetParent&&e.querySelector('img,svg')&&/\u00b7/.test(e.innerText)&&e.innerText.length>10&&e.innerText.length<400);
  const seen=new Set();
  for(const e of divs){
    const t=e.innerText.replace(/\n+/g,' | ').trim();
    if(seen.has(t)) continue; seen.add(t);
    out.push(t);
  }
  return out.slice(0,30);
})()""")
for r in rows: print(r)
