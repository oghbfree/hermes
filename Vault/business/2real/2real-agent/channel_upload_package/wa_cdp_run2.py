# CDP-direct driver v2: reloads web.whatsapp.com before EACH item (after a save WA
# lands on the item detail view and the Catalogue leaf is no longer findable).
# Usage: python wa_cdp_run.py <count>
import json, os, sys, time
import wa_cdp_run as h

PKG = r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package"
src = open(os.path.join(PKG, "wa_catalog_lib.py"), encoding="utf-8").read()
# the lib's functions resolve js/cdp in THIS module's globals — provide them BEFORE exec
js = h.js
cdp = h.cdp
exec(compile(src, "wa_catalog_lib.py", "exec"), globals())

def reload_wa():
    h.js("location.reload()")
    time.sleep(12)
    for _ in range(6):
        t = h.page_text()
        if t and len(t) > 500 and "Loading" not in t[:60]:
            break
        time.sleep(4)
    return h.page_text()[:120].replace("\n", " ")

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
    r = wa_add_item(x["wa_title"], desc, photo)
    if r == "SAVED":
        posted.add(jid)
        json.dump(sorted(posted), open(os.path.join(PKG, "wa_catalog_posted.json"), "w"))
        ex = os.path.join(PKG, "wa_catalog_existing.json")
        base = json.load(open(ex)) if os.path.exists(ex) else []
        base.append(x["wa_title"])
        json.dump(sorted(set(base)), open(ex, "w"))
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
        head = reload_wa()
        r = post_one_item(x, posted)
        print(x["jiji_id"], "->", r, flush=True)
        if r == "SAVED":
            done += 1
        elif r != "SKIP duplicate" and not str(r).startswith("SKIP"):
            # one retry after a fresh reload
            head = reload_wa()
            r2 = post_one_item(x, posted)
            print(x["jiji_id"], "retry ->", r2, flush=True)
            if r2 == "SAVED":
                done += 1
        results.append([x["jiji_id"], r])
    print("DONE", done, json.dumps(results))
