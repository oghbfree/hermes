#!/usr/bin/env python3
"""
gap_pipeline.py — the full "what do I own but haven't listed" chain, in order.

Built 16/11/26. Fixes the real problem: the Sunday Christmas Gap Re-scan was reading a
gap list that nothing ever regenerated, computed from a Zobaze snapshot nothing refreshed.

H's ruling (16/11/26): the June Zobaze snapshot is ACCEPTABLE as a permanent working base,
because it is dominated by slow-moving stock. So this script does NOT block on staleness —
it reports the snapshot date for transparency and carries on.

Order matters:
  1. gdrive_sync.py            Zobaze export (Drive) -> inventory_agent.json
  2. jiji_ads_harvest_cdp.py   live Jiji ads (API)   -> jiji_ads_performance.json
  3. christmas_gap_analysis.py inventory vs Jiji catalogue -> christmas_gap_list.json
  4. christmas_rescan.py       gap list vs LIVE jiji + alias map -> marks listed, writes
                               CHRISTMAS_PRIORITY_LIST.md and the review file

Why this order: step 3 rebuilds the gap list from scratch (wiping `listed` flags), and
step 4 re-derives them from live Jiji using the persistent alias map — so the alias
knowledge survives every rebuild.

Fail-safe: a failed step does not abort the chain. Each step reports ok/fail and the final
summary states plainly what is stale, so the cron reports truthfully instead of silently
presenting old numbers as new.

Run:  python gap_pipeline.py
"""
import json
import os
import subprocess
import sys
import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable

INVENTORY = os.path.join(HERE, "inventory_agent.json")
LIVE = os.path.join(HERE, "jiji_ads_performance.json")
CATALOGUE = os.path.join(HERE, "jiji_listings_full.json")
GAP = os.path.join(HERE, "christmas_gap_list.json")
ALIASES = os.path.join(HERE, "jiji_title_aliases.json")


def age_days(path):
    if not os.path.isfile(path):
        return None
    return round((datetime.datetime.now() - datetime.datetime.fromtimestamp(os.path.getmtime(path))).total_seconds() / 86400, 1)


def run(script, timeout=600):
    p = os.path.join(HERE, script)
    if not os.path.isfile(p):
        return {"step": script, "ok": False, "reason": "script missing"}
    try:
        r = subprocess.run([PY, p], cwd=HERE, capture_output=True, text=True, timeout=timeout)
        tail = (r.stdout or "").strip().splitlines()
        err = (r.stderr or "").strip().splitlines()
        return {
            "step": script,
            "ok": r.returncode == 0,
            "exit": r.returncode,
            "last_line": (tail[-1][:200] if tail else ""),
            "error": (err[-1][:200] if err and r.returncode != 0 else ""),
        }
    except subprocess.TimeoutExpired:
        return {"step": script, "ok": False, "reason": f"timeout after {timeout}s"}
    except Exception as e:
        return {"step": script, "ok": False, "reason": f"{type(e).__name__}: {e}"}


def main():
    steps = []

    # 1 — Zobaze export from Drive (harmless if already synced)
    steps.append(run("gdrive_sync.py", timeout=300))

    # 2 — live Jiji ads (needs the persistent browser alive; watchdog keeps it up)
    steps.append(run("jiji_ads_harvest_cdp.py", timeout=900))

    # 3 — rebuild the gap: Zobaze inventory vs Jiji catalogue
    steps.append(run("christmas_gap_analysis.py", timeout=600))

    # 4 — cross-check against live Jiji, mark what is already posted
    steps.append(run("christmas_rescan.py", timeout=900))

    inv_age = age_days(INVENTORY)
    cat_age = age_days(CATALOGUE)
    live_age = age_days(LIVE)

    gap_items, known, unknown, pot = [], 0, 0, 0.0
    snap = None
    if os.path.isfile(GAP):
        try:
            d = json.load(open(GAP, encoding="utf-8"))
            gap_items = [i for i in d.get("items", []) if not i.get("listed")]
            snap = d.get("generated")
            for i in gap_items:
                if float(i.get("cost") or 0) > 0:
                    known += 1
                    pot += float(i.get("margin") or 0) * float(i.get("stock") or 0)
                else:
                    unknown += 1
        except Exception:
            pass

    # snapshot date recorded by the Drive sync log, so the report can name it
    zobaze_snapshot = "unknown"
    sl = os.path.join(HERE, "sync_log.json")
    if os.path.isfile(sl):
        try:
            log = json.load(open(sl, encoding="utf-8"))
            last = log[-1] if isinstance(log, list) and log else log
            zobaze_snapshot = f"{last.get('file_name')} (file dated {str(last.get('file_modified'))[:10]})"
        except Exception:
            pass

    failed = [s for s in steps if not s["ok"]]
    summary = {
        "generated": datetime.datetime.now().isoformat(timespec="seconds"),
        "steps": steps,
        "failed_steps": [s["step"] for s in failed],
        "zobaze_snapshot": zobaze_snapshot,
        "file_ages_days": {"inventory_agent(zobaze)": inv_age,
                           "jiji_listings_full(catalogue)": cat_age,
                           "jiji_ads_performance(live)": live_age},
        "gap_total_unlisted": len(gap_items),
        "gap_with_known_cost": known,
        "gap_cost_missing": unknown,
        "verifiable_profit_unlisted": round(pot),
        "gap_list_written": snap,
        "alias_map_entries": (len(json.load(open(ALIASES, encoding="utf-8")).get("map", {}))
                              if os.path.isfile(ALIASES) else 0),
    }

    # ---- human summary ----
    print("=" * 66)
    print("2REAL GAP PIPELINE —", summary["generated"])
    print("=" * 66)
    for s in steps:
        mark = "OK  " if s["ok"] else "FAIL"
        detail = s.get("last_line") or s.get("error") or s.get("reason") or ""
        print(f"  [{mark}] {s['step']:28} {detail[:70]}")

    print()
    print(f"Zobaze snapshot in use : {zobaze_snapshot}")
    print(f"  inventory file age   : {inv_age} days  (H-approved as a permanent slow-stock base)")
    print(f"  Jiji catalogue age   : {cat_age} days")
    print(f"  live Jiji ads age    : {live_age} days")
    print()
    print(f"UNLISTED GAP           : {len(gap_items)} items")
    print(f"  with known COGS      : {known}")
    print(f"  COGS missing         : {unknown}")
    print(f"  verifiable profit    : GH₵ {pot:,.0f}")
    print(f"  alias map entries    : {summary['alias_map_entries']}")

    warnings = []
    if failed:
        warnings.append("FAILED STEP(S): " + ", ".join(summary["failed_steps"]) + " — numbers may be stale.")
    if live_age is not None and live_age > 2:
        warnings.append(f"live Jiji harvest is {live_age} days old — 'already posted' filtering may be wrong.")
    if cat_age is not None and cat_age > 4:
        warnings.append(f"Jiji catalogue is {cat_age} days old — run jiji_refresh.py first.")
    if inv_age is not None and inv_age > 60:
        warnings.append(f"Zobaze inventory is {inv_age} days old (accepted by H as the slow-stock base).")
    if warnings:
        print("\nWARNINGS")
        for w in warnings:
            print("  !! " + w)
    else:
        print("\nNo warnings.")

    print("\n--MACHINE_JSON--")
    print(json.dumps(summary, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
