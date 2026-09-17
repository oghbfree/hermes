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
message_thread_id = 4  # Mum Health topic

text = (
    "Evening check-in \u2014 Mum (Wed 16/09)\n\n"
    "\u2022 **Dinner:** what did she have, and did she finish it?\n"
    "\u2022 **Evening meds:** BP reading for the check. If BP is 100\u2013140, give Furosemide 20mg. **Stop if BP is below 100 or above 140** \u2014 let me know either way.\n"
    "\u2022 **Today\u2019s doctor visit (Focos, 12:00):** how did it go \u2014 any advice or new medication from the doctor?\n"
    "\u2022 **Pain/discomfort:** any back pain or anything troubling her?\n"
    "\u2022 **Energy & mood:** how was she through the day?\n"
    "\u2022 **Brief day summary** \u2014 anything out of the ordinary (falls, dizziness, missed meals).\n\n"
    "Reply when you\u2019re settled."
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

try:
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read().decode('utf-8'))
        if result.get('ok'):
            print('SUCCESS: message_id=' + str(result['result']['message_id']))
        else:
            print('FAILED: ' + str(result.get('description', result)))
            sys.exit(1)
except Exception as e:
    print('ERROR: ' + str(e))
    sys.exit(1)