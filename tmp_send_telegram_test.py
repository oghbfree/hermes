import requests, json

with open(r'C:\Users\User\.hermes\.env') as f:
    for line in f:
        if line.startswith("TELEGRAM_BOT_TOKEN=***            token = line.strip().split("=", 1)[1]
            break

chat_id = "-1003784520976"
base_url = f"https://api.telegram.org/bot{token}/sendMessage"

# Test main chat
resp = requests.post(base_url, json={
    "chat_id": chat_id,
    "text": "[TEST] Content Review Report - Week 2026-06-23\nAttempting to confirm delivery channel."
}, timeout=15)
print("Main chat:", resp.status_code, resp.text[:200])
