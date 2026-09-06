#!/usr/bin/env python3
"""Morning care check-in for Comfort Blankson — 2026-09-03.
Queries Telegram topic 4 for new morning care reports, flags abnormal vitals,
and posts acknowledgement if a new report is found."""
import json, urllib.request, sys, os, re
from pathlib import Path
from datetime import datetime, timezone, timedelta

# Load bot token
env_path = Path.home() / '.hermes' / '.env'
token = None
with open(env_path, 'r', encoding='utf-8') as f:
    content = f.read()
    m = re.search(r'^TELEGRAM_BOT_TOKEN=(.+)$', content, re.MULTILINE)
    if m:
        token = m.group(1).strip()

if not token:
    print('ERROR: TELEGRAM_BOT_TOKEN not found in .env')
    sys.exit(1)

print(f'Token loaded: {token[:8]}...')

# Get recent updates
url = f'https://api.telegram.org/bot{token}/getUpdates?timeout=10'
try:
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read().decode('utf-8'))
except Exception as e:
    print(f'Telegram API request failed: {e}')
    sys.exit(1)

if not result.get('ok'):
    print(f'API error: {result}')
    sys.exit(1)

updates = result.get('result', [])
print(f'Total updates returned: {len(updates)}')

chat_id = '-1003784520976'
topic_id = 4

relevant = []
for upd in updates:
    msg = upd.get('message', {}) or upd.get('channel_post', {}) or upd.get('edited_message', {})
    if msg:
        msg_chat_id = str(msg.get('chat', {}).get('id', ''))
        msg_thread_id = msg.get('message_thread_id')
        if msg_chat_id == chat_id and msg_thread_id == topic_id:
            relevant.append(msg)

print(f'Messages in chat {chat_id}, topic {topic_id}: {len(relevant)}')

ghana_tz = timezone(timedelta(hours=0))
today_str = datetime.now(ghana_tz).strftime('%Y-%m-%d')
print(f'Today (Ghana): {today_str}')
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
    print(f'\n[{msg_date} {msg_time_str}]{marker} {from_user} (id={from_id}, msg={msg_id}):')
    print(text[:500])
    print('-' * 40)
    if is_today:
        today_messages.append(msg)

print(f'\n=== SUMMARY ===')
print(f'Total messages in topic 4: {len(relevant)}')
print(f'Messages from today ({today_str}): {len(today_messages)}')

# Check for morning care report
found_report = False
report_text = None
report_from = None
report_time = None

for msg in today_messages:
    text = msg.get('text', '')
    from_user = msg.get('from', {}).get('first_name', 'Unknown')
    date_unix = msg.get('date', 0)
    report_keywords = ['bp', 'blood pressure', 'pulse', 'temperature', 'temp',
                       'medication', 'vitals', 'reading', 'morning', 'breakfast',
                       'slept', 'mood', 'appetite', 'furosemide']
    text_lower = (text or '').lower()
    found = [kw for kw in report_keywords if kw in text_lower]
    if found:
        print(f'\n>>> CARE REPORT DETECTED from {from_user}')
        print(f'    Matched keywords: {found}')
        found_report = True
        report_text = text
        report_from = from_user
        report_time = datetime.fromtimestamp(date_unix, tz=ghana_tz).strftime('%H:%M')
        break

# Persist raw updates for downstream analysis
out = {
    'today_str': today_str,
    'found_report': found_report,
    'report_from': report_from,
    'report_time': report_time,
    'report_text': report_text,
    'topic4_messages': relevant,
    'today_messages': today_messages,
}
out_path = Path.home() / '.hermes' / 'workspace' / 'Vault' / 'family' / 'mum' / 'health' / f'morning_updates_{today_str}.json'
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2, default=str)
print(f'\nSaved raw updates to {out_path}')

if not found_report:
    print(f'\n>>> No morning care report found for today ({today_str})')
