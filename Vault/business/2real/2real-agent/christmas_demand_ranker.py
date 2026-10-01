#!/usr/bin/env python3
"""
Christmas 2026 Demand Ranking — scores all Jiji listings against researched
demand signals (Ghana/Africa + UK/global), outputs Top 500 for WhatsApp Status
+ Facebook Marketplace.
Sources: Sagaci Research (Africa BF intent), GhanaWeb/NewsGhana (Accra Xmas),
GlobalData UK Tools, Hobbycraft UK (gift trends), Visa VCA holiday data.
"""
import json, re
from collections import defaultdict

BASE = r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent"

# ── Demand model: keyword sets per demand pillar (weight = research priority)
DEMAND = {
    "electronics_appliances": (54, [  # Africa #1 (54%)
        "phone","iphone","samsung","tablet","ipad","laptop","tv","smart tv","speaker",
        "bluetooth","headphone","earbud","airpod","charger","power bank","camera",
        "drone","console","game","watch","smart watch","fitbit","projector","decoder",
    ]),
    "home_kitchen": (40, [  # home goods 28% + appliance gift culture
        "blender","kettle","microwave","iron","fan","rice cooker","air fryer","fryer",
        "toaster","cookware","pot set","knife set","cutlery","bedding","blanket",
        "curtain","vacuum","sewing","water dispenser","juicer","mixer","coffee",
    ]),
    "tools_tradesmen": (45, [  # UK trend + tradesmen year-end bonuses; H's core
        "drill","impact","grinder","saw","sander","router","jigsaw","multitool",
        "wrench","spanner","socket set","plier","screwdriver","hammer","level",
        "tool set","tool box","toolkit","measure","ratchet","torque","work light",
        "welding","generator","compressor","nail gun","planer","lathe","stand",
    ]),
    "auto_travel": (30, [  # Christmas travel season
        "jump starter","tyre","tire","inflator","dash cam","car","vehicle","obd",
        "battery charger","oil","jack","booster","polish","wax","toolbox truck",
    ]),
    "toys_kids": (22, [  # 12% intent but pure gift; H has Leapfrog/LEGO-type stock
        "toy","lego","leapfrog","kids","child","baby","nintendo","playstation","xbox",
        "puzzle","doll","bike kids","scooter","trampoline","educational","rc car","drone kids",
    ]),
    "security_smart": (20, [
        "lock","cctv","security","alarm","doorbell","yale","ring","camera smart",
        "smart door","safe","intercom","sensor","floodlight pir","trail camera",
    ]),
    "power_solar_light": (25, [  # dumsor-proofing + festive lighting
        "solar","inverter","battery","ups","led strip","fairy","floodlight","lantern",
        "torch","rechargeable","generator","extension","socket","dimmer","spotlight",
    ]),
    "giftable_premium": (18, [
        "watch","perfume","sunglasses","wallet","backpack","umbrella","grooming",
        "trimmer","shaver","massager","scales","fitness","binocular","telescope",
    ]),
    "consumables_giftwrap": (10, [
        "gift","hamper","pack of","set of","bundle","24 pack","decor","ornament",
        "christmas","fairy lights","ribbon","candle",
    ]),
}
EXCLUDE = ["empty","used only","damaged","not working","faulty","spares or repair"]

def score(item):
    title = (item.get("title") or "").lower()
    price = (item.get("price_obj") or {}).get("value") or 0
    if any(x in title for x in EXCLUDE):
        return None
    s, pillars = 0.0, []
    for name, (weight, kws) in DEMAND.items():
        hits = [k for k in kws if k in title]
        if hits:
            pillar_score = weight * (0.7 + 0.1 * len(hits))
            s += pillar_score
            pillars.append(name)
    if not pillars:
        return None
    # Accessory penalty — standalone chargers/batteries/cases aren't gift-anchors
    acc = re.search(r"\b(charger only|battery only|spare|replacement|case only|bracket|mount|holder)\b", title)
    if acc: s *= 0.55
    # Complete-kit bonus — "with battery and charger", "kit", "set" sells better
    if re.search(r"\b(kit|with battery|with charger|set|combo|complete)\b", title): s *= 1.15
    # Price-band sweet spots (research: value-conscious gifting)
    if price:
        if 80 <= price <= 500: s *= 1.25      # gift sweet spot
        elif 500 < price <= 1200: s *= 1.1    # aspirational gift
        elif price > 5000: s *= 0.85          # luxury — harder at Christmas
        elif price < 80: s *= 0.9             # low ticket — status post filler
    return s, pillars

items = json.load(open(f"{BASE}\\jiji_listings_full.json"))["items"]
ranked = []
for it in items:
    r = score(it)
    if r:
        ranked.append({"title": it.get("title"), "price": (it.get("price_obj") or {}).get("value"),
                       "url": "https://jiji.com.gh" + (it.get("url") or ""), "score": round(r[0],1),
                       "pillars": r[1]})
ranked.sort(key=lambda x: -x["score"])

top500 = ranked[:500]
json.dump(top500, open(f"{BASE}\\christmas_top500.json","w"), indent=1)

def channel(p):
    if p and p >= 800: return "FB Marketplace (visual, high-ticket)"
    if p and p <= 500: return "WhatsApp Status (fast mover)"
    return "Both"

# Report with pillar spread
by_pillar = defaultdict(int)
for t in top500:
    for p in t["pillars"]: by_pillar[p] += 1

lines = ["# 🎄 Christmas 2026 — Top 500 Ranked Listings",
"","**Demand model:** Ghana/Africa research — electronics & appliances #1 (54%), home/kitchen (28-40%), tools/tradesmen (UK trend), auto/travel, toys, security, power/solar. Price sweet spot GHS 80–500 for gifting.","",
f"**Scored:** {len(items)} listings → {len(ranked)} matched demand → Top 500 selected","",
"## Pillar spread of the Top 500",""]
for p,c in sorted(by_pillar.items(), key=lambda kv:-kv[1]):
    lines.append(f"- {p}: {c} listings")
lines += ["","## Top 60 (preview — full 500 in christmas_top500.json)","",
"| # | Item | Price | Score | Channel |","|---|------|-------|-------|---------|"]
for i,t in enumerate(top500[:60],1):
    lines.append(f"| {i} | {t['title'][:60]} | {t['price'] or '—'} | {t['score']} | {channel(t['price'])} |")
open(f"{BASE}\\christmas_top500.md","w").write("\n".join(lines))
print(f"Ranked {len(ranked)}, saved top {len(top500)}")
for i,t in enumerate(top500[:15],1):
    print(f"{i:2d}. [{t['score']:6.1f}] {t['price'] or '—':>6} {t['title'][:65]}")
print("\nPillar spread:", dict(sorted(by_pillar.items(), key=lambda kv:-kv[1])))
