import json, urllib.request, os, sys

ENV_PATH = os.path.join(os.path.expanduser("~"), ".hermes", ".env")
token = None
with open(ENV_PATH, "r", encoding="utf-8") as f:
    for line in f:
        if "TELEGRAM_BOT_TOKEN" in line and "=" in line:
            token = line.strip().split("=", 1)[1].strip()
            break

if not token:
    print("ERROR: TELEGRAM_BOT_TOKEN not found in .env")
    sys.exit(1)

CHAT_ID = "-1003784520976"
THREAD_ID = "20"

text = (
    "📋 INTEGRATED DAILY SYNTHESIS — 2026-06-22\n\n"
    "🔴 CRITICAL (4):\n"
    "1. Fix WhatsApp bridge (BOM in openclaw/package.json + re-pair)\n"
    "2. Complete medical eval for H's head shock (Jun 12)\n"
    "3. Restore Comfort care log (6-day gap)\n"
    "4. Run manual backup (6 days stale)\n\n"
    "⚠️ HEALTH ESCALATIONS:\n"
    "• Comfort: BP 149/80 AM spike, severe insomnia, leg edema unchanged 5+ days, care log gap\n"
    "• H: Electrical shock Jun 12 unreviewed, 10-day health log gap, awaiting priority response\n"
    "• Dad: Evening check-in sent, afternoon failed — no clinical data today\n\n"
    "💼 BUSINESS:\n"
    "• Ghana: 27/37 suppliers contacted; #29 sent today; 0 delivered (WhatsApp down 60+ days)\n"
    "• Sammy/Jnr: Telegram fallback active, WhatsApp dead\n"
    "• Recruitment: 52 total, 0 new today; Charlotte Nortey top nurse priority\n"
    "• Content: June 21 generation done (11 images, 28 captions, 2 videos)\n\n"
    "🔒 SECURITY: 🔴 HIGH RISK — 3 FAIL, 7 WARN, 4 PASS\n"
    "• bws_cache.json 15+ plaintext keys, sensitive files world-readable, WhatsApp unpaired 55+ days\n"
    "• Google OAuth expired at 08:01 today; 16 backup .env copies; AGENTS.md BOM (new)\n\n"
    "🖥️ SYSTEM: Partial recovery today\n"
    "• ~25 cron jobs ran today. Successes: briefing, ghana inquiry, weekly review, kanban sync\n"
    "• Failures: mum-health-evening, health-check-evening, 2Real sync (12/14/16/18), security 18:04\n"
    "• Missing: daily-backup, cron-status-report, nightly-consolidation\n\n"
    "🎯 TODAY: Fix BOM → restore WhatsApp → run backup → complete H medical review\n\n"
    "Full report: workspace/memories/insights/INTEGRATED_INSIGHTS_2026-06-22.md"
)

payload = json.dumps({
    "chat_id": CHAT_ID,
    "message_thread_id": int(THREAD_ID),
    "text": text
}, ensure_ascii=False).encode("utf-8")

url = f"https://api.telegram.org/bot{token}/sendMessage"
req = urllib.request.Request(url, data=payload, headers={
    "Content-Type": "application/json; charset=utf-8"
}, method="POST")

try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        result = json.loads(resp.read().decode("utf-8"))
        if result.get("ok"):
            print(f"Sent successfully: message_id={result['result']['message_id']} thread={THREAD_ID}")
        else:
            print(f"Telegram error: {result}")
except Exception as e:
    print(f"Delivery failed: {e}")
