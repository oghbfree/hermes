#!/usr/bin/env python3
"""Evening care check-in for Comfort Blankson — 2026-09-03 (Thu).
Queries Telegram topic 4 for today's/new afternoon reports, posts the evening
check-in prompt, and flags any care report for downstream capture."""
import json, urllib.request, sys, re
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

chat_id = '-1003784520976'
topic_id = 4
ghana_tz = timezone(timedelta(hours=0))
today_str = datetime.now(ghana_tz).strftime('%Y-%m-%d')
print(f'Today (Ghana): {today_str}')

# --- 1. Query recent updates in topic 4 ---
url = f'https://api.telegram.org/bot{token}/getUpdates?timeout=10'
try:
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read().decode('utf-8'))
except Exception as e:
    print(f'Telegram getUpdates failed: {e}')
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
    if msg_date == today_str:
        today_messages.append(msg)
        from_user = msg.get('from', {}).get('first_name', 'Unknown')
        text = msg.get('text', msg.get('caption', '(no text)'))
        msg_time = datetime.fromtimestamp(date_unix, tz=ghana_tz).strftime('%H:%M')
        msg_id = msg.get('message_id', '?')
        print(f'\n[TODAY {msg_time}] {from_user} (msg={msg_id}):')
        print((text or '')[:800])
        print('-' * 40)

print(f'\n=== SUMMARY ===')
print(f'Total messages in topic 4: {len(relevant)}')
print(f"Messages from today ({today_str}): {len(today_messages)}")

# --- 2. Detect a care report among today's messages ---
report_keywords = ['dinner', 'furosemide', 'bp', 'blood pressure', 'pulse', 'temp',
                   'pain', 'swell', 'mood', 'energy', 'complaint', 'appetite',
                   'legon', 'botanical', 'outing', 'day']
report_text = None
report_from = None
report_time = None
for msg in today_messages:
    text = msg.get('text', '') or ''
    tl = text.lower()
    found = [kw for kw in report_keywords if kw in tl]
    if len(found) >= 2:
        print(f'\n>>> CARE/detail message from {msg.get("from", {}).get("first_name", "?")}: {found}')
        report_from = msg.get('from', {}).get('first_name', 'Unknown')
        report_text = text
        report_time = datetime.fromtimestamp(msg.get('date', 0), tz=ghana_tz).strftime('%H:%M')
        break

# Persist raw view for downstream capture
out = {
    'today_str': today_str,
    'found_report': bool(report_text),
    'report_from': report_from,
    'report_time': report_time,
    'report_text': report_text,
    'today_messages': today_messages,
}
out_path = Path.home() / '.hermes' / 'workspace' / 'Vault' / 'family' / 'mum' / 'health' / f'evening_updates_{today_str}.json'
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2, default=str)
print(f'Saved raw updates to {out_path}')

# --- 3. Post evening check-in prompt ---
message = (
    "🌆 Good evening — Comfort (Mum) evening check-in\n\n"
    "Hope the evening is calm and comfortable. A few quick things to help "
    "us track her day:\n\n"
    "🍽️ Dinner — has she eaten? What did she have?\n"
    "💊 Evening medications — Furosemide 20mg taken (yes/no)? Any BP reading before/after?\n"
    "🤕 Any pain, discomfort, or issues to note (back, legs/feet swelling, itching)?\n"
    "⚡ Energy & mood — how is she feeling tonight?\n"
    "📝 Overall — how was her day today? (Did the Legon Botanical Gardens outing go ahead? 🌿)\n\n"
    "Thank you for looking after her. 🙏"
)

payload = json.dumps({
    'chat_id': chat_id,
    'message_thread_id': topic_id,
    'text': message,
}, ensure_ascii=False).encode('utf-8')

post_url = f'https://api.telegram.org/bot{token}/sendMessage'
try:
    req = urllib.request.Request(
        post_url, data=payload,
        headers={'Content-Type': 'application/json; charset=utf-8'},
        method='POST')
    with urllib.request.urlopen(req, timeout=15) as resp:
        result = json.loads(resp.read().decode('utf-8'))
    if result.get('ok'):
        print(f"\n✅ Evening check-in posted to topic {topic_id} (msg id: {result.get('result', {}).get('message_id')})")
    else:
        print(f"❌ Telegram API error: {result}")
        sys.exit(1)
except Exception as e:
    print(f'❌ Error posting message: {e}')
    sys.exit(1)

print('\nDONE')