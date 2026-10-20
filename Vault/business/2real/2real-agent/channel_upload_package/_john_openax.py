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
# Use backend 25465 (Open chat button). Get box model.
bm = send('DOM.getBoxModel', backendNodeId=25465)
if 'model' in bm:
    c=bm['model']['content']
    x=(c[0]+c[2])/2; y=(c[1]+c[3])/2
    print("clicking", x, y)
    click(x,y); time.sleep(6)
else:
    print("no box model:", bm)
print("URL:", js("location.href"))
print("HAS textbox:", js("!!document.querySelector('div[role=textbox]')"))
body=js("document.body.innerText")
print("TAIL:", (body or '')[-600:])
