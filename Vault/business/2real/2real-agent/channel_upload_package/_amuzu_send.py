import os, json, time, sys, websocket, urllib.request
sys.path.insert(0, r'C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package')
os.environ['FB_CDP_URL'] = 'http://127.0.0.1:9222'
import cdp_harness as C

# get inbox tab ws
data = json.loads(urllib.request.urlopen('http://127.0.0.1:9222/json', timeout=5).read())
inbox = [t for t in data if 'inbox' in t.get('url','')]
if not inbox:
    print('NO_INBOX_TAB'); sys.exit(1)
ws = websocket.create_connection(inbox[0]['webSocketDebuggerUrl'], timeout=60, suppress_origin=True)

def ev(expr, awaitp=True):
    ws.send(json.dumps({"id": 1, "method": "Runtime.evaluate",
                        "params": {"expression": expr, "returnByValue": True,
                                   "awaitPromise": awaitp, "timeout": 40000}}))
    while True:
        m = json.loads(ws.recv())
        if m.get('id') == 1:
            if 'error' in m:
                return 'ERR:' + str(m['error'])
            if m.get('result', {}).get('exceptionDetails'):
                return 'EXC'
            return m.get('result', {}).get('result', {}).get('value')

# what's in composer now
c = ev("(() => { var eds=[...document.querySelectorAll('[contenteditable=true]')].filter(e=>e.offsetParent!==null); if(!eds.length) return 'NO_ED'; return eds[0].innerText; })()")
print('COMPOSER:', repr(c)[:100])
# if text present, click send; else type again
if c and 'GHS 500' not in c:
    reply = "The Bosch Drill Jigsaw PST 50a is GHS 500. Yes I'm on WhatsApp - message me there on 0204252252. I've also got other drills and tools available. MoMo or cash, no credit. Pickup Oyarifa by appointment or we arrange delivery."
    r = ev("(async () => { var ed=[...document.querySelectorAll('[contenteditable=true]')].filter(e=>e.offsetParent!==null)[0]; if(!ed) return 'NO_ED'; ed.focus(); document.execCommand('insertText', false, %s); await new Promise(r=>setTimeout(r,500)); return ed.innerText.slice(0,30); })()" % json.dumps(reply))
    print('RETYPED:', r)
    time.sleep(1)
# click send button
s = ev("""(() => {
  var btns=[...document.querySelectorAll('[role=button]')].filter(e=>e.offsetParent!==null);
  var snd=btns.find(e=>/^send$/i.test((e.getAttribute('aria-label')||'').trim()));
  if(!snd) return 'NO_SEND';
  snd.focus(); snd.click(); return 'SENT';
})()""")
print('SEND:', s)
time.sleep(3)
# verify
v = ev("(() => { var eds=[...document.querySelectorAll('[contenteditable=true]')].filter(e=>e.offsetParent!==null); var t=document.body.innerText; return JSON.stringify({composer:(eds.length?eds[0].innerText.trim():'NO_ED'), seen:t.includes('GHS 500. Yes I')}); })()")
print('VERIFY:', v)