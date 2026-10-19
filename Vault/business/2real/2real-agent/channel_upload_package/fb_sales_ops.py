#!/usr/bin/env python3
"""FB Marketplace sales-ops helpers for the batch poster cron.

Capabilities (H's request):
  1. FB-optimised listing  -> optimize_listing(title, details, specs) enriches title/desc
  2. Buyer message handling + nudge/revive -> BuyerThreads
  3. Slow-item price drop (H-approval gated) -> PriceDrops
  4. Bundle recommendations -> recommend_bundles(item)
  5. General listing option + cross-sell into FB groups -> cross_sell_targets()

Business rules enforced: no discounts without H approval (price drops are PROPOSALS);
no credit; CTA WhatsApp 0204252252.
"""
import json, os, re, datetime

AGENT = r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent"
PKG = os.path.join(AGENT, "channel_upload_package")
BUYER_F = os.path.join(AGENT, "FB_BUYER_MESSAGES.json")
PERF_F = os.path.join(AGENT, "FB_LISTING_PERFORMANCE.json")
BUNDLE_F = os.path.join(AGENT, "FB_BUNDLES_AND_GROUPS.json")
CTA = "WhatsApp 0204252252"

def _load(p, default):
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception:
        return default

def _save(p, d):
    json.dump(d, open(p, "w", encoding="utf-8"), indent=2)

# ── 1. FB-OPTIMISED LISTING ────────────────────────────────────────────────
def optimize_listing(title, details="", specs="", keywords=None):
    """Return an FB-optimised (title, description). Title: brand+product+spec+trust
    suffix. Description: hook line + key specs + buyer-relevant detail + CTA.
    Keywords enrich search visibility; never invent specs or change the price."""
    kws = keywords or []
    # Title: append the strongest keyword naturally, then the trust suffix once
    t = title.strip().rstrip("—").strip()
    extra = [k for k in kws if k.lower() not in t.lower()]
    if extra and "—" not in t:
        t = f"{t} — {extra[0].title()}"
    if "uk imported" not in t.lower() and ", quality checked" not in t.lower():
        t = f"{t}, UK Imported, Quality Checked"
    elif "uk imported" not in t.lower():
        t = f"{t}, UK Imported"
    # Description: hook + specs + what's included + payment + CTA
    spec_line = re.sub(r"\s+", " ", (specs or details or "")).strip()
    if len(spec_line) > 120:
        spec_line = spec_line[:119].rstrip() + "…"
    hook = "Quality UK-imported, ready to use."
    parts = [hook]
    if spec_line:
        parts.append(spec_line)
    parts.append("Collection Oyarifa or Accra delivery. MoMo or cash only.")
    parts.append(CTA)
    return t, "\n".join(parts)

# ── 2. BUYER MESSAGES + NUDGE/REVIVE ───────────────────────────────────────
class BuyerThreads:
    def __init__(self):
        self.d = _load(BUYER_F, {"threads": [], "nudge_policy": {"first_nudge_hours": 24, "second_nudge_hours": 72, "max_nudges": 2}})

    def upsert(self, thread_id, **fields):
        for t in self.d["threads"]:
            if t.get("id") == thread_id:
                t.update(fields); t["updated"] = datetime.datetime.now().isoformat()
                _save(BUYER_F, self.d); return t
        t = {"id": thread_id, "nudges_sent": 0, "status": "open",
             "created": datetime.datetime.now().isoformat()}
        t.update(fields)
        self.d["threads"].append(t); _save(BUYER_F, self.d); return t

    def due_for_nudge(self):
        """Threads where WE spoke last and the buyer went quiet past the policy window."""
        pol = self.d["nudge_policy"]; now = datetime.datetime.now(); out = []
        for t in self.d["threads"]:
            if t.get("status") not in ("open", "nudged"):
                continue
            if t.get("nudges_sent", 0) >= pol["max_nudges"]:
                continue
            if t.get("last_dir") != "out":
                continue
            last = t.get("last_out") or t.get("updated")
            if not last:
                continue
            try:
                hrs = (now - datetime.datetime.fromisoformat(last)).total_seconds() / 3600
            except Exception:
                continue
            gate = pol["first_nudge_hours"] if t.get("nudges_sent", 0) == 0 else pol["second_nudge_hours"]
            if hrs >= gate:
                out.append({**t, "hours_since_last_out": round(hrs, 1)})
        return out

    def nudge_text(self, t, n):
        """Warm revive/nudge copy — no pressure, no discount-offering (H approves discounts)."""
        item = t.get("listing_title", "the item")
        if n == 0:
            return (f"Hi! Just checking in on the {item} you asked about — still available if you'd "
                    f"like it. Happy to answer any questions. {CTA}")
        return (f"Hi again — the {item} is still here if you're still interested. "
                f"No rush, just let me know. {CTA}")

    def mark_nudged(self, thread_id):
        for t in self.d["threads"]:
            if t.get("id") == thread_id:
                t["nudges_sent"] = t.get("nudges_sent", 0) + 1
                t["status"] = "nudged"
                t["last_out"] = datetime.datetime.now().isoformat()
                t["last_dir"] = "out"
                _save(BUYER_F, self.d); return t
        return None

