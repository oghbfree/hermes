#!/usr/bin/env python3
"""Morning care check-in for Comfort Blankson — 2026-07-03.
Queries Telegram topic 4 for new morning care reports, flags abnormal vitals,
and posts acknowledgement."""
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
url = f'https://api.telegram.org/bot{token}/getUpdates?offset=-50&timeout=10'
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

# Filter messages in topic 4
relevant = []
for upd in updates:
    msg = upd.get('message', {})
    if msg:
        msg_chat_id = str(msg.get('chat', {}).get('id', ''))
        msg_thread_id = msg.get('message_thread_id')
        if msg_chat_id == chat_id and msg_thread_id == topic_id:
            relevant.append(msg)

print(f'Messages in chat {chat_id}, topic {topic_id}: {len(relevant)}')

# Ghana is UTC+0 (same as UTC)
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

for msg in today_messages:
    text = msg.get('text', '').lower()
    from_user = msg.get('from', {}).get('first_name', 'Unknown')
    report_keywords = ['bp', 'blood pressure', 'pulse', 'temperature', 'temp', 
                       'medication', 'vitals', 'reading', 'morning', 'breakfast',
                       'slept', 'mood', 'appetite']
    found = [kw for kw in report_keywords if kw in text]
    if found:
        print(f'\n>>> CARE REPORT DETECTED from {from_user}')
        print(f'    Matched keywords: {found}')
        found_report = True
        report_text = msg.get('text', '')
        report_from = from_user
        break

if found_report:
    print('\n--- VITALS ANALYSIS ---')
    text_lower = report_text.lower()
    
    # Check BP
    bp_flag = 'Not found'
    sys_bp = 0
    dia_bp = 0
    bp_match = re.search(r'bp\s*[:=]?\s*(\d+)\s*[/]\s*(\d+)', text_lower, re.IGNORECASE)
    if bp_match:
        sys_bp = int(bp_match.group(1))
        dia_bp = int(bp_match.group(2))
        bp_flag = '⚠️ HIGH' if sys_bp >= 140 or dia_bp >= 90 else '✅ Normal'
        print(f'BP: {sys_bp}/{dia_bp} — {bp_flag}')
    else:
        print('BP: Not found in report')
    
    # Check Pulse
    pulse_flag = 'Not found'
    pulse = 0
    pulse_match = re.search(r'pulse\s*[:=]?\s*(\d+)', text_lower, re.IGNORECASE)
    if not pulse_match:
        pulse_match = re.search(r'\bp\s*[:=]?\s*(\d+)', text_lower, re.IGNORECASE)
    if pulse_match:
        pulse = int(pulse_match.group(1))
        pulse_flag = '⚠️ OUT OF RANGE' if pulse < 60 or pulse > 100 else '✅ Normal'
        print(f'Pulse: {pulse} bpm — {pulse_flag}')
    else:
        print('Pulse: Not found in report')
    
    # Check Temperature
    temp_flag = 'Not found'
    temp = 0.0
    temp_match = re.search(r'temp(?:erature)?\s*[:=]?\s*([\d.]+)\s*°?c?', text_lower, re.IGNORECASE)
    if temp_match:
        temp = float(temp_match.group(1))
        temp_flag = '⚠️ HIGH (fever)' if temp > 37.5 else '✅ Normal'
        print(f'Temperature: {temp}°C — {temp_flag}')
    else:
        print('Temperature: Not found in report')
    
    # Build acknowledgement
    ack = f'✅ Morning report received, thank you {report_from}!'
    alerts = []
    if 'HIGH' in bp_flag:
        alerts.append(f'⚠️ BP: {sys_bp}/{dia_bp} — elevated (>140/90), please monitor.')
    if 'OUT' in pulse_flag:
        alerts.append(f'⚠️ Pulse: {pulse} bpm — outside normal range (60-100).')
    if 'HIGH' in temp_flag:
        alerts.append(f'⚠️ Temperature: {temp}°C — fever threshold exceeded.')
    if alerts:
        ack += '\n' + '\n'.join(alerts)
    
    # Post acknowledgement
    ack_payload = json.dumps({
        'chat_id': chat_id,
        'message_thread_id': topic_id,
        'text': ack
    }, ensure_ascii=False).encode('utf-8')
    
    ack_url = f'https://api.telegram.org/bot{token}/sendMessage'
    try:
        ack_req = urllib.request.Request(ack_url, data=ack_payload, 
                                         headers={'Content-Type': 'application/json; charset=utf-8'},
                                         method='POST')
        with urllib.request.urlopen(ack_req, timeout=15) as ack_resp:
            ack_result = json.loads(ack_resp.read().decode('utf-8'))
        if ack_result.get('ok'):
            print(f'\n✅ Acknowledgement posted successfully')
        else:
            print(f'\n❌ Failed to post acknowledgement: {ack_result}')
    except Exception as e:
        print(f'\n❌ Error posting acknowledgement: {e}')
    
    # Archive the report
    report_content = f"""# Morning Report — {today_str}

**Caregiver:** {report_from}
**Time:** Received via Telegram topic 4

---

## Vitals
| Measurement | Value | Status |
|-------------|-------|--------|
| **BP** | {sys_bp}/{dia_bp} | {bp_flag} |
| **Pulse** | {pulse} bpm | {pulse_flag} |
| **Temperature** | {temp}°C | {temp_flag} |

---

## Full Report
```
{report_text}
```

*Archived by morning care check-in cron*
"""
    archive_path = Path.home() / '.hermes' / 'workspace' / 'Vault' / 'family' / 'mum' / 'health' / f'{today_str}_morning_report.md'
    try:
        with open(archive_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        print(f'\n✅ Report archived to {archive_path}')
    except Exception as e:
        print(f'\n❌ Failed to archive report: {e}')
    
    print(f'\n--- ACKNOWLEDGEMENT POSTED ---\n{ack}')
else:
    print('\n>>> No morning care report found for today ({})'.format(today_str))