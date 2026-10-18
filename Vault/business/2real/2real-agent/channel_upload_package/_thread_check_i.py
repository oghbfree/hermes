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
def open_thread(name):
    send('Page.navigate',url='https://www.facebook.com/marketplace/inbox')
    time.sleep(6)
    js("""(() => {
      const els=[...document.querySelectorAll('div')].filter(e=>e.offsetParent&&e.querySelector('img,svg')&&e.innerText.startsWith('%s')&&e.innerText.includes('\\u00b7')&&e.innerText.length<800);
      (els.sort((a,b)=>a.innerText.length-b.innerText.length)[0]||{}).click?.();
      return 'ok';
    })()""" % name)
    time.sleep(6)
    t = js("""(() => {
      const t=document.body.innerText; const i=t.indexOf('Messages'); const j=t.lastIndexOf('Compose');
      return i>=0&&j>i ? t.slice(i,j) : t.slice(-2500);
    })()""")
    print('=====', name, '=====')
    print((t or '')[-1800:])

for n in ['Ananman','Hellen']:
    open_thread(n)
