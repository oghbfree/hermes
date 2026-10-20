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
# find John's thread link among the rows
r = js(r"""(() => {
  const links=[...document.querySelectorAll('a[href*="/marketplace/profile/"], a[href*="/messages/t/"], a[role=link]')].filter(e=>e.offsetParent);
  const row=links.find(e=>/Sony 2 Long Loudspeakers|John/i.test(e.textContent||'') && e.textContent.length<400);
  return row ? {href:row.href, text:row.textContent.replace(/\n/g,' | ').slice(0,300)} : 'NOT FOUND';
})()""")
print("JOHN ROW:", r)
