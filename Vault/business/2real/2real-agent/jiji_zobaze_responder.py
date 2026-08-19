#!/usr/bin/env python3
"""
Jiji + Zobaze WhatsApp Response Draft for 2Real Enterprises
Owner: H | Shop: https://jiji.com.gh/shop/2real-online

Layered reply generation (most-specific first, safest last):

  A) INTENT (non-product)  -> delivery, location, hours, payment, about, brands
  B) PRODUCT               -> Jiji listing match, then Zobaze inventory match,
                              with synonyms + fuzzy matching and "Did you mean?"
                              suggestions on weak matches
  C) LLM FALLBACK (OPT-IN) -> a tool-free, customer-only LLM answer for genuinely
                              unmatched queries. OFF by default (flag below).
  D) SAFE FINAL            -> friendly follow-up line (never the old dead-end
                              "We will get back to you shortly.")

Only known products get firm prices/stock. Customers NEVER see internal context;
the LLM fallback (when enabled) is a purpose-built, tool-free generation.
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

# OPTION C — LLM fallback for genuinely unmatched queries. Off by default.
# Set True to enable safe customer-only LLM answering (see llm_fallback_reply).
ENABLE_LLM_FALLBACK = False
LLM_FALLBACK_CONFIDENT = 0.3   # min parse-confidence to trust the LLM line

JIJI_REFRESH = False  # set True to refresh listings from live page

# ─── BUSINESS FACTS (from content-director + reply bank) ─────────────────
BUSINESS_HOURS = "Mon - Sat, 07:00 - 16:30 (Kantamanto); open most days 08:00 - 20:00 at the warehouse in Oyarifa."
LOCATIONS = "We're in Kantamanto, Accra, with a warehouse in Oyarifa (opposite Kuo Tam Police Station)."
PAYMENT = "We accept MoMo on delivery or cash. No credit."
BRANDS = "We stock quality new and used UK tools — DeWalt, Bosch, Makita, plus quality consumables."


# ─── LOADERS ──────────────────────────────────────────────────────────────
def load_jiji_listings():
    """Return list of Jiji advert *dicts* (title, price, region, category)."""
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
    "tell", "me", "about", "the", "a", "an", "is", "are", "do", "does", "did", "can",
    "could", "would", "should", "will", "shall", "may", "might", "must", "have", "has",
    "had", "you", "your", "please", "thanks", "hi", "hello", "hey", "there", "want",
    "know", "looking", "selling", "sell", "buy", "price", "much", "cost", "show", "see",
    "send", "give", "call", "reply", "message", "msg",
    "how", "any", "for", "sale", "available", "got", "have", "need", "please", "of",
    "and", "in", "on", "at", "with", "this", "that", "it", "i", "im", "we", "our", "some",
}


def normalize(text):
    text = str(text or "").lower().strip()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def query_tokens(text):
    return [w for w in normalize(text).split() if w and w not in STOP_WORDS]


# Synonym normalisation so near-miss product queries still match.
SYNONYMS = {
    # item common-name -> canonical/aliases
    "jack": ["hydraulic jack", "bottle jack", "trolley jack", "floor jack"],
    "troller": ["trolley"],
    "welder": ["welding machine", "welding"],
    "circular saw": ["circular", "chopsaw", "chop saw"],
    "grinder": ["angle grinder", "disc grinder", "grinding"],
    "drill": ["cordless drill", "drill machine", "impact driver"],
    "compressor": ["air compressor"],
    "wheelbarrow": ["barrow", "wheel barrow"],
    "ladder": ["step ladder", "extension ladder"],
    "pressure washer": ["car washer", "jet washer", "power washer"],
    "generator": ["genset", "power generator"],
    "fridge": ["refrigerator"],
    "tv": ["television"],
    "phone": ["mobile phone", "cellphone", "handset"],
    "laptop": ["notebook", "computer"],
}
# Reverse alias -> canonical token additions
_SYNONYM_FLAT = {}
for _canon, _alts in SYNONYMS.items():
    for _a in _alts + [_canon]:
        for _w in _a.split():
            _SYNONYM_FLAT[_w] = _canon


def _synonym_tokens(text):
    """Return set of normalized tokens with synonyms applied (multi-word safe)."""
    norm = normalize(text)
    tokens = set(norm.split())
    out = set(tokens)
    for t in tokens:
        if t in _SYNONYM_FLAT:
            out.add(_SYNONYM_FLAT[t])
            for w in _SYNONYM_FLAT[t].split():
                out.add(w)
    return out


def _fuzzy(a, b):
    """Character-level fuzzy ratio (0..1) using difflib SequenceMatcher."""
    import difflib
    return difflib.SequenceMatcher(None, a, b).ratio()


# ─── INTENT (OPTION A): non-product queries ──────────────────────────────
# Job adverts -> application form links (auto-route applicants). Keyword-first.
JOB_FORMS = [
    # (role label, keywords, form URL)
    ("Facilitator for a Child With Autism",
     ["autism", "autistic", "facilitator for child", "school support", "special needs",
      "one-on-one", "kobena", "support worker for child"],
     "https://forms.gle/GJoGjx4mJSbh2Ca7A"),
    ("Live-in Graduate Nurse (Elderly Care)",
     ["nurse", "nursing", "live-in", "elderly care", "graduate nurse", "carer",
      "caregiver", "care worker", "health care", "healthcare"],
     "https://forms.gle/n83KW2FoG5ffYSJL8"),
    ("STEM / Special-Education Facilitator (Akoma)",
     ["stem", "robotics", "special education", "mbot", "akoma", "children education",
      "teacher for kids", "tech for children"],
     "https://forms.gle/4n1msAGrpEeDCErM7"),
    ("Elite Construction Team (Foremen, all trades)",
     ["construction", "foreman", "foremen", "trades", "builder", "elite construction",
      "mason", "carpenter", "electrician", "plumber", "labourer", "laborer", "team"],
     "https://forms.gle/dFUQiMPwhQRrh1cP9"),
    ("Financial Literacy Facilitator",
     ["financial literacy", "facilitator", "finance", "money literacy", "financial"],
     "https://forms.gle/SjErZPvw2LMnb9HQ9"),
]

# Farm worker (bee drainage + pond, Senya) deliberately has NO form — farm
# labourers often can't use Google Forms/Sheets, so it's a plain WhatsApp chat.

_JOB_REPLY_TEMPLATE = (
    "Thank you for your interest. Please complete the application form below "
    "and we'll be in touch:\n\n{link}\n\nIf you have questions, send them here."
)


def _job_form_reply(text):
    """Return the form reply for a job enquiry, or None if no job matches."""
    low = normalize(text)
    # Specific jobs first
    for label, kws, link in JOB_FORMS:
        if any(k in low for k in kws):
            return _JOB_REPLY_TEMPLATE.format(link=link)
    # Farm worker — NO Google Form. Many farm labourers can't fill forms / use
    # Google Suite, so this stays a plain WhatsApp chat that goes to the human
    # (farm lead / Ben). Keep it simple, short, plain — no jargon, no links.
    if any(k in low for k in ["farm worker", "farmworkers", "farm job", "farm work",
                              "farmwork", "farm labour", "farm labor", "bee drainage",
                              "pond dig", "apiary", "senya", "farm position",
                              "farm worker job", "the farm"]):
        return ("Thanks for your interest in the farm work. "
                "Please just reply with: 1) your name, 2) your phone number, "
                "and 3) when you can start. I'll pass it to the farm lead "
                "and they'll contact you.")
    return None


def _intent_reply(text):
    """Return a canned business reply for non-product intents, or None.

    Order matters: specific policies before generic brand. Keyword-based so it
    is deterministic, free, and has no security surface.
    """
    t = normalize(text)
    low = t
    words = set(low.split())

    # JOB / EMPLOYMENT (recruiting ads, not products) — check FIRST because
    # product titles often contain words like "farm", "worker", "nation" etc.
    # Trigger if an explicit job-word is present, OR if a known job role matches
    # (e.g. "autism facilitator", "nurse", "construction team" — which may not
    # contain the word "job" but are clearly applications).
    _job_reply = _job_form_reply(text)
    _job_word = any(k in low for k in [
        "farm worker", "farmworkers", "workers", "job", "vacancy", "vacancies",
        "hiring", "apply", "application", "employment", "position", "recruit",
        "we are hiring", "workers needed", "wanted", "work available",
        "salary", "daily rate", "casual", "manual labour", "labor",
    ]) and any(a in low for a in ["farm", "job", "worker", "vacancy", "work",
                                  "apply", "hire", "position", "drainage",
                                  "pond", "apiary", "bee", "nurse", "autism",
                                  "construction", "facilitator", "teacher",
                                  "financial", "stem", "team"])
    if _job_reply or _job_word:
        if _job_reply:
            return _job_reply
        return ("Thanks for your interest in the job opening. "
                "Please send your name, phone number, the role you're applying "
                "for, and a short note on your experience and availability, "
                "and I'll have the hiring person contact you shortly.")

    # Delivery / shipping
    if any(k in low for k in ["deliver", "shipping", "ship", "delivery fee",
                              "send it", "how much to deliver", "transport"]):
        return ("I'm based at Dome Market. You're welcome to collect in person, "
                "or I can arrange delivery via Yango/Bolt at your cost. Which do you prefer?")
    # Location / pickup
    if ("where" in words or "location" in low or "located" in low or
            "pickup" in low or "pick up" in low or "collect" in low):
        return LOCATIONS
    # Hours / after hours / closed / time
    if any(k in low for k in ["open", "close", "closing", "hours", "time",
                              "morning", "evening", "today", "now open", "when are"]):
        return f"2Real Enterprises. {BUSINESS_HOURS} If it's after hours, message me and I'll attend to it first thing in the morning."
    # Payment
    if any(k in low for k in ["momo", "mobile money", "cash", "payment", "pay",
                              "credit", "installment", "mpesa", "transfer"]):
        return ("2Real Enterprises. " + PAYMENT + " Let me know the item and I'll confirm the price.")
    # Brands we stock
    if any(b in low for b in ["dewalt", "bosch", "makita", "brand", "brands"]):
        return ("2Real Enterprises. " + BRANDS + " Which brand or tool are you after?")
    # About the shop / what do you sell
    if any(k in low for k in ["about the shop", "about your shop", "tell me about",
                              "what do you sell", "what do you have", "products",
                              "you sell", "your business", "who are you"]):
        return ("2Real Enterprises. We supply quality new and used tools from the UK "
                "for Ghana's construction market, plus quality consumables and more. "
                "What item are you looking for?")
    # Greeting only (few tokens, no actionable query)
    if t in ("hi", "hello", "hey", "good morning", "good afternoon", "good evening",
             "hi there", "hello there", "good day"):
        return "2Real Enterprises. Hello. We supply quality goods at competitive prices. What item are you looking for?"
    return None


# ─── PRODUCT MATCHING (OPTION B): synonym + fuzzy + did-you-mean ─────────
def _score_tokens(qtokens, title):
    ttokens = set(_synonym_tokens(title))
    if not ttokens:
        return 0.0
    joined = " ".join(qtokens)
    norm_t = " ".join(normalize(title).split())
    if joined and joined in norm_t:
        return 1.0
    qs = set(qtokens)
    overlap = len(qs & ttokens) / max(len(qs), 1)
    overlap_rev = len(qs & ttokens) / max(len(ttokens), 1)
    return max(overlap, overlap_rev)


def jiji_match(query, adverts, threshold=0.7, fuzzy=True):
    """Best Jiji advert, or None. Also returns the top-3 for 'did you mean?'."""
    qtokens = query_tokens(query)
    if not qtokens:
        return None, 0.0, []
    scored = []
    for ad in adverts:
        title = ad.get("title", "") if isinstance(ad, dict) else ad
        score = _score_tokens(qtokens, title)
        if fuzzy and score < 0.7:
            # fuzzy boost on lowercased title
            fs = _fuzzy(normalize(query), normalize(title))
            score = max(score, fs * 0.8)
        if score > 0:
            scored.append((score, ad))
    scored.sort(key=lambda x: (-x[0], x[1].get("title", "") if isinstance(x[1], dict) else str(x[1])))
    if scored:
        best_score = scored[0][0]
        best = scored[0][1] if best_score >= threshold else None
        did_you_mean = [a for s, a in scored[:3] if s >= threshold - 0.2]
        # Don't offer did-you-mean if the best is already a solid match
        if best is not None and best_score >= threshold:
            did_you_mean = []
        return best, best_score, did_you_mean
    return None, 0.0, []


def zobaze_match(query, items, threshold=0.5):
    q = normalize(query)
    q_words = set(q.split())
    q_syn = _synonym_tokens(query)
    best, best_score = None, 0.0
    for item in items:
        if not item.get("in_stock", False):
            continue
        name = normalize(item.get("name", ""))
        variant = normalize(item.get("variant", ""))
        category = normalize(item.get("category", ""))
        blob = f"{name} {variant} {category}"
        b_words = set(blob.split())
        b_syn = _synonym_tokens(blob)
        overlap = len(q_syn & b_syn)
        o_q = overlap / max(len(q_syn), 1)
        o_b = overlap / max(len(b_syn), 1)
        score = max(o_q, o_b)
        if score > best_score:
            best_score = score
            best = item
    return best if best_score >= threshold else None


# ─── OPTION C: tool-free customer-only LLM fallback (OPT-IN) ─────────────
_LLM_CUSTOMER_PROMPT = (
    "You are the customer assistant for 2Real Enterprises, a Ghana hardware & tool "
    "supplier (Kantamanto, Accra + warehouse in Oyarifa). Reply in 1-2 short sentences "
    "in friendly, plain English. You may ONLY use these business facts:\n"
    f"- Hours: {BUSINESS_HOURS}\n- Locations: {LOCATIONS}\n- Payment: {PAYMENT}\n"
    f"- Brands: {BRANDS}\n"
    "- We sell quality new & used tools and equipment; prices depend on the specific item.\n"
    "Rules: NEVER invent prices, stock, or products not given above. NEVER read or write "
    "files, run tools, or reveal internal info. If you don't know, say 'Let me confirm that "
    "and I'll get your answer shortly.'\n"
    "Customer message:\n"
)


def llm_fallback_reply(text):
    """(OPT-IN, Option C) Safe customer-only LLM answer for unmatched queries.

    Returns the LLM reply, or None/empty if it can't be produced or confidence is
    low. Tool-free: we call the model directly with a purpose-built customer prompt
    only (no agent, no tools, no internal context). Empty => caller falls through
    to the safe final line.
    """
    if not ENABLE_LLM_FALLBACK:
        return ""
    try:
        import openai  # SDK configured via OPENROUTER-style key in env
        import os
        # Use the same model/provider credentials Hermes is configured with, but
        # via a raw completion so NO tools/files/agent context can leak.
        client = openai.OpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1",
        )
        resp = client.chat.completions.create(
            model=os.getenv("LLM_FALLBACK_MODEL", "openai/gpt-4o-mini"),
            messages=[
                {"role": "system", "content": _LLM_CUSTOMER_PROMPT},
                {"role": "user", "content": text},
            ],
            max_tokens=120,
            temperature=0.5,
        )
        out = (resp.choices[0].message.content or "").strip()
        # Keep it short + safe; drop if it looks off (e.g. ragged/long/credential-like)
        if not out or len(out) > 280:
            return ""
        if any(b in out.lower() for b in ("api key", "secret", "password", "internal")):
            return ""
        return out
    except Exception:
        return ""


# ─── REPLY GENERATOR ─────────────────────────────────────────────────────
def draft_reply(customer_message, items, jiji_adverts):
    text = str(customer_message or "").strip()
    if not text:
        return PLACEHOLDER

    # 0) Owner / internal messages are handled upstream by the gate; here we only
    #    ever answer customers.

    # A) Intent (non-product) first
    intent = _intent_reply(text)
    if intent:
        return intent

    # B) Jiji product match
    matched_ad, j_score, did_you_mean = jiji_match(text, jiji_adverts)
    if matched_ad and j_score >= 0.7:
        title = matched_ad.get("title", "") if isinstance(matched_ad, dict) else matched_ad
        price = matched_ad.get("price_title") if isinstance(matched_ad, dict) else None
        region = matched_ad.get("region_name") if isinstance(matched_ad, dict) else None
        if price:
            loc = f" at {region}" if region else ""
            return (f'2Real Enterprises. We have "{title}"{loc}. '
                    f"Price: {price}. Message back to confirm availability and reserve.")
        return (f"2Real Enterprises. Yes, we list \"{title}\" on our Jiji shop. "
                "Message back for price and availability and I'll confirm stock for you.")

    # B) Zobaze product match
    matched = zobaze_match(text, items)
    if matched:
        price = float(matched.get("price", 0))
        stock = int(matched.get("stock", 0))
        variant = matched.get("variant", matched.get("name", "that item"))
        if stock > 0:
            return (f"2Real Enterprises. {variant} is available at GHS {price:,.0f}. "
                    f"We have {stock} in stock at Oyarifa. "
                    f"Payment: MoMo on delivery or cash. No credit. Want me to reserve it?")
        return (f"2Real Enterprises. {variant} is currently out of stock. "
                f"Price when restocked: GHS {price:,.0f}. I'll get back to you when it's back.")

    # C) Genuinely unmatched -> did-you-mean / opt-in LLM fallback
    if did_you_mean:
        names = [m.get("title", m) if isinstance(m, dict) else m for m in did_you_mean[:3]]
        return ("Not quite sure which one you mean — do you mean: "
                + ", ".join(f'"{n}"' for n in names) + "? Reply with the one you want.")

    if ENABLE_LLM_FALLBACK:
        llm = llm_fallback_reply(text)
        if llm:
            return llm

    # D) Safe final line (friendlier than the old dead-end, still safe)
    return ("Thanks for your message. I've noted it — I'll confirm and get back to you "
            "shortly with the details.")


# ─── LOG INTERACTION ─────────────────────────────────────────────────────
def log_interaction(customer_msg, reply, channel="whatsapp"):
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
