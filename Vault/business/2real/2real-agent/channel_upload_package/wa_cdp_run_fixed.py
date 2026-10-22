# Fixed CDP driver: opens Tools -> Catalogue via TRUSTED coordinate clicks
# (synthetic JS MouseEvent dispatch fails after a page reload -> whole-queue FAIL).
# Reuses wa_catalog_lib.py proven fill/country/commit helpers.
import json, os, sys, time
import wa_cdp_run as h

js, cdp, page_text = h.js, h.cdp, h.page_text

PKG = r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package"
src = open(os.path.join(PKG, "wa_catalog_lib.py"), encoding="utf-8").read()
exec(compile(src, "wa_catalog_lib.py", "exec"), globals())

def trusted_click(x, y):
    cdp("Input.dispatchMouseEvent", type="mousePressed", x=int(x), y=int(y), button="left", clickCount=1)
    cdp("Input.dispatchMouseEvent", type="mouseReleased", x=int(x), y=int(y), button="left", clickCount=1)

def find_rect(js_filter, fallback=None):
    """js_filter: JS snippet evaluating to an element ref of which we want center rect.
    Returns (x,y) center or None."""
    r = js("""(() => {
      const el = %s;
      if(!el) return null;
      const rc = el.getBoundingClientRect();
      return JSON.stringify({x:rc.x+rc.width/2, y:rc.y+rc.height/2});
    })()""" % js_filter)
    if not r or r == "null":
        return None
    p = json.loads(r)
    return (p["x"], p["y"])

# --- trusted openers ---
def open_tools_trusted():
    """Trusted-click the left-rail Tools (storefront) icon."""
    xy = find_rect("""[...document.querySelectorAll('[aria-label=Tools],[title=Tools]')].filter(e=>e.offsetParent!==null)[0]""")
    if not xy:
        return "FAIL tools-node"
    trusted_click(*xy)
    time.sleep(2.5)
    return "ok"

def open_catalogue_trusted():
    """Trusted-click the visible 'Catalogue' leaf (exact text, inside Tools panel)."""
    xy = find_rect("""[...document.querySelectorAll('*')].filter(e=>e.offsetParent!==null&&(e.textContent||'').trim()==='Catalogue'&&e.children.length===0)[0]""")
    if not xy:
        return "noCat"
    trusted_click(*xy)
    time.sleep(3)
    return "ok"

CARD_CENTERED = """(() => {
  const c=[...document.querySelectorAll('*')].filter(e=>e.offsetParent!==null&&(e.textContent||'').trim()==='Add new item'&&e.children.length===0)[0];
  if(!c) return 'gone';
  const t=c.parentElement.parentElement;
  t.scrollIntoView({block:'center'});
  const rc=t.getBoundingClientRect();
  let y=rc.y+rc.height/2;
  if(y<40){ window.scrollBy(0,y-80); }
  const rc2=t.getBoundingClientRect();
  return JSON.stringify({x:rc2.x+rc2.width/2,y:Math.max(rc2.y+rc2.height/2,40)});
})()"""

def open_catalogue_panel():
    """Ensure we are on the Catalogue panel. Returns 'ok' / 'FAIL <reason>'."""
    # If already showing Add new item, we're on it.
    if js("(() => (document.body.innerText||'').includes('Add new item'))()") is True:
        return "ok"
    if open_tools_trusted() != "ok":
        return "FAIL tools"
    time.sleep(2)
    if open_catalogue_trusted() != "ok":
        return "FAIL catalogue"
    if js("(() => (document.body.innerText||'').includes('Add new item'))()") is not True:
        return "FAIL catalogue-open"
    return "ok"

def wa_add_item_fixed(title, desc, photo_path, country="Ghana"):
    if open_catalogue_panel() != "ok":
        return "FAIL catalogue"
    r = js(CARD_CENTERED)
    if r == "gone":
        return "FAIL add card"
    p = json.loads(r); trusted_click(p["x"], p["y"])
    time.sleep(4)
    if not wa_drawer_open():
        return "FAIL drawer"
    if wa_fill_fields(title, desc, photo_path) != "ok":
        return "FAIL fields"
    if wa_set_country(country) != "OK":
        return wa_set_country(country)
    return wa_commit()

def reload_wa():
    js("location.reload()")
    time.sleep(12)
    for _ in range(8):
        t = page_text()
        if t and len(t) > 400 and "Loading" not in t[:60] and "logging" not in t.lower()[:60]:
            return t[:100].replace("\n", " ")
        time.sleep(4)
    return page_text()[:100].replace("\n", " ")

def post_one_item(x, posted):
    jid = x["jiji_id"]
    photo = os.path.join(PKG, x["photo"])
    if not os.path.exists(photo):
        return "FAIL no photo"
    if is_duplicate(x["wa_title"]):
        posted.add(jid)
        json.dump(sorted(posted), open(os.path.join(PKG, "wa_catalog_posted.json"), "w"))
        return "SKIP duplicate"
    base = x["wa_title"].rsplit(" ", 1)[0]
    line = "Brand New, Sealed" if x.get("condition", "USED") == "NEW" else "UK Pre-Owned, Tested Working"
    desc = f"{base}. {line}. Delivery available across Accra. Call/WhatsApp 0204252252"
    r = wa_add_item_fixed(x["wa_title"], desc, photo)
    if r == "SAVED":
        posted.add(jid)
        json.dump(sorted(posted), open(os.path.join(PKG, "wa_catalog_posted.json"), "w"))
        ex = os.path.join(PKG, "wa_catalog_existing.json")
        base_list = json.load(open(ex)) if os.path.exists(ex) else []
        base_list.append(x["wa_title"])
        json.dump(sorted(set(base_list)), open(ex, "w"))
    return r

if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    queue = json.load(open(os.path.join(PKG, "wa_queue.json")))
    pp = os.path.join(PKG, "wa_catalog_posted.json")
    posted = set(json.load(open(pp)))
    results, done = [], 0
    for x in queue:
        if done >= count:
            break
        if x["jiji_id"] in posted:
            continue
        try:
            r = post_one_item(x, posted)
        except Exception as e:
            r = "FAIL EXC:" + str(e)[:80]
        print(x["jiji_id"], "->", r, flush=True)
        if r == "SAVED":
            done += 1
        elif r == "SKIP duplicate":
            continue
        # any other FAIL: retry once (reload to clear state), then move on
        elif str(r).startswith("FAIL"):
            print("  retrying once...", flush=True)
            try:
                head = reload_wa()
                r2 = post_one_item(x, posted)
            except Exception as e:
                r2 = "FAIL EXC:" + str(e)[:80]
            print(x["jiji_id"], "-> retry:", r2, flush=True)
            if r2 == "SAVED":
                done += 1
            else:
                results.append((str(x["jiji_id"]), f"FAIL:{r2}"))
        else:
            results.append((str(x["jiji_id"]), r))
    print(json.dumps({"attempted_done": done, "hard_fails": results}, default=str))