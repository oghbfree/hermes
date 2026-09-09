import json, urllib.request, os, subprocess

# Extract token via od hex dump (file is hex-encoded; grep fails)
result = subprocess.run(
    ['od', '-A', 'n', '-t', 'x1', os.path.expanduser('~/.hermes/.env')],
    capture_output=True, text=True
)
hex_str = result.stdout.strip().replace(' ', '').replace('\n', '')
raw_bytes = bytes.fromhex(hex_str)
content = raw_bytes.decode('utf-8', errors='replace')
token = None
for line in content.split('\n'):
    if line.strip().startswith('TELEGRAM_BOT_TOKEN='):
        token = line.strip().split('=', 1)[1].strip().strip('"').strip("'")
        break
if not token:
    print('ERROR: token not found')
    raise SystemExit(1)

chat_id = '-1003784520976'
message_thread_id = 4  # Mum Health topic

text = (
    "Evening check-in — Mum (Tue 08/09)\n\n"
    "• **Dinner:** what did she have, and did she finish it?\n"
    "• **Evening meds:** BP reading for the check. If BP is 100–140, give Furosemide 20mg. "
    "**Stop if BP is below 100 or above 140** — let me know either way.\n"
    "• **Pain/discomfort:** any back pain or anything troubling her?\n"
    "• **Energy & mood:** how was she through the day?\n"
    "• **Brief day summary** — anything out of the ordinary.\n\n"
    "Reply when you're settled."
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
        result_json = json.loads(resp.read().decode('utf-8'))
        if result_json.get('ok'):
            print('SUCCESS: message_id=' + str(result_json['result']['message_id']))
        else:
            print('FAILED: ' + str(result_json.get('description', result_json)))
            raise SystemExit(1)
except Exception as e:
    print('ERROR: ' + str(e))
    raise SystemExit(1)