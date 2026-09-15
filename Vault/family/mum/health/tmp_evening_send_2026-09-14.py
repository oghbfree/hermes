import json, sys, urllib.request
from pathlib import Path

def get_token(path):
    p = Path(path)
    if not p.exists():
        return None
    data = p.read_text(encoding='utf-8')
    for line in data.replace('\r\n', '\n').split('\n'):
        line = line.strip()
        if line.startswith('TELEGRAM_BOT_TOKEN='):
            return line.split('=', 1)[1].strip()
    return None

def getme(tok):
    url = 'https://api.telegram.org/bot{}/getMe'.format(tok)
    try:
        with urllib.request.urlopen(url, timeout=15) as r:
            return json.loads(r.read().decode('utf-8')).get('ok', False)
    except Exception:
        return False

home = get_token(r'C:\Users\User\.hermes\.env') or ''
appdata = get_token(r'C:\Users\User\AppData\Local\hermes\.env') or ''
# Try both simple read, then fall back to hex-od decode if hex-encoded
def get_token_hex(path):
    import subprocess, os
    try:
        r = subprocess.run(['od','-A','n','-t','x1', path], capture_output=True, text=True)
        content = bytes.fromhex(r.stdout.strip().replace(' ','').replace('\n','')).decode('utf-8', errors='replace')
        for line in content.split('\n'):
            line=line.strip()
            if line.startswith('TELEGRAM_BOT_TOKEN='):
                return line.split('=',1)[1].strip().strip('"').strip("'")
    except Exception:
        return None
    return None

TOKEN = home if getme(home) else (appdata if getme(appdata) else None)
if not TOKEN:
    for p in [r'C:\Users\User\.hermes\.env', r'C:\Users\User\AppData\Local\hermes\.env']:
        t = get_token_hex(p)
        if t and getme(t):
            TOKEN = t
            break
if not TOKEN:
    print('NO VALID TOKEN FOR DELIVERY'); sys.exit(1)

chat_id = '-1003784520976'
thread = 4  # Mum Health topic

message = (
    "🌙 EVENING CHECK-IN — Comfort (Mon 14 Sep 2026)\n\n"
    "Please update for this evening:\n"
    "• Dinner — what did she eat and how much?\n"
    "• Evening meds — Furosemide 20mg (yes/no)? Any BP reading before/after? "
    "**Stop if BP is below 100 or above 140** — let me know either way.\n"
    "• Pain / discomfort — back, hip, neck, leg/feet swelling, anything new\n"
    "(we're watching BP closely after the high readings on Sunday 13 Sep; "
    "doctor appointment is Wed 16 Sep)\n"
    "• Energy & mood — how was she through the day?\n"
    "• Brief overall day summary — any falls, dizziness, missed meals, "
    "medication refusal, or anything unusual?\n\n"
    "Reply here when you're settled. 🙏"
)

url = 'https://api.telegram.org/bot{}/sendMessage'.format(TOKEN)
payload = json.dumps({
    'chat_id': chat_id,
    'message_thread_id': thread,
    'text': message,
    'parse_mode': 'Markdown'
}, ensure_ascii=False).encode('utf-8')

req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json; charset=utf-8'}, method='POST')
try:
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read().decode('utf-8'))
        if result.get('ok'):
            print('SUCCESS: msg_id={}'.format(result['result']['message_id']))
        else:
            print('FAILED: {}'.format(result)); sys.exit(1)
except urllib.error.HTTPError as e:
    print('HTTP Error: {} {}'.format(e.code, e.read().decode('utf-8'))); sys.exit(1)
except Exception as e:
    print('ERROR: {}'.format(e)); sys.exit(1)