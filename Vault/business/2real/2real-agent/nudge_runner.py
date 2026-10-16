import json, time, re, sys, os
from datetime import datetime

WS = os.path.dirname(os.path.abspath(__file__))
QUEUE = os.path.join(WS, 'nudge_queue.json')
LOG = os.path.join(WS, 'nudge_sent_log.json')

def load(p):
    with open(p, encoding='utf-8') as f:
        return json.load(f)

def save_log(entries):
    tmp = LOG + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(entries, f, ensure_ascii=False, indent=1)
    os.replace(tmp, LOG)

queue = load(QUEUE)
log = load(LOG)
done_users = {e.get('user_id') for e in log if e.get('user_id')}
logged_chats = {e.get('chat_id') for e in log}

# build remaining list, newest-first queue order, dedupe by user
remaining = []
for q in queue:
    cid = q['chat_url'].split('/profile-messages/')[1].split('?')[0]
    if q['user_id'] in done_users or cid in logged_chats:
        continue
    remaining.append((q, cid))

LIMIT = int(sys.argv[1]) if len(sys.argv) > 1 else 20
batch = remaining[:LIMIT]
print(f"REMAINING_TOTAL={len(remaining)} BATCH={len(batch)}")
for q, cid in batch:
    print("TODO", q['name'], cid)