# ── 3. SLOW-ITEM PRICE DROP (proposals only — H approves) ──────────────────
class PriceDrops:
    def __init__(self):
        self.d = _load(PERF_F, {"listings": [], "price_drop_policy": {
            "slow_after_days": 14, "drop_pct": 10, "max_total_drop_pct": 30, "requires_H_approval": True}})

    def register(self, jiji_id, title, price, posted_date=None, **kw):
        for l in self.d["listings"]:
            if l["jiji_id"] == jiji_id:
                l.update({k: v for k, v in kw.items() if v is not None}); _save(PERF_F, self.d); return l
        l = {"jiji_id": jiji_id, "title": title, "price": price,
             "posted_date": posted_date or datetime.date.today().isoformat(),
             "views": 0, "chats": 0, "sold": False, "price_drops": 0}
        l.update(kw); self.d["listings"].append(l); _save(PERF_F, self.d); return l

    def slow_candidates(self):
        """Listings past the slow window, unsold, low engagement, room to drop."""
        pol = self.d["price_drop_policy"]; today = datetime.date.today(); out = []
        for l in self.d["listings"]:
            if l.get("sold"):
                continue
            try:
                age = (today - datetime.date.fromisoformat(l["posted_date"])).days
            except Exception:
                continue
            if age < pol["slow_after_days"]:
                continue
            total_drop = l.get("price_drops", 0) * pol["drop_pct"]
            if total_drop >= pol["max_total_drop_pct"]:
                continue
            new_price = int(round(l["price"] * (1 - pol["drop_pct"] / 100.0)))
            out.append({**l, "age_days": age, "proposed_price": new_price,
                        "drop_pct": pol["drop_pct"], "needs_H_approval": pol["requires_H_approval"]})
        return out

# ── 4. BUNDLE RECOMMENDATIONS ──────────────────────────────────────────────
def recommend_bundles(item_title, max_n=2):
    """Return bundle suggestions that GENUINELY fit the item.

    Match order (fix 18 Oct 26 — the old fallback bundles[:1] offered
    'Adhesives Starter' for every unrelated item):
      1. exact item-hint overlap with the title (e.g. 'circular saw')
      2. category-keyword overlap (bundle 'categories' list)
      3. NOTHING — return [] rather than an irrelevant bundle.
    Only append a 'Pairs well with...' line when a real match exists.
    """
    b = _load(BUNDLE_F, {"bundles": []})
    tl = item_title.lower()
    exact, cat = [], []
    for bun in b.get("bundles", []):
        if any(h in tl for h in bun.get("items_hint", [])):
            exact.append(bun)
        elif any(k in tl for k in bun.get("categories", [])):
            cat.append(bun)
    out = (exact or cat)[:max_n]
    return out

# ── 5. GENERAL LISTING + CROSS-SELL GROUPS ─────────────────────────────────
def cross_sell_targets(category=""):
    """FB groups to cross-post into (policy caps groups/run; H approves new groups)."""
    b = _load(BUNDLE_F, {"fb_groups": [], "cross_sell_policy": {"max_groups_per_run": 2, "needs_H_approval_for_new_groups": True}})
    pol = b.get("cross_sell_policy", {})
    groups = b.get("fb_groups", [])
    cl = category.lower()
    ranked = sorted(groups, key=lambda g: 0 if cl and cl.split("/")[0] in (g.get("category_focus","").lower()) else 1)
    return {"groups": ranked[:pol.get("max_groups_per_run", 2)],
            "needs_H_approval_for_new_groups": pol.get("needs_H_approval_for_new_groups", True)}

def general_listing(title, body):
    """Format a non-product / general post (service, announcement, wanted)."""
    return {"title": title, "description": f"{body}\n\n{CTA}", "type": "general"}

if __name__ == "__main__":
    # smoke test
    t, d = optimize_listing("Bosch PST 650 Jigsaw", details="500W jigsaw, cuts 65mm wood",
                            specs="500W, 65mm wood, 3100spm, SDS", keywords=["power tools", "jigsaw"])
    print("TITLE:", t)
    print("DESC:\n", d)
    print("BUNDLES for a drill:", [b["name"] for b in recommend_bundles("Parkside Cordless Drill")])
    print("CROSS-SELL:", cross_sell_targets("tools"))