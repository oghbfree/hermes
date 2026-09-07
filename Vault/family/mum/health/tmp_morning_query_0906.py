import json, urllib.request, re, sys
from pathlib import Path
from datetime import datetime, timezone, timedelta

env_path = Path.home() / '.hermes' / '.env'
token = None
with open(env_path, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if 'TELEGRAM_BOT_TOKEN' in line and '=' in line:
            token = line.split('=', 1)[1].strip().strip('"').strip("'")
            break
if not token:
    print('ERROR: token not found'); sys.exit(1)

url = f'https://api.telegram.org/bot{token}/getUpdates?timeout=10'
try:
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read().decode('utf-8'))
except Exception as e:
    print(f'API request failed: {e}'); sys.exit(1)

if not result.get('ok'):
    print('API error:', result); sys.exit(1)

updates = result.get('result', [])
print(f'Total updates: {len(updates)}')
chat_id = '-1003784520976'
topic_id = 4
relevant = []
for upd in updates:
    msg = upd.get('message', {}) or upd.get('channel_post', {}) or upd.get('edited_message', {})
    if msg:
        if str(msg.get('chat', {}).get('id','')) == chat_id and msg.get('message_thread_id') == topic_id:
            relevant.append(msg)
print(f'Messages in topic 4: {len(relevant)}')
ghana = timezone(timedelta(hours=0))
today = datetime.now(ghana).strftime('%Y-%m-%d')
print(f'Today (Ghana): {today}')
for msg in relevant:
    from_user = msg.get('from',{}).get('first_name','Unknown')
    text = msg.get('text', msg.get('caption','(no text)'))
    mt = datetime.fromtimestamp(msg.get('date',0), tz=ghana)
    md = mt.strftime('%Y-%m-%d')
    mark = ' [TODAY]' if md==today else ''
    print(f'\n[{md} {mt.strftime("%H:%M")}]{mark} {from_user} (id={msg.get("from",{}).get("id","?")}, msg={msg.get("message_id","?")}):')
    print(text[:800])
    print('-'*40)