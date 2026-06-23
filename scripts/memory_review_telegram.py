import json, urllib.request, sys
from pathlib import Path

env_path = Path.home() / '.hermes' / '.env'
token = None
with open(env_path, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if 'TELEGRAM_BOT_TOKEN' in line and '=' in line:
            token = line.split('=', 1)[1].strip().strip('"').strip("'")
            break

if not token:
    print("ERROR: TELEGRAM_BOT_TOKEN not found")
    sys.exit(1)

chat_id = '-1003784520976'
message_thread_id = 20

text = (
    "🧠 Memory Review — Daily Session Logs (2026-06-23)\n\n"
    "Processed 5 cron sessions in past 24h:\n\n"
    "1. brain-dump-processing (02:54): No new brain dumps found.\n"
    "2. habit-reflect (02:41): Akoma Robotics school pipeline flagged for restructuring. "
    "WhatsApp Bridge Health Monitor proposed (every 2h) to auto-trigger bulk Ghana supplier sends when gateway is restored.\n"
    "3. ghana-dashboard-inquiry (02:38): Supplier #30 (+233 54 203 4633) inquiry sent. "
    "28 sent / 5 pending. Next: #31 (+233 54 203 1450). Gateway DOWN 61+ days.\n"
    "4. daily-backup (02:28): Backup completed. 28,806 files, ~2.7GB. "
    "Path: backup_20260623_022849.\n"
    "5. security-policy-check (02:24): Credential exposure found (partial tokens in 294 request dumps). "
    "concurrent_log_handler missing; gateway crash on 2026-06-22. Google OAuth expired 2026-06-17.\n\n"
    "Issue summary:\n"
    "- content-assets/content-output dirs missing from backup\n"
    "- MSYS symlink repair failed: latest is a directory, not a symlink\n"
    "- 294 request dump JSONs contain partial sk-or-v1... tokens\n"
    "- Restore action: chmod 600 on .env/auth/config; install concurrent_log_handler; refresh Google OAuth\n"
    "- Akoma marketing strategy needs restructuring into pipeline doc\n"
)

url = 'https://api.telegram.org/bot' + token + '/sendMessage'
payload = json.dumps({
    'chat_id': chat_id,
    'message_thread_id': message_thread_id,
    'text': text
}, ensure_ascii=False).encode('utf-8')

req = urllib.request.Request(url, data=payload, headers={
    'Content-Type': 'application/json; charset=utf-8'
}, method='POST')

with urllib.request.urlopen(req, timeout=30) as resp:
    result = json.loads(resp.read().decode('utf-8'))
    if result.get('ok'):
        print('SUCCESS: message_id=' + str(result['result']['message_id']))
    else:
        print('FAILED: ' + str(result))
        sys.exit(1)
