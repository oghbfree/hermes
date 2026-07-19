import os, json, urllib.request, time, sys
from pathlib import Path

env_path = Path.home() / '.hermes' / '.env'
token = None
if env_path.exists():
    try:
        with open(env_path, 'r', encoding='utf-8') as f:
            data = f.read()
        for line in data.replace('\r\n', '\n').replace('\r', '\n').split('\n'):
            line = line.strip()
            if line.startswith('TELEGRAM_BOT_TOKEN='):
                token = line.split('=', 1)[1].strip()
                break
    except Exception as e:
        print('ERROR reading .env:', e)
        sys.exit(1)

if not token:
    print('ERROR: TELEGRAM_BOT_TOKEN not found')
    sys.exit(1)

# Chat ID for the group with topic 20
chat_id = '-1003784520976'
message_thread_id = 20

message = '''📋 **Daily Processing Report — 2026-07-11**

**Sessions Processed**: 10 kanban tasks (2026-07-10)

**✅ Completed Tasks**
• **t_f96d328c** — UK Gov future-proofing: 7 regulatory domains, OFSI/FCA monitor script, 10 actions this week
• **t_a80c0771** — Junior ISAs/SIPPs for Kobena (11) & Nenyi (10): AJ Bell + Vanguard Global All Cap, £700/mo total. Need AJ Bell compliance call for Ghana-resident eligibility
• **t_b21f32ef** — Akoma Robotics school pipeline: 50 targets in Accra, 2-3 partnerships Month 1, FB ads addressing 8 admin concerns, $40→$300→$630-1050 budget phases
• **t_ca76518e** — Phone consolidation: 5-phase plan, Smarty PAC/STAC codes documented
• **t_91f700ef** — FB Marketplace daily habits: 10-15 min routine + weekly sprints
• **t_6f9bf79a** — Free/secondhand platform check: no items
• **t_3915149b** — EDF setup checklist copied to workspace

**🚫 Blocked**
• **t_2098e55f** — Dr Ferguson order for Mum: missing 7 details (herb names, multivitamin brand, quantities, supplier, Ghana address, payment, trip deadline). Clinical constraints: CKD Stage 3b, ferritin 404 (NO iron), phosphate 2.91 (NO phosphate)

**⚠️ Issues**
• 87.4% cron failure rate (118/135) — systemic Connection errors
• WhatsApp gateway down 61+ days (affects Akoma ads, Mum check-ins)
• Security audit missing Jul 8
• Daily notes gap: no 2026-07-09/10 entries (now created retroactively)

**📝 Memory Updated**: MEMORY.md refreshed with Junior ISA/SIPP recs, Akoma pipeline, phone codes, Dr Ferguson blocker, all issues.
'''

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

parts = chunks(message, 3800)
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