import json, time, urllib.request, websocket, sys
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

# go back to inbox list first
send('Page.navigate',url='https://www.facebook.com/marketplace/inbox')
time.sleep(6)
for name in ['Chris','Awurabena','Nii']:
    CLICK = r"""(() => {
      const rows=[...document.querySelectorAll('div')].filter(e=>e.offsetParent&&e.innerText.startsWith('%s')&&e.innerText.includes('\u00b7')&&e.innerText.length<700&&e.querySelector('img,svg'));
      const el=rows.sort((a,b)=>a.innerText.length-b.innerText.length)[0];
      if(!el) return 'notfound';
      el.click(); return 'clicked';
    })()""" % name
    r=js(CLICK)
    time.sleep(6)
    # extract conversation part: after 'Messages' marker to 'Compose'
    TXT = r"""(() => {
      const t=document.body.innerText;
      const i=t.indexOf('Messages');
      const j=t.lastIndexOf('Compose');
      return i>=0&&j>i ? t.slice(i,j) : t.slice(-2500);
    })()"""
    print('=====',name, r)
    print(js(TXT)[-2600:])
    # back to list
    send('Page.navigate',url='https://www.facebook.com/marketplace/inbox')
    time.sleep(6)
