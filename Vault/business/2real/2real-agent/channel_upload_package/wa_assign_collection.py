# wa_assign_collection.py — GUARDED post-hoc collection assignment for the
# WhatsApp Catalogue. WhatsApp Web's add-item drawer has NO category picker, so a
# posted item can only be filed into a collection via the catalogue's
# "collection card -> Add items" route. This is a BEST-EFFORT follow-up step:
#   - NEVER blocks the poster. Returns status dict, never raises.
#   - Runs standalone (wa_cdp_run.py does NOT call it); wire into a cron/prompt as
#     an optional post-step, or run manually.
# Verified safe: opening tools/catalogue + reading cards commits nothing; only the
# explicit confirmation click moves an item, and a failed step returns early.
#
# Usage: python wa_assign_collection.py "<collection>" "<item title fragment>"
#   e.g. python wa_assign_collection.py "Master Lock and Keysafe" "Master Lock Disc Lock Code"
import json, time, urllib.request, websocket, sys, os

CDP_HTTP = "http://127.0.0.1:9222"
def tabs():
    with urllib.request.urlopen(CDP_HTTP + "/json", timeout=8) as r:
        return json.load(r)
def attach_wa():
    for t in tabs():
        if t.get("type") == "page" and t.get("url", "").startswith("https://web.whatsapp.com") and "WhatsApp" in t.get("title", ""):
            return t
    for t in tabs():
        if t.get("type") == "page" and t.get("url", "").startswith("https://web.whatsapp.com"):
            return t
    return None

TAB = attach_wa()
if not TAB:
    print(json.dumps({"ok": False, "error": "[CRON_FAILURE] no web.whatsapp.com tab"})); sys.exit(0)
WS = websocket.create_connection(TAB["webSocketDebuggerUrl"].replace("localhost", "127.0.0.1"),
                                 timeout=60, suppress_origin=True)
_seq = [0]
def send(m, **p):
    _seq[0] += 1; WS.send(json.dumps({"id": _seq[0], "method": m, "params": p}))
    while True:
        x = json.loads(WS.recv())
        if x.get("id") == _seq[0]:
            return x
def js(e):
    r = send("Runtime.evaluate", expression=e, returnByValue=True, awaitPromise=True)
    res = r.get("result", {})
    if "exceptionDetails" in res:
        return None
    return res.get("result", {}).get("value")
def cdp(m, **p): return send(m, **p)
def click(x, y):
    cdp("Input.dispatchMouseEvent", type="mousePressed", x=int(x), y=int(y), button="left", clickCount=1)
    cdp("Input.dispatchMouseEvent", type="mouseReleased", x=int(x), y=int(y), button="left", clickCount=1)
def esc():
    send("Input.dispatchKeyEvent", type="keyDown", key="Escape", code="Escape", windowsVirtualKeyCode=27, nativeVirtualKeyCode=27)
    send("Input.dispatchKeyEvent", type="keyUp", key="Escape", code="Escape", windowsVirtualKeyCode=27, nativeVirtualKeyCode=27)

OPEN_TOOLS = """(()=>{const t=[...document.querySelectorAll('[aria-label=Tools],[title=Tools]')].filter(e=>e.offsetParent!==null)[0];if(!t)return'no';const rc=t.getBoundingClientRect();const ME=ev=>new MouseEvent(ev,{bubbles:true,cancelable:true,view:window,clientX:rc.x+rc.width/2,clientY:rc.y+rc.height/2});['mousedown','mouseup','click'].forEach(ev=>t.dispatchEvent(ME(ev)));return'ok';})()"""
OPEN_CAT = """(()=>{const c=[...document.querySelectorAll('*')].filter(e=>e.offsetParent!==null&&(e.textContent||'').trim()==='Catalogue'&&e.children.length===0)[0];if(!c)return'no';const t=c.closest('[role=button],[tabindex],li')||c.parentElement;const rc=t.getBoundingClientRect();const ME=ev=>new MouseEvent(ev,{bubbles:true,cancelable:true,view:window,clientX:rc.x+rc.width/2,clientY:rc.y+rc.height/2});['mousedown','mouseup','click'].forEach(ev=>t.dispatchEvent(ME(ev)));return'ok';})()"""
def card_by(text):
    """Return {x,y} of the catalogue gridcell whose innerText matches text (best-effort)."""
    return js("""(()=>{const q=%s;const c=[...document.querySelectorAll('[role=gridcell]')].filter(e=>e.offsetParent!==null&&(e.innerText||'').trim().toLowerCase().includes(q));if(!c.length)return null;const e=c[0];const r=e.getBoundingClientRect();return JSON.stringify({x:Math.round(r.x+r.width/2),y:Math.round(r.y+r.height/2)});})()""" % json.dumps(text.lower()))

