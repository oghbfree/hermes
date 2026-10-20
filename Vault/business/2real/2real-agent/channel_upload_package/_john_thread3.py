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
send('Page.navigate',url='https://www.facebook.com/marketplace/inbox')
time.sleep(8)
# Try to find thread links via aria/role and message thread url patterns
r = js(r"""(() => {
  const out=[];
  const els=[...document.querySelectorAll('a[href], div[role=link], [data-nosnippet] a')].filter(e=>e.offsetParent);
  const seen=new Set();
  for(const a of els){
    const href=a.href||a.getAttribute('href')||'';
    const t=(a.textContent||'').replace(/\s+/g,' ').trim();
    if(t.length>5 && (href.includes('messages') || href.includes('marketplace') || href.includes('profile'))) {
      const k=t.slice(0,25);
      if(!seen.has(k)){seen.add(k); out.push(t.slice(0,120)+'  >>>  '+href.slice(0,90));}
    }
  }
  return out.slice(0,40);
})()""")
for x in (r or []): print(x)
print("---- current URL:", js("location.href"))
