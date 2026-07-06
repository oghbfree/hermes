import json, urllib.request, sys, os, re
from pathlib import Path
from datetime import datetime, timezone, timedelta

env_path = Path.home() / '.hermes' / '.env'
token = None
try:
    with open(env_path, 'r', encoding='utf-8') as f:
        content = f.read()
        m = re.search(r'^TELEGRAM_BOT_TOKEN=(.+)$', content, re.MULTILINE)
        if m:
            token = m.group(1).strip()
except Exception as e:
    print('ERROR reading token:', e)
    sys.exit(1)

if not token:
    print('ERROR: No token found')
    sys.exit(1)

print('Token loaded: ' + token[:8] + '...')

chat_id = '-1003784520976'
topic_id = 4
text = """Evening check-in for Mum:
• Dinner — have you eaten? What?
• Evening medications taken?
• Any pain, discomfort, or issues?
• Energy and mood?
• Overall day summary — how was today?"""

url = f'https://api.telegram.org/bot{token}/sendMessage'
data = json.dumps({
    'chat_id': chat_id,
    'message_thread_id': topic_id,
    'text': text
}).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        result = json.loads(resp.read().decode('utf-8'))
        if result.get('ok'):
            print('Message sent successfully. Message ID:', result['result']['message_id'])
        else:
            print('API error:', result)
except Exception as e:
    print('Request failed:', e)
    sys.exit(1)