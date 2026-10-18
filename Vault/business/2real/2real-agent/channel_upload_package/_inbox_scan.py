import json, time, urllib.request, websocket, sys
D='http://127.0.0.1:9222'
tabs=[t for t in json.load(urllib.request.urlopen(D+'/json')) if t['type']=='page' and 'facebook.com' in t['url']]
conn=websocket.create_connection(tabs[0]['webSocketDebuggerUrl'],timeout=60,suppress_origin=True)
mid=[0]
def send(m,**p):
    mid[0]+=1; i=mid[0]
    conn.send(json.dumps({'id':i,'method':m,'params':p}))
    while True:
        msg=json.loads(conn.recv())
        if msg.get('id')==i: return msg.get('result',{})
def js(e):
    r=send('Runtime.evaluate',expression=e,returnByValue=True,awaitPromise=False)
    if r.get('exceptionDetails'): return 'ERR: '+json.dumps(r['exceptionDetails'])[:300]
    return r.get('result',{}).get('value')

JS_ROWS = r"""(() => {
  const cand=[...document.querySelectorAll('div,span')].filter(e=>e.offsetParent&&e.childElementCount>0&&/^(Hellen|Chris|Awurabena|Nii|.+)$/.test(e.innerText.trim().split('\n')[0])&&e.innerText.length>60&&e.innerText.length<700&&e.querySelector('img,svg'));
  const seen=new Set(); const out=[];
  for(const e of cand){
    const key=e.innerText.slice(0,40);
    if(seen.has(key)) continue; seen.add(key);
    out.push({tag:e.tagName, role:e.getAttribute('role'), cls:(e.className||'').toString().slice(0,40), txt:e.innerText.slice(0,160).replace(/\n/g,' | ')});
    if(out.length>=10) break;
  }
  return out;
})()"""
print(json.dumps(js(JS_ROWS), indent=1)[:3000])
