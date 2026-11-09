# Robust WA catalogue poster.
# KEY: the left rail (Tools icon) is inside a CSS transform, so getBoundingClientRect
# returns WRONG coords (x=-290) for it — locate it by elementFromPoint SCAN instead.
# All main-panel elements (Catalogue, Add new item, drawer fields) give correct
# rects. Use rect-centre trusted clicks for those.
# Post items by jiji_id from argv. Mark posted.json ONLY on real SAVED.
import json, sys, time, websocket, urllib.request, os, base64

CDP_HTTP = "http://127.0.0.1:9222"
PKG = r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package"

def list_tabs():
    with urllib.request.urlopen(CDP_HTTP + "/json", timeout=10) as r:
        return json.load(r)

TAB = [t for t in list_tabs() if t.get("type") == "page" and t.get("url", "").startswith("https://web.whatsapp.com")][0]
WS = websocket.create_connection(TAB["webSocketDebuggerUrl"].replace("localhost", "127.0.0.1"), timeout=120, suppress_origin=True)
_seq = [0]

def _send(method, **params):
    _seq[0] += 1
    WS.send(json.dumps({"id": _seq[0], "method": method, "params": params}))
    deadline = time.time() + 100
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
    out = dict(r); out.pop("id", None); return out

def trusted_click(x, y):
    cdp("Input.dispatchMouseEvent", type="mousePressed", x=int(x), y=int(y), button="left", clickCount=1)
    cdp("Input.dispatchMouseEvent", type="mouseReleased", x=int(x), y=int(y), button="left", clickCount=1)

def rect_center(txt, xr=(0, 1536), yr=(0, 700)):
    """Return (x,y) rect-centre of the first element whose exact text==txt,
    within viewport. Uses getBoundingClientRect (reliable for main-panel)."""
    expr = """(() => {
      const els=[...document.querySelectorAll('*')].filter(e=>(e.textContent||'').trim()===%s);
      for(const e of els){
        const r=e.getBoundingClientRect();
        if(r.width>0&&r.height>0&&r.x>=%d&&r.y>%d&&r.x<innerWidth&&r.y<innerHeight){
          return JSON.stringify({x:r.x+r.width/2,y:r.y+r.height/2});
        }
      }
      return null;
    })()""" % (json.dumps(txt), xr[0], yr[0])
    r = js(expr)
    if not r or r == "null": return None
    p = json.loads(r); return (p["x"], p["y"])

def find_pos_scan(aria, xr=(0, 100), yr=(0, 700), step=2):
    """elementFromPoint scan for the Tools rail (transformed -> rects wrong)."""
    expr = ("""(() => {
      for(let y=%d;y<=%d;y+=%d){ for(let x=%d;x<=%d;x+=%d){
        const el=document.elementFromPoint(x,y);
        if(el && el.getAttribute && el.getAttribute('aria-label')===%s){ return {x,y}; }
      }} return null; })()""" % (yr[0], yr[1], step, xr[0], xr[1], step, json.dumps(aria)))
    r = js(expr)
    if not r or r == "null": return None
    return (int(r["x"]), int(r["y"]))

def drawer_open():
    return js("(() => (document.body.innerText||'').includes('Add images'))()") is True

def fill_fields(title, desc_leaf, photo_path):
    b64 = base64.b64encode(open(photo_path, "rb").read()).decode()
    return js("""(async () => {
      const ed=[...document.querySelectorAll('div[contenteditable=true]')].filter(e=>e.offsetParent!==null);
      const name=ed.find(e=>(e.getAttribute('aria-label')||'')==='Name');
      if(!name) return 'noName';
      name.focus(); document.execCommand('insertText', false, %s);
      await new Promise(r=>setTimeout(r,400));
      const desc=ed.find(e=>(e.getAttribute('aria-label')||'')==='Description');
      if(desc){ desc.focus(); document.execCommand('insertText', false, %s); }
      await new Promise(r=>setTimeout(r,400));
      const inp=[...document.querySelectorAll('input[type=file]')].find(f=>f.accept&&f.accept.includes('image'));
      if(!inp) return 'nofile';
      const bin=atob('%s'); const bytes=new Uint8Array(bin.length);
      for(let i=0;i<bin.length;i++)bytes[i]=bin.charCodeAt(i);
      const dt=new DataTransfer(); dt.items.add(new File([bytes],'photo.jpg',{type:'image/jpeg'}));
      inp.files=dt.files; inp.dispatchEvent(new Event('change',{bubbles:true}));
      return 'ok';
    })()""" % (json.dumps(title), json.dumps(desc_leaf), b64))

