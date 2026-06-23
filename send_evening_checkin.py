import json, urllib.request, os

env_path = os.path.join(os.path.expanduser("~"), ".hermes", ".env")
token = None
with open(env_path, "r", encoding="utf-8") as f:
    for line in f:
        if "TELEGRAM_BOT_TOKEN" in line and "=" in line:
            token = line.strip().split("=", 1)[1].strip()
            break

message = (
    "🫂 Evening care check-in for Comfort Blankson (Mum)\n\n"
    "A few quick updates please:\n\n"
    "1. Dinner — has she eaten? What did she have?\n"
    "2. Evening medications — have they been taken?\n"
    "3. Any pain, discomfort, or issues we should know about?\n"
    "4. Energy and mood — how does she seem this evening?\n"
    "5. Overall day summary — how was today for her?\n\n"
    "Thank you 🌙"
)

payload = json.dumps({
    "chat_id": "-1003784520976",
    "message_thread_id": "4",
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
except urllib.error.HTTPError as e:
    print(json.dumps({
        "ok": False,
        "error_code": e.code,
        "description": e.read().decode("utf-8", errors="replace")
    }, ensure_ascii=False, indent=2))
