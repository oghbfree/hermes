#!/usr/bin/env python3
"""Scrape ALL 2Real Jiji listings via Jiji's listing JSON API (865+ items).
Writes jiji_page_listings.json with titles + full advert metadata."""
import json, re, sys, time, urllib.request
from pathlib import Path

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
USER_ID = "rbPd2oROVhelYWPjYkQWbhpx"
API = f"https://jiji.com.gh/api_web/v1/listing?user_id={USER_ID}&webp=true&page=1"
OUT = Path(__file__).parent / "jiji_page_listings.json"
OUT_FULL = Path(__file__).parent / "jiji_listings_full.json"

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=45).read().decode("utf-8", errors="ignore"))

def items_from_payload(payload):
    al = payload.get("adverts_list") or {}
    count = al.get("count")
    adverts = al.get("adverts") or []
    titles = []
    meta_list = []
    for a in adverts:
        title = a.get("title") or (a.get("fb_view_content_data") or {}).get("content_name") or ""
        if title:
            titles.append(title)
        meta_list.append({
            "title": title,
            "price_obj": a.get("price_obj"),
            "price_title": a.get("price_title"),
            "category_name": a.get("category_name"),
            "region_name": a.get("region_name"),
            "guid": a.get("guid"),
            "url": a.get("url"),
            "status": a.get("status"),
            "details": a.get("details")[:300] if a.get("details") else "",
        })
    return titles, count, meta_list

def main():
    all_titles, all_meta = [], []
    seen = set()
    total = None
    url = API
    pages = 0
    for _ in range(200):
        try:
            payload = fetch(url)
        except Exception as e:
            print(f"error fetching {url}: {e}", file=sys.stderr)
            break
        titles, count, meta = items_from_payload(payload)
        if total is None: total = count
        new = 0
        for t, m in zip(titles, meta):
            key = t
            if key not in seen:
                seen.add(key); all_titles.append(t); all_meta.append(m); new += 1
        pages += 1
        nxt = payload.get("next_url")
        if isinstance(nxt, str) and nxt.startswith("http"):
            pass
        elif isinstance(nxt, dict):
            nxt = nxt.get("url") or nxt.get("next_url")
        else:
            nxt = None
        print(f"page {pages}: {len(titles)} titles ({new} new) total={total} next={'yes' if nxt else 'no'}", file=sys.stderr)
        if not nxt or not (isinstance(nxt, str) and nxt.startswith("http")) or new == 0:
            break
        url = nxt
        time.sleep(1)
    result = {"count": total, "scraped": len(all_titles), "titles": all_titles}
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    # full metadata in a separate file (maybe large)
    OUT_FULL.write_text(json.dumps({"count": total, "scraped": len(all_meta), "items": all_meta}, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"count": total, "pages": pages, "scraped": len(all_titles), "out": str(OUT)}, indent=2))

if __name__ == "__main__":
    main()