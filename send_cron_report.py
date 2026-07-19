import json
import urllib.request
import os
import tempfile
import subprocess

# Read token from .env
env_path = os.path.join(os.path.expanduser("~"), ".hermes", ".env")
token = None
with open(env_path, "r", encoding="utf-8") as f:
    for line in f:
        if "TELEGRAM_BOT_TOKEN" in line and "=" in line:
            token = line.strip().split("=", 1)[1].strip()
            break

if not token:
    print("ERROR: TELEGRAM_BOT_TOKEN not found in .env")
    exit(1)

# Read the report
report_path = os.path.join(os.path.expanduser("~"), ".hermes", "cron", "output", "cron-status-report", "2026-07-12_daily-cron-status.md")
with open(report_path, "r", encoding="utf-8") as f:
    content = f.read()

# Write to a temp file
with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as tmp:
    tmp.write(content)
    tmp_path = tmp.name

# Send as document via curl
cmd = [
    'curl', '-s', '-X', 'POST',
    f'https://api.telegram.org/bot{token}/sendDocument',
    '-F', f'chat_id=-1003784520976',
    '-F', 'message_thread_id=20',
    '-F', f'document=@{tmp_path}',
    '-F', 'caption=📊 Daily Cron Status Report — 12 July 2026',
    '-F', 'parse_mode=Markdown'
]
result = subprocess.run(cmd, capture_output=True, text=True)
print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)
print("Return code:", result.returncode)

# Clean up
os.unlink(tmp_path)