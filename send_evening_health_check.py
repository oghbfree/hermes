import json, urllib.request, os

env_path = os.path.join(os.path.expanduser("~"), ".hermes", ".env")
token = None
with open(env_path, "r", encoding="utf-8") as f:
    for line in f:
        if "TELEGRAM_BOT_TOKEN" in line and "=" in line:
            token = line.strip().split("=", 1)[1].strip()
            break

if not token:
    print("ERROR: Token not found")
    exit(1)

message = """🌙 Evening Health Check

Hey H, winding down for the day?

Please log:
• 🍽️ Dinner — have you eaten? What did you have?
• ☕ Drinks — what have you had today?
• 🩺 Symptoms — any aches, pains, or issues?
• ⚡ Energy — how are you feeling out of 10?
• 😴 Sleep — how did you sleep last night?

Rest well! 🌙"""

payload = json.dumps({
    "chat_id": "-1003784520976",
    "message_thread_id": 2,
    "text": message
}, ensure_ascii=False).encode("utf-8")

url = f"https://api.telegram.org/bot{token}/sendMessage"
req = urllib.request.Request(url, data=payload, headers={
    "Content-Type": "application/json; charset=utf-8"
}, method="POST")

try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        result = json.loads(resp.read().decode("utf-8"))
        print(json.dumps(result, ensure_ascii=False, indent=2))
except Exception as e:
    print(f"ERROR: {e}")
