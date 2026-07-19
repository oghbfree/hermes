import json
import urllib.request
import os

# Read token from .env
env_path = os.path.join(os.path.expanduser("~"), ".hermes", ".env")
token = None
with open(env_path, "r", encoding="utf-8") as f:
    for line in f:
        if "TELEGRAM_BOT_TOKEN" in line and "=" in line:
            token = line.strip().split("=", 1)[1].strip()
            break

if not token:
    print("ERROR: TELEGRAM_BOT_TOKEN not found in .env")
    exit(1)

# Read the report file
report_path = r"C:\Users\User\.hermes\cron\output\cron-status-report\2026-07-14_daily-cron-status.md"
with open(report_path, "r", encoding="utf-8") as f:
    content = f.read()

# Telegram limits messages to 4096 chars - use file upload for long reports
# We'll send as a document
url = f"https://api.telegram.org/bot{token}/sendDocument"

# Prepare multipart form data
import uuid
boundary = uuid.uuid4().hex

body = b""
body += f"--{boundary}\r\n".encode()
body += f'Content-Disposition: form-data; name="chat_id"\r\n\r\n-1003784520976\r\n'.encode()
body += f"--{boundary}\r\n".encode()
body += f'Content-Disposition: form-data; name="message_thread_id"\r\n\r\n28\r\n'.encode()
body += f"--{boundary}\r\n".encode()
body += f'Content-Disposition: form-data; name="document"; filename="daily-cron-status-2026-07-14.md"\r\n'.encode()
body += b"Content-Type: text/markdown\r\n\r\n"
body += content.encode("utf-8")
body += f"\r\n--{boundary}--\r\n".encode()

req = urllib.request.Request(
    url,
    data=body,
    headers={
        "Content-Type": f"multipart/form-data; boundary={boundary}",
    },
    method="POST"
)

try:
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read().decode("utf-8"))
        print(json.dumps(result, indent=2, ensure_ascii=False))
except Exception as e:
    print(f"ERROR: {e}")
    # Fallback: send as text message (truncated)
    text_url = f"https://api.telegram.org/bot{token}/sendMessage"
    fallback_text = "📊 **Daily Cron Status Report — 14 July 2026**\n\n" + content[:3500] + "\n\n... (truncated, full report saved to cron output)"
    payload = json.dumps({
        "chat_id": "-1003784520976",
        "message_thread_id": 28,
        "text": fallback_text,
        "parse_mode": "Markdown"
    }, ensure_ascii=False).encode("utf-8")
    req2 = urllib.request.Request(text_url, data=payload, headers={"Content-Type": "application/json; charset=utf-8"}, method="POST")
    with urllib.request.urlopen(req2, timeout=15) as resp:
        result = json.loads(resp.read().decode("utf-8"))
        print("Fallback send result:", json.dumps(result, indent=2, ensure_ascii=False))