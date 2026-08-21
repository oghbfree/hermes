#!/usr/bin/env python3
"""Evening care check-in for Comfort Blankson — 2026-08-21.
Posts a warm, concise evening check-in prompt to Telegram topic 4 (Mum Health).
"""
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

# Ghana is UTC+0
ghana_tz = timezone(timedelta(hours=0))
today_str = datetime.now(ghana_tz).strftime('%Y-%m-%d')

message = (
    "🌆 Good evening — Comfort (Mum) evening check-in\n\n"
    "Hope the evening is calm and comfortable. A few quick things to help us "
    "keep track of her day:\n\n"
    "🍽️ Dinner — has she eaten? What did she have?\n"
    "💊 Evening medications — taken? Any missed or skipped?\n"
    "🤕 Any pain, discomfort, or issues to note?\n"
    "⚡ Energy & mood — how is she feeling tonight?\n"
    "📝 Overall — how was her day today?\n\n"
    "Thank you for looking after her! 🙏"
)

payload = json.dumps({
    'chat_id': chat_id,
    'message_thread_id': topic_id,
    'text': message,
}, ensure_ascii=False).encode('utf-8')

url = f'https://api.telegram.org/bot{token}/sendMessage'
try:
    req = urllib.request.Request(
        url, data=payload,
        headers={'Content-Type': 'application/json; charset=utf-8'},
        method='POST')
    with urllib.request.urlopen(req, timeout=15) as resp:
        result = json.loads(resp.read().decode('utf-8'))
    if result.get('ok'):
        print(f'✅ Evening check-in posted to topic {topic_id} ({today_str})')
        print(f'   Message id: {result.get("result", {}).get("message_id")}')
    else:
        print(f'❌ Telegram API error: {result}')
        sys.exit(1)
except Exception as e:
    print(f'❌ Error posting message: {e}')
    sys.exit(1)