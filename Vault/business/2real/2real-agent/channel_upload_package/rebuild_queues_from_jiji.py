#!/usr/bin/env python3
"""Rebuild the FB/WA upload queues from FRESH Jiji data (source of truth).

WHY: The Weekly Jiji Catalog Refresh (cron 063e05279b98) keeps jiji_listings_full.json
current, but the FB/WA queues (next50.json / wa_queue.json) were built from the STALE
meta_feed_full.csv (Sep 29) — so FB/WA were posting outdated prices (e.g. TP-Link Tapo
C200 was 870 in the feed but 650 on live Jiji). This script regenerates the batch from
the live Jiji export (active listings, current prices) and cross-references the feed
ONLY for image URLs, then promotes to the FB/WA queues.

Run after a fresh Jiji scrape (weekly cron does this). Safe to re-run (idempotent).
"""
import json, csv, re, os, sys, shutil

AGENT = r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent"
PKG = os.path.join(AGENT, "channel_upload_package")
JIJI = os.path.join(AGENT, "jiji_listings_full.json")
FEED = os.path.join(PKG, "meta_feed_full.csv")
BATCH = os.path.join(PKG, "next50_batch2.json")

def slug_of(url):
    m = re.search(r"([A-Za-z0-9]{15,})\.html", url or "")
    return m.group(1) if m else None

def load_jiji():
    with open(JIJI, encoding="utf-8") as f:
        raw = json.load(f)
    return raw.get("items", raw if isinstance(raw, list) else [])

def load_feed():
    """{slug: (numeric_id, title, image_url)} from the feed."""
    out = {}
    if not os.path.exists(FEED):
        return out
    with open(FEED, encoding="utf-8") as f:
        r = csv.reader(f)
        next(r, None)
        for row in r:
            if len(row) >= 8:
                s = slug_of(row[6])
                if s:
                    try:
                        out[s] = (int(float(row[0])), row[1], row[7])
                    except (ValueError, TypeError):
                        continue
    return out

def main():
    items = load_jiji()
    feed = load_feed()
    jiji_by_slug = {}
    for i in items:
        s = slug_of(i.get("url", ""))
        if s:
            jiji_by_slug[s] = i

    batch = []
    for s, ji in jiji_by_slug.items():
        if str(ji.get("status", "")).lower() != "active":
            continue
        title = ji.get("title", "")
        if not title:
            continue
        price = (ji.get("price_obj") or {}).get("value")
        if price is None:
            pt = ji.get("price_title") or ""
            m = re.search(r"([\d,]+\.?\d*)", pt.replace("GH₵", "").replace("GHS", ""))
            price = int(float(m.group(1).replace(",", ""))) if m else 0
        # numeric id + image MUST come from the feed (photos/{id}.jpg)
        if s not in feed:
            continue
        fid, f_title, img = feed[s]
        if not img:
            continue
        batch.append({
            "jiji_id": fid,               # real numeric id -> matches photos/{id}.jpg
            "title": title,               # fresh Jiji title
            "price": int(price),          # FRESH Jiji price (source of truth)
            "image": img,
            "url": "https://jiji.com.gh" + (ji.get("url", "") if str(ji.get("url", "")).startswith("/") else ji.get("url", "")),
            "score": 50.0,
        })

    batch.sort(key=lambda x: -x.get("price", 0))
    print(f"REBUILT: {len(batch)} active items from fresh Jiji (matched to feed images)")

    # Ensure local photos exist for every queued item (FB/WA post photos/{id}.jpg)
    import urllib.request
    imgdir = os.path.join(PKG, "photos")
    os.makedirs(imgdir, exist_ok=True)
    dl_ok = dl_fail = have = 0
    for x in batch:
        p = os.path.join(imgdir, "%d.jpg" % x["jiji_id"])
        if os.path.exists(p):
            have += 1
            continue
        try:
            req = urllib.request.Request(x["image"], headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as r, open(p, "wb") as f:
                f.write(r.read())
            dl_ok += 1
        except Exception as e:
            dl_fail += 1
    print(f"PHOTOS: {have} present, {dl_ok} downloaded, {dl_fail} failed")

    if os.path.exists(BATCH):
        shutil.copy(BATCH, BATCH + ".prejiji")
    json.dump(batch, open(BATCH, "w", encoding="utf-8"), indent=1)
    print(f"WROTE: {BATCH} ({len(batch)} items)")
    print("NEXT: run promote_batch2.py to push to FB (next50.json) + WA (wa_queue.json)")

if __name__ == "__main__":
    main()