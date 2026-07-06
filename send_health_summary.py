import json, urllib.request, sys, re
from pathlib import Path
from datetime import datetime, timezone, timedelta

# Load token from .env
env_path = Path.home() / '.hermes' / '.env'
token = None
with open(env_path, 'r', encoding='utf-8') as f:
    content = f.read()
    m = re.search(r'^TELEGRAM_BOT_TOKEN=(.+)$', content, re.MULTILINE)
    if m:
        token = m.group(1).strip()

if not token:
    print('ERROR: No TELEGRAM_BOT_TOKEN found in .env')
    sys.exit(1)

chat_id = '-1003784520976'
topic_id = 2  # Health Log topic

# Ghana time
ghana_tz = timezone(timedelta(hours=0))
now = datetime.now(ghana_tz)
date_str = now.strftime('%Y-%m-%d')
day_name = now.strftime('%A')

message = (
    f"🌅 *Morning Health Check — {day_name}, {date_str}*\n\n"
    f"🔴 *Electrical Shock (12 Jun)* — 22 days ago, medical eval still pending (3 weeks overdue!)\n"
    f"   Signs to watch: headache, dizziness, confusion, nausea, vision changes\n\n"
    f"🟡 *Pending Follow-ups*\n"
    f"  • Achalasia — last OGD Dec 2018, manometry never confirmed\n"
    f"  • Upper GI symptoms (May 20) — no clinical follow-up\n"
    f"  • Blood work stale since Mar 2020 — MCV high, GFR borderline\n\n"
    f"🟢 *Stable*\n"
    f"  • Eyes healthy (Sep 2025 — IOP normal)\n"
    f"  • No acute pericarditis episodes\n\n"
    f"📋 *Yesterday (2 Jul)*\n"
    f"  🍳 Ate well: 3x fried eggs (breakfast), 2x boiled eggs (lunch), Kontomire w/ garden egg stew (dinner)\n"
    f"  ⚠️ No vitals recorded — last BP Jun 1 (118/76, pulse 80)\n\n"
    f"⚠️ *Data Gaps*\n"
    f"  • No vitals since Jun 1 (33 days)\n"
    f"  • No symptom/energy logs\n"
    f"  • No meals logged for Jul 3\n\n"
    f"✅ *Action Items*\n"
    f"  1. 🔴 Confirm doctor visit for electrical shock (22 days overdue)\n"
    f"  2. 🟡 Book updated blood work\n"
    f"  3. 🟡 Log today's vitals & meals"
)

url = f'https://api.telegram.org/bot{token}/sendMessage'
payload = json.dumps({
    'chat_id': chat_id,
    'message_thread_id': topic_id,
    'text': message,
    'parse_mode': 'Markdown'
}).encode('utf-8')

req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
try:
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read().decode('utf-8'))
    if result.get('ok'):
        print(f'SUCCESS: Message sent to chat {chat_id}, topic {topic_id}')
        print(f'  Message ID: {result["result"]["message_id"]}')
    else:
        print(f'API ERROR: {result}')
except Exception as e:
    print(f'REQUEST FAILED: {e}')
    sys.exit(1)