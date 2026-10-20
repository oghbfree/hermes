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
time.sleep(9)
# Find smallest container whose text contains 'Loudspeakers' and get its clickable box
r = js(r"""(() => {
  const all=[...document.querySelectorAll('*')];
  const cands=all.filter(e=>{
    if(!e.offsetParent) return false;
    const t=e.textContent||'';
    if(!/Loudspeakers/.test(t)) return false;
    const r=e.getBoundingClientRect();
    return r.width>0&&r.height>0&&r.width<600&&r.height<200;
  });
  // pick the SMALLEST area one
  cands.sort((a,b)=>{const ra=a.getBoundingClientRect(),rb=b.getBoundingClientRect();return ra.width*ra.height-rb.width*rb.height;});
  if(!cands.length) return 'NONE';
  const c=cands[0]; const r=c.getBoundingClientRect();
  // walk up until we find a clickable ancestor (role=button/link or has onClick)
  let node=c; let depth=0;
  while(node && depth<8){
    const role=node.getAttribute&&node.getAttribute('role');
    const clk=(node.getAttribute&&node.getAttribute('data-nosnippet'));
    if(role==='link'||role==='button'||node.tagName==='A') break;
    node=node.parentElement; depth++;
  }
  if(node){const nr=node.getBoundingClientRect(); return JSON.stringify({x:nr.x+nr.width/2,y:nr.y+nr.height/2,rsz:[nr.width,nr.height],txt:c.textContent.replace(/\s+/g,' ').slice(0,80)});}
  return JSON.stringify({x:r.x+r.width/2,y:r.y+r.height/2,rsz:[r.width,r.height],txt:c.textContent.replace(/\s+/g,' ').slice(0,80)});
})()""")
print("TGT:", r)
try:
    tgt=json.loads(r)
    click(int(tgt['x']),int(tgt['y'])); time.sleep(6)
    print("URL:", js("location.href"))
    import re
    body=js("document.body.innerText")
    # extract the convo area - find lines mentioning Loudspeakers or a composer
    print("CONTAINS Loudspeakers:", 'Loudspeakers' in (body or ''))
    print("TAIL:", (body or '')[-900:])
except Exception as e:
    print("err", e)
