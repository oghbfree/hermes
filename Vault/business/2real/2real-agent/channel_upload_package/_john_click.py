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
def click(x,y):
    send('Input.dispatchMouseEvent',type='mousePressed',x=x,y=y,button='left',clickCount=1)
    send('Input.dispatchMouseEvent',type='mouseReleased',x=x,y=y,button='left',clickCount=1)
# enumerate candidate click targets for the John row in left list
r = js(r"""(() => {
  const out=[];
  for(const e of [...document.querySelectorAll('*')]){
    if(!e.offsetParent) continue;
    const t=e.textContent||'';
    if(!t.includes('Loudspeakers')||!t.includes('Thumbs')) continue;
    const r=e.getBoundingClientRect();
    if(r.width<10||r.height<10||r.width>700) continue;
    out.push({tag:e.tagName,role:e.getAttribute('role'),x:Math.round(r.x+r.width/2),y:Math.round(r.y+r.height/2),w:Math.round(r.width),h:Math.round(r.height),txt:t.replace(/\s+/g,' ').slice(0,55)});
    if(out.length>=12) break;
  }
  return out;
})()""")
for o in (r or []): print(o)
