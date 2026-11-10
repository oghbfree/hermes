# Diagnostic: inspect current WA tab state around the country dropdown.
import json, time, websocket, urllib.request

CDP = "http://127.0.0.1:9222"
tabs = json.load(urllib.request.urlopen(CDP + "/json", timeout=10))
cands = [t for t in tabs if t.get("type") == "page" and t.get("url", "").startswith("https://web.whatsapp.com")]
print("WA tabs:", len(cands))
for t in cands:
    print("  - title:", repr(t.get("title")), "url:", t["url"][:60])
tab = [t for t in cands if "WhatsApp" in t.get("title","")][0] if cands else cands[0]
WS = websocket.create_connection(tab["webSocketDebuggerUrl"].replace("localhost","127.0.0.1"), timeout=60, suppress_origin=True)
seq=[0]
def _send(method, **params):
    seq[0]+=1; WS.send(json.dumps({"id":seq[0],"method":method,"params":params}))
    while True:
        m=json.loads(WS.recv())
        if m.get("id")==seq[0]: return m
def js(expr):
    r=_send("Runtime.evaluate", expression=expr, returnByValue=True, awaitPromise=True, timeout=30000)
    if "exceptionDetails" in r.get("result",{}):
        return "EXC:"+json.dumps(r["result"]["exceptionDetails"].get("exception",{}))[:200]
    return r.get("result",{}).get("result",{}).get("value")

print("\n--- body snippets ---")
body = js("(document.body.innerText||'').slice(0,400)")
print(repr(body))
print("\nopen role=menu overlays:", js("[...document.querySelectorAll('[role=menu]')].filter(e=>e.offsetParent!==null).length"))
print("drawer 'Add images' present:", js("(document.body.innerText||'').includes('Add images')"))
print("country 'Country of origin' leaf present:", js("[...document.querySelectorAll('*')].filter(e=>e.offsetParent!==null&&(e.textContent||'').trim().startsWith('Country of origin')&&e.children.length===0).map(e=>{const r=e.getBoundingClientRect();return {t:(e.textContent||'').trim().slice(0,30),x:Math.round(r.x),y:Math.round(r.y),w:Math.round(r.width)}})"))
print("'Åland Islands' present:", js("(document.body.innerText||'').includes('Åland Islands')"))
# check contenteditable Name/Description
print("contenteditable labels:", js("[...document.querySelectorAll('div[contenteditable=true]')].filter(e=>e.offsetParent!==null).map(e=>(e.getAttribute('aria-label')||'?')).slice(0,6)"))
WS.close()