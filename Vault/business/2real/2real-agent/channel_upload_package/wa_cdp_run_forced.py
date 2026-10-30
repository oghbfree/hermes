# Forced CDP poster: posts SPECIFIC remaining jiji_ids from wa_queue.json via the
# proven wa_add_item flow, marking posted.json ONLY on a real SAVED result.
# Bypasses the fuzzy dedupe (which false-positives on same-brand similar items).
# Usage: python wa_cdp_run_forced.py <jiji_id> [<jiji_id> ...]
import json, sys, time, websocket, urllib.request, os

CDP_HTTP = "http://127.0.0.1:9222"
pkg = r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package"

def list_tabs():
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

src = open(pkg + r"\\wa_catalog_lib.py", encoding="utf-8").read()
glb = dict(globals())
exec(compile(src, "wa_catalog_lib.py", "exec"), glb)
wa_add_item = glb["wa_add_item"]

queue = {str(x["jiji_id"]): x for x in json.load(open(pkg + r"\wa_queue.json"))}
postedp = pkg + r"\wa_catalog_posted.json"
ex = pkg + r"\wa_catalog_existing.json"

def load_list(p):
    return list(json.load(open(p))) if os.path.exists(p) else []

ids = sys.argv[1:]
report = []
for sid in ids:
    if sid not in queue:
        report.append([sid, "SKIP not-in-queue"]); continue
    x = queue[sid]
    photo = os.path.join(pkg, x["photo"])
    if not os.path.exists(photo):
        report.append([sid, "FAIL no photo"]); continue
    cond = x.get("condition", "USED")
    base = x["wa_title"].rsplit(" ", 1)[0]
    if cond == "NEW":
        line = "Brand New, Sealed"
    else:
        line = "UK Pre-Owned, Tested Working"
    desc = f"{base}. {line}. Delivery available across Accra. Call/WhatsApp 0204252252"
    r = wa_add_item(x["wa_title"], desc, photo)
    report.append([sid, r])
    if r == "SAVED":
        posted = load_list(postedp)
        if sid not in [str(p) for p in posted]:
            posted.append(str(sid)); json.dump(sorted(posted), open(postedp, "w"))
        ex_l = load_list(ex)
        if x["wa_title"] not in ex_l:
            ex_l.append(x["wa_title"]); json.dump(sorted(set(ex_l)), open(ex, "w"))
    time.sleep(2)

print(json.dumps({"results": report}, indent=1, default=str))
