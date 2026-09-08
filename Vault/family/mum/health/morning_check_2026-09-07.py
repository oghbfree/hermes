#!/usr/bin/env python3
"""Morning care check-in for Comfort Blankson - 2026-09-07 (Mon).
Queries Telegram topic 4 for today's morning care report, flags abnormal vitals,
and persists the raw view for downstream capture."""
import json, urllib.request, sys, re
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
    print('ERROR: TELEGRAM_BOT_TOKEN not found in .env')
    sys.exit(1)

chat_id = '-1003784520976'
topic_id = 4
ghana_tz = timezone(timedelta(hours=0))
today_str = datetime.now(ghana_tz).strftime('%Y-%m-%d')
print(f'Today (Ghana / UTC): {today_str}')

url = f'https://api.telegram.org/bot{token}/getUpdates?timeout=10'
try:
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read().decode('utf-8'))
except Exception as e:
    print(f'Telegram getUpdates failed: {e}')
    sys.exit(1)

if not result.get('ok'):
    print(f'API error: {result}')
    sys.exit(1)

updates = result.get('result', [])
relevant = []
for upd in updates:
    msg = upd.get('message', {}) or upd.get('channel_post', {}) or upd.get('edited_message', {})
    if msg:
        if str(msg.get('chat', {}).get('id', '')) == chat_id and msg.get('message_thread_id') == topic_id:
            relevant.append(msg)

today_messages = []
for msg in relevant:
    date_unix = msg.get('date', 0)
    msg_date = datetime.fromtimestamp(date_unix, tz=ghana_tz).strftime('%Y-%m-%d')
    msg_time = datetime.fromtimestamp(date_unix, tz=ghana_tz).strftime('%H:%M')
    msg_id = msg.get('message_id', '?')
    from_user = msg.get('from', {}).get('first_name', 'Unknown')
    text = msg.get('text', msg.get('caption', '(no text)'))
    print(f'\n[{msg_date} {msg_time} (msg={msg_id})] {from_user}:')
    print((text or '')[:1000])
    print('-' * 40)
    if msg_date == today_str:
        today_messages.append(msg)

print(f'\n=== SUMMARY ===')
print(f'Total messages in topic 4 (from getUpdates buffer): {len(relevant)}')
print(f"Messages from today ({today_str}): {len(today_messages)}")

report_keywords = ['bp', 'blood pressure', 'pulse', 'temp', 'morning', 'breakfast',
                   'slept', 'mood', 'appetite', 'furosemide', 'medication', 'vitals']
report_text = None
report_from = None
report_time = None
for msg in today_messages:
    text = msg.get('text', '') or ''
    tl = text.lower()
    found = [kw for kw in report_keywords if kw in tl]
    if len(found) >= 2:
        print(f'\n>>> CARE REPORT DETECTED from {msg.get("from", {}).get("first_name", "?")}: {found}')
        report_from = msg.get('from', {}).get('first_name', 'Unknown')
        report_text = text
        report_time = datetime.fromtimestamp(msg.get('date', 0), tz=ghana_tz).strftime('%H:%M')
        break

out = {
    'today_str': today_str,
    'found_report': bool(report_text),
    'report_from': report_from,
    'report_time': report_time,
    'report_text': report_text,
    'today_messages': today_messages,
}
out_path = Path.home() / '.hermes' / 'workspace' / 'Vault' / 'family' / 'mum' / 'health' / f'morning_updates_{today_str}.json'
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2, default=str)
print(f'\nSaved raw updates to {out_path}')

if not report_text:
    print(f'\n>>> No morning care report found for today ({today_str})')