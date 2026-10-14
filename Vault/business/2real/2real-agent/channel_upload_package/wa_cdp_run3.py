# v3: same as v2 but the Add-new-item card is ALWAYS scrolled to panel center before
# the trusted click (v2 left it at y~10 under the header -> drawer never opened).
import json, os, sys, time
import wa_cdp_run as h

js, cdp = h.js, h.cdp
PKG = r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package"
src = open(os.path.join(PKG, "wa_catalog_lib.py"), encoding="utf-8").read()
exec(compile(src, "wa_catalog_lib.py", "exec"), globals())

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

def wa_add_item2(title, desc, photo_path, country="Ghana"):
    if js(WA_OPEN_TOOLS) != "ok": return "FAIL tools"
    time.sleep(3)
    if js(WA_OPEN_CATALOGUE) == "noCat": return "FAIL catalogue"
    time.sleep(3)
    r = js(CARD_CENTERED)
    if r == "gone": return "FAIL add card"
    p = json.loads(r); wa_trusted_click(p["x"], p["y"])
    time.sleep(4)
    if not wa_drawer_open(): return "FAIL drawer"
    if wa_fill_fields(title, desc, photo_path) != "ok": return "FAIL fields"
    if wa_set_country(country) != "OK": return wa_set_country(country)
    return wa_commit()

def reload_wa():
    h.js("location.reload()")
    time.sleep(12)
    for _ in range(6):
        t = h.page_text()
        if t and len(t) > 500 and "Loading" not in t[:60]:
            break
        time.sleep(4)

def post_one_item(x, posted):
    jid = x["jiji_id"]
    photo = os.path.join(PKG, x["photo"])
    if not os.path.exists(photo):
        return "FAIL no photo"
    if is_duplicate(x["wa_title"]):
        posted.add(jid)
        json.dump(sorted(posted), open(os.path.join(PKG, "wa_catalog_posted.json"), "w"))
        return "SKIP duplicate"
    desc = DESC_TMPL.format(title=x["wa_title"].rsplit(" ", 1)[0]).replace("\n", " ")
    r = wa_add_item2(x["wa_title"], desc, photo)
    if r == "SAVED":
        posted.add(jid)
        json.dump(sorted(posted), open(os.path.join(PKG, "wa_catalog_posted.json"), "w"))
        ex = os.path.join(PKG, "wa_catalog_existing.json")
        base = json.load(open(ex)) if os.path.exists(ex) else []
        base.append(x["wa_title"])
        json.dump(sorted(set(base)), open(ex, "w"))
    return r

if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    queue = json.load(open(os.path.join(PKG, "wa_queue.json")))
    pp = os.path.join(PKG, "wa_catalog_posted.json")
    posted = set(json.load(open(pp)))
    done, results = 0, []
    for x in queue:
        if done >= count:
            break
        if x["jiji_id"] in posted:
            continue
        reload_wa()
        r = post_one_item(x, posted)
        print(x["jiji_id"], "->", r, flush=True)
        if r == "SAVED":
            done += 1
        elif not r.startswith("SKIP"):
            reload_wa()
            r2 = post_one_item(x, posted)
            print(x["jiji_id"], "retry ->", r2, flush=True)
            if r2 == "SAVED":
                done += 1
        results.append([x["jiji_id"], r])
    print("DONE", done, json.dumps(results))
