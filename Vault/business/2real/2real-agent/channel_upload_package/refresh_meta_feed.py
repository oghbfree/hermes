#!/usr/bin/env python3
"""refresh_meta_feed.py — refresh meta_feed_full.csv from the LIVE Jiji account scrape.

Pulls every ACTIVE listing from jiji_listings_full.json that is resolvable to a numeric
jiji_id (via jiji_guid_map.json) and NOT already in the feed or catalogue, fetches its
main advert image URL from the live listing page, and appends a fresh feed row so the
FB/WA feeder pool grows (207 -> ~1,000+ ids). Jiji = inventory source of truth.

Paced (WAF-aware, 1.3s between HTML fetches). Resumable: skips already-appended ids.
Backs up meta_feed_full.csv once at start.
"""
import json, os, csv, re, sys, time, shutil, datetime, urllib.request

AGENT = r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent"
PKG = os.path.join(AGENT, "channel_upload_package")
FEED = os.path.join(PKG, "meta_feed_full.csv")
GUIDMAP = os.path.join(PKG, "jiji_guid_map.json")
JIJI = os.path.join(AGENT, "jiji_listings_full.json")
LOG = os.path.join(PKG, "meta_feed_refresh_progress.json")

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"


def slug_of(url):
    m = re.search(r"([A-Za-z0-9]{15,})\.html", url or "")
    return m.group(1) if m else None


def read_feed():
    out = {}
    if not os.path.exists(FEED):
        return out
    with open(FEED, encoding="utf-8") as f:
        r = csv.reader(f)
        next(r, None)
        for row in r:
            if row and row[0].isdigit():
                out[int(row[0])] = row
    return out


def find_main_img(html):
    """Return the primary advert photo (first pictures-ghana .jpg) from a listing page."""
    cands = re.findall(r"https://pictures-ghana\.jijistatic\.net/([A-Za-z0-9_\-]+\.jpg)", html)
    return ("https://pictures-ghana.jijistatic.net/" + cands[0]) if cands else None


def fetch_img(nid, url):
    page = "https://jiji.com.gh" + url.split("?")[0]
    try:
        req = urllib.request.Request(page, headers={"User-Agent": UA})
        html = urllib.request.urlopen(req, timeout=40).read().decode("utf-8", errors="ignore")
        return find_main_img(html)
    except Exception as e:
        return None


def main():
    LIMIT = int(sys.argv[1]) if len(sys.argv) > 1 else 400  # max listings to add this run

    # back up feed once
    if not os.path.exists(FEED + ".refresh_bak"):
        shutil.copy(FEED, FEED + ".refresh_bak")
        print("backup:", FEED + ".refresh_bak")

    guidmap = json.load(open(GUIDMAP, encoding="utf-8"))
    guid2id = {v["guid"]: k for k, v in guidmap.items() if v.get("guid")}

    act = [i for i in json.load(open(JIJI, encoding="utf-8")).get("items", [])
           if str(i.get("status", "")).lower() == "active"]

    # existing feed ids
    feed = read_feed()
    # catalogue/posted/queue known ids (already handled, don't re-add)
    known = set()
    for f in ("wa_catalog_posted.json", "wa_queue.json"):
        fp = os.path.join(PKG, f)
        if os.path.exists(fp):
            d = json.load(open(fp, encoding="utf-8"))
            if isinstance(d, list):
                for x in d:
                    if isinstance(x, (int, str)) and str(x).isdigit():
                        known.add(int(x))
                    elif isinstance(x, dict) and x.get("jiji_id"):
                        known.add(int(x["jiji_id"]))

    # candidates: active, resolvable id, not in feed, not known-posted/queued
    cands = []
    for it in act:
        g = it.get("guid")
        nid = guid2id.get(g)
        if not nid:
            continue
        nid = int(nid)
        if nid in feed or nid in known:
            continue
        price = (it.get("price_obj") or {}).get("value") or 0
        cands.append((nid, it.get("title", ""), price, it.get("url", "")))
    print(f"CANDIDATES to add: {len(cands)}")

    progress = {}
    if os.path.exists(LOG):
        try:
            progress = json.load(open(LOG, encoding="utf-8"))
        except Exception:
            progress = {}

    added = 0
    for nid, title, price, url in cands:
        if added >= LIMIT:
            print("reached limit", LIMIT)
            break
        if nid in progress and progress[nid].get("img"):
            continue  # already resolved earlier run
        img = fetch_img(nid, url)
        progress[nid] = {"img": img, "title": title, "price": price, "url": url}
        if img:
            added += 1
        else:
            pass  # keep in progress so we retry next run
        if added % 25 == 0:
            print(f"  ...resolved {added} (nid {nid})")
            json.dump(progress, open(LOG, "w", encoding="utf-8"), indent=1)
        time.sleep(1.3)

    json.dump(progress, open(LOG, "w", encoding="utf-8"), indent=1)
    print(f"RESOLVED images for {added} new listings this run. Appending to feed...")

    # append resolvable rows to feed
    f = open(FEED, "a", encoding="utf-8", newline="")
    w = csv.writer(f)
    appended = 0
    for nid, meta in progress.items():
        if not meta.get("img"):
            continue
        if int(nid) in feed:
            continue
        title = meta["title"]
        price = meta.get("price") or 0
        link = "https://jiji.com.gh" + (meta["url"].split("?")[0] if meta["url"].startswith("/") else meta["url"])
        desc = f"{title}\nBrand new in stock.\nPrice: GHS {price}\n\nMoMo or cash only - no credit.\nPickup by appointment in Oyarifa or we arrange delivery (Yango/Bolt).\nCall/WhatsApp: 0204252252"
        w.writerow([nid, title, desc, "in stock", "new", f"{price}.00 GHS", link, meta["img"], ""])
        feed[int(nid)] = None
        appended += 1
    f.close()
    print(f"APPENDED {appended} rows -> meta_feed_full.csv")


if __name__ == "__main__":
    main()