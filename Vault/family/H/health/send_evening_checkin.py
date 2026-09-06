import json, urllib.request, os, sys

env_path = os.path.expanduser("~/.hermes/.env")
token = None
with open(env_path, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line.startswith('TELEGRAM_BOT_TOKEN='):
            token = line.split('=', 1)[1].strip()
            if token.startswith('"') and token.endswith('"'):
                token = token[1:-1]
            elif token.startswith("'") and token.endswith("'"):
                token = token[1:-1]
            break

if not token:
    print("NO TOKEN")
    sys.exit(2)

chat_id = '-1003784520976'
message_thread_id = 2

text = """🌙 Evening Health Check

Evening H — hope the day went well!

Quick end-of-day log:
• 🍽️ Dinner — what did you have?
• 🩺 Symptoms today — anything to note?
• ⚡ Energy out of 10?
• 😴 How was your sleep last night?

Rest well! 🛌"""

url = f'https://api.telegram.org/bot{token}/sendMessage'
payload = json.dumps({
    'chat_id': chat_id,
    'message_thread_id': message_thread_id,
    'text': text
}, ensure_ascii=False).encode('utf-8')

req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json; charset=utf-8'}, method='POST')
try:
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read().decode('utf-8'))
        if not result.get('ok'):
            print(f'FAILED: {result.get("description", result)}')
            sys.exit(1)
        else:
            print(f'SENT message_id={result["result"]["message_id"]}')
except Exception as e:
    print(f'ERROR: {e}')
    sys.exit(1)