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
message_thread_id = 928

text = """📊 **Ghana Supplier Research — Daily Report (2026-07-15)**

**Dashboard Dealers**: 37 contacts | 34 inquiries sent | 0 pending | 1 confirmed stock | 1 quoted (6k GHS) | 3 in-person quotes (5k GHS)
✅ Phase complete — all contacted

**Steering Rack Dealers**: 7 contacts | 2 inquiries sent | 2 pending | 1 price confirmed (2k GHS) | 1 hot lead (Dan - combo) | 1 in-person quote (1,700 GHS)

**Today's Action**:
• #4 Steering (+233 24 835 5104) — Inquiry prepared & queued for delivery

**WhatsApp Gateway**: DOWN since ~2026-05-23 (73+ days) — all inquiries queued, not delivered

**Critical Gap**: No single supplier confirmed for BOTH steering conversion AND dashboard
→ Dan (+233 24 989 2219) is the hot lead for combo service

**Next Run**: Prepare inquiry for steering #1 (+233 24 824 4333)

---
*Inquiry message (casual Ghanaian English):*
"Morning, I dey find Kia Rio steering rack + RHD→LHD conversion. You get am? Need price for rack + ends, whether you fit do the conversion, and if you fit change dashboard too. I ready come collect if price sweet me. Let me know ASAP."*"""

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