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
# Find the thread row item: a clickable element whose text is 'John ... Loudspeakers' within the main inbox list
r = js(r"""(() => {
  const main=document.querySelector('[role=main]');
  const nodes=[...main.querySelectorAll('a,div[role=link],[aria-label]')].filter(e=>e.offsetParent);
  // find one whose direct text starts with John and mentions Loudspeakers but is NOT the huge container
  const row=nodes.find(e=>{
    const r=e.getBoundingClientRect();
    if(r.width>700||r.height>250) return false;
    const t=e.textContent||'';
    return t.includes('John') && t.includes('Loudspeakers') && e.closest('[role=main]');
  });
  if(!row) return 'NONE';
  const r2=row.getBoundingClientRect();
  return JSON.stringify({x:Math.round(r2.x+r2.width/2),y:Math.round(r2.y+r2.height/2),w:Math.round(r2.width),h:Math.round(r2.height),txt:row.textContent.replace(/\s+/g,' ').slice(0,70)});
})()""")
print("ROW:", r)
try:
    t=(json.loads(r)); click(t['x'],t['y']); time.sleep(6)
    print("URL:", js("location.href"))
except Exception as e:
    print("err",e)
body=js("document.body.innerText")
# Find a composer present?
print("HAS textarea:", js("!!document.querySelector('div[role=textbox]')"))
print("TAIL:", (body or '')[-700:])
