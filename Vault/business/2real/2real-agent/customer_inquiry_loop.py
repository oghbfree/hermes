#!/usr/bin/env python3
"""
2Real Enterprises — Customer Inquiry Processing Loop
====================================================
Runs every 10 minutes via cron. Scans customer interactions for
unresolved inquiries, flags SLA breaches, and tracks pending items.

Loop engineering: Discover → Assign → Act → Verify → Persist

The WhatsApp gateway hook handles auto-replies for KNOWN items.
This loop handles the BACKLOG — items that got placeholders, 
pending follow-ups, SLA breaches, and team coordination.
"""
import json
import re
import os
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

# ─── PATHS ──────────────────────────────────────────────────────────────────
WORKSPACE = Path(r"C:\Users\User\.hermes\workspace\Vault\business\2real")
AGENT_DIR = WORKSPACE / "2real-agent"
INTERACTIONS_LOG = WORKSPACE / "customer-interactions.md"
INVENTORY_FILE = AGENT_DIR / "inventory_agent.json"
LEADS_FILE = AGENT_DIR / "customer_leads.json"
SOURCING_LOG = AGENT_DIR / "sourcing_log.json"
LOOP_STATE = AGENT_DIR / "loop_state.json"

PLACEHOLDER = "We will get back to you shortly."

# ─── HELPERS ────────────────────────────────────────────────────────────────

