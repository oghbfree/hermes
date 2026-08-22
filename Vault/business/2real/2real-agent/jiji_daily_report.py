#!/usr/bin/env python3
"""
2Real — Jiji Daily Performance Report Generator
================================================
Stores daily metrics and compares day-over-day changes.
Data is collected by the cron job agent via browser tool.

Also reads customer-interactions.md to show what customers
are enquiring about most — helps decide what stock to order.
"""
import json
import re
import os
from pathlib import Path
from datetime import datetime
from collections import Counter

BASE = Path(r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent")
HISTORY_FILE = BASE / "jiji_daily_history.json"
INTERACTIONS_FILE = BASE.parent / "customer-interactions.md"
INVENTORY_FILE = BASE / "inventory_agent.json"
INQUIRY_TRENDS_FILE = BASE / "inquiry_trends.json"

# ─── INQUIRY ANALYSIS ──────────────────────────────────────────────────────

def load_inventory():
    if not INVENTORY_FILE.exists():
        return []
    with open(INVENTORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def load_interactions():
    if not INTERACTIONS_FILE.exists():
        return []
    text = INTERACTIONS_FILE.read_text(encoding="utf-8", errors="ignore")
    entries = []
    current = {}
    for line in text.split("\n"):
        m_date = re.match(r"##\s+(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2})", line)
        if m_date:
            if current:
                entries.append(current)
            current = {"timestamp": m_date.group(1), "customer": "", "reply": ""}
            continue
        m_cust = re.match(r"-\s+\*\*Customer:\*\*\s+(.+)", line)
        if m_cust and current:
            current["customer"] = m_cust.group(1).strip()
        m_reply = re.match(r"-\s+\*\*Reply:\*\*\s+(.+)", line)
        if m_reply and current:
            current["reply"] = m_reply.group(1).strip()
    if current:
        entries.append(current)
    return entries

def extract_items(text):
    text = text.lower().strip()
    stop_words = {"the","a","an","is","are","do","does","did","can","could",
                  "would","should","will","shall","may","might","you","your",
                  "please","thanks","hi","hello","hey","there","want","have",
                  "got","get","looking","need","price","much","how","much",
                  "cost","tell","me","about","for","and","or","but","not",
                  "some","any","all","this","that","i","we","my","our","its",
                  "it","to","of","in","on","at","by","with","from","as","into",
                  "through","during","before","after","above","below","between",
                  "out","off","over","under","again","further","then","once",
                  "here","there","when","where","why","which","who","whom",
                  "what","has","had","do","does","did","doing","say","says",
                  "just","very","too","also","if","then","than","no","yes",
                  "know","see","buy","sell","stock","available","have","can"}
    words = re.findall(r"[a-z0-9]+", text)
    return [w for w in words if len(w) > 2 and w not in stop_words]

def match_to_inventory(item_words, inventory):
    matches = []
    for item in inventory:
        name = re.sub(r"[^a-z0-9\s]", "", (item.get("name","") or "").lower())
        variant = re.sub(r"[^a-z0-9\s]", "", (item.get("variant","") or "").lower())
        cat = re.sub(r"[^a-z0-9\s]", "", (item.get("category","") or "").lower())
        blob = f"{name} {variant} {cat}"
        overlap = sum(1 for w in item_words if w in blob)
        if overlap >= 1:
            score = overlap / max(len(item_words), 1)
            matches.append({
                "score": score,
                "name": item.get("name",""),
                "variant": item.get("variant",""),
                "price": item.get("price",0),
                "stock": item.get("stock",0),
                "in_stock": item.get("in_stock", False)
            })
    matches.sort(key=lambda x: -x["score"])
    return matches[:3]

def get_customer_request_trends():
    inventory = load_inventory()
    entries = load_interactions()
    if not entries:
        return {}
    
    all_keywords = []
    placeholder_replies = {"we will get back to you shortly", "we'll get back to you shortly"}
    
    for e in entries:
        msg = e.get("customer", "")
        reply = e.get("reply", "").lower().strip()
        is_unresolved = reply in placeholder_replies or reply == ""
        words = extract_items(msg)
        all_keywords.append({
            "message": msg,
            "words": words,
            "unresolved": is_unresolved,
            "timestamp": e.get("timestamp", ""),
            "reply": e.get("reply", "")
        })
    
    word_counts = Counter()
    for k in all_keywords:
        for w in set(k["words"]):
            word_counts[w] += 1
    
    matched_items = []
    unknown_requests = []
    
    for k in all_keywords:
        if k["unresolved"] and k["words"]:
            matches = match_to_inventory(k["words"], inventory)
            if matches:
                matched_items.append({
                    "message": k["message"],
                    "timestamp": k["timestamp"],
                    "best_match": matches[0]
                })
            else:
                unknown_requests.append({
                    "message": k["message"],
                    "timestamp": k["timestamp"]
                })
    
    stock_found_but_unreplied = {}
    for m in matched_items:
        name = m["best_match"]["name"]
        if name not in stock_found_but_unreplied:
            stock_found_but_unreplied[name] = {
                "name": name,
                "variant": m["best_match"]["variant"],
                "price": m["best_match"]["price"],
                "stock": m["best_match"]["stock"],
                "count": 0
            }
        stock_found_but_unreplied[name]["count"] += 1
    
    unknown_keywords = Counter()
    for u in unknown_requests:
        for w in extract_items(u["message"]):
            unknown_keywords[w] += 1
    
    top_unknown = [{"keyword": w, "count": c} for w, c in unknown_keywords.most_common(10) if c >= 2]
    
    return {
        "total_inquiries": len(entries),
        "unresolved_count": sum(1 for k in all_keywords if k["unresolved"]),
        "top_keywords": [{"word": w, "count": c} for w, c in word_counts.most_common(10)],
        "items_in_stock_missed": sorted(stock_found_but_unreplied.values(),
                                         key=lambda x: -x["count"])[:5],
        "items_customers_want_not_in_stock": top_unknown[:5],
        "unknown_count": len(unknown_requests)
    }

def save_inquiry_trends(trends):
    history = []
    if INQUIRY_TRENDS_FILE.exists():
        try:
            with open(INQUIRY_TRENDS_FILE) as f:
                history = json.load(f)
        except:
            history = []
    today = datetime.now().strftime("%Y-%m-%d")
    entry = {"date": today, "trends": trends, "saved_at": datetime.now().isoformat()}
    for i, h in enumerate(history):
        if h.get("date") == today:
            history[i] = entry
            with open(INQUIRY_TRENDS_FILE, "w") as f:
                json.dump(history, f, indent=2)
            return
    history.append(entry)
    history = history[-90:]
    with open(INQUIRY_TRENDS_FILE, "w") as f:
        json.dump(history, f, indent=2)

# ─── EXISTING FUNCTIONS ────────────────────────────────────────────────────

def save_today(data):
    history = []
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE) as f:
                history = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            history = []
    today = datetime.now().strftime("%Y-%m-%d")
    for entry in history:
        if entry.get("date") == today:
            entry.update(data)
            entry["updated_at"] = datetime.now().isoformat()
            with open(HISTORY_FILE, "w") as f:
                json.dump(history, f, indent=2)
            return
    data["date"] = today
    data["saved_at"] = datetime.now().isoformat()
    history.append(data)
    history = history[-90:]
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

def get_yesterday():
    if not HISTORY_FILE.exists():
        return {}
    try:
        with open(HISTORY_FILE) as f:
            history = json.load(f)
        if len(history) >= 2:
            return history[-2]
        return {}
    except:
        return {}

def format_report(today_data):
    yesterday = get_yesterday()
    
    lines = [
        "\U0001f4ca *2REAL JIJI DAILY REPORT*",
        f"\U0001f4c5 {datetime.now().strftime('%A, %d %b %Y')}",
        "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500",
        "",
        "\U0001f4cc *Account Overview*",
    ]
    
    for key, label in [("active", "Active listings"), ("reviewing", "Reviewing"),
                       ("draft", "Drafts"), ("declined", "Declined"),
                       ("closed", "Closed"), ("followers", "Followers"),
                       ("feedback", "Feedback"), ("clients", "New clients")]:
        val = today_data.get(key)
        if val is not None:
            prev = yesterday.get(key)
            change = ""
            if prev is not None and prev != val:
                diff = int(val) - int(prev)
                if diff > 0:
                    change = f" \U0001f4c8 +{diff}"
                elif diff < 0:
                    change = f" \U0001f4c9 {diff}"
            lines.append(f"  \u2022 {label}: {val}{change}")
    
    if today_data.get("top_remaining"):
        lines.append("")
        lines.append(f"\u2b50 *TOP+ Credits Remaining:* {today_data['top_remaining']}")
        lines.append(f"\u23f3 Expires: {today_data.get('top_expires', 'N/A')}")
    
    if today_data.get("whatsapp_ads_active"):
        lines.append("")
        lines.append(f"\U0001f4f1 *WhatsApp Ads:* Active until {today_data.get('whatsapp_ads_until', 'N/A')}")
    
    top_items = today_data.get("top_items", [])
    if top_items:
        lines.append("")
        lines.append("\U0001f525 *Top Performing Items (by impressions):*")
        for i, item in enumerate(top_items[:5], 1):
            lines.append(f"  {i}. {item.get('name','?')} \u2014 GHS {item.get('price',0):,.0f}")
            lines.append(f"     \U0001f441 {item.get('impressions',0)} views | \U0001f464 {item.get('visitors',0)} visitors | \U0001f4ac {item.get('chats',0)} chats")
    
    # ─── CUSTOMER REQUEST TRENDS ───────────────────────────────────────
    trends = get_customer_request_trends()
    if trends:
        save_inquiry_trends(trends)
        
        lines.append("")
        lines.append("\U0001f4ac *Top Customer Requests (all time):*")
        
        missed = trends.get("items_in_stock_missed", [])
        if missed:
            lines.append("  \U0001f7e2 *In stock \u2014 missed by auto-reply:*")
            for m in missed[:3]:
                lines.append(f"     \u2022 {m['name']} {m.get('variant','')} \u2014 GHS {m.get('price',0):,.0f} ({m['count']}x asked, {m['stock']} in stock)")
        
        unknown = trends.get("items_customers_want_not_in_stock", [])
        if unknown:
            lines.append("  \U0001f7e1 *Not in inventory \u2014 consider ordering:*")
            for u in unknown[:3]:
                lines.append(f"     \u2022 \"{u['keyword']}\" \u2014 asked {u['count']} times")
        
        lines.append("")
        lines.append(f"  \U0001f4ca {trends['total_inquiries']} total inquiries | {trends['unresolved_count']} unresolved | {trends['unknown_count']} unknown items")
    
    attention = today_data.get("needs_attention", [])
    if attention:
        lines.append("")
        lines.append("\u26a0\ufe0f *Needs Attention:*")
        for item in attention[:3]:
            lines.append(f"  \u2022 {item}")
    
    actions = today_data.get("action_items", [])
    if actions:
        lines.append("")
        lines.append("\U0001f3af *Suggested Actions:*")
        for a in actions:
            lines.append(f"  \u2022 {a}")
    
    lines.append("")
    lines.append("\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500")
    
    return "\n".join(lines)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        history = []
        if HISTORY_FILE.exists():
            with open(HISTORY_FILE) as f:
                history = json.load(f)
        if history:
            last = history[-1]
            print(format_report(last))
        else:
            print("No Jiji data collected yet. Run the collection first.")
        sys.exit(0)
    
    try:
        data = json.loads(sys.argv[1])
        save_today(data)
        print(format_report(data))
    except (json.JSONDecodeError, IndexError):
        print("Usage: jiji_daily_report.py '<json_data>'")
        print("  or: echo '<json_data>' | jiji_daily_report.py")