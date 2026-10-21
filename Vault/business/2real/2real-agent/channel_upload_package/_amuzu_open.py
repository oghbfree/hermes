import os, json, time, websocket
import sys
sys.path.insert(0, r'C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package')
os.environ['FB_CDP_URL']='http://127.0.0.1:9222'
import cdp_harness as C
tabs=C.list_tabs()
inbox=[t for t in tabs if 'inbox' in t['url']][0]
ws=websocket.create_connection(inbox['webSocketDebuggerUrl'],timeout=60,suppress_origin=True)
def ev(expr,awaitp=True):
    ws.send(json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":expr,"returnByValue":True,"awaitPromise":awaitp,"timeout":40000}}))
    while True:
        m=json.loads(ws.recv())
        if m.get('id')==1:
            if 'error' in m: return 'ERR:'+str(m['error'])
            if m.get('result',{}).get('exceptionDetails'): return 'EXC'
            return m.get('result',{}).get('result',{}).get('value')

# click on Amuzu thread row
r=ev("""(() => {
  const el=[...document.querySelectorAll('[role=button]')].filter(e=>e.offsetParent!==null&&/Amuzu\\s+Bosch Drill Jigsaw PST 50a/.test(e.textContent||'')&&(e.textContent||'').length<300).sort((a,b)=>a.getBoundingClientRect().width-b.getBoundingClientRect().width)[0];
  if(!el) return 'no';
  const rc=el.getBoundingClientRect();
  return JSON.stringify({x:rc.x+rc.width/2,y:rc.y+rc.height/2});
})()""")
print('amuzu target:', r)
if r and r!='no':
    p=json.loads(r)
    C.click_at_xy(int(p['x']),int(p['y']))
    time.sleep(4)
    txt=ev("(() => { const ed=[...document.querySelectorAll('[contenteditable=true]')].filter(e=>e.offsetParent!==null)[0]; if(!ed) return JSON.stringify({open:false}); return JSON.stringify({open:true,body:document.body.innerText.slice(-1400)}); })()")
    print('opened:', txt[:400])