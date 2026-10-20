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
ax=send('Accessibility.getFullAXTree')
nodes=ax.get('nodes',[])
print("total AX nodes:", len(nodes))
# find nodes whose name mentions Loudspeakers or John
for n in nodes:
    name=n.get('name',{}) or {}
    name_txt = name.get('value','') if isinstance(name,dict) else ''
    if 'Loudspeaker' in name_txt or ('John' in name_txt and len(name_txt)<120):
        print("ROLE:", n.get('role',{}).get('value'), "| NAME:", name_txt[:90], "| nid:", n.get('nodeId'), "| backend:", n.get('backendDOMNodeId'))
