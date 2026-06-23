import json, urllib.request, os

# Read token from .env
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

message = """🌙 Good Evening, Robert!

Just checking in with you tonight — hope you've had a good day. 💙

🍽️ Evening meal — Have you had dinner? What did you have? Had enough to drink today?

💊 Medications — Did you take all your medicines today, no issues?

🚶 Mobility & activity — How were you getting about today? Any walks or exercises?

😊 Energy & mood — How's your energy been? Feeling in good spirits?

🤕 Any pain or discomfort — Anything bothering you we should know about?

📋 Overall — How are you feeling tonight?

No rush at all — reply whenever you're comfortable. We're here for you. 💙"""

payload = json.dumps({
    "chat_id": "-1003784520976",
    "message_thread_id": 1,
    "text": message
}, ensure_ascii=False).encode("utf-8")

url = f"https://api.telegram.org/bot{token}/sendMessage"
req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json; charset=utf-8"}, method="POST")
with urllib.request.urlopen(req, timeout=15) as resp:
    result = json.loads(resp.read().decode("utf-8"))
    print(json.dumps(result, ensure_ascii=False, indent=2))
