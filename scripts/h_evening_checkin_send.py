import json, urllib.request, sys
from pathlib import Path

env_path = Path.home() / '.hermes' / '.env'
token = None
with open(env_path, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if 'TELEGRAM_BOT_TOKEN' in line and '=' in line:
            token = line.split('=', 1)[1].strip().strip('"').strip("'")
            break

if not token:
    print("ERROR: TELEGRAM_BOT_TOKEN not found")
    sys.exit(1)

chat_id = '-1003784520976'
message_thread_id = 2  # Health Log topic

text = (
    "\U0001F319 Evening Health Check\n\n"
    "Evening H — hope the day went well!\n\n"
    "Quick end-of-day log:\n"
    "\u2022 \U0001F37D\uFE0F **Dinner** — what did you have?\n"
    "\u2022 \U0001FA7A **Symptoms today** — anything to note?\n"
    "\u2022 \u26A1 **Energy out of 10?**\n"
    "\u2022 \U0001F634 **How was your sleep last night?**\n\n"
    "Rest well! \U0001F6CC"
)

url = 'https://api.telegram.org/bot' + token + '/sendMessage'
payload = json.dumps({
    'chat_id': chat_id,
    'message_thread_id': message_thread_id,
    'text': text
}, ensure_ascii=False).encode('utf-8')

req = urllib.request.Request(url, data=payload, headers={
    'Content-Type': 'application/json; charset=utf-8'
}, method='POST')

try:
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read().decode('utf-8'))
        if result.get('ok'):
            print('SUCCESS: message_id=' + str(result['result']['message_id']))
        else:
            print('FAILED: ' + str(result.get('description', result)))
            sys.exit(1)
except Exception as e:
    print('ERROR: ' + str(e))
    sys.exit(1)