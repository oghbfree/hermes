import os, json, urllib.request, sys
from pathlib import Path

env_path = Path.home() / '.hermes' / '.env'
token = None
if env_path.exists():
    try:
        with open(env_path, 'r', encoding='utf-8') as f:
            data = f.read()
        for line in data.replace('\r\n', '\n').replace('\r', '\n').split('\n'):
            line = line.strip()
            if line.startswith('TELEGRAM_BOT_TOKEN='):
                token = line.split('=', 1)[1].strip()
                break
    except Exception as e:
        print('ERROR reading .env:', e); sys.exit(1)

if not token:
    print('ERROR: TELEGRAM_BOT_TOKEN not found'); sys.exit(1)

chat_id = '-1003784520976'
message_thread_id = 4  # Mum Health topic (topic 4)

message = (
    "Afternoon check-in — Mum (Comfort Blankson), 12/09/26.\n\n"
    "Please update on the following:\n"
    "• Lunch — what did she eat, and did she finish it?\n"
    "• Afternoon medication — was the Furosemide 20mg given this afternoon (BP before dosing)?\n"
    "• Pain / discomfort — any back, hip, neck or new pain since this morning? (Checking after yesterday's fall.)\n"
    "• Energy / mood — how is she feeling this afternoon?\n"
    "• Any incidents since the morning report (falls, dizziness, unusual symptoms, refusal of care)?\n\n"
    "Thanks."
)

if len(message) > 4000:
    message = message[:4000] + '\n\n... (truncated)'

url = 'https://api.telegram.org/bot{}/sendMessage'.format(token)
payload = json.dumps({
    'chat_id': chat_id,
    'message_thread_id': message_thread_id,
    'text': message,
    'parse_mode': 'Markdown'
}, ensure_ascii=False).encode('utf-8')

req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json; charset=utf-8'}, method='POST')
try:
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read().decode('utf-8'))
        if result.get('ok'):
            print('SUCCESS: msg_id={}'.format(result['result']['message_id']))
        else:
            print('FAILED: {}'.format(result.get('description', result))); sys.exit(1)
except urllib.error.HTTPError as e:
    print('HTTP Error: {} {}'.format(e.code, e.read().decode('utf-8'))); sys.exit(1)
except Exception as e:
    print('ERROR: {}'.format(e)); sys.exit(1)