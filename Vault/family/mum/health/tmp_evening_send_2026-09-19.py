import json, sys, urllib.request
from pathlib import Path

def get_token(path):
    p = Path(path)
    if not p.exists():
        return None
    try:
        data = p.read_text(encoding='utf-8')
    except Exception:
        return None
    for line in data.replace('\r\n', '\n').split('\n'):
        line = line.strip()
        if line.startswith('TELEGRAM_BOT_TOKEN='):
            return line.split('=', 1)[1].strip().strip('"').strip("'")
    return None

def get_token_hex(path):
    import subprocess
    try:
        r = subprocess.run(['od','-A','n','-t','x1', path], capture_output=True, text=True)
        content = bytes.fromhex(r.stdout.strip().replace(' ','').replace('\n','')).decode('utf-8', errors='replace')
        for line in content.split('\n'):
            line = line.strip()
            if line.startswith('TELEGRAM_BOT_TOKEN='):
                return line.split('=',1)[1].strip().strip('"').strip("'")
    except Exception:
        return None
    return None

def getme(tok):
    url = 'https://api.telegram.org/bot{}/getMe'.format(tok)
    try:
        with urllib.request.urlopen(url, timeout=15) as r:
            return json.loads(r.read().decode('utf-8')).get('ok', False)
    except Exception:
        return False

candidates = []
for p in [r'C:\Users\User\.hermes\.env', r'C:\Users\User\AppData\Local\hermes\.env']:
    t = get_token(p)
    if t: candidates.append(t)
for p in [r'C:\Users\User\.hermes\.env', r'C:\Users\User\AppData\Local\hermes\.env']:
    t = get_token_hex(p)
    if t: candidates.append(t)

TOKEN = None
seen = set()
for t in candidates:
    if t in seen: continue
    seen.add(t)
    if getme(t):
        TOKEN = t
        break

if not TOKEN:
    print('NO VALID TOKEN FOR DELIVERY'); sys.exit(1)
print('VALID TOKEN FOUND (len={})'.format(len(TOKEN)))

chat_id = '-1003784520976'
thread = 4  # Mum Health topic

message = (
    "\U0001F319 EVENING CHECK-IN \u2014 Comfort (Sat 19 Sep 2026)\n\n"
    "Evening update please:\n"
    "\u2022 Dinner \u2014 what did she eat and how much?\n"
    "\u2022 Evening meds \u2014 Furosemide 20mg (yes/no)? "
    "Any BP reading before/after? **Stop if BP below 100 or above 140** \u2014 let me know either way.\n"
    "\u2022 Pain / discomfort \u2014 back, hip, neck, leg/feet swelling, anything new\n"
    "\u2022 Energy & mood \u2014 how was she through the day?\n"
    "\u2022 Brief overall day summary \u2014 any falls, dizziness, missed meals, "
    "medication refusal, anything unusual?\n\n"
    "Fluids reminder \u2014 keep water going (sodium was high on the labs). "
    "Reply here when you're settled. \U0001F64F"
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
            print('SUCCESS: msg_id={} thread={}'.format(result['result']['message_id'], result['result'].get('message_thread_id')))
        else:
            print('FAILED: {}'.format(result)); sys.exit(1)
except urllib.error.HTTPError as e:
    print('HTTP Error: {} {}'.format(e.code, e.read().decode('utf-8'))); sys.exit(1)
except Exception as e:
    print('ERROR: {}'.format(e)); sys.exit(1)