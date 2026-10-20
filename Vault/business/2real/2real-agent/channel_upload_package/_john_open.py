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
send('Page.navigate',url='https://www.facebook.com/marketplace/inbox')
time.sleep(8)
# Find the row containing John / Sony and click it
r = js(r"""(() => {
  const nodes=[...document.querySelectorAll('*')].filter(e=>e.offsetParent && e.children.length===0 && /Sony 2 Long Loudspeakers/.test(e.textContent||''));
  let best=null;
  for(const n of nodes){
    const r=n.getBoundingClientRect();
    if(r.width>0&&r.height>0 && (!best|| r.width*r.height < best.area)){best={x:r.x+r.width/2,y:r.y+r.height/2,area:r.width*r.height,txt:n.textContent.slice(0,80)};}
  }
  return best?JSON.stringify(best):'NOTFOUND';
})()""")
print("CLICK TARGET:", r)
try:
    tgt=json.loads(r)
    click(tgt['x'],tgt['y']); time.sleep(5)
except Exception as e:
    print("click err", e)
print("URL now:", js("location.href"))
txt = js("document.body.innerText")
# print the last ~800 chars of the convo
print("BODY TAIL:", txt[-1200:])
