#!/usr/bin/env python3
"""
2Real Christmas Countdown Tracker
Runs inside the Daily Jiji Report and the Monday gap re-scan.
Computes: days to Christmas, days to UK order deadline, gap progress.
"""
import json
from pathlib import Path
from datetime import datetime

BASE = Path(r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent")
GAP_FILE = BASE / "christmas_gap_list.json"
PROGRESS_FILE = BASE / "christmas_progress.json"

# Fixed dates (year-agnostic except Christmas)
UK_ORDER_DEADLINE = "2026-10-31"   # last day to order UK stock arriving in time
CHRISTMAS = "2026-12-25"


def days_until(date_str):
    target = datetime.strptime(date_str, "%Y-%m-%d")
    return (target - datetime.now()).days


def get_progress():
    """Load or initialise Christmas listing progress."""
    if PROGRESS_FILE.exists():
        try:
            return json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    gap = json.loads(GAP_FILE.read_text(encoding="utf-8")) if GAP_FILE.exists() else {}
    prog = {
        "total_gap": gap.get("total_gap", 0),
        "gap_remaining": gap.get("total_gap", 0),
        "history": [],
    }
    PROGRESS_FILE.write_text(json.dumps(prog, indent=2))
    return prog


def _gap_of(entry):
    """History entries before 05 Oct 2026 used key 'listed' to hold gap remaining."""
    if "gap_remaining" in entry:
        return entry["gap_remaining"]
    return entry.get("listed", 0)


def record_gap(n_gap):
    """Monday re-scan: record the current gap remaining (items not on Jiji)."""
    prog = get_progress()
    prog["gap_remaining"] = n_gap
    prog.pop("listed", None)  # drop legacy mislabelled key
    today = datetime.now().strftime("%Y-%m-%d")
    prog["history"] = [h for h in prog.get("history", []) if h.get("date") != today]
    prog["history"].append({"date": today, "gap_remaining": n_gap})
    prog["history"] = prog["history"][-60:]
    PROGRESS_FILE.write_text(json.dumps(prog, indent=2))
    return prog


def countdown_block():
    """Produce the Christmas countdown section for the daily report."""
    prog = get_progress()
    d_christmas = days_until(CHRISTMAS)
    d_uk = days_until(UK_ORDER_DEADLINE)
    weeks = d_christmas // 7

    remaining = int(prog.get("gap_remaining", prog.get("listed", 0)))

    lines = []
    lines.append("\U0001f384 *CHRISTMAS COUNTDOWN*")
    lines.append(f"  \u23f3 {d_christmas} days ({weeks} weeks) to Christmas")
    if d_uk >= 0:
        urgency = "\U0001f534 URGENT" if d_uk <= 14 else "\U0001f7e1"
        lines.append(f"  \U0001f69b UK order deadline: {d_uk} days left ({urgency} — after {UK_ORDER_DEADLINE} shipping won't arrive in time)")
    else:
        lines.append(f"  \U0001f534 UK ORDER DEADLINE PASSED — Christmas stock must now come locally")
    lines.append(f"  \U0001f4cb Gap items remaining: {remaining} not on Jiji")

    # Pace check: to clear the gap before Nov 15 (boost deadline)
    try:
        boost_deadline = datetime.strptime("2026-11-15", "%Y-%m-%d")
        days_to_boost = (boost_deadline - datetime.now()).days
        if remaining > 0 and days_to_boost > 0:
            per_day = remaining / days_to_boost
            lines.append(f"  \U0001f4c8 Pace needed: {per_day:.0f} listings/day to clear gap by Nov 15 (TOP+ boost deadline)")
    except Exception:
        pass

    # Weekly trend (last 2 entries)
    hist = prog.get("history", [])
    if len(hist) >= 2:
        prev = _gap_of(hist[-2])
        delta = remaining - prev
        verb = "cleared" if delta < 0 else "added"
        lines.append(f"  \U0001f4c5 Week-on-week: {delta:+d} gap items ({abs(delta)} {verb})")
    lines.append("")
    return "\n".join(lines), {"d_christmas": d_christmas, "d_uk": d_uk, "remaining": remaining}


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        prog = record_gap(int(sys.argv[1]))
        print(f"Recorded: gap remaining = {prog['gap_remaining']} items not on Jiji")
    block, _ = countdown_block()
    print(block)