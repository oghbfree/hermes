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
INVENTORY_FILE = BASE / "inventory_agent.json"
LEADS_FILE = BASE / "customer_leads.json"
INTERACTIONS_FILE = BASE.parent / "customer-interactions.md"
SIP_LOG_FILE = BASE / "phone_call_log.json"

# ─── INVENTORY MATCHING ────────────────────────────────────────────────────
def load_inventory():
    if not INVENTORY_FILE.exists():
        return []
    with open(INVENTORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

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

# ─── WEBHOOK HANDLER ────────────────────────────────────────────────────────
def handle_webhook(transcript, summary="", customer_number="", caller_name=""):
    """
    Entry point. Called by the AI voice agent via webhook when a call ends.
    
    Expected input:
        transcript: full text of the call
        summary: AI-generated summary (what customer wanted)
        customer_number: caller's phone number (if available)
        caller_name: caller's name if captured
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
    
    # Generate team message
    team_msg_lines = [
        f"📞 Phone Inquiry - {caller_name or customer_number or 'Unknown'}",
        f"📋 {summary or 'No summary'}",
    ]
    
    if matches:
        team_msg_lines.append("")
        team_msg_lines.append("📦 Matched Inventory:")
        for score, item in matches[:3]:
            stock_status = f"{item.get('stock')} in stock" if int(item.get("stock",0)) > 0 else "OUT OF STOCK"
            price = float(item.get("price",0))
            name = item.get("name","?")
            team_msg_lines.append(f"  • {name} — GHS {price:,.0f} ({stock_status})")
    
    team_msg_lines.append("")
    if action == "IN_STOCK":
        team_msg_lines.append("✅ IN STOCK — Ready to quote customer")
    elif action == "SOURCE":
        team_msg_lines.append("🔍 OUT OF STOCK — John to source UK comparables")
    else:
        team_msg_lines.append("❓ NOT IN SYSTEM — Team to check if we can source")
    
    team_msg_lines.append(f"Call ID: {call_id}")
    
    print("=== TEAM MESSAGE ===")
    print("\n".join(team_msg_lines))
    print("=== END ===")
    
    return {
        "call_id": call_id,
        "action_needed": action,
        "matches": [m[1].get("name") for m in matches],
        "team_message": "\n".join(team_msg_lines)
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