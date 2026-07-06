import json, urllib.request, sys, os, re
from pathlib import Path
from datetime import datetime, timezone, timedelta

env_path = Path.home() / '.hermes' / '.env'
token = None
with open(env_path, 'r', encoding='utf-8') as f:
    content = f.read()
    m = re.search(r'^TELEGRAM_BOT_TOKEN=(.+)$', content, re.MULTILINE)
    if m:
        token = m.group(1).strip()

if not token:
    print('ERROR: No token found')
    sys.exit(1)

print('Token loaded: ' + token[:8] + '...')

# getUpdates with offset=-50 to get recent messages
url = 'https://api.telegram.org/bot' + token + '/getUpdates?offset=-50&timeout=10'
req = urllib.request.Request(url)
try:
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read().decode('utf-8'))
except Exception as e:
    print('Request failed: ' + str(e))
    sys.exit(1)

if not result.get('ok'):
    print('API error: ' + str(result))
    sys.exit(1)

updates = result.get('result', [])
print('Total updates returned: ' + str(len(updates)))

chat_id = '-1003784520976'
topic_id = 4

relevant = []
for upd in updates:
    msg = upd.get('message', {})
    if msg:
        msg_chat_id = str(msg.get('chat', {}).get('id', ''))
        msg_thread_id = msg.get('message_thread_id')
        if msg_chat_id == chat_id and msg_thread_id == topic_id:
            relevant.append(msg)

print('')
print('Messages in chat ' + chat_id + ', topic ' + str(topic_id) + ': ' + str(len(relevant)))

# Ghana timezone is UTC+0
ghana_tz = timezone(timedelta(hours=0))
today_str = datetime.now(ghana_tz).strftime('%Y-%m-%d')

print('Today (Ghana): ' + today_str)
print('=' * 60)

today_messages = []
for msg in relevant:
    from_user = msg.get('from', {}).get('first_name', 'Unknown')
    from_id = msg.get('from', {}).get('id', '?')
    text = msg.get('text', msg.get('caption', '(no text)'))
    date_unix = msg.get('date', 0)
    msg_id = msg.get('message_id', '?')
    
    msg_time = datetime.fromtimestamp(date_unix, tz=ghana_tz)
    msg_date = msg_time.strftime('%Y-%m-%d')
    msg_time_str = msg_time.strftime('%H:%M')
    
    is_today = (msg_date == today_str)
    marker = ' [TODAY]' if is_today else ''
    
    print('')
    print('[' + msg_date + ' ' + msg_time_str + ']' + marker + ' ' + from_user + ' (id=' + str(from_id) + ', msg=' + str(msg_id) + '):')
    print(text[:500])
    print('-' * 40)
    
    if is_today:
        today_messages.append(msg)

print('')
print('=== SUMMARY ===')
print('Total messages in topic 4: ' + str(len(relevant)))
print('Messages from today (' + today_str + '): ' + str(len(today_messages)))

# Check if any today's message looks like a morning care report
for msg in today_messages:
    text = msg.get('text', '').lower()
    from_user = msg.get('from', {}).get('first_name', 'Unknown')
    report_keywords = ['bp', 'blood pressure', 'pulse', 'temperature', 'temp', 'medication', 'vitals', 'reading', 'morning']
    found = [kw for kw in report_keywords if kw in text]
    if found:
        print('')
        print('>>> CARE REPORT DETECTED from ' + from_user)
        print('    Matched keywords: ' + str(found))
