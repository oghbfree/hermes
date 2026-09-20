#!/usr/bin/env python3
"""
2Real Christmas Gap Analysis — Zobaze items NOT on Jiji
Matches in-stock inventory against Jiji catalog, outputs prioritized listing targets.
"""
import json
import re
from pathlib import Path
from datetime import datetime

BASE = Path(r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent")
INVENTORY = json.loads((BASE / "inventory_agent.json").read_text(encoding="utf-8"))
JIJI = json.loads((BASE / "jiji_listings_full.json").read_text(encoding="utf-8"))
JIJI_TITLES = [str(x.get("title", "")) for x in JIJI.get("items", [])]

STOP = {"the","a","an","and","or","for","with","new","used","brand","uk","of","in","on","set","2","1"}

def norm(t):
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9\s]", " ", str(t).lower())).strip()

def tokens(t):
    return set(w for w in norm(t).split() if w not in STOP and len(w) > 1)

# Pre-index Jiji titles
jiji_tokens = [(t, tokens(t)) for t in JIJI_TITLES]

# Christmas gift potential by category keywords
GIFT_CATS = ["toy", "lego", "leapfrog", "game", "nintendo", "xbox", "playstation", "ps4", "ps5",
             "kitchen", "blender", "air fryer", "coffee", "watch", "headphone", "earbud",
             "speaker", "tv", "tablet", "camera", "phone", "perfume", "beauty"]

def gift_score(name):
    n = norm(name)
    return sum(2 for g in GIFT_CATS if g in n)

results = []
matched_count = 0
for it in INVENTORY:
    if not it.get("in_stock", False):
        continue
    name = f"{it.get('name','')} {it.get('variant','')}".strip()
    it_toks = tokens(name)
    if not it_toks:
        continue

    best, best_score = None, 0.0
    for title, ttoks in jiji_tokens:
        overlap = len(it_toks & ttoks) / max(len(it_toks), 1)
        if overlap > best_score:
            best_score = overlap
            best = title

    if best_score >= 0.6:
        matched_count += 1
        continue  # already on Jiji

    price = float(it.get("price", 0) or 0)
    cost = float(it.get("cost", 0) or 0)
    stock = int(it.get("stock", 0) or 0)
    margin = price - cost if cost else price * 0.3
    gs = gift_score(name)
    priority = margin * (2 if gs else 1) * (1.2 if stock > 2 else 1)

    results.append({
        "name": name[:70], "price": price, "cost": cost, "stock": stock,
        "margin": round(margin), "gift": bool(gs), "priority": round(priority),
        "best_partial_match": best[:50] if best else "", "partial_score": round(best_score, 2)
    })

results.sort(key=lambda x: -x["priority"])

print(f"In-stock inventory: {sum(1 for i in INVENTORY if i.get('in_stock'))}")
print(f"Matched to Jiji (>=60% tokens): {matched_count}")
print(f"GAP — not confidently on Jiji: {len(results)}")
print(f"\n--- TOP 30 LISTING TARGETS (prioritized: margin x gift-potential x stock) ---\n")
for i, r in enumerate(results[:30], 1):
    gift = "🎁" if r["gift"] else "  "
    print(f"{i:>2}.{gift} GHS {r['price']:>7,.0f} | stock {r['stock']:>2} | margin ~{r['margin']:>6,.0f} | {r['name']}")

out = BASE / "christmas_gap_list.json"
out.write_text(json.dumps({"generated": datetime.now().isoformat(), "total_gap": len(results), "items": results}, indent=2))
print(f"\nSaved -> {out}")