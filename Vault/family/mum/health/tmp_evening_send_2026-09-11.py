import json, urllib.request, sys, subprocess, os

# Extract token reliably via od hex dump (the .env is hex-encoded)
r = subprocess.run(['od', '-A', 'n', '-t', 'x1', os.path.expanduser('~/.hermes/.env')],
                   capture_output=True, text=True)
content = bytes.fromhex(r.stdout.strip().replace(' ', '').replace('\n', '')).decode('utf-8', errors='replace')
token = None
for line in content.split('\n'):
    if line.strip().startswith('TELEGRAM_BOT_TOKEN='):
        token = line.strip().split('=', 1)[1].strip().strip('"').strip("'")
        break
if not token:
    print('ERROR: token not found'); sys.exit(1)

chat_id = '-1003784520976'
message_thread_id = 4  # Mum Health topic

text = (
    "🌙 EVENING CHECK-IN — Comfort (Fri 11 Sep 2026)\n\n"
    "Please update for this evening:\n"
    "• Dinner — what she ate and how much\n"
    "• Evening meds — Furosemide 20mg (yes/no)? Any BP reading before/after? "
    "**Stop if BP is below 100 or above 140** — let me know either way.\n"
    "• Pain / discomfort — back, neck, legs/feet swelling, anything new\n"
    "• Energy & mood — how was she through the day?\n"
    "• Brief overall day summary — anything out of the ordinary\n\n"
    "Reply here when you're settled. 🙏"
)

url = 'https://api.telegram.org/bot' + token + '/sendMessage'
payload = json.dumps({
    'chat_id': chat_id,
    'message_thread_id': message_thread_id,
    'text': text
}, ensure_ascii=False).encode('utf-8')

req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json; charset=utf-8'}, method='POST')
try:
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read().decode('utf-8'))
        if result.get('ok'):
            print('SUCCESS: message_id=' + str(result['result']['message_id']))
        else:
            print('FAILED: ' + str(result)); sys.exit(1)
except Exception as e:
    print('ERROR: ' + str(e)); sys.exit(1)