def set_country(country="Ghana"):
    # scroll the drawer scroll container so 'Country of origin' is visible
    js("""(() => {
      const c=[...document.querySelectorAll('div')].find(e=>e.offsetParent!==null&&e.scrollHeight>e.clientHeight+100&&(e.textContent||'').includes('Country of origin')&&e.clientWidth>600);
      if(c){ // scroll only until label visible
        const lbl=[...document.querySelectorAll('div,span,label')].find(e=>e.offsetParent!==null&&(e.textContent||'').trim().startsWith('Country of origin'));
        if(lbl){ const r=lbl.getBoundingClientRect(); if(r.y>=innerHeight){ c.scrollTop+= (r.y-innerHeight+120); } }
      }
      return 'ok';
    })()""")
    time.sleep(1.2)
    p = rect_center("Country of origin (required)", (100, 1500), (100, 700))
    if not p:
        p = rect_center("Country of origin", (100, 1500), (100, 700))
    if not p: return "FAIL country open"
    trusted_click(*p); time.sleep(2.5)
    bt = js("(document.body.innerText||'')") or ""
    if "Åland Islands" not in bt:
        return "FAIL country list"
    gp = rect_center(country, (200, 1400), (150, 700))
    if not gp: return "FAIL country row"
    trusted_click(*gp); time.sleep(2)
    sp = rect_center("Save", (400, 1536), (400, 700))
    if sp: trusted_click(*sp)
    for _ in range(8):
        time.sleep(1.5)
        if "Åland Islands" not in (js("(document.body.innerText||'')") or ""):
            return "OK"
    return "FAIL country save"

def commit():
    expr = """(() => {
      const bs=[...document.querySelectorAll('div[role=button],button')].filter(e=>e.offsetParent!==null&&(e.textContent||'').trim()==='Add to catalogue');
      if(!bs.length) return null;
      const t=bs[bs.length-1];
      const rc=t.getBoundingClientRect();
      return JSON.stringify({x:rc.x+rc.width/2,y:rc.y+rc.height/2});
    })()"""
    r = js(expr)
    if not r or r == "null": return "FAIL commit btn"
    p = json.loads(r); trusted_click(p["x"], p["y"])
    for _ in range(10):
        time.sleep(2)
        bt = js("(document.body.innerText||'')") or ""
        if "Item saved" in bt: return "SAVED"
        if "Add images" not in bt: return "SAVED"
    return "FAIL commit"

def post_item(x):
    title = x["wa_title"]
    base = title.rsplit(" ", 1)[0]
    line = "Brand New, Sealed" if x.get("condition", "USED") == "NEW" else "UK Pre-Owned, Tested Working"
    desc = f"{base}. {line}. Delivery available across Accra. Call/WhatsApp 0204252252"
    photo = os.path.join(PKG, x["photo"])
    if not os.path.exists(photo): return "FAIL no photo"

    if drawer_open():
        js("""(() => {
          const b=[...document.querySelectorAll('button[aria-label]')].filter(e=>/close|back/i.test(e.getAttribute('aria-label')||''));
          if(b.length){ const e=b[0]; const ME=ev=>new MouseEvent(ev,{bubbles:true,cancelable:true,view:window}); ['mousedown','mouseup','click'].forEach(ev=>e.dispatchEvent(ME(ev))); }
          return 'closed';
        })()""")
        time.sleep(2)
    bt = js("(document.body.innerText||'')") or ""
    if "Add new item" not in bt:
        tp = find_pos_scan("Tools")
        if not tp: return "FAIL tools"
        trusted_click(*tp); time.sleep(3)
        cp = rect_center("Catalogue", (100, 1400), (100, 500))
        if cp:
            trusted_click(*cp); time.sleep(3)
        if "Add new item" not in (js("(document.body.innerText||'')") or ""):
            return "FAIL catalogue-open"
    ap = rect_center("Add new item", (50, 1100), (50, 500))
    if not ap: return "FAIL add card"
    trusted_click(*ap); time.sleep(4)
    if not drawer_open(): return "FAIL drawer"
    if fill_fields(title, desc, photo) != "ok": return "FAIL fields"
    time.sleep(3)
    cc = set_country("Ghana")
    if cc != "OK": return cc
    return commit()

def main():
    ids = sys.argv[1:]
    queue = {str(x["jiji_id"]): x for x in json.load(open(os.path.join(PKG, "wa_queue.json")))}
    postedp = os.path.join(PKG, "wa_catalog_posted.json")
    exp = os.path.join(PKG, "wa_catalog_existing.json")
    def load_list(p): return list(json.load(open(p))) if os.path.exists(p) else []
    report = []
    for sid in ids:
        if sid not in queue:
            report.append([sid, "SKIP not-in-queue"]); continue
        try:
            r = post_item(queue[sid])
        except Exception as e:
            r = "FAIL EXC:" + str(e)[:120]
        report.append([sid, r])
        if r == "SAVED":
            posted = load_list(postedp)
            if str(sid) not in [str(p) for p in posted]:
                posted.append(str(sid)); json.dump(sorted(posted), open(postedp, "w"))
            ex_l = load_list(exp)
            t = queue[sid]["wa_title"]
            if t not in ex_l:
                ex_l.append(t); json.dump(sorted(set(ex_l)), open(exp, "w"))
            print("SAVED", sid, flush=True)
        else:
            print("FAIL", sid, r, flush=True)
        time.sleep(2)
    print(json.dumps({"results": report}, indent=1, default=str))

main()