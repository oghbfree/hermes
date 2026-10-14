# CDP-direct driver for wa_catalog_lib.py (browser harness unavailable; port 9222 alive).
# Usage: python wa_cdp_run.py <count>  — runs wa_post_next(count) on the WhatsApp Business tab.
import json, sys, time, websocket

CDP_HTTP = "http://127.0.0.1:9222"

def list_tabs():
    import urllib.request
    with urllib.request.urlopen(CDP_HTTP + "/json", timeout=10) as r:
        return json.load(r)

def attach_wa_tab():
    cands = [t for t in list_tabs()
             if t.get("type") == "page" and t.get("url", "").startswith("https://web.whatsapp.com")]
    if not cands:
        raise SystemExit("[CRON_FAILURE] no web.whatsapp.com tab found")
    # prefer a tab that looks logged in (title contains 'WhatsApp')
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
    out = dict(r)
    out.pop("id", None)
    return out

def page_text():
    return js("(document.body.innerText||'')") or ""

if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    # sanity: logged in? QR wall check
    head = page_text()[:300].replace("\n", " ")
    print("TAB:", TAB["title"][:60])
    if "Loading" in head and "WhatsApp" in head:
        print("WA still loading, waiting 20s...")
        time.sleep(20); head = page_text()[:300].replace("\n", " ")
    if "Log in" in head or "qr" in head.lower()[:120]:
        print("[CRON_FAILURE] WhatsApp login wall:", head)
        sys.exit(2)
    print("page head:", head[:150])
    src = open(r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package\wa_catalog_lib.py", encoding="utf-8").read()
    exec(compile(src, "wa_catalog_lib.py", "exec"), globals())
    assert "wa_post_next" in globals(), "lib not loaded"
    report = wa_post_next(count)
    print(json.dumps(report, indent=1, default=str))
