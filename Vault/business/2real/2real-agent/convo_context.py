# convo_context.py — conversational-context layer for the 2Real responder.
# ========================================================================
# WHY: the matcher (jiji_zobaze_responder.draft_reply) is STATELESS — it sees
# only the customer's latest message and matches it cold against the whole
# catalog. When H asks "8, 10 or 12mm staples?" and the customer replies "10",
# the system gets just "10" with no memory that the conversation is about
# staples, so it returns irrelevant items containing "10".
#
# This layer gives the matcher per-chat memory: what item is on the table and
# what follow-up question was asked, so a terse answer ("10", "12mm", "blue",
# "bigger") is resolved AGAINST the prior item instead of matched cold.
#
# Design: pure helpers, no network, deterministic (free, deepseek hands tier).
# Usage (wire into draft_reply), per chat:
#   ctx = load_convo(chat_id)          # get stored state
#   resolved = resolve_message(raw, ctx)  # enrich terse follow-ups w/ context
#   reply = draft_reply(resolved, items, titles, ...)   # existing matcher
#   save_convo(chat_id, ctx)           # store updated state

import json, re, re as _re, time
from pathlib import Path

CONVO_PATH = Path(r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\whatsapp_convo_state.json")
TTL_SECONDS = 30 * 60  # 30 min of context freshness
MAX_HISTORY = 12       # turns kept per chat

# Follow-up reply signals: words/units that mark a terse answer conveying
# SIZE / SPEC / CHOICE about the item already on the table.
_SIZE_UNIT = r"(mm|mm\b|cm|cm\b|inch|inches|in\b|ml|litre|litres|l\b|kg|g\b|w\b|watt|watts|v\b|volt|volts|ah\b|amp|amps|gb\b|tb\b|mhz|hz)"
_BARE = r"^\d{1,3}$"                     # "10", "12"
_SPECIFIED = r"^\d{1,4}(\.\d+)?\s*(" + _SIZE_UNIT + r")$"  # "10mm", "12 mm"


def _norm(text):
    if not text:
        return ""
    return re.sub(r"\s+", " ", str(text).lower().strip())


# Phrases that carry no product identity — drop when deriving the current item
# from a customer query (keeps 'staple' from 'do you have staples for sale').
_FILLER = r"\b(do|you|have|has|got|any|for|sale|sell|i|we|need|want|looking|price|how|much|is|are|there|pls|please|ok|thanks|thank|a|an|the|of|to)\b"


def _product_noun(query):
    """Extract the (mostly) product noun(s) from a customer query so a terse
    follow-up can be rebuilt as '<item> <answer>'. E.g. 'do you have staples for
    sale' -> 'staple'."""
    t = _norm(query)
    t = re.sub(_FILLER, " ", t)
    words = [w for w in t.split() if len(w) > 1]
    # keep the tail (product words come last in typical queries)
    keep = words[-3:] if words else [t]
    return " ".join(keep).strip()


def is_terse_followup(raw, item=None):
    """True if 'raw' looks like an answer to a follow-up question rather than a
    fresh product query: a bare number or a number+unit. Optionally gated on a
    size question being pending for the given item."""
    t = _norm(raw)
    if not t:
        return False
    if re.match(_BARE, t):
        return True
    if re.match(_SPECIFIED, t):
        return True
    # size/colour words without a number ("blue", "bigger") — only if an item is live
    if item and re.match(r"^(blue|red|green|black|white|large|big|small|long|short|medium|bigger|smaller)$", t):
        return True
    return False


def pending_size_question(text):
    """Does the seller's last message convey a size/spec CHOICE that expects a
    terse customer answer? Triggered by a size unit OR words like size/colour/
    which/what, regardless of a '?' (real WhatsApp messages often omit it, e.g.
    \"do you want sized staples 8 10 or 12mm\")."""
    if not text:
        return False
    t = _norm(text)
    # a size/spec marker, or a selecting word near the end
    if re.search(r"(size|mm\b|cm\b|inch|milli|ml\b|watt|w\b|volt|v\b|ah\b|gb\b|colour|color|which|what)", t):
        # only if the message is SHORT and mostly numbers/units/choice words
        # (a long product-ingredient message must not linger as a pending question)
        return len(t) <= 90
    return False


def _inherit_unit(seller_msg, answer):
    """If the seller's question carried a unit (e.g. 'mm') and the customer's
    bare answer is just a number ('10'), attach that unit so the matcher hits the
    exact size ('staple 10mm') instead of any title containing '10'."""
    if not re.match(_BARE, answer):
        return answer
    t = _norm(seller_msg or "")
    m = re.search(r"(\d*\s*(mm|cm|inch|inches|ml|litre|litres|l|kg|watt|w|volt|v|ah|gb|hz|mhz))\b", t)
    if m:
        unit = m.group(2).strip()
        # no space: keep it ONE token so '10mm' doesn't split into '10' + 'mm'
        # (a bare '10' would substring-match '1000pcs' — wrong).
        return f"{answer}{unit}"
    return answer


def resolve_message(raw, ctx):
    """
    Return (resolved_text, meta) where resolved_text is what should be fed to the
    matcher, and meta explains what happened.

    Rules:
    1. If the incoming message is a terse follow-up AND there is a live item in
       context with a size question pending, rebuild the query as
       "<item> <answer>" so the matcher finds the RIGHT listing (e.g. item
       'staples' + answer '10' -> 'staples 10mm' when the seller's question used mm).
    2. Otherwise if it's a terse follow-up but no live item, keep as-is (the
       matcher's quality gate already refuses vague single words).
    3. Otherwise (normal product query) pass through unchanged.
    """
    raw = str(raw or "").strip()
    if not raw:
        return "", {"kind": "empty"}
    item = (ctx or {}).get("current_item", "") or ""
    pending = bool((ctx or {}).get("size_question_pending"))
    if is_terse_followup(raw, item) and pending and item:
        answer = _inherit_unit((ctx or {}).get("last_seller_msg", ""), _norm(raw))
        rebuilt = f"{item} {answer}"
        return rebuilt, {"kind": "resolved", "item": item, "answer": answer,
                         "rebuilt": rebuilt}
    if is_terse_followup(raw) and not item:
        return raw, {"kind": "terse_no_context", "answer": _norm(raw)}
    return raw, {"kind": "pass_through"}


def _load_all():
    if not CONVO_PATH.exists():
        return {}
    try:
        return json.loads(CONVO_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _save_all(data):
    CONVO_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")


def _chat_bucket(chat_id):
    return f"chat::{chat_id}"


def load_convo(chat_id):
    d = _load_all().get(_chat_bucket(chat_id)) or {}
    if not d:
        return {"history": [], "current_item": "", "size_question_pending": False, "ts": time.time()}
    # expire after TTL
    if time.time() - d.get("ts", 0) > TTL_SECONDS:
        return {"history": [], "current_item": "", "size_question_pending": False, "ts": time.time()}
    return d


def save_convo(chat_id, ctx):
    d = _load_all()
    d[_chat_bucket(chat_id)] = ctx
    # prune stale chats
    now = time.time()
    for k in list(d):
        if isinstance(d[k], dict) and now - d[k].get("ts", 0) > 48 * 3600:
            del d[k]
    _save_all(d)


def update_context(chat_id, seller_msg="", customer_msg="", reply="", current_item=""):
    """
    Record a turn. Key responsibilities:
      - 'current_item' (the item actively being discussed) is set explicitly when
        the caller knows it; otherwise we try to derive it from the last chat's
        customer product query in history.
      - Whether a size question is pending: derived from the seller's last message.
    Returns the updated ctx.
    """
    ctx = load_convo(chat_id)
    hist = ctx.get("history", [])
    turn = {"from": "seller", "text": seller_msg, "at": time.time()}
    if customer_msg:
        turn = {"from": "customer", "text": customer_msg, "at": time.time()}
    hist.append(turn)
    hist = hist[-MAX_HISTORY:]

    if current_item:
        ctx["current_item"] = current_item
    else:
        # derive current item: last customer product query that wasn't a terse answer
        for t_rev in reversed(hist):
            if t_rev["from"] == "customer" and t_rev["text"] and not is_terse_followup(t_rev["text"]):
                ctx["current_item"] = _product_noun(t_rev["text"])
                break

    # Only (re)set the size-question-pending flag from a seller message when one is
    # actually present. A customer-only turn must NOT clear a pending question the
    # seller just asked (previously: draft_reply's seller_msg="" wiped it to False,
    # so "10" never resolved against the item).
    if seller_msg and seller_msg.strip():
        ctx["size_question_pending"] = pending_size_question(seller_msg)
        ctx["last_seller_msg"] = seller_msg  # keep for unit inheritance ("mm")
    ctx["history"] = hist
    ctx["ts"] = time.time()
    save_convo(chat_id, ctx)
    return ctx


if __name__ == "__main__":
    # quick self-test mirroring H's real case:
    # H asks "do you want sized staples — 8, 10 or 12mm?" ; customer replies "10"
    ctx = {"current_item": "staple", "size_question_pending": True, "history": [], "ts": time.time()}
    resolved, meta = resolve_message("10", ctx)
    print(f"IN : '10'   (ctx staples, size q pending)")
    print(f"OUT: '{resolved}'  meta={meta['kind']}  => feeds matcher 'staple 10'")

    # no context -> stays terse (matcher quality gate will refuse / stay quiet)
    resolved2, meta2 = resolve_message("10", {"current_item": "", "size_question_pending": False})
    print(f"IN : '10'   (no context)")
    print(f"OUT: '{resolved2}'  meta={meta2['kind']}")

    # normal fresh product query passes through
    resolved3, meta3 = resolve_message("i want a wireless mouse", {})
    print(f"IN : 'i want a wireless mouse'")
    print(f"OUT: '{resolved3}'  meta={meta3['kind']}")