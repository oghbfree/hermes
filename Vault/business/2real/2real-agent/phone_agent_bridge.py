"""
2Real Enterprises — Phone Call Integration Layer
================================================
Bridge between AI voice agents (Retell AI / Africa's Talking) 
and the existing 2Real WhatsApp + inventory system.

When a call comes in:
1. AI answers and handles conversation
2. Webhook POSTs the transcript + summary here
3. This script processes it:
   - Checks inventory for items mentioned
   - Determines action needed (in stock / source / team check)
   - Logs to customer_leads.json
   - Generates a WhatsApp-ready message for the team group
"""

import json
import os
import sys
import hashlib
from pathlib import Path
from datetime import datetime

# ─── PATHS ──────────────────────────────────────────────────────────────────
BASE = Path(r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent")
# JIJI is the source of truth (NOT Zobaze/inventory_agent.json, which is stale June data).
# The live Jiji scraper output holds all current listings with real prices/stock.
INVENTORY_FILE = BASE / "jiji_listings_full.json"   # source of truth (dict: {count, scraped, items})
LEADS_FILE = BASE / "customer_leads.json"
INTERACTIONS_FILE = BASE.parent / "customer-interactions.md"
SIP_LOG_FILE = BASE / "phone_call_log.json"

# ─── INVENTORY MATCHING ────────────────────────────────────────────────────
def load_inventory():
    """Load from Jiji (source of truth). jiji_listings_full.json is {count, scraped, items: [...]}.
    Normalise to a list of items with name/variant/category/price/stock fields."""
    if not INVENTORY_FILE.exists():
        return []
    with open(INVENTORY_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    items = data.get("items", []) if isinstance(data, dict) else data
    out = []
    for it in items or []:
        if not isinstance(it, dict):
            continue
        # Jiji fields vary; map to the searchable shape
        name = it.get("title") or it.get("name") or it.get("subject") or ""
        price = it.get("price") or it.get("price_value") or 0
        try:
            price = float(str(price).replace(",", "").replace("GH₵", "").strip() or 0)
        except (ValueError, TypeError):
            price = 0.0
        out.append({
            "name": name,
            "variant": it.get("variant", ""),
            "category": it.get("category", ""),
            "price": price,
            "stock": int(it.get("stock", 1) or 1),   # Jiji listing = offered; treat as in-stock unless noted
            "url": it.get("url", ""),
            "jiji_id": it.get("jiji_id") or it.get("id"),
        })
    return out

def search_inventory(query, inventory):
    """Fuzzy match query words against inventory items."""
    import re
    q = re.sub(r"[^a-z0-9\s]", "", query.lower().strip())
    q_words = set(q.split()) - {"the","a","an","is","are","do","does","did",
        "can","you","your","please","thanks","hi","hello","hey","want","have",
        "got","get","looking","need","price","much","how","much","cost","tell",
        "about","for","and","or","but","not","some","any","all","this","that"}
    if not q_words:
        return []
    
    results = []
    for item in inventory:
        name = re.sub(r"[^a-z0-9\s]", "", (item.get("name","") or "").lower())
        variant = re.sub(r"[^a-z0-9\s]", "", (item.get("variant","") or "").lower())
        cat = re.sub(r"[^a-z0-9\s]", "", (item.get("category","") or "").lower())
        blob = set(f"{name} {variant} {cat}".split())
        overlap = len(q_words & blob)
        score = overlap / max(len(q_words), 1)
        if score >= 0.4:
            results.append((score, item))
    
    results.sort(key=lambda x: -x[0])
    return results[:3]

# ─── LOGGING ────────────────────────────────────────────────────────────────
def log_call(transcript, summary, items_found, action_needed, customer_number=None):
    """Log a phone call interaction."""
    calls = []
    if SIP_LOG_FILE.exists():
        with open(SIP_LOG_FILE, "r", encoding="utf-8") as f:
            try: calls = json.load(f)
            except: calls = []
    
    entry = {
        "timestamp": datetime.now().isoformat(),
        "customer_number": customer_number or "unknown",
        "transcript": transcript[:2000],  # truncated for storage
        "summary": summary,
        "items_found": items_found,
        "action_needed": action_needed,
        "call_id": hashlib.md5(f"{datetime.now()}{transcript[:100]}".encode()).hexdigest()[:12]
    }
    calls.append(entry)
    calls = calls[-500:]  # keep last 500
    with open(SIP_LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(calls, f, indent=2)
    
    return entry["call_id"]

# ─── WHATSAPP LEAD LOGGING ─────────────────────────────────────────────────
def log_lead(customer_number, message, items, call_id):
    """Add a lead entry from a phone call."""
    leads = []
    if LEADS_FILE.exists():
        with open(LEADS_FILE, "r", encoding="utf-8") as f:
            try: leads = json.load(f)
            except: leads = []
    
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "source": "phone_call",
        "customer_number": customer_number,
        "customer_msg": message[:200],
        "matched_items": [{"name": i[1].get("name"), "price": i[1].get("price"), "stock": i[1].get("stock")} for i in items],
        "call_id": call_id,
        "status": "pending",
        "priority": "HIGH" if items else "MEDIUM"
    }
    leads.append(entry)
    with open(LEADS_FILE, "w", encoding="utf-8") as f:
        json.dump(leads, f, indent=2)

# ─── TICKET HELPERS ─────────────────────────────────────────────────────────
def _extract_items(summary, matches):
    """Best-effort: the matched item names, else the first line of the summary."""
    if matches:
        return " + ".join(str(m[1].get("name", "?")).strip() for m in matches[:3])
    # fallback: first meaningful sentence of the summary
    s = (summary or "").strip().split("\n")[0][:120]
    return s or "(item not captured — ask for it)"

def _PAYMENT_RULE(delivery_type):
    """Anti-loss payment rule — own riders vs Yango/Uber (H's policy, 19/10/26)."""
    if delivery_type == "OUR_RIDERS":
        return "💵 PAY: OK to collect payment on delivery (customer pays our rider before release)."
    return "💵 PAY: CUSTOMER MUST PAY H FIRST (MoMo preferred) BEFORE dispatch — Yango/Uber rider is NOT trusted to collect on delivery."

# ─── WEBHOOK HANDLER ────────────────────────────────────────────────────────
def handle_webhook(transcript, summary="", customer_number="", caller_name="", location="", delivery_type="APP_RIDER"):
    """
    Entry point. Called by the AI voice agent via webhook when a call ends.
    
    Expected input:
        transcript: full text of the call
        summary: AI-generated summary (what customer wanted)
        customer_number: caller's phone number (if available)
        caller_name: caller's name if captured
        location: customer's drop-off landmark (if captured) — always ask
        delivery_type: 'OUR_RIDERS' (trusted, pay-on-delivery OK) or 'APP_RIDER' (Yango/Uber, pay-before only). Default APP_RIDER = safest.
    """
    inventory = load_inventory()
    
    # Search transcript AND summary separately, take best match
    trans_matches = search_inventory(transcript, inventory)
    summ_matches = search_inventory(summary, inventory) if summary else []
    
    trans_best = trans_matches[0] if trans_matches else (0, None)
    summ_best = summ_matches[0] if summ_matches else (0, None)
    
    matches = trans_matches
    if summ_best[0] > trans_best[0]:
        matches = summ_matches
    
    # Determine action needed
    if matches:
        best = matches[0][1]
        stock = int(best.get("stock", 0))
        if stock > 0:
            action = "IN_STOCK"
        else:
            action = "SOURCE"
    else:
        action = "TEAM_CHECK"
    
    # Log
    call_id = log_call(transcript, summary, [m[1].get("name") for m in matches], action, customer_number)
    log_lead(customer_number or "unknown", summary or transcript[:200], matches, call_id)
    
    # Build the JOHN ACTION TICKET (the WhatsApp task sent to John to execute).
    # Format per H (19/10/26): "customer wants X, location is X, WhatsApp contact X — need to fulfil."
    # Always includes the dispatch/payment rule + the deliver-type so John packs right.
    ticket_lines = [
        "🔨 JOHN — ACTION TICKET (fulfil this order)",
        f"👤 Customer: {caller_name or customer_number or 'caller'}" ,
        f"📞 Customer WhatsApp: {customer_number or '(ask for number)'}",
        f"📦 Customer wants: {_extract_items(summary or transcript, matches)}",
        f"📍 Customer location: {location or '(ASK — nearest Accra/Tema landmark, not just town)'}",
        f"🚚 Delivery: {delivery_type}",
    ]
    ticket_lines.append("")
    ticket_lines.append("✅ YOUR JOB: pick + pack this item, organise the delivery, meet the customer/rider on handover.")
    ticket_lines.append("🧾 Organise + label as part of your standard duties.")
    if action == "IN_STOCK":
        ticket_lines.append("🟢 IN STOCK on Jiji — pack from shelf.")
    elif action == "SOURCE":
        ticket_lines.append("🟠 NOT on Jiji — find/source UK comparable, then confirm price with H before quoting.")
    else:
        ticket_lines.append("⚪ Not matched to a listing — ask customer for the exact item, then confirm with H.")
    ticket_lines.append("")
    ticket_lines.append(_PAYMENT_RULE(delivery_type))
    ticket_lines.append(f"Call ID: {call_id}")
    
    print("=== JOHN ACTION TICKET ===")
    print("\n".join(ticket_lines))
    print("=== END ===")
    
    return {
        "call_id": call_id,
        "action_needed": action,
        "matches": [m[1].get("name") for m in matches],
        "team_message": "\n".join(ticket_lines)
    }

# ─── CLI ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Called with transcript as argument (test mode)
        transcript = " ".join(sys.argv[1:])
        result = handle_webhook(transcript, summary="Customer inquiry from phone call")
        print(json.dumps(result, indent=2))
    else:
        print("Usage: python phone_agent_bridge.py '<call transcript>'")
        print("  or: call handle_webhook() from your voice agent webhook")