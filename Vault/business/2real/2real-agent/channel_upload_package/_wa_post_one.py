# Post a single given jiji_id via wa_catalog_lib functions, bypassing the buggy fuzzy matcher.
# Usage: python3 _wa_post_one.py <jiji_id>
import json, sys, time, urllib.request, websocket
CDP_HTTP = "http://127.0.0.1:9222"
def list_tabs():
    with urllib.request.urlopen(CDP_HTTP + "/json", timeout=10) as r:
        return json.load(r)
cands = [t for t in list_tabs() if t.get("type")=="page" and t.get("url","").startswith("https://web.whatsapp.com")]
for t in cands:
    if "WhatsApp" in t.get("title",""): TAB=t; break
else: TAB=cands[0]
print("TAB:", TAB["title"][:50])
WS=websocket.create_connection(TAB["webSocketDebuggerUrl"].replace("localhost","127.0.0.1"),timeout=180,suppress_origin=True)
_seq=[0]
def _send(m,**p):
    _seq[0]+=1; WS.send(json.dumps({"id":_seq[0],"method":m,"params":p}))
    while True:
        msg=json.loads(WS.recv())
        if msg.get("id")==_seq[0]: return msg
def js(expr):
    r=_send("Runtime.evaluate",expression=expr,returnByValue=True,awaitPromise=True,timeout=120000)
    res=r.get("result",{})
    if "exceptionDetails" in res: return "EXC:"+str(res["exceptionDetails"].get("exception",{}).get("description",""))[:200]
    return res.get("result",{}).get("value")
def cdp(m,**p):
    return _send(m,**p)

# load lib
src=open(r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package\wa_catalog_lib.py",encoding="utf-8").read()
exec(compile(src,"wa_catalog_lib.py","exec"),globals())

jid=sys.argv[1]
q=json.load(open(r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package\wa_queue.json"))
x=next(i for i in q if str(i['jiji_id'])==jid)
import os
pkg=r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package"
photo=os.path.join(pkg,x['photo'])
cond=x.get('condition','USED')
line='Brand New, Sealed' if cond=='NEW' else 'UK Pre-Owned, Tested Working'
base=x['wa_title'].rsplit(' ',1)[0]
desc=f"{base}. {line}. Delivery available across Accra. Call/WhatsApp 0204252252"
print("posting", jid, "|", x['wa_title'])
print("desc:", desc)
time.sleep(2)
r=wa_add_item(x['wa_title'], desc, photo)
print("RESULT:", r)
if r=='SAVED':
    postedp=pkg+r"\wa_catalog_posted.json"
    posted=set(json.load(open(postedp)))
    posted.add(jid)
    json.dump(sorted(posted), open(postedp,'w'))
    ex=pkg+r"\wa_catalog_existing.json"
    base2=json.load(open(ex))
    base2.append(x['wa_title'])
    json.dump(sorted(set(base2)), open(ex,'w'))
    print("COMMITTED to posted.json + existing.json")