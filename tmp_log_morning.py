import json, datetime, os

entry = {
    "date": "2026-07-06 07:02",
    "channel": "telegram",
    "recipient": "Sammy (Kantamanto)",
    "recipient_phone": "0575252253",
    "type": "morning_business_inquiry",
    "status": "delivered",
    "reason": "WhatsApp bridge offline (state: fatal, error: whatsapp_not_paired, Day 66+). Fallback to Telegram via hermes send.",
    "message_drafted": "Good morning Sammy! Quick check-in for Monday: Store status, weekend sales, stock levels (1049 total, 665 in stock, 384 OOS, 480 low stock), customer issues, needs.",
    "inventory_summary": {
        "total_items": 1049,
        "in_stock": 665,
        "out_of_stock": 384,
        "low_stock": 480
    },
    "delivered": True,
    "delivered_at": "2026-07-06 07:02",
    "fallback_channel": "telegram",
    "fallback_target": "telegram:-1003784520976:20",
    "fallback_status": "delivered",
    "fallback_delivered_at": "2026-07-06 07:02",
    "notes": "WhatsApp bridge remains offline (Day 66+). Fallback message delivered to Telegram topic 20 via hermes send. Inventory: 1049 total, 665 in stock, 384 OOS, 480 low stock."
}

def append_log(path):
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = {"entries": []}
        if isinstance(data, dict) and "entries" in data:
            data["entries"].append(entry)
        elif isinstance(data, list):
            data.append(entry)
        else:
            data = [entry]
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Logged to {path}")
    except Exception as e:
        print(f"ERROR logging to {path}: {e}")

# Canonical Vault copy
vault_path = r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\morning_inquiry_log.json"
append_log(vault_path)

# Workspace sync copy
ws_path = r"C:\Users\User\.hermes\workspace\2real-agent\morning_inquiry_log.json"
append_log(ws_path)

# Human-readable log
human_path = r"C:\Users\User\.hermes\workspace\memory\logs\business_interactions.md"
human_entry = f"\n2026-07-06 07:02 | Sammy (Kantamanto) | morning_business_inquiry | telegram | delivered | WhatsApp offline (Day 66+) | Inventory: 1049/665/384/480"
try:
    os.makedirs(os.path.dirname(human_path), exist_ok=True)
    with open(human_path, "a", encoding="utf-8") as f:
        f.write(human_entry)
    print(f"Logged to {human_path}")
except Exception as e:
    print(f"ERROR logging to {human_path}: {e}")

print("ALL_LOGS_DONE")