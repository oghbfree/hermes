"""Minimal CDP harness exposing js/goto_url/wait_for_load/click_at_xy for fb_post_lib.

Reconnects to the given tab WS URL on demand; survives across execute_code calls
because the module is re-imported fresh each call (config via env vars).
"""
import os, json, time, urllib.request
from websocket import create_connection

DEBUG_URL = os.environ.get("FB_CDP_URL", "http://127.0.0.1:9222")  # live dedicated browser port (see launch_2real_browser.sh)

def list_tabs():
    data = json.loads(urllib.request.urlopen(DEBUG_URL + "/json", timeout=5).read())
    return [t for t in data if t.get("type") == "page"]

def _ws_for_url_filter(substr, exclude_substr=None):
    tabs = list_tabs()
    cands = [t for t in tabs if substr in t["url"] and (exclude_substr is None or exclude_substr not in t["url"])]
    if not cands:
        raise RuntimeError("no tab matching %r" % substr)
    return cands[0]["webSocketDebuggerUrl"]

_conn = None
_ws = None

def connect(substr="/marketplace/create/item", exclude_substr=None):
    global _conn, _ws
    for sub in (substr, "facebook.com/marketplace", "facebook.com"):
        try:
            _ws = _ws_for_url_filter(sub, exclude_substr)
            break
        except RuntimeError:
            continue
    else:
        req = urllib.request.Request(DEBUG_URL + "/json/new?url=https://www.facebook.com/marketplace/create/item", method="PUT")
        data = json.loads(urllib.request.urlopen(req, timeout=10).read())
        time.sleep(2)
        _ws = data["webSocketDebuggerUrl"]
    if _conn:
        try: _conn.close()
        except Exception: pass
    _conn = create_connection(_ws, timeout=120, suppress_origin=True)
    return _conn

def _send(method, **params):
    global _conn
    if _conn is None:
        connect()
    mid = _conn.send(json.dumps({"id": 1, "method": method, "params": params}))
    while True:
        msg = json.loads(_conn.recv())
        if msg.get("id") == 1:
            if "error" in msg:
                raise RuntimeError(msg["error"])
            return msg.get("result", {})

def js(expr):
    r = _send("Runtime.evaluate", expression=expr, returnByValue=True, awaitPromise=False, timeout=60000)
    if r.get("exceptionDetails"):
        return None
    return r.get("result", {}).get("value")

def js_async(expr, timeout=60):
    r = _send("Runtime.evaluate", expression=expr, returnByValue=True, awaitPromise=True, timeout=timeout * 1000)
    if r.get("exceptionDetails"):
        return None
    return r.get("result", {}).get("value")

def goto_url(url):
    _send("Page.navigate", url=url)
    time.sleep(5)

def wait_for_load(timeout=30):
    t0 = time.time()
    while time.time() - t0 < timeout:
        s = js("document.readyState")
        if s == "complete":
            return True
        time.sleep(1)
    return False

def click_at_xy(x, y):
    """Real trusted click via CDP input domain."""
    try:
        _send("Input.dispatchMouseEvent", type="mouseMoved", x=x, y=y)
        _send("Input.dispatchMouseEvent", type="mousePressed", x=x, y=y, button="left", clickCount=1)
        _send("Input.dispatchMouseEvent", type="mouseReleased", x=x, y=y, button="left", clickCount=1)
        return True
    except Exception as e:
        print("click_at_xy err:", e)
        return False
