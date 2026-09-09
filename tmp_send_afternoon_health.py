import os, json, urllib.request, urllib.error

env_path = os.path.join(os.path.expanduser("~"), ".hermes", ".env")
token = None
with open(env_path, "r", encoding="utf-8") as f:
    for line in f:
        if line.strip().startswith("TELEGRAM_BOT_TOKEN="):
            token = line.strip().split("=", 1)[1].strip()
            break

if not token:
    print("NO_TOKEN")
    raise SystemExit(1)

text = (
    "\U0001F324\uFE0F Afternoon Health Check\n\n"
    "Hey H, how's the day going?\n\n"
    "Please log:\n"
    "\u2022 \U0001F37D\uFE0F Lunch \u2014 have you eaten? What did you have?\n"
    "\u2022 \u2615 Drinks \u2014 what have you had since morning?\n"
    "\u2022 \U0001FA7A Symptoms \u2014 any aches, pains, or issues?\n"
    "\u2022 \u26A1 Energy \u2014 how are you feeling out of 10?\n\n"
    "Keep going! \U0001F4AA"
)

payload = json.dumps({
    "chat_id": "-1003784520976",
    "message_thread_id": 2,
    "text": text
}, ensure_ascii=False).encode("utf-8")

url = f"https://api.telegram.org/bot{token}/sendMessage"
req = urllib.request.Request(
    url,
    data=payload,
    headers={"Content-Type": "application/json; charset=utf-8"},
    method="POST"
)
try:
    with urllib.request.urlopen(req, timeout=20) as resp:
        result = json.loads(resp.read().decode("utf-8"))
        if result.get("ok"):
            print("SENT", result["result"]["message_id"])
        else:
            print("FAIL", json.dumps(result))
except urllib.error.HTTPError as e:
    print("HTTP_ERROR", e.code, e.read().decode("utf-8"))
except Exception as e:
    print("ERROR", repr(e))