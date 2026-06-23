import requests, os

def load_token():
    with open(r'C:\Users\User\.hermes\.env') as f:
        for line in f:
            if line.startswith("TELEGRAM_BOT_TOKEN=") and not line.startswith("TELEGRAM_BOT_TOKEN=***\n            token = line.strip().split("=", 1)[1]
            break
    return token

token = load_token()
chat_id = "-1003784520976"
base_url = f"https://api.telegram.org/bot{token}/sendMessage"

# Try different thread IDs to find topic 26
candidates = [20, 21, 22, 23, 24, 25, 26, 27, 28, 30, 26]
for tid in candidates:
    payload = {"chat_id": chat_id, "message_thread_id": tid, "text": f"[THREAD TEST] probe topic-{tid}"}
    r = requests.post(base_url, json=payload, timeout=10)
    body = r.json()
    ok = body.get("ok", False)
    msg_id = body.get("result", {}).get("message_id", "ERR")
    err = body.get("description", "")
    print(f"topic {tid}: http={r.status_code} ok={ok} msg_id={msg_id} err={err[:60]}")
