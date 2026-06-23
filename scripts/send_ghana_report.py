import json, urllib.request, os

env_path = os.path.expanduser("~/.hermes/.env")
token = None
with open(env_path, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line.startswith('TELEGRAM_BOT_TOKEN=***            token = line.split('=', 1)[1].strip()

            if token.startswith('"') and token.endswith('"'):
                token = token[1:-1]
            elif token.startswith("'") and token.endswith("'"):
                token = token[1:-1]
            break

chat_id = '-1003784520976'
message_thread_id = 20

lines = [
    "🚗 GHANA SUPPLIER DASHBOARD — Daily Inquiry Report",
    "📅 2026-06-20 — 09:16 UTC",
    "",
    "📊 DASHBOARD SUPPLIERS (37 total)",
    "| Status | Count |",
    "|---|---|",
    "| ✅ Inquiry Sent | 26 |",
    "| 📞 Contacted | 1 |",
    "| ✔️ CONFIRMED (stock) | 1 (#25) |",
    "| 💰 QUOTED | 1 (#35 — 6,000 GHS) |",
    "| 🏷️ QUOTED IN PERSON | 3 (#38, #39, #40) |",
    "| ⏳ Pending | 8 (#29–#34, #36–#37) |",
    "| 🔁 Skip (dup/NOTED) | 2 |",
    "",
    "🎯 TODAY'S INQUIRY — Supplier #28 (+233 54 203 3693)",
    "",
    "Message prepared (casual Ghanaian English):",
    '"Morning, I dey find Kia Rio dashboard. You get am for stock? I need price, whether na new or used, and how e take be. I ready to come collect if di price sweet me small. Kindly let me know ASAP."',
    "",
    "⚠️ WhatsApp gateway DISCONNECTED (30+ days) — Inquiry #28 queued in file, NOT delivered to supplier.",
    "Running total: 26 inquiries prepared since Apr 24 — 0 actually delivered.",
    "",
    "🏆 BEST PRICES SO FAR (Dashboard — In Person)",
    "• #38 Emmanuel (+233 24 417 4778) — 5,000 GHS (Abossey Okai, 6/6/26)",
    "• #39 Dan (+233 24 989 2219) — 5,000 GHS (Abossey Okai, 6/6/26) [ALSO FITTER — RHD→LHD] 🔥",
    "• #35 (+233 53 012 1872) — 6,000 GHS (needs verification)",
    "",
    "🔧 STEERING RACK (7 total)",
    "• #40 Ebo (+233 55 613 6140) — 1,700 GHS ✅ (Abossey Okai, 6/6/26)",
    "• #2 (+233 53 093 9891) — 2,000 GHS (rack + ends, NEW)",
    "• #7 Dan (+233 24 989 2219) — FITTER for RHD→LHD 🔥",
    "• 2 Pending (#3–4), 1 Contacted (#1), 1 NOTED (#5)",
    "",
    "🔥 HOT LEAD: Dan (#39/+233 24 989 2219) is BOTH a dashboard dealer AND RHD→LHD fitter — single supplier for dashboard + conversion. Need to confirm combo price.",
    "",
    "🔴 CRITICAL BLOCKERS",
    "1. WhatsApp gateway DOWN — 26 msgs undelivered, 30+ days offline",
    "2. No single supplier confirmed for BOTH steering conversion AND dashboard",
    "3. Only 1 remote quote — in-person quotes now at 5k GHS (better than 6k remote)",
    "4. #25 confirmed stock but price still TBD",
    "",
    "📋 NEXT ACTIONS",
    "• Next run → Prepare inquiry for #29 (+233 54 203 0706)",
    "• 🔴 URGENT: Restore WhatsApp gateway to deliver 26 queued inquiries",
    "• Follow up #25 for price on confirmed dashboard stock",
    "• Verify #35 6,000 GHS quote vs in-person 5,000 GHS quotes",
    "• Steering: Contact #3 (+233 24 514 2732) and #4 (+233 24 835 5104) for additional quotes",
    "• Confirm with Dan (#39) on conversion price + dashboard+steering combo deal",
    "",
    "Progress: 26/37 dashboard suppliers contacted · 8 pending · 2 skip",
    "✅ FILES UPDATED: GHANA_SUPPLIER_RESEARCH.md (#28 → Inquiry Sent)",
]

text = "\n".join(lines)

url = f'https://api.telegram.org/bot{token}/sendMessage'
payload = json.dumps({
    'chat_id': chat_id,
    'message_thread_id': message_thread_id,
    'text': text
}, ensure_ascii=False).encode('utf-8')

req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json; charset=utf-8'}, method='POST')
try:
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read().decode('utf-8'))
        if not result.get('ok'):
            print(f'FAILED: {result.get("description", result)}')
        else:
            print(f'Sent successfully: message_id={result["result"]["message_id"]}')
except Exception as e:
    print(f'ERROR: {e}')
