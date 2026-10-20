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

MSG = "Hi John! Yes — the Sony 2 Long Loudspeakers (6 Ohms, 90W) are still available at GHS 900. UK used, tested working. MoMo or cash only, no credit. Pickup in Oyarifa by appointment or delivery arranged within Accra. Call/WhatsApp 0204252252"

# confirm we are still in John/Sony thread before sending
ph = js("(document.querySelector('div[role=textbox]')||{}).getAttribute && document.querySelector('div[role=textbox]').getAttribute('aria-label')")
print("textbox placeholder:", ph)
assert ph and 'John' in ph and 'Loudspeaker' in ph, "WRONG THREAD - aborting"
print("CONFIRMED John/Sony thread")

# set text via native setter
r = js(r"""(() => {
  const tb=document.querySelector('div[role=textbox]');
  if(!tb) return 'NO_TB';
  const setter=Object.getOwnPropertyDescriptor(window.HTMLElement.prototype,'innerText').set || Object.getOwnPropertyDescriptor(window.HTMLElement.prototype,'textContent').set;
  // contenteditable: use execCommand for reliable insertion
  tb.focus();
  document.execCommand('insertText', false, %s);
  return 'inserted';
})()""" % json.dumps(MSG))
print("insert:", r)
time.sleep(2)
# verify text present
now = js("(document.querySelector('div[role=textbox]')||{innerText:''}).innerText")
print("textbox now:", (now or '')[:90])
# press Enter to send (FB sends on Enter), fallback click send button
send('Input.dispatchKeyEvent',type='keyDown',key='Enter',code='Enter',windowsVirtualKeyCode=13,nativeVirtualKeyCode=13)
send('Input.dispatchKeyEvent',type='keyUp',key='Enter',code='Enter',windowsVirtualKeyCode=13,nativeVirtualKeyCode=13)
time.sleep(4)
after = js("(document.querySelector('div[role=textbox]')||{innerText:'EMPTY'}).innerText")
print("textbox after send (should be EMPTY):", repr(after[:60]))
print("URL:", js("location.href"))
