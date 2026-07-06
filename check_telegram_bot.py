import json, urllib.request, sys, re
from pathlib import Path

env_path = Path.home() / '.hermes' / '.env'
token = None
with open(env_path, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line.startswith('TELEGRAM_BOT_TOKEN=***            token = line[len('TELEGRAM_BOT_TOKEN='):]
            break

if not token:
    print('ERROR: No token')
    sys.exit(1)

# Check bot info
url = 'https://api.telegram.org/bot' + token + '/getMe'
req = urllib.request.Request(url)
with urllib.request.urlopen(req, timeout=15) as resp:
    info = json.loads(resp.read().decode('utf-8'))
print('BOT INFO:')
print(json.dumps(info, indent=2, ensure_ascii=False)[:800])

# Now try getUpdates with different parameters
print('\n\n--- getUpdates (no offset) ---')
url2 = 'https://api.telegram.org/bot' + token + '/getUpdates?timeout=5'
req2 = urllib.request.Request(url2)
with urllib.request.urlopen(req2, timeout=20) as resp2:
    updates_result = json.loads(resp2.read().decode('utf-8'))

print('ok: ' + str(updates_result.get('ok')))
print('result count: ' + str(len(updates_result.get('result', []))))

if not updates_result.get('ok'):
    print('Description: ' + str(updates_result.get('description', '')))

# Try with allowed_updates specified
print('\n\n--- getUpdates (allowed_updates=message) ---')
url3 = 'https://api.telegram.org/bot' + token + '/getUpdates?timeout=5&allowed_updates=["message"]'
req3 = urllib.request.Request(url3)
with urllib.request.urlopen(req3, timeout=20) as resp3:
    updates_result2 = json.loads(resp3.read().decode('utf-8'))

print('result count: ' + str(len(updates_result2.get('result', []))))
