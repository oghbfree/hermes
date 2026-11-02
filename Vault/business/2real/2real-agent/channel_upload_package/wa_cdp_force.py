# One-off forced poster for verified-genuine items the fuzzy matcher false-positives on.
# Usage: python wa_cdp_force.py <jiji_id> [more jiji_ids...]
# Posts ONLY the given ids via wa_add_item (skips is_duplicate), records to posted.json only on SAVED.
import json, sys, time, websocket, os

CDP_HTTP = "http://127.0.0.1:9222"
def list_tabs():
    import urllib.request
    with urllib.request.urlopen(CDP_HTTP + "/json", timeout=10) as r:
        return json.load(r)
def attach_wa_tab():
    cands=[t for t in list_tabs() if t.get("type")=="page" and t.get("url","").startswith("https://web.whatsapp.com")]
    if not cands: raise SystemExit("[CRON_FAILURE] no web.whatsapp.com tab")
    for t in cands:
        if "WhatsApp" in t.get("title",""): return t
    return cands[0]

TAB=attach_wa_tab()
WS=websocket.create_connection(TAB["webSocketDebuggerUrl"].replace("localhost","127.0.0.1"),timeout=120,suppress_origin=True)
_seq=[0]
def _send(method,**params):
    _seq[0]+=1; WS.send(json.dumps({"id":_seq[0],"method":method,"params":params}))
    deadline=time.time()+110
    while time.time()<deadline:
        m=json.loads(WS.recv())
        if m.get("id")==_seq[0]: return m
    raise TimeoutError(method)
def js(expr):
    r=_send("Runtime.evaluate",expression=expr,returnByValue=True,awaitPromise=True,timeout=90000)
    res=r.get("result",{})
    if "exceptionDetails" in res: return "EXC:"+json.dumps(res["exceptionDetails"].get("exception",{}).get("description",""))[:200]
    return res.get("result",{}).get("value")
def cdp(method,**params): return _send(method,**params)
def page_text(): return js("(document.body.innerText||'')") or ""

if __name__=="__main__":
    ids=[a for a in sys.argv[1:]]
    head=page_text()[:300].replace("\n"," ")
    if "Log in" in head or "qr" in head.lower()[:120]:
        print("[CRON_FAILURE] WhatsApp login wall"); sys.exit(2)
    pkg=r'C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package'
    g={'js':js,'cdp':cdp}
    src=open(pkg+r'\wa_catalog_lib.py',encoding="utf-8").read()
    exec(compile(src,"wa_catalog_lib.py","exec"),g)
    wa_add_item=g['wa_add_item']
    q=json.load(open(pkg+r'\wa_queue.json'))
    postp=pkg+r'\wa_catalog_posted.json'
    expp=pkg+r'\wa_catalog_existing.json'
    post=set(json.load(open(postp)))
    results=[]
    for rid in ids:
        x=next((z for z in q if str(z['jiji_id'])==rid),None)
        if not x: results.append((rid,'not in queue')); continue
        photo=os.path.join(pkg,x['photo'])
        if not os.path.exists(photo): results.append((rid,'FAIL no photo')); continue
        cond=x.get('condition','USED')
        base=x['wa_title'].rsplit(' ',1)[0]
        line='Brand New, Sealed' if cond=='NEW' else 'UK Pre-Owned, Tested Working'
        desc=f"{base}. {line}. Delivery available across Accra. Call/WhatsApp 0204252252"
        r=wa_add_item(x['wa_title'],desc,photo)
        results.append((rid,r))
        if r=='SAVED':
            post.add(rid)
            json.dump(sorted(post),open(postp,'w'))
            ex=json.load(open(expp)) if os.path.exists(expp) else []
            ex.append(x['wa_title']); json.dump(sorted(set(ex)),open(expp,'w'))
        else:
            time.sleep(8)
    print(json.dumps({'results':results},indent=1,default=str))