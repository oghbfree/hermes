#!/usr/bin/env python3
import urllib.request, urllib.parse, json

with open("C:/Users/User/.hermes/.env") as f:
    for line in f:
        if line.startswith("TELEGRAM_BOT_TOKEN="):
            BOT_TOKEN = line.strip().split("=", 1)[1]

CHAT_ID = "-1003784520976"
THREAD_ID = "2"

text = """📊 Weekly Health Synthesis — 2026-06-16 to 2026-06-22

⚠️ No health log entries recorded this week. Most recent logs: Jun 9–12, 2026.

🔴 Red Flags:
• No entries for 10+ consecutive days — gap must not continue
• Unresolved follow-up on June 12 electrical shock — no med eval confirmed; no symptom monitoring logged
• Symptoms and energy completely unmonitored for full week

🟡 Watch:
• June 12 electrical shock still open — pending neuro eval; watch for headache, dizziness, confusion, nausea, vision changes
• No vitals (BP/pulse) recorded — baseline data gap
• Nutrition log silent — meal consistency cannot be confirmed

🟢 Good:
• Prior entries (Jun 9–12) showed balanced meals (fish, turkey, eggs, complex carbs)
• Supplement routine (Vit C, garlic, ACV) active as of May
• BP 118/76 logged June 1 — within normal range

📈 Trends:
• Energy: No data this period
• Nutrition: Cannot assess
• Symptoms: Cannot track

💡 Recommendations:
1. Resume daily health log immediately — even minimal entries
2. Prioritize medical follow-up for Jun 12 shock — neuro effects can be delayed
3. Have caregiver log meals, symptoms, and energy daily if possible"""

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
data = urllib.parse.urlencode({
    "chat_id": CHAT_ID,
    "message_thread_id": THREAD_ID,
    "text": text
}).encode("utf-8")

req = urllib.request.Request(url, data=data)
with urllib.request.urlopen(req) as resp:
    result = json.loads(resp.read().decode())
    print(json.dumps(result, indent=2))
