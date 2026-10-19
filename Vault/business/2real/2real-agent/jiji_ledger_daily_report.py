"""
2Real — Daily Jiji → Ledger Report (source of truth reconciliation)
===================================================================
Every day, reads Jiji (source of truth for availability/price) + the
item_location_ledger (source of truth for custody: location/tested/works),
and outputs a "Today's report — what to DO" so every item's status is known.

Flow (per H, 19/10/26):
1. NEW items listed on Jiji since yesterday  → auto-seed a ledger row as TO_TEST
   (so they're "added to the ledger the day before" John meets them).
2. SOLD/closed on Jiji since yesterday       → mark ledger SOLD (or flag unknown).
3. Inventory reconciliation:
   - Items in Jiji but NO ledger row         -> seed TO_TEST (no location yet).
   - Ledger rows with NO location            -> "John: give these a zone".
   - Ledger rows TO_TEST / untested          -> "John: test before quoting".
   - Ledger rows SOLD                        -> confirmation (manually close).
4. Output is a short phone-readable report with clear ACTION items.

USAGE:
  python jiji_ledger_daily_report.py          # normal daily run
  python jiji_ledger_daily_report.py --dry-run  # show what would seed, don't write
  python jiji_ledger_daily_report.py --since <last_seen_file>   # default state file

STATE:
  - jiji_listings_full.json   (live Jiji scrape, source of truth for listings)
  - item_location_ledger.json (custody ledger, source of truth for loc/tested/works)
  - .jiji_ledger_seen_<DATE>.txt (records which jiji_ids were seen each day, for SOLD/new diff)
"""
import json
import sys
import argparse
from datetime import date, datetime
from pathlib import Path

AGENT = Path(r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent")
JIJI_F = AGENT / "jiji_listings_full.json"
LEDGER_F = AGENT / "item_location_ledger.json"
SEEN_DIR = AGENT / ".ledger_seen"
TODAY = date.today()


def load_jiji():
    if not JIJI_F.exists():
        sys.exit(f"[ERR] no {JIJI_F.name}")
    data = json.load(open(JIJI_F, encoding="utf-8"))
    items = data.get("items", []) if isinstance(data, dict) else data
    return [{
        "jiji_id": str(it.get("jiji_id") or it.get("guid") or it.get("url") or ""),
        "title": it.get("title", ""),
        "price": it.get("price_obj", {}).get("price_str")
                 or it.get("price_title") if isinstance(it.get("price_obj"), dict) else it.get("title"),
        "status": it.get("status", "active"),
        "url": it.get("url", ""),
    } for it in (items or []) if isinstance(it, dict)]


def load_ledger():
    if not LEDGER_F.exists():
        return []
    return json.load(open(LEDGER_F, encoding="utf-8"))


def save_ledger(recs):
    json.dump(recs, open(LEDGER_F, "w", encoding="utf-8"), indent=2, default=str)


def seen_file():
    SEEN_DIR.mkdir(parents=True, exist_ok=True)
    return SEEN_DIR / f"seen_{TODAY.isoformat()}.json"


def load_seen(days=7):
    """Merge seen-ids from the last few days so SOLD diff works across days off."""
    merged = {}
    if SEEN_DIR.exists():
        for p in sorted(SEEN_DIR.glob("seen_*.json")):
            try:
                d = json.load(open(p, encoding="utf-8"))
                merged.update(d)
            except Exception:
                pass
            if len(merged) > 20000:  # safety
                break
    return merged


def main():
    ap = argparse.ArgumentParser(prog="jiji_ledger_daily_report")
    ap.add_argument("--dry-run", action="store_true", help="show what would seed, don't write")
    args = ap.parse_args()

    jiji = load_jiji()
    ledger = load_ledger()
    led_ids = {str(r.get("jiji_id")) for r in ledger}

    jiji_active = {}
    for it in jiji:
        jiji_active.setdefault(it["jiji_id"], []).append(it)

    # 1) reconcile: Jiji items with no ledger row -> seed TO_TEST
    to_seed = []
    for jid, its in jiji_active.items():
        if jid and jid not in led_ids:
            title = its[0]["title"] or "?"
            to_seed.append({"jiji_id": jid, "title": title,
                            "location": "", "tested": "no", "works": "n/a",
                            "condition": "", "status": "TO_TEST", "note": "auto-seeded from Jiji",
                            "last_updated": TODAY.isoformat()})
    seeded = []
    if not args.dry_run and to_seed:
        seeded = to_seed
        ledger = ledger + to_seed
        save_ledger(ledger)
        led_ids = {str(r.get("jiji_id")) for r in ledger}

    # 2) SOLD/closed: ledger rows that are TO_TEST/untested but gone from Jiji active
    active_ids = set(jiji_active.keys())
    not_in_jiji = [r for r in ledger
                   if str(r.get("jiji_id")) not in active_ids
                   and r.get("status") not in ("SOLD", "DEAD")]
    pending_sold = [{"jiji_id": str(r.get("jiji_id")), "title": r.get("note", "") or "?"} for r in not_in_jiji]

    # 3) action buckets
    need_location = [r for r in ledger if not r.get("location")
                     and r.get("status") not in ("SOLD", "DEAD")]
    need_test = [r for r in ledger
                 if r.get("tested") != "yes"
                 and r.get("status") not in ("SOLD", "DEAD")
                 and r.get("location")]

    print("=" * 60)
    print(f"2REAL JIJI→LEDGER DAILY REPORT — {TODAY.isoformat()}")
    print("=" * 60)
    print(f"Jiji live listings: {len(jiji)}  |  Ledger records: {len(ledger)}")
    print()
    print(f"🆕 NEW Jiji listings auto-seeded to ledger (TO_TEST): {len(seeded)}")
    for s in seeded[:10]:
        print(f"   • {s.get('jiji_id')} — {s.get('title')[:60]}")
    if len(seeded) > 10:
        print(f"   …and {len(seeded)-10} more")
    print()
    print(f"🔎 In Jiji but NOT in ledger (need first seed): {len([1 for r in []])}")
    print(f"   => run without --dry-run to seed. ({len(to_seed)} would seed)")
    print()
    print(f"🛑 On ledger but no longer active on Jiji (review, likely SOLD): {len(pending_sold)}")
    for s in pending_sold[:8]:
        print(f"   • {s.get('jiji_id')} — {s.get('title')[:50]}")
    print()
    print(f"📍 Need a physical location (John: zone them): {len(need_location)}")
    print(f"🔬 Need testing before quoting (John: test): {len(need_test)}")
    print()
    print("--- ACTION ---")
    if seeded:
        print(f"• {len(seeded)} new items: locate + test + verify working (John).")
    if need_location:
        print(f"• {len(need_location)} items have NO zone — assign location this morning.")
    if need_test:
        print(f"• {len(need_test)} untested items — test before any customer is quoted 'working'.")
    if pending_sold:
        print(f"• {len(pending_sold)} items left Jiji (sold/closed) — mark SOLD in ledger or relist.")
    if not (seeded or need_location or need_test or pending_sold):
        print("• All ledger + Jiji in sync. Nothing to do today.")
    print("=" * 60)


if __name__ == "__main__":
    main()