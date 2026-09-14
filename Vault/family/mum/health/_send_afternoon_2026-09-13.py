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

home = get_token(r'C:\Users\User\.hermes\.env')
appdata = get_token(r'C:\Users\User\AppData\Local\hermes\.env')

TOKEN = appdata if (appdata and getme(appdata)) else home
if not TOKEN or not getme(TOKEN):
    print('NO VALID TOKEN FOR DELIVERY'); sys.exit(1)

chat_id = '-1003784520976'
thread = 4  # Mum Health topic

message = (
    "🕐 Afternoon check-in \u2014 Mum (Comfort Blankson), 13/09/26 (Sun).\n\n"
    "Note: the morning report wasn't received today, so please cover this morning in the update too.\n\n"
    "\u2022 Breakfast & Lunch \u2014 what did she eat, and how much did she finish?\n"
    "\u2022 Medication \u2014 Furosemide 20mg: was the morning dose given, and any afternoon dose? (Please include BP before dosing.)\n"
    "\u2022 Pain / discomfort \u2014 any back, hip, neck or new pain? (Checking after the 11 Sep fall.)\n"
    "\u2022 Energy / mood \u2014 how is she feeling this afternoon?\n"
    "\u2022 Sleep last night \u2014 any insomnia? (She was awake ~1am\u20135am on 12 Sep; also no evening bed-laying as agreed.)\n"
    "\u2022 Any incidents since yesterday (falls, dizziness, unusual symptoms, refusal of care)?\n\n"
    "Thanks."
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