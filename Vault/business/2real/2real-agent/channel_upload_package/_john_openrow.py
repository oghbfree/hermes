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
# Click the thread row button backend 24861
bm = send('DOM.getBoxModel', backendNodeId=24861)
if 'model' in bm:
    c=bm['model']['content']; x=(c[0]+c[2])/2; y=(c[1]+c[3])/2
    print("row click",round(x,1),round(y,1))
    click(x,y); time.sleep(7)
else:
    print("no box:", bm)
# Check conversation header - look for 'Sony' near the top and whether we are in John's chat
hdr = js(r"""(() => {
  const els=[...document.querySelectorAll('[role=main] *')].filter(e=>e.offsetParent && e.children.length===0);
  const soy=els.filter(e=>/Sony 2 Long Loudspeakers/.test(e.textContent||'')).map(e=>e.getBoundingClientRect());
  return "Sony-leaf-count:"+soy.length;
})()""")
print(hdr)
body=js("document.body.innerText")
# Is the visible conversation John/Sony now? search for recent buyer message
print("has 'Thumbs up':", 'Thumbs up' in (body or ''))
print("TAIL:", (body or '')[-500:])
