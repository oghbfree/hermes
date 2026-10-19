"""
2Real — Item Location & Testing Ledger (for John / H to maintain)
=================================================================
For the ~500 individual items ready to list. Each physical item has a record:
  WHERE it is (location/zone), has it been TESTED, does it WORK (tested status),
  where it lives in Jiji (jiji_id) so buyer's expectations are managed.

WHY: Jiji is the sales inventory (source of truth for AVAILABILITY). But a Jiji
listing alone doesn't tell you "where is this item physically" or "has it been
tested/verified working". This ledger fills that gap per-item.

USAGE:
  python item_location_ledger.py add  <jiji_id> --loc "B1" --tested yes --works yes
  python item_location_ledger.py upd  <jiji_id> --loc "B2" --tested yes --works no --note "psu dead"
  python item_location_ledger.py ls   [--need-location] [--need-tested] [--not-working] [--sold]
  python item_location_ledger.py expect <jiji_id>   # customer-facing expectation line from status
  python item_location_ledger.py csv          # export for import into the Google sheet tracker

ITEM STATUS LIFECYCLE (full behind-the-scenes state of every item we sell):
  UNLISTED   - physically here, not yet on Jiji (need locate+test+list)
  LOCATED    - location logged, awaiting test
  TO_TEST    - location known, needs testing (John queue)
  TESTED-WORKING - tested, works  -> LIST IT as "Tested Working"
  TESTED-BROKEN  - tested, broken -> LIST as "For Parts / Repair" (honest, manages expectation)
  SOLD       - sold + delivered (archived)
  DEAD/RETURN- unsellable (rain damage, condemned) -> condemned-buyer/clearance
Each record also carries location, tested, works, condition, note, last_updated.

EXPECT command: reads the item's status and outputs the EXACT customer-facing
expectation line to use in the listing / when quoting — so we never over-promise.
"""
import json, sys, os, argparse
from datetime import date
from pathlib import Path

LEDGER = Path(__file__).resolve().parent / "item_location_ledger.json"


def load():
    if not LEDGER.exists():
        return []
    try:
        return json.load(open(LEDGER, encoding="utf-8"))
    except Exception:
        return []


def save(recs):
    json.dump(recs, open(LEDGER, "w", encoding="utf-8"), indent=2, default=str)


def find(recs, jid):
    for r in recs:
        if str(r.get("jiji_id")) == str(jid):
            return r
    return None


def cmd_add(args):
    recs = load()
    if find(recs, args.jiji_id):
        print(f"already exists for jiji_id {args.jiji_id} — use 'upd' instead"); sys.exit(1)
    recs.append({
        "jiji_id": str(args.jiji_id),
        "location": args.loc or "",
        "tested": args.tested or "no",
        "works": args.works or "n/a",
        "condition": args.condition or "",
        "status": (args.status or ""),
        "note": args.note or "",
        "last_updated": date.today().isoformat(),
    })
    save(recs)
    print(f"added {args.jiji_id} -> loc={args.loc} tested={args.tested} works={args.works}")


def cmd_upd(args):
    recs = load()
    r = find(recs, args.jiji_id)
    if r is None:
        print(f"not found {args.jiji_id} — use 'add' first"); sys.exit(1)
    if args.loc is not None: r["location"] = args.loc
    if args.tested is not None: r["tested"] = args.tested
    if args.works is not None: r["works"] = args.works
    if args.condition is not None: r["condition"] = args.condition
    if args.status is not None: r["status"] = args.status
    if args.note is not None: r["note"] = args.note
    r["last_updated"] = date.today().isoformat()
    save(recs)
    print(f"updated {args.jiji_id}")


def derive_status(r):
    """Compute the behind-the-scenes status + the customer-facing expectation line."""
    status = r.get("status", "")
    if not status:
        # derive from tested/works
        if r.get("tested") == "yes" and r.get("works") == "yes":
            status = "TESTED-WORKING"
        elif r.get("tested") == "yes" and r.get("works") == "no":
            status = "TESTED-BROKEN"
        elif r.get("tested") == "yes" and r.get("works") == "n/a":
            status = "TESTED-NA"
        elif r.get("tested") == "no" and r.get("location"):
            status = "TO_TEST"
        elif r.get("location") and not r.get("tested") == "no":
            status = "LOCATED"
        elif not r.get("location"):
            status = "UNLISTED"
        else:
            status = "UNLISTED"
    # Customer-facing expectation line (never over-promise)
    if status == "TESTED-WORKING":
        exp = "UK Pre-Owned, TESTED WORKING — powers on & functions"
    elif status == "TESTED-BROKEN":
        exp = "For Parts / Repair — tested, NOT working (honest: defect present)"
    elif status == "TESTED-NA":
        exp = "Tested OK for its type (no power requirement / n-a)"
    elif status == "TO_TEST":
        exp = "NOT YET TESTED — sold as-is, or test first before promising condition"
    elif status == "LOCATED":
        exp = "Located, TEST PENDING — do not quote 'working' until tested"
    elif status == "SOLD":
        exp = "SOLD — no longer available"
    elif status == "DEAD":
        exp = "UNSELLABLE — do not list; send to condemned-buyer/clearance"
    else:  # UNLISTED
        exp = "Not yet processed — locate + test + list before quoting"
    return status, exp


