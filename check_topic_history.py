import json, urllib.request, sys
from pathlib import Path
from datetime import datetime, timezone, timedelta

env_path = Path.home() / '.hermes' / '.env'
token = None
with open(env_path, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line.startswith('TELEGRAM_BOT_TOKEN='):
            token = line[len('TELEGRAM_BOT_TOKEN='):]
            break

if not token:
    print('ERROR: No token')
    sys.exit(1)

chat_id = '-1003784520976'

# Try to get chat info
url = 'https://api.telegram.org/bot' + token + '/getChat'
payload = json.dumps({'chat_id': chat_id}).encode('utf-8')
req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'}, method='POST')
with urllib.request.urlopen(req, timeout=15) as resp:
    chat_info = json.loads(resp.read().decode('utf-8'))
print('CHAT INFO:')
print(json.dumps(chat_info, indent=2, ensure_ascii=False)[:1200])

# Try getUpdates with a wider net - positive offset=0 means get all unprocessed
print('\n\n--- getUpdates with offset=0 ---')
url2 = 'https://api.telegram.org/bot' + token + '/getUpdates?offset=0&timeout=5'
req2 = urllib.request.Request(url2)
with urllib.request.urlopen(req2, timeout=20) as resp2:
    result2 = json.loads(resp2.read().decode('utf-8'))
print('result count:', len(result2.get('result', [])))

# Check if there's a pending update file or offset stored somewhere
print('\n\n--- Checking for stored offsets ---')
hermes_dir = Path.home() / '.hermes'
for f in hermes_dir.rglob('*.json'):
    if 'offset' in f.name.lower() or 'update' in f.name.lower() or 'telegram' in f.name.lower():
        print('Found:', f)
        try:
            data = json.loads(f.read_text(encoding='utf-8'))
            print('  Content:', str(data)[:200])
        except:
            pass
