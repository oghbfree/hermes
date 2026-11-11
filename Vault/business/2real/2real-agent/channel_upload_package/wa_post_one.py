# One-off direct poster for a single item, bypassing the fuzzy is_duplicate check
# (which false-positives on same-brand titles sharing words, e.g. two Roscomar shoes).
# Usage: python wa_post_one.py <jiji_id>
import json, sys, time, os, websocket

CDP_HTTP = "http://127.0.0.1:9222"
pkg = r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package"

def list_tabs():
    import urllib.request
    with urllib.request.urlopen(CDP_HTTP + "/json", timeout=10) as r:
        return json.load(r)

def attach_wa_tab():
    cands = [t for t in list_tabs()
             if t.get("type") == "page" and t.get("url", "").startswith("https://web.whatsapp.com")]
    if not cands:
        raise SystemExit("[CRON_FAILURE] no web.whatsapp.com tab found")
    for t in cands:
        if "WhatsApp" in t.get("title", ""):
            return t
    return cands[0]

TAB = attach_wa_tab()
WS = websocket.create_connection(TAB["webSocketDebuggerUrl"].replace("localhost", "127.0.0.1"),
                                 timeout=120, suppress_origin=True)
_seq = [0]
def _send(method, **params):
    _seq[0] += 1
    WS.send(json.dumps({"id": _seq[0], "method": method, "params": params}))
    deadline = time.time() + 110
    while time.time() < deadline:
        msg = json.loads(WS.recv())
        if msg.get("id") == _seq[0]:
            return msg
    raise TimeoutError(method)
def js(expr):
    r = _send("Runtime.evaluate", expression=expr, returnByValue=True, awaitPromise=True, timeout=90000)
    res = r.get("result", {})
    if "exceptionDetails" in res:
        return "EXC:" + json.dumps(res["exceptionDetails"].get("exception", {}).get("description", ""))[:200]
    return res.get("result", {}).get("value")
def cdp(method, **params):
    r = _send(method, **params)
    out = dict(r); out.pop("id", None)
    return out

print("TAB:", TAB["title"][:60])
src = open(os.path.join(pkg, "wa_catalog_lib.py"), encoding="utf-8").read()
exec(compile(src, "wa_catalog_lib.py", "exec"), globals())

target = sys.argv[1]
queue = json.load(open(os.path.join(pkg, "wa_queue.json")))
item = next(x for x in queue if str(x["jiji_id"]) == target)
title = item["wa_title"]
photo = os.path.join(pkg, item["photo"])
cond = item.get("condition", "USED")
base = title.rsplit(" ", 1)[0]
line = "Brand New, Sealed" if cond == "NEW" else "UK Pre-Owned, Tested Working"
desc = f"{base}. {line}. Delivery available across Accra. Call/WhatsApp 0204252252"

r = wa_add_item(title, desc, photo)
print("RESULT:", r, "| item:", title, "| cond:", cond)
if r == "SAVED":
    postedp = os.path.join(pkg, "wa_catalog_posted.json")
    posted = set(json.load(open(postedp)))
    posted.add(target)
    json.dump(sorted(posted), open(postedp, "w"))
    exp = os.path.join(pkg, "wa_catalog_existing.json")
    ex = set(json.load(open(exp))) if os.path.exists(exp) else set()
    ex.add(title)
    json.dump(sorted(ex), open(exp, "w"))
    print("STATE_UPDATED: posted.json + existing.json include", target)
else:
    print("STATE_UNCHANGED: not saved, posted.json not modified for", target)