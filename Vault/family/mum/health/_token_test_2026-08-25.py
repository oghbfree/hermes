#!/usr/bin/env python3
import json, re, sys, urllib.request
from pathlib import Path

env_path = Path.home() / '.hermes' / '.env'
token = None
try:
    content = env_path.read_text(encoding='utf-8')
    m = re.search(r'^TELEGRAM_BOT_TOKEN=(.+)$', content, re.MULTILINE)
    if m:
        token = m.group(1).strip()
except Exception as e:
    print(f'ERROR reading .env: {e}')
    sys.exit(2)

if not token:
    print('ERROR: TELEGRAM_BOT_TOKEN not found in .env')
    sys.exit(1)

# getMe to validate token (do not print token)
url = f'https://api.telegram.org/bot{token}/getMe'
try:
    req = urllib.request.Request(url, method='GET')
    with urllib.request.urlopen(req, timeout=15) as resp:
        result = json.loads(resp.read().decode('utf-8'))
    if result.get('ok'):
        bot = result['result']
        print(f'✅ Token VALID. Bot: @{bot.get("username")} (id {bot.get("id")})')
    else:
        print(f'❌ getMe error: {result.get("description")}')
        sys.exit(1)
except Exception as e:
    print(f'❌ Error calling getMe: {e}')
    sys.exit(1)