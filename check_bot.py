import json, urllib.request, sys
from pathlib import Path

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

print('Token loaded:', token[:8] + '...')

# Check bot info
url = 'https://api.telegram.org/bot' + token + '/getMe'
req = urllib.request.Request(url)
with urllib.request.urlopen(req, timeout=15) as resp:
    info = json.loads(resp.read().decode('utf-8'))
print('BOT INFO:')
print(json.dumps(info, indent=2, ensure_ascii=False)[:800])

# getUpdates
print('\n--- getUpdates ---')
url2 = 'https://api.telegram.org/bot' + token + '/getUpdates?timeout=5'
req2 = urllib.request.Request(url2)
with urllib.request.urlopen(req2, timeout=20) as resp2:
    updates_result = json.loads(resp2.read().decode('utf-8'))

print('ok:', updates_result.get('ok'))
print('result count:', len(updates_result.get('result', [])))
if not updates_result.get('ok'):
    print('Description:', updates_result.get('description', ''))
