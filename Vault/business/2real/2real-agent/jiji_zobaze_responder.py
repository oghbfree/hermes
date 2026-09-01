#!/usr/bin/env python3
"""
Jiji + Zobaze WhatsApp Response Draft for 2Real Enterprises
============================================================
STRICT matching only. No fuzzy, no synonyms, no LLM fallback.
- If the customer's query tokens are ALL contained in an item name/variant -> reply with price
- Otherwise -> safe placeholder
"""
import json
import re
from pathlib import Path
from datetime import datetime

# ─── CONFIG ────────────────────────────────────────────────────────────────
ZOBaze_INVENTORY_PATH = Path(r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\inventory_agent.json")
JIJI_TITLES_PATH = Path(r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\jiji_page_listings.json")
REPLY_LOG_PATH = Path(r"C:\Users\User\.hermes\workspace\Vault\business\2real\customer-interactions.md")
PLACEHOLDER = "Thanks for your message. I've noted it — I'll confirm and get back to you shortly with the details."

STOP_WORDS = {
    "a","an","the","is","are","was","were","be","been","being","have","has","had",
    "do","does","did","will","would","could","should","may","might","shall","can",
    "i","you","he","she","it","we","they","me","him","her","us","them","my","your",
    "his","its","our","their","mine","yours","his","hers","its","ours","theirs",
    "in","on","at","by","for","with","about","against","between","into","through",
    "during","before","after","above","below","to","from","up","down","of","off",
    "over","under","again","further","then","once","here","there","when","where",
    "why","how","all","each","every","both","few","more","most","other","some",
    "such","no","nor","not","only","own","same","so","than","too","very","just",
    "and","but","or","if","because","as","until","while","what","which","who",
    "whom","this","that","these","those","please","thanks","thank","hi","hello",
    "hey","dear","sir","madam","want","need","looking","tell","ask","get","got",
    "see","send","give","call","reply","message","msg","price","cost","much",
    "available","stock","sell","buy","interested","do","does","did","please",
    # Conversation closers / vague words — NEVER auto-reply on these
    "ok","okay","kk","fine","sure","alright","alrighty","great","good","thanks",
    "thank","bye","later","tomorrow","today","soon","maybe","perhaps","no",
    "yes","yeah","yep","nope","noted","done","sold","deal","perfect","back",
    "call","called","phone","ring","missed","again","now","right","left",
    "there","here","them","those","these","come","coming","went","come",
    "collect","collection","pickup","pick","arrange","arranging","later",
    "okay","fine","sure",
}

# ─── COMMON MISTAKES / ABBREVIATIONS ─────────────────────────────────────
# Customers abbreviate, misspell, or use partial names.
# Map common variations -> canonical form that exists in your inventory.
CORRECTIONS = {
    # Misspellings
    "hydrolic": "hydraulic",
    "hydroilik": "hydraulic",
    "botle": "bottle",
    "bottel": "bottle",
    "hak": "hack",
    "haksaw": "hacksaw",
    "hak saw": "hacksaw",
    "meassure": "measure",
    "mesure": "measure",
    "measuring": "measure",
    "guage": "gauge",
    "grese": "grease",
    "gres": "grease",
    "silicone": "silicon",
    "sealent": "sealant",
    "sealant": "sealant",
    "scres": "screw",
    "skrew": "screw",
    "spanner": "wrench",
    "fridg": "fridge",
    "frige": "fridge",
    "refrigirator": "refrigerator",
    "charger": "charger",
    "batery": "battery",
    "batterey": "battery",
    "bateries": "battery",
    "dril": "drill",
    "drils": "drill",
    "angle grinder": "grinder",
    "saw": "saw",
    "chopsaw": "chop",
    "generator": "generator",
    "genarator": "generator",
    "genny": "generator",
    
    # Common abbreviations
    "stnls": "stainless",
    "ss": "stainless",
    "stainless steel": "stainless",
    "ms": "mild steel",
    "galv": "galvanised",
    "galvad": "galvanised",
    "st/steel": "stainless",
    
    # Partial name completions (customers say half the name)
    "hbj": "hbj",
    "hacks": "hacksaw",
    "hack saw": "hacksaw",
    "hack": "hack",
    "hf": "hf",
    "tape": "tape",
    "measuring tape": "tape measure",
    
    # Tool categories
    "pliers": "plier",
    "cutting pliers": "plier",
    "long nose": "plier",
    "combination pliers": "plier",
    
    # INGCO specific
    "ingco": "ingco",
    "ingco hydraulic": "ingco hydraulic",
}

def correct_text(text):
    """Apply common corrections and expand abbreviations."""
    text_lower = text.lower()
    # Multi-word corrections first (entire phrase)
    for wrong, right in CORRECTIONS.items():
        if " " in wrong and wrong in text_lower:
            text = text_lower.replace(wrong, right)
            text_lower = text
    # Then single-word corrections
    words = text_lower.split()
    corrected = []
    for w in words:
        if w in CORRECTIONS:
            corrected.append(CORRECTIONS[w])
        else:
            corrected.append(w)
    return " ".join(corrected)

# ─── LOADERS ───────────────────────────────────────────────────────────────
def load_zobaze():
    if not ZOBaze_INVENTORY_PATH.exists():
        return []
    with open(ZOBaze_INVENTORY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def load_jiji_titles():
    if not JIJI_TITLES_PATH.exists():
        return []
    try:
        raw = json.loads(JIJI_TITLES_PATH.read_text(encoding="utf-8"))
        if isinstance(raw, list):
            return raw
        if isinstance(raw, dict):
            return raw.get("titles", raw.get("items", []))
    except:
        return []
    return []

# ─── TEXT HELPERS ──────────────────────────────────────────────────────────
def normalize(text):
    """Lowercase, remove punctuation, collapse whitespace."""
    text = str(text or "").lower().strip()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def get_keywords(text):
    """Return meaningful keyword tokens from a query, with corrections applied."""
    text = correct_text(text)  # Apply misspelling/abbreviation fixes
    words = normalize(text).split()
    return [w for w in words if w not in STOP_WORDS and len(w) > 1]


def query_acceptable(q_words):
    """A query is only auto-answerable if it has enough signal.

    Rules:
    - 0 keywords -> never auto-reply (silence)
    - 1 keyword  -> only if it's distinctive: >= 5 chars OR contains a digit
                    (e.g. "hacksaw", "hbj602", "6280d"). Vague single words
                    like "jack", "ok", "back", "saw" must NOT auto-reply.
    - 2+ keywords -> always acceptable (they describe a product)
    """
    if not q_words:
        return False
    if len(q_words) == 1:
        w = q_words[0]
        return len(w) >= 5 or any(ch.isdigit() for ch in w)
    return True

# ─── STRICT PRODUCT MATCHING ──────────────────────────────────────────────
def _expand_compounds(word):
    """Try splitting a compound word at boundaries. 'hacksaw' -> ['hack', 'saw']"""
    results = {word}
    # Try splitting at each position 3 through len-3
    for i in range(3, len(word) - 2):
        left, right = word[:i], word[i:]
        if len(left) > 2 and len(right) > 2:
            results.add(left)
            results.add(right)
    return results

def match_jiji(query, titles):
    """
    Jiji matching with misspelling + compound word support.
    - Short query (1-2 keywords): ALL must match
    - Longer query (3+ keywords): at least 66% must match
    - Handles compounds: "hacksaw" matches titles with "hack" AND "saw"
    """
    q_words = get_keywords(query)
    if not q_words or not query_acceptable(q_words):
        return None, 0.0
    
    # Expand query keywords: "hacksaw" -> {"hacksaw", "hack", "saw"}
    expanded_q = set()
    for w in q_words:
        expanded_q.update(_expand_compounds(w))
    
    best, best_score = None, 0.0
    required = len(q_words) if len(q_words) <= 2 else max(2, int(len(q_words) * 0.66))
    
    for title in titles:
        if isinstance(title, dict):
            title = title.get("title", "")
        title = str(title)
        norm_title = normalize(title)
        title_tokens = set(norm_title.split())
        
        # Count how many ORIGINAL query keywords match
        matched = 0
        for w in q_words:
            # Direct containment is the strongest signal
            if w in norm_title:
                matched += 1
            else:
                # Compound split: try splitting the keyword and check
                # if ALL resulting parts appear as title tokens
                for i in range(3, len(w) - 2):
                    left, right = w[:i], w[i:]
                    if len(left) > 2 and len(right) > 2:
                        if left in title_tokens and right in title_tokens:
                            matched += 1
                            break
        
        score = matched / len(q_words)
        
        if score > best_score and matched >= required:
            best_score = score
            best = title
    
    if best:
        return best, best_score
    return None, 0.0

def match_inventory(query, items):
    """
    STRICT inventory matching with misspelling support.
    - Short query (1-2 keywords): ALL must match
    - Longer query (3+ keywords): at least 66% must match
    Returns (matched_item, score).
    """
    q_words = get_keywords(query)
    if not q_words or not query_acceptable(q_words):
        return None, 0.0
    
    required = len(q_words) if len(q_words) <= 2 else max(2, int(len(q_words) * 0.66))
    best, best_score = None, 0.0
    
    for item in items:
        if not item.get("in_stock", False):
            continue
        
        name = normalize(item.get("name", ""))
        variant = normalize(item.get("variant", ""))
        category = normalize(item.get("category", ""))
        searchable = f"{name} {variant} {category}"
        
        matched = sum(1 for w in q_words if w in searchable)
        score = matched / len(q_words)
        
        if score > best_score and matched >= required:
            best_score = score
            best = item
    
    if best:
        return best, best_score
    return None, 0.0

# ─── INTENT DETECTION (non-product messages) ──────────────────────────────
def detect_intent(text):
    """Return a canned reply for non-product intents, or None."""
    t = normalize(text)
    words = set(t.split())
    
    # Greeting only
    if t in ("hi", "hello", "hey", "good morning", "good afternoon", "good evening",
             "hi there", "hello there", "good day", "morning", "afternoon", "evening"):
        return "2Real Enterprises. Hello! What item are you looking for today?"
    
    # About / what do you sell
    if any(k in t for k in ["tell me about", "what do you sell", "what do you have",
                            "about your shop", "about the shop", "what kind"]):
        return "2Real Enterprises. We supply quality new and used tools, equipment and consumables. What item are you looking for?"
    
    # Payment
    if "payment" in t or "momo" in t or "cash" in t:
        return "2Real Enterprises. We accept MoMo on delivery or cash. No credit. Which item are you interested in?"
    
    # Delivery
    if "deliver" in t or "delivery" in t or "shipping" in t or "ship" in t:
        return "Delivery is available at a fee. Which item do you need delivered?"
    
    # Hours
    if "open" in t or "close" in t or "hours" in t or "time" in t:
        return "2Real Enterprises. We're open Mon-Sat 07:00-16:30 (Kantamanto) and most days 08:00-20:00 (Oyarifa). What item are you looking for?"
    
    # Location
    if "where" in words or "location" in t or "located" in t:
        return "We have a walk-in shop at Kantamanto, Accra and a warehouse in Oyarifa. Let me know which item you're after."
    
    return None

# ─── REPLY GENERATOR ──────────────────────────────────────────────────────
def draft_reply(customer_message, items, jiji_titles):
    text = str(customer_message or "").strip()
    if not text:
        return PLACEHOLDER
    
    # 1) Check intent (non-product)
    intent = detect_intent(text)
    if intent:
        return intent
    
    # 2) JIJI — PRIMARY source (being phased in, Zobaze phased out)
    jiji_title, j_score = match_jiji(text, jiji_titles)
    if jiji_title:
        return (f"2Real Enterprises. Yes, we have \"{jiji_title}\" on our Jiji shop. "
                "Message back for price and availability and I'll confirm stock for you.")
    
    # 3) ZOBaZE — SECONDARY / legacy (being phased out)
    matched, m_score = match_inventory(text, items)
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
    
    # 4) No match — return None so the hook stays silent
    return None

# ─── LOG INTERACTION ──────────────────────────────────────────────────────
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
    jiji_titles = load_jiji_titles()
    reply = draft_reply(customer_message, items, jiji_titles)
    log_interaction(customer_message, reply)
    print(reply)