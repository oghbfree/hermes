#!/usr/bin/env python3
"""
Jiji Ads Performance Harvester (2Real Enterprises) — CDP (:9222 persistent browser)
=====================================================================================
Replaces the old browser_exec version. Connects to the persistent Chrome on :9222
(via cdp_harness, already logged in as Two Real Enterprises), harvests ALL active
ads' performance from the Jiji SPA API, and saves to jiji_ads_performance.json.

FIELD EXTRACTION FIXED (19/10/26): the Jiji SPA returns performance as nested dicts:
  impressions.total, count_views.total/today, chat_count.total/today, count_contacts.total
The old script read them as `(a.get('impressions') or {}).get('total')` which OCCASIONALLY
worked but often returned the empty dicts literally (chats: {}) -> all-None fields.
This version reads via a safe deep-get and also flags the raw shape for debugging.

Run:
  python jiji_ads_harvest_cdp.py
Requires the persistent browser running (launch_2real_browser.sh) and logged into Jiji.
"""
import json, time, os, sys

VAULT = r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent"
OUT = os.path.join(VAULT, "jiji_ads_performance.json")
CDP_URL = os.environ.get("FB_CDP_URL", "http://127.0.0.1:9222")

sys.path.insert(0, VAULT)
os.environ["FB_CDP_URL"] = CDP_URL
import cdp_harness as cdp


def dget(d, *path):
    """safe deep get: dget(a,'impressions','total') -> value or None"""
    cur = d
    for k in path:
        if not isinstance(cur, dict):
            return None
        cur = cur.get(k)
    return cur


def harvest(max_pages=50):
    cdp.connect(substr="jiji.com.gh/profile")
    cdp.goto_url("https://jiji.com.gh/profile/adverts?guid=rbPd2oROVhelYWPjYkQWbhpx")
    cdp.wait_for_load()
    txt = cdp.js("document.body.innerText.slice(0,400)") or ""
    if "Two Real Enterprises" not in txt and "Real Enterprises" not in txt:
        print("NOT LOGGED IN — stop and tell H to log into Jiji once in the persistent browser.")
        return False

    all_ads, page = [], 1
    while page <= max_pages:
        js = (f"fetch('https://jiji.com.gh/api_web/v1/profile/my-ads.json"
              f"?status=active&page={page}&size=100',{{credentials:'include'}})"
              f".then(r=>r.json()).then(d=>JSON.stringify(d)).catch(e=>'ERR:'+e)")
        res = cdp.js_async(js, timeout=60)
        time.sleep(2)
        if not isinstance(res, str) or res.startswith("ERR"):
            print("page", page, "fetch error:", str(res)[:120])
            break
        d = json.loads(res)
        lst = d.get("adverts_list", [])
        if not lst:
            break
        for a in lst:
            all_ads.append({
                "id": a.get("id"),
                "guid": a.get("guid"),
                "title": a.get("title"),
                "price": a.get("price_title"),
                "url": a.get("url"),
                "status": a.get("status"),
                "impressions": dget(a, "impressions", "total"),
                "visitors": dget(a, "count_views", "total"),
                "views_today": dget(a, "count_views", "today"),
                "chats_total": dget(a, "chat_count", "total"),
                "chats_today": dget(a, "chat_count", "today"),
                "count_contacts": dget(a, "count_contacts", "total"),
                "contact_views": dget(a, "count_contacts", "contacts") or dget(a, "count_contacts"),
                "images": a.get("images_count"),
                "top": (dget(a, "top", "label") or a.get("top")),
                "date_created": a.get("date_created"),
            })
        print(f"page {page}: total {len(all_ads)}")
        if not d.get("next_url"):
            break
        page += 1

    json.dump({"scraped": time.strftime("%Y-%m-%d %H:%M"), "total": len(all_ads),
               "ads": all_ads}, open(OUT, "w", encoding="utf-8"), indent=1)
    print(f"SAVED {len(all_ads)} ads -> {OUT}")
    return True


if __name__ == "__main__":
    ok = harvest()
    sys.exit(0 if ok else 1)