def cmd_ls(args):
    recs = load()
    if args.need_location:
        recs = [r for r in recs if not r.get("location")]
    if args.need_tested:
        recs = [r for r in recs if r.get("tested") != "yes" and not r.get("status") == "SOLD"]
    if args.not_working:
        recs = [r for r in recs if r.get("works") == "no" or derive_status(r)[0] == "TESTED-BROKEN"]
    if args.sold:
        recs = [r for r in recs if derive_status(r)[0] == "SOLD"]
    if not recs:
        print("(empty)"); return
    hdr = f"{'JIJI_ID':<12} {'STATUS':<18} {'LOC':<12} {'T':<4} {'W':<5} NOTE"
    print(hdr); print("-" * len(hdr))
    for r in recs:
        st, _ = derive_status(r)
        print(f"{str(r.get('jiji_id')):<12} {st:<18} {str(r.get('location','')):<12} "
              f"{str(r.get('tested','')):<4} {str(r.get('works','')):<5} {str(r.get('note',''))[:44]}")


def cmd_expect(args):
    recs = load()
    r = find(recs, args.jiji_id)
    if r is None:
        print(f"not found {args.jiji_id} — use 'add' first"); sys.exit(1)
    st, exp = derive_status(r)
    print(f"Item {args.jiji_id}:")
    print(f"  Status (behind-the-scenes): {st}")
    print(f"  Location: {r.get('location') or '(none yet)'} | Tested: {r.get('tested')} | Works: {r.get('works')}")
    if r.get("note"): print(f"  Note: {r.get('note')}")
    print(f"  ▶ CUSTOMER EXPECTATION LINE: {exp}")


def cmd_csv(args):
    recs = load()
    import csv, io
    out = io.StringIO()
    w = csv.writer(out)
    w.writerow(["jiji_id", "location", "tested", "works", "condition", "note", "last_updated"])
    for r in recs:
        w.writerow([r.get("jiji_id"), r.get("location"), r.get("tested"), r.get("works"),
                    r.get("condition"), r.get("note"), r.get("last_updated")])
    print(out.getvalue())


def main():
    ap = argparse.ArgumentParser(prog="item_location_ledger")
    sub = ap.add_subparsers(dest="cmd", required=True)
    st_choices = ["UNLISTED","LOCATED","TO_TEST","TESTED-WORKING","TESTED-BROKEN","TESTED-NA","SOLD","DEAD"]
    pa = sub.add_parser("add"); pa.add_argument("jiji_id"); pa.add_argument("--loc"); pa.add_argument("--tested", choices=["yes","no"]); pa.add_argument("--works", choices=["yes","no","n/a"]); pa.add_argument("--condition"); pa.add_argument("--status", choices=st_choices); pa.add_argument("--note"); pa.set_defaults(fn=cmd_add)
    pu = sub.add_parser("upd"); pu.add_argument("jiji_id"); pu.add_argument("--loc"); pu.add_argument("--tested", choices=["yes","no"]); pu.add_argument("--works", choices=["yes","no","n/a"]); pu.add_argument("--condition"); pu.add_argument("--status", choices=st_choices); pu.add_argument("--note"); pu.set_defaults(fn=cmd_upd)
    pl = sub.add_parser("ls"); pl.add_argument("--need-location", action="store_true"); pl.add_argument("--need-tested", action="store_true"); pl.add_argument("--not-working", action="store_true"); pl.add_argument("--sold", action="store_true"); pl.set_defaults(fn=cmd_ls)
    pe = sub.add_parser("expect"); pe.add_argument("jiji_id"); pe.set_defaults(fn=cmd_expect)
    pc = sub.add_parser("csv"); pc.set_defaults(fn=cmd_csv)
    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()