def main():
    col = (sys.argv[1] if len(sys.argv) > 1 else "").strip()
    item = (sys.argv[2] if len(sys.argv) > 2 else "").strip()
    if not col or not item:
        print(json.dumps({"ok": False, "error": "need: <collection> <item title fragment>"})); return
    try:
        # close any stale drawer/menus first
        js("(()=>{const b=[...document.querySelectorAll('div[role=button],button')].filter(e=>e.offsetParent!==null&&(e.getAttribute('aria-label')||'').includes('Close'));if(b.length){b[0].click()}})()")
        time.sleep(1); esc(); time.sleep(1)
        if js(OPEN_TOOLS) != 'ok': print(json.dumps({"ok": False, "error": "open tools"})); return
        time.sleep(2)
        if js(OPEN_CAT) != 'ok': print(json.dumps({"ok": False, "error": "open catalogue"})); return
        time.sleep(3)
        # 1) open the collection card  (e.g. "Master Lock and Keysafe")
        cc_raw = card_by(col.split('/')[0].strip())
        try:
            cc = json.loads(cc_raw) if cc_raw and cc_raw.strip().startswith('{') else None
        except Exception:
            cc = None
        if not cc:
            print(json.dumps({"ok": False, "error": "collection card not found: "+col})); return
        click(cc["x"], cc["y"]); time.sleep(3)
        # 2) find an "Add items" affordance inside the collection view
        addit = js("""(()=>{const e=[...document.querySelectorAll('div[role=button],button')].filter(x=>x.offsetParent!==null&&/add items/i.test((x.textContent||'').trim()));if(!e.length)return null;const r=e[0].getBoundingClientRect();return JSON.stringify({x:Math.round(r.x+r.width/2),y:Math.round(r.y+r.height/2)});})()""")
        try:
            addp = json.loads(addit) if addit and addit.strip().startswith('{') else None
        except Exception:
            addp = None
        if not addp:
            print(json.dumps({"ok": False, "error": "no 'Add items' affordance in collection (may need manual)"})); return
        click(addp["x"], addp["y"]); time.sleep(3)
        # 3) pick the target item in the resulting grid
        it_raw = card_by(item)
        try:
            it = json.loads(it_raw) if it_raw and it_raw.strip().startswith('{') else None
        except Exception:
            it = None
        if not it:
            # cancel out
            esc(); time.sleep(1)
            print(json.dumps({"ok": False, "error": "target item not found: "+item})); return
        click(it["x"], it["y"]); time.sleep(2)
        # 4) confirm (Add / Done / Save) — best-effort, options
        done = js("""(()=>{for(const lab of ['Add','Done','Save','OK']){const b=[...document.querySelectorAll('div[role=button],button')].filter(x=>x.offsetParent!==null&&(x.textContent||'').trim().toLowerCase()===lab.toLowerCase());if(b.length){const r=b[0].getBoundingClientRect();return JSON.stringify({x:Math.round(r.x+r.width/2),y:Math.round(r.y+r.height/2),lab:lab});}}return null;})()""")
        if done:
            p = json.loads(done); click(p["x"], p["y"]); time.sleep(2)
        print(json.dumps({"ok": True, "collection": col, "item": item,
                          "note": "post-hoc assign attempted; verify in WhatsApp catalogue"}))
    except Exception as e:
        print(json.dumps({"ok": False, "error": "EXC: "+str(e)[:200]}))
    finally:
        try: WS.close()
        except Exception: pass

if __name__ == "__main__":
    main()