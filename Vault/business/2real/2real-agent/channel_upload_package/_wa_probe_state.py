import json, time, sys, urllib.request, websocket
CDP_HTTP = "http://127.0.0.1:9222"
def list_tabs():
    with urllib.request.urlopen(CDP_HTTP + "/json", timeout=10) as r:
        return json.load(r)
cands = [t for t in list_tabs() if t.get("type")=="page" and t.get("url","").startswith("https://web.whatsapp.com")]
for t in cands:
    if "WhatsApp" in t.get("title",""): TAB=t; break
else: TAB=cands[0]
print("TAB:",TAB["title"][:50])
WS=websocket.create_connection(TAB["webSocketDebuggerUrl"].replace("localhost","127.0.0.1"),timeout=60,suppress_origin=True)
_seq=[0]
def _send(m,**p):
    _seq[0]+=1; WS.send(json.dumps({"id":_seq[0],"method":m,"params":p}))
    while True:
        msg=json.loads(WS.recv())
        if msg.get("id")==_seq[0]: return msg
def js(expr):
    r=_send("Runtime.evaluate",expression=expr,returnByValue=True,awaitPromise=True)
    res=r.get("result",{})
    if "exceptionDetails" in res: return "EXC:"+str(res["exceptionDetails"].get("exception",{}).get("description",""))[:200]
    return res.get("result",{}).get("value")
# probe for open drawer (Add images), open menu overlays, and current body snippet
print("has_add_images:", js("(document.body.innerText||'').includes('Add images')"))
print("menu_overlay_count:", js("[...document.querySelectorAll('[role=menu]')].filter(e=>e.offsetParent!==null).length"))
print("drawer_fields:", js("document.querySelectorAll('div[contenteditable=true][aria-label]').length"))
print("toast:", repr((js("(document.body.innerText||'')") or '').split(chr(10))[-6:]))
head=(js("(document.body.innerText||'')") or "").replace(chr(10),' | ')
print("tail:", head[-400:])