#!/usr/bin/env python3
"""
Jiji + Zobaze WhatsApp Response Draft for 2Real Enterprises
Owner: H | Shop: https://jiji.com.gh/shop/2real-online Behavior:
- Match customer message to Jiji listings OR Zobaze inventory only
- If found → item-specific reply (name, price, availability)
- If not found → placeholder: "We will get back to you shortly."
- NO off-topic advice, NO wandering, NO orders outside these two sources
"""

import json
import re
from pathlib import Path
from datetime import datetime

# ─── CONFIG ───────────────────────────────────────────────────────────────
JIJI_SHOP_URL = "https://jiji.com.gh/shop/2real-online"
ZOBaze_INVENTORY_PATH = Path(r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\inventory_agent.json")
JIJI_TITLES_PATH = Path(r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\jiji_page_listings.json")
REPLY_LOG_PATH = Path(r"C:\Users\User\.hermes\workspace\Vault\business\2real\customer-interactions.md")
PLACEHOLDER = "We will get back to you shortly."
JIJI_REFRESH = False  # set True to refresh jiji_page_listings.json from live page

# ─── JIJI PAGE SCRAper ────────────────────────────────────────────────────
def refresh_jiji_titles() -> list:
    try:
        import urllib.request
        req = urllib.request.Request(JIJI_SHOP_URL, headers={"User-Agent":"Mozilla/5.0"})
        html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", errors="ignore")
        titles = re.findall(r'qa-advert-title[^<]*>([^<]+)', html)
        cleaned = []
        for t in titles:
            t = t.strip()
            t = t.replace("&#39;", "'").replace("&amp;", "&").replace("&nbsp;", " ")
            if t:
                cleaned.append(t)
        if cleaned:
            with open(JIJI_TITLES_PATH, "w", encoding="utf-8") as f:
                json.dump(cleaned, f, indent=2, ensure_ascii=False)
        return cleaned
    except Exception:
        return []

# ─── LOADERS ──────────────────────────────────────────────────────────────
def load_jiji_listings() -> list:
    """Return list of Jiji advert *dicts* (title, price, region, category).
    Reads the full listings file; falls back to bare titles from the legacy file."""
    if JIJI_REFRESH:
        try:
            import subprocess
            subprocess.run([sys.executable, str(Path(__file__).parent / "jiji_scrape_all.py")],
                           timeout=180, cwd=str(Path(__file__).parent))
        except Exception:
            pass
    full = Path(__file__).parent / "jiji_listings_full.json"
    items = []
    if full.exists():
        try:
            data = json.loads(full.read_text(encoding="utf-8"))
            items = data.get("items") or []
        except Exception:
            items = []
    if items:
        return items
    # legacy fallback: jiji_page_listings.json (now {"titles": [...]} or bare list)
    if not JIJI_TITLES_PATH.exists():
        return []
    try:
        raw = json.loads(JIJI_TITLES_PATH.read_text(encoding="utf-8"))
    except Exception:
        return []
    if isinstance(raw, list):
        return [{"title": t} for t in raw]
    if isinstance(raw, dict):
        return [{"title": t} for t in raw.get("titles", [])]
    return []

def load_zobaze():
    if not ZOBaze_INVENTORY_PATH.exists():
        return []
    with open(ZOBaze_INVENTORY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

# ─── TEXT HELPERS ─────────────────────────────────────────────────────────
STOP_WORDS = {
    "tell","me","about","the","a","an","is","are","do","does","did","can",
    "could","would","should","will","shall","may","might","must","have","has",
    "had","you","your","please","thanks","hi","hello","hey","there","want",
    "know","looking","selling","sell","buy","price","much","cost","show","see",
    "send","give","call","reply","message","msg",
    "how","any","for","sale","available","got","have","need","please","of",
    "and","in","on","at","with","this","that","it","i","im","we","our","some",
}

def normalize(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text

def query_tokens(text: str):
    return [w for w in normalize(text).split() if w not in STOP_WORDS]

def jiji_match(query: str, adverts: list):
    qtokens = query_tokens(query)
    best_title, best_score = None, 0.0
    for ad in adverts:
        title = ad.get("title", "") if isinstance(ad, dict) else ad
        ttokens = set(normalize(title).split())
        if not ttokens:
            continue
        joined = " ".join(qtokens)
        norm_t = " ".join(ttokens)
        score = 0.0
        if joined and joined in norm_t:
            score = 1.0
        else:
            overlap = len(set(qtokens) & ttokens) / max(len(qtokens), 1)
            overlap_rev = len(set(qtokens) & ttokens) / max(len(ttokens), 1)
            score = max(overlap, overlap_rev)
        if score >= 0.7 and score > best_score:
            best_score = score
            best_title = ad
    return best_title, best_score

def zobaze_match(query: str, items: list):
    q = normalize(query)
    q_words = set(q.split())
    best, best_score = None, 0.0
    for item in items:
        if not item.get("in_stock", False):
            continue
        name = normalize(item.get("name", ""))
        variant = normalize(item.get("variant", ""))
        category = normalize(item.get("category", ""))
        blob = f"{name} {variant} {category}"
        b_words = set(blob.split())
        overlap = len(q_words & b_words)
        o_q = overlap / max(len(q_words), 1)
        o_b = overlap / max(len(b_words), 1)
        score = max(o_q, o_b)
        if score > best_score and score >= 0.55:
            best_score = score
            best = item
    return best

# ─── REPLY GENERATOR ─────────────────────────────────────────────────────
def draft_reply(customer_message: str, items: list, jiji_adverts: list) -> str:
    # 1) Jiji first (with price/region when available)
    matched_ad, j_score = jiji_match(customer_message, jiji_adverts)
    if matched_ad and j_score >= 0.7:
        title = matched_ad.get("title", "") if isinstance(matched_ad, dict) else matched_ad
        price = matched_ad.get("price_title") if isinstance(matched_ad, dict) else None
        region = matched_ad.get("region_name") if isinstance(matched_ad, dict) else None
        if price:
            loc = f" at {region}" if region else ""
            return (
                f"2Real Enterprises. We have \"{title}\"{loc}. "
                f"Price: {price}. Message back to confirm availability and reserve."
            )
        # No price available: still answer from listing name
        return f"2Real Enterprises. Yes, we list \"{title}\" on our Jiji shop. Message back for price and availability and I'll confirm stock for you."

    # 2) Zobaze only if Jiji did not match or matched weakly
    matched = zobaze_match(customer_message, items)
    if matched:
        price = float(matched.get("price", 0))
        stock = int(matched.get("stock", 0))
        variant = matched.get("variant", matched.get("name", "that item"))
        if stock > 0:
            return (
                f"2Real Enterprises. {variant} is available at GHS {price:,.0f}. "
                f"We have {stock} in stock at Oyarifa. "
                f"Payment: MoMo on delivery or cash. No credit. "
                f"Want me to reserve it?"
            )
        return (
            f"2Real Enterprises. {variant} is currently out of stock. "
            f"Price when restocked: GHS {price:,.0f}. "
            f"I'll get back to you when it's back."
        )

    # 3) Placeholder
    return PLACEHOLDER

# ─── LOG INTERACTION ─────────────────────────────────────────────────────
def log_interaction(customer_msg: str, reply: str, channel: str = "whatsapp"):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = f"\n## {ts}\n- **Channel:** {channel}\n- **Customer:** {customer_msg}\n- **Reply:** {reply}\n"
    with open(REPLY_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(entry)

# ─── MAIN ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python jiji_zobaze_responder.py '<customer message>'")
        sys.exit(1)

    customer_message = " ".join(sys.argv[1:])
    items = load_zobaze()
    jiji_titles = load_jiji_listings()
    reply = draft_reply(customer_message, items, jiji_titles)
    log_interaction(customer_message, reply)
    print(reply)