def load_inventory():
    if not INVENTORY_FILE.exists():
        return []
    with open(INVENTORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def load_leads():
    if not LEADS_FILE.exists():
        return []
    with open(LEADS_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_leads(leads):
    with open(LEADS_FILE, "w", encoding="utf-8") as f:
        json.dump(leads, f, indent=2, ensure_ascii=False)

def load_state():
    if not LOOP_STATE.exists():
        return {"last_processed_line": 0, "processed_hashes": []}
    with open(LOOP_STATE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {"last_processed_line": 0, "processed_hashes": []}

def save_state(state):
    with open(LOOP_STATE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

def item_in_inventory(query, inventory):
    """Check if a query item exists in inventory (simple token match)."""
    q = re.sub(r"[^a-z0-9\s]", "", query.lower().strip())
    q_words = set(q.split())
    stop_words = {"tell", "me", "about", "the", "a", "an", "is", "are", "do", 
                  "does", "did", "can", "you", "your", "please", "thanks", "hi",
                  "hello", "hey", "want", "have", "has", "had", "price", "much",
                  "how", "show", "see", "send", "give", "call", "reply", "message"}
    q_tokens = q_words - stop_words
    if not q_tokens:
        return None
    
    best, best_score = None, 0
    for item in inventory:
        name = re.sub(r"[^a-z0-9\s]", "", item.get("name", "").lower())
        variant = re.sub(r"[^a-z0-9\s]", "", item.get("variant", "").lower())
        cat = re.sub(r"[^a-z0-9\s]", "", item.get("category", "").lower())
        blob = set(f"{name} {variant} {cat}".split())
        overlap = len(q_tokens & blob)
        score = overlap / max(len(q_tokens), 1)
        if score > best_score and score >= 0.4:
            best_score = score
            best = item
    return best

def parse_interactions(text):
    """Parse customer-interactions.md into structured entries."""
    entries = []
    current = {}
    lines = text.split("\n")
    
    for line in lines:
        m_date = re.match(r"##\s+(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2})", line)
        if m_date:
            if current:
                entries.append(current)
            current = {"timestamp": m_date.group(1), "channel": "whatsapp", "customer": "", "reply": ""}
            continue
        m_chan = re.match(r"-\s+\*\*Channel:\*\*\s+(.+)", line)
        if m_chan and current:
            current["channel"] = m_chan.group(1).strip()
        m_cust = re.match(r"-\s+\*\*Customer:\*\*\s+(.+)", line)
        if m_cust and current:
            current["customer"] = m_cust.group(1).strip()
        m_reply = re.match(r"-\s+\*\*Reply:\*\*\s+(.+)", line)
        if m_reply and current:
            current["reply"] = m_reply.group(1).strip()
    
    if current:
        entries.append(current)
    return entries

# ─── CORE PROCESSING ────────────────────────────────────────────────────────

def process_inquiry(entry, inventory, leads):
    """Process a single inquiry entry and return actions needed."""
    customer_msg = entry.get("customer", "")
    reply_sent = entry.get("reply", "")
    timestamp = entry.get("timestamp", "")
    
    # Skip if already processed
    entry_hash = f"{timestamp}|{customer_msg}"
    
    try:
        entry_time = datetime.strptime(timestamp, "%Y-%m-%d %H:%M")
    except ValueError:
        entry_time = datetime.now()
    
    now = datetime.now()
    age_hours = (now - entry_time).total_seconds() / 3600
    
    result = {
        "hash": entry_hash,
        "timestamp": timestamp,
        "customer_msg": customer_msg,
        "reply_sent": reply_sent,
        "age_hours": round(age_hours, 1),
        "status": "resolved",
        "action": None,
        "note": ""
    }
    
    # Case 1: Auto-matched (has real reply, not placeholder)
    if reply_sent and reply_sent != PLACEHOLDER and reply_sent != "We will get back to you shortly.":
        result["status"] = "auto_resolved"
        result["note"] = f"Auto-replied with item details"
        return result
    
    # Case 2: Got placeholder — unresolved
    if reply_sent == PLACEHOLDER or reply_sent == "We will get back to you shortly.":
        inventory_match = item_in_inventory(customer_msg, inventory)
        
        if inventory_match:
            price = float(inventory_match.get("price", 0))
            stock = int(inventory_match.get("stock", 0))
            name = inventory_match.get("name", "Unknown")
            
            if stock > 0:
                result["status"] = "stock_found_but_missed"
                result["action"] = "SEND_REPLY"
                result["match"] = {
                    "name": name,
                    "price": price,
                    "stock": stock,
                    "variant": inventory_match.get("variant", ""),
                }
                result["note"] = f"{name} IS in stock at GHS {price:,.0f} — hook missed it. MANUAL REPLY NEEDED."
                result["priority"] = "HIGH"
            else:
                result["status"] = "out_of_stock"
                result["action"] = "SOURCE"
                result["match"] = {
                    "name": name,
                    "price": price,
                    "stock": 0,
                    "cost": inventory_match.get("cost", 0),
                }
                result["note"] = f"{name} is out of stock. Needs UK sourcing or supplier check."
                result["priority"] = "MEDIUM"
        else:
            result["status"] = "unknown_item"
            result["action"] = "TEAM_CHECK"
            result["note"] = "Item not in inventory. Team needs to verify if we can source it."
            result["priority"] = "LOW" if age_hours < 4 else "HIGH"
        
        # SLA breach check
        if age_hours > 24:
            result["note"] += f" ⚠️ SLA BREACH — {age_hours:.0f} hours since inquiry!"
            result["priority"] = "CRITICAL"
    
    return result

def main():
    print(f"=== 2Real Customer Inquiry Loop === {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    inventory = load_inventory()
    leads = load_leads()
    state = load_state()
    
    if not INTERACTIONS_LOG.exists():
        print(f"❌ Interactions log not found at {INTERACTIONS_LOG}")
        return
    
    text = INTERACTIONS_LOG.read_text(encoding="utf-8")
    entries = parse_interactions(text)
    
    if not entries:
        print("No interaction entries found.")
        return
    
    print(f"📊 Processing {len(entries)} total interaction entries\n")
    
    # Process all entries (check for items needing attention)
    results = []
    new_leads = []
    
    for entry in entries:
        result = process_inquiry(entry, inventory, leads)
        results.append(result)
        
        # Track unresolved in leads
        if result["status"] != "auto_resolved":
            existing = [l for l in leads if l.get("customer_msg") == result["customer_msg"]]
            if not existing:
                new_lead = {
                    "timestamp": result["timestamp"],
                    "customer_msg": result["customer_msg"],
                    "reply_sent": result["reply_sent"],
                    "status": result["status"],
                    "age_hours": result["age_hours"],
                    "priority": result.get("priority", "LOW"),
                    "last_checked": datetime.now().isoformat(),
                    "checked_count": 1,
                }
                if "match" in result:
                    new_lead["match"] = result["match"]
                new_leads.append(new_lead)
    
    # ─── SUMMARY ──────────────────────────────────────────────────────────
    auto_resolved = [r for r in results if r["status"] == "auto_resolved"]
    stock_found = [r for r in results if r["status"] == "stock_found_but_missed"]
    out_of_stock = [r for r in results if r["status"] == "out_of_stock"]
    unknown = [r for r in results if r["status"] == "unknown_item"]
    critical = [r for r in results if r.get("priority") == "CRITICAL"]
    high = [r for r in results if r.get("priority") == "HIGH"]
    
    # Update leads file with new entries
    if new_leads:
        leads.extend(new_leads)
        save_leads(leads)
        print(f"📝 Added {len(new_leads)} new leads to customer_leads.json")
    
    # Print summary
    print(f"✅ Auto-resolved: {len(auto_resolved)}")
    print(f"🔴 Stock exists but hook didn't match: {len(stock_found)}")
    print(f"🟡 Out of stock (needs sourcing): {len(out_of_stock)}")
    print(f"⚪ Unknown items (team check): {len(unknown)}")
    print(f"⚠️  SLA breaches (>24h): {len(critical)}\n")
    
    # Print actionable items
    if stock_found:
        print("═══ 🚨 ITEMS IN STOCK — MISSED BY HOOK ═══")
        for r in stock_found[:5]:
            m = r.get("match", {})
            print(f"  [{r['timestamp']}] {m.get('name','?')} — GHS {m.get('price',0):,.0f} ({m.get('stock',0)} in stock)")
            print(f"  Customer said: \"{r['customer_msg'][:60]}\"")
            print(f"  🎯 Reply: \"2Real Enterprises. {m.get('variant',m.get('name',''))} is available at GHS {m.get('price',0):,.0f}. We have {m.get('stock',0)} in stock at Oyarifa. Payment: MoMo on delivery or cash. No credit. Want me to reserve it?\"")
            print()
    
    if critical:
        print("═══ 🔴 CRITICAL SLA BREACHES ═══")
        for r in critical[:3]:
            print(f"  [{r['timestamp']}] {r['age_hours']:.0f}h pending — \"{r['customer_msg'][:60]}\"")
            print(f"  Action: {r['action']}")
            print()
    
    if high and not stock_found:
        print("═══ 🟡 HIGH PRIORITY ═══")
        for r in high[:3]:
            print(f"  [{r['timestamp']}] \"{r['customer_msg'][:60]}\"")
            print(f"  Action: {r['action']}")
            print()
    
    # Update state
    state["last_run"] = datetime.now().isoformat()
    state["total_entries"] = len(entries)
    state["unresolved"] = len(stock_found) + len(out_of_stock) + len(unknown)
    state["critical"] = len(critical)
    save_state(state)
    
    print(f"---\n🏁 Loop complete. Next run checks for new entries.")

if __name__ == "__main__":
    main()