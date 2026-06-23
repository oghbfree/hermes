import json, urllib.request, os

# Read token from .env
env_path = os.path.join(os.path.expanduser("~"), ".hermes", ".env")
token = None
with open(env_path, "r", encoding="utf-8") as f:
    for line in f:
        if line.strip().startswith("TELEGRAM_BOT_TOKEN=***            token = line.strip().split("=", 1)[1].strip()
            break

if not token:
    print("ERROR: token not found")
    exit(1)

message = """\U0001f319 Evening Check-In — Comfort Blankson

Hi Mum! Just checking in with you this evening \U0001f49b

\U0001f37d\ufe0f Dinner — Have you eaten? What did you have?

\U0001f48a Medications — Did you take your evening pills?

\U0001f915 Any pain, discomfort, or issues we should know about?

\u26a1 Energy & Mood — How are you feeling right now?

\U0001f4cb Overall — How was your day today?

No rush — reply whenever you're comfortable. We're here for you. \U0001f499"""

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
