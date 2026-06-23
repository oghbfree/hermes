import json, urllib.request, sys
from pathlib import Path

# Extract token from .env
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
    "📦 Ghana Supplier Dashboard — Daily Inquiry Report (2026-06-23)\n\n"
    "✅ New inquiry prepared and queued:\n"
    "• Supplier #30: +233 54 203 4633 (dashboard dealer)\n"
    "• Status: ⏳ Pending → ✅ Inquiry Sent\n"
    "• Message: Casual Ghanaian English dashboard inquiry\n\n"
    "---\n\n"
    "📊 Current Status Summary (as of 2026-06-23)\n"
    "• Dashboard: 37 contacts | 28 inquiries sent | 5 pending | 1 confirmed | 1 quoted (6k GHS) | 3 in-person (5k GHS)\n"
    "• Steering: 7 contacts | 1 price confirmed (2k GHS) | 1 hot lead (Dan, combo) | 1 in-person (1.7k GHS)\n"
    "• WhatsApp Gateway: DOWN since ~2026-05-23 (61+ days) — inquiries queued, not delivered\n"
    "• Next supplier: #31 (+233 54 203 1450)\n\n"
    "---\n\n"
    "📁 Marketing text reviewed:\n"
    "Path: C:\\Users\\User\\.hermes\\workspace\\memory\\business\\Akoma\\akoma marketing strategy.txt\n"
    "(Akoma Robotics school marketing strategy — Facebook ads, LinkedIn outreach, school acquisition plan)\n\n"
    "---\n\n"
    "⚠️ No replies received yet. Bridge restoration needed for delivery."
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
