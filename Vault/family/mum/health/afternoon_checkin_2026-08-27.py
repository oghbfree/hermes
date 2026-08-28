#!/usr/bin/env python3
"""Afternoon care check-in for Comfort Blankson — 2026-08-27.

NOTE: This cron session had no terminal/execute_code tool, so this script could
not be invoked in-process. Content is duplicated as the delivered final message
(via the job's configured delivery destination). Kept on disk as the record/
re-runnable artifact.
"""
import json, urllib.request, sys, re
from pathlib import Path

def get_token():
    env_path = Path.home() / '.hermes' / '.env'
    with open(env_path, 'r', encoding='utf-8') as f:
        return re.search(r'^TELEGRAM_BOT_TOKEN=(.+)$', f.read(), re.MULTILINE).group(1).strip()

def build_message():
    return (
        "🌤️ AFTERNOON CHECK-IN — Comfort (Thu 27 Aug 2026)\n\n"
        "Please update for this afternoon:\n"
        "🍽️ Lunch — what she ate and how much\n"
        "💊 Afternoon meds — Furosemide 20mg (yes/no)? Any BP reading before/after?\n"
        "🤕 Pain / discomfort — back, swelling in legs/feet, itching, anything new\n"
        "⚡ Energy & mood\n"
        "📝 Any incidents since this morning\n\n"
        "Reply here when ready. 🙏"
    )

def post(topic_id=4):
    token = get_token()
    payload = json.dumps({
        'chat_id': '-1003784520976',
        'message_thread_id': topic_id,
        'text': build_message(),
    }, ensure_ascii=False).encode('utf-8')
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    req = urllib.request.Request(
        url, data=payload,
        headers={'Content-Type': 'application/json; charset=utf-8'},
        method='POST')
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode('utf-8'))

if __name__ == '__main__':
    print('Run with a python interpreter to post to Telegram topic 4')
    print(build_message())