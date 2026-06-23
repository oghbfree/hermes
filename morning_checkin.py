import json, urllib.request, os

# Read token
env_path = os.path.join(os.path.expanduser("~"), ".hermes", ".env")
token = None
with open(env_path, "r", encoding="utf-8") as f:
    for line in f:
        if line.strip().startswith("TELEGRAM_BOT_TOKEN="):
            token = line.strip().split("=", 1)[1].strip()
            break

if not token:
    print("ERROR: token not found")
    exit(1)

message = """Good morning, Comfort! 🌅 It's your morning check-in. How are you doing today?

🍳 Breakfast — Have you eaten yet? What did you have?
💊 Medications — Did you take your morning pills?
🤕 Any pain, discomfort, or issues to report?
😊 Energy & mood — How are you feeling this morning?
🚶 Mobility — Any changes in how you're moving around?

Take your time and let us know how you're doing. We're here for you! 💛"""

payload = json.dumps({
    "chat_id": "-1003784520976",
    "message_thread_id": 4,
    "text": message
}, ensure_ascii=False).encode("utf-8")

url = f"https://api.telegram.org/bot{token}/sendMessage"
req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json; charset=utf-8"}, method="POST")
with urllib.request.urlopen(req, timeout=15) as resp:
    result = json.loads(resp.read().decode("utf-8"))
    print(json.dumps(result, ensure_ascii=False, indent=2))
