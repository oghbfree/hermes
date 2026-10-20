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
body=js("document.body.innerText")
# find the John/Sony convo - show the portion mentioning Sony or our reply text
idx = body.find('Sony 2 Long')
print("REPLY TEXT in body:", 'at GHS 900' in body or 'the Sony 2 Long' in body)
import re
# print a chunk around 'Loudspeakers'
for m in re.finditer('Loudspeaker', body):
    s=max(0,m.start()-60); print("...", body[s:m.start()+220].replace('\n',' | '))
    break
# print last 800 chars
print("=====BODY TAIL=====")
print(body[-900:])
