import os, json, urllib.request, time, sys
from pathlib import Path

def read_env_token(env_path):
    token = None
    with open(env_path, 'r', encoding='utf-8') as f:
        data = f.read()
    for sep in ('\n', '\r\n'):
        if sep in data:
            break
    for line in data.replace('\r\n', '\n').replace('\r', '\n').split('\n'):
        line = line.strip()
        if line.startswith('TELEGRAM_BOT_TOKEN='):
            token = line.split('=', 1)[1].strip()
            break
    return token

env_path = Path.home() / '.hermes' / '.env'
token = None
if env_path.exists():
    try:
        token = read_env_token(env_path)
    except Exception as e:
        print('ERROR reading .env:', e)

if not token:
    print('ERROR: TELEGRAM_BOT_TOKEN not found')
    sys.exit(1)

path = Path(r'C:\Users\User\.hermes\workspace\memories\insights\INTEGRATED_INSIGHTS_2026-06-09.md')
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

if 'TELEGRAM_BOT_TOKEN' not in token:
    print('WARNING: token may be invalid or empty')

chat_id = '-1003784520976'
message_thread_id = 10
url = 'https://api.telegram.org/bot{}/sendMessage'.format(token)

def chunks(s, n):
    if len(s) <= n:
        return [s]
    out, last = [], 0
    while last < len(s):
        cut = s.find('\n', last + n)
        if cut == -1 or cut <= last:
            cut = last + n
        out.append(s[last:cut])
        last = cut
    return out

parts = chunks(text, 3800)
print('Sending {} part(s) to topic {}'.format(len(parts), message_thread_id))

for i, part in enumerate(parts, 1):
    payload = json.dumps({
        'chat_id': chat_id,
        'message_thread_id': message_thread_id,
        'text': part
    }, ensure_ascii=False).encode('utf-8')
    req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json; charset=utf-8'}, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode('utf-8'))
            if result.get('ok'):
                print('SUCCESS: part={} msg_id={}'.format(i, result['result']['message_id']))
            else:
                print('FAILED part={}: {}'.format(i, result.get('description', result)))
                sys.exit(1)
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8')
        print('HTTP Error part={}: {} {}'.format(i, e.code, body))
        sys.exit(1)
    except Exception as e:
        print('ERROR part={}: {}'.format(i, e))
        sys.exit(1)
    time.sleep(1)

print('DONE: sent {} message(s)'.format(len(parts)))
