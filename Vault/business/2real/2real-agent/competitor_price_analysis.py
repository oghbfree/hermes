#!/usr/bin/env python3
"""Competitor price analysis — combines Jiji scan with 2Real inventory costs."""
import json
import re
import statistics
from pathlib import Path

BASE = Path(r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent")
INVENTORY = json.loads((BASE / "inventory_agent.json").read_text(encoding="utf-8"))
SCAN = json.loads((BASE / "competitor_scan_raw.json").read_text(encoding="utf-8"))

# Map: our inventory item (search terms) -> scan key
MATCHES = [
    # (scan_key, inventory search terms, product-type filter note)
    ("hydraulic bottle jack (manual scan)", ["hydraulic bottle jack"], "comparable all"),
    ("bosch sds rotary hammer", ["GBH 2-26"], "SDS-class only"),
    ("makita drill", ["6280d"], "exact model"),
    ("yale smart door lock", ["yale"], "smart locks only"),
    ("black decker cordless drill", ["Black And Decker", "cordless drill"], "18v class"),
    ("hacksaw frame", ["Hack Saw Frame"], "frames only"),
    ("tile cutter", ["Tile Cutter"], "manual large"),
    ("jump starter", ["Jump Starter"], "12v portable"),
    ("padlock", ["140t"], "keyed pair"),
    ("silicone sealant", ["Acetic Silicone"], "acetic 280ml+"),
]

def find_item(terms):
    for it in INVENTORY:
        blob = f"{it.get('name','')} {it.get('variant','')}".lower()
        if all(t.lower() in blob for t in terms):
            return it
    return None

def median_comps(prices, note=""):
    if not prices:
        return None, None, None
    s = sorted(prices)
    med = statistics.median(s)
    if len(s) >= 4:
        lo, hi = s[len(s)//4], s[3*len(s)//4]
    else:
        lo, hi = s[0], s[-1]
    return med, lo, hi

print("=" * 100)
print("2REAL COMPETITOR PRICE ANALYSIS — Jiji Ghana (live scan, 17 Sep 2026)")
print("=" * 100)

report = []
for scan_key, terms, note in MATCHES:
    ours = find_item(terms)
    prices = SCAN.get(scan_key, [])
    if not prices and scan_key == "hydraulic bottle jack (manual scan)":
        prices = [280, 550, 350, 410, 625, 210, 160, 460, 890, 350, 515, 1135, 400, 338, 210]
    med, lo, hi = median_comps(prices)
    if med is None:
        print(f"\n!! No competitor prices for {scan_key}")
        continue
        print(f"\n!! Could not find inventory item for {terms}")
        continue
    p = float(ours.get("price", 0))
    c = float(ours.get("cost", 0) or 0)
    stock = ours.get("stock", 0)
    name = f"{ours.get('name','')} {ours.get('variant','')}".strip()[:45]
    floor = c * 1.25 if c else None

    verdict = ""
    action = ""
    if med:
        ratio = p / med
        if ratio > 1.25:
            verdict = f"OVERPRICED {ratio:.0%} of market"
            action = f"Cut to GHS {med:,.0f} or justify premium in title"
        elif ratio < 0.75:
            verdict = f"UNDERPRICED ({ratio:.0%} of market)"
            action = f"Raise toward GHS {max(med*0.9, floor or 0):,.0f}"
        else:
            verdict = "AT MARKET"
            action = "Keep — maybe small tweak"

    print(f"\n{ours.get('name','')} {ours.get('variant','')}")
    print(f"  OURS:  GHS {p:,.0f} (cost GHS {c:,.0f}, stock {stock}) | floor GHS {floor:,.0f}" if c else
          f"  OURS:  GHS {p:,.0f} (cost unknown, stock {stock})")
    print(f"  MARKET: median GHS {med:,.0f} | range GHS {lo:,.0f} - {hi:,.0f} | n={len(prices)} | filter: {note}")
    print(f"  VERDICT: {verdict}")
    print(f"  ACTION:  {action}")
    report.append({
        "item": name, "our_price": p, "cost": c, "stock": stock,
        "median": med, "low": lo, "high": hi, "verdict": verdict, "action": action
    })

(BASE / "competitor_price_analysis.json").write_text(json.dumps(report, indent=2))
print("\nSaved -> competitor_price_analysis.json")