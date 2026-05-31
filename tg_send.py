import json, urllib.request, os

# Read token
env_path = os.path.join(os.path.expanduser("~"), ".hermes", ".env")
token = None
with open(env_path, "r", encoding="utf-8") as f:
    for line in f:
        if line.strip().startswith("TELEGRAM_BOT_TOKEN="):
            token = line.strip().split("=", 1)[1].strip()
            break

if not token:
    print("ERROR: token not found")
    exit(1)

message = """📊 Mum's Weekly Health Review — May 25-31, 2026

🔴 Red Flags
• WhatsApp check-in failed (May 27) - OpenClaw gateway DOWN, no bridge to reach Mum directly
• Chest pain episode (May 31) - slight mid-chest pain, resolved with water (likely oesophageal spasm/reflux). Recurrence >5 min or with radiating pain/sweating/SOB = A&E immediately
• Feet swelling persistent (May 31) - bilateral oedema unchanged from baseline CKD 3b
• XL cuff still not obtained - bicep 45cm, standard cuff gives unreliable readings. BP data this week (132/64 on May 23) may be inaccurate
• No vitals recorded since May 23 - 8 days without BP/pulse check
• Medication confirmation incomplete - Lasix (furosemide) and other meds not confirmed on May 31

🟡 Watch
• Appetite good all week - ate fully at every logged meal (breakfast May 23 & 31, dinner May 23)
• Diet appropriate - compliant with Dr Ferguson diet (vegan-leaning, no dairy/wheat/nuts). Hausa Koko, cocoa, Baldwin's Tincture all good
• Mood/cognition alert and responsive (May 31)
• Mobility stable - shuffling gait, no change from baseline
• Hip pain (bilateral, slight) - musculoskeletal/positional, monitor
• Housebound status permanent - social isolation risk

🟢 Good
• Full meals on all logged days (May 23: breakfast + lunch + dinner; May 31: breakfast)
• Baldwin's Tincture taken (May 31)
• Baldwin's Concoction taken (May 23)
• No acute deteriorations today
• BP 132/64 (May 23) within acceptable range for Comfort (HTN target <150/90 per NICE). Pulse 82 normal
• BNP normal (124, Mar 2026) - no heart failure

📈 Trends
• Logging improving vs early May - entries on May 23 (full day), May 27 (check-in attempted), May 31 (morning check with clinical detail)
• BP: Only one reading this week (132/64 on May 23). Previous was 138/78 (Mar 2026). Fluctuating pattern continues but latest readings acceptable
• Kidney function: eGFR 41 (Mar 2026, Stage 3b CKD). No new bloods this week - due for repeat U&E
• Oedema: Persistent bilateral - unchanged baseline. Needs Lasix compliance verification
• Weight/BMI: 87kg, BMI 39.2 - no change data this week

💡 Recommendations

1. Obtain XL/large cuff BP monitor ASAP - bicep 45cm makes standard cuff readings unreliable. Critical for accurate hypertension management.

2. Confirm Lasix administration - feet swelling is persistent. Carer should verify furosemide is being given daily and log it. If worsening oedema or SOB develops, admit immediately.

3. Chase nephrology follow-up - eGFR 41 (Stage 3b CKD), elevated phosphate (2.91), elevated ferritin (404). These need monitoring. Also chase elevated ferritin investigation (persistent since Aug 2024).

4. Restore WhatsApp bridge - OpenClaw gateway needs restart so direct check-ins with Mum can resume. Important for daily welfare checks.

5. Book diabetic annual review - flagged as due/ongoing since Mar 2026. HbA1c was at upper limit (41) - needs recheck."""

payload = json.dumps({
    "chat_id": "-1003784520976",
    "message_thread_id": 4,
    "text": message
}, ensure_ascii=False).encode("utf-8")

url = f"https://api.telegram.org/bot{token}/sendMessage"
req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json; charset=utf-8"}, method="POST")
with urllib.request.urlopen(req, timeout=15) as resp:
    result = json.loads(resp.read().decode("utf-8"))
    print(json.dumps(result, ensure_ascii=False, indent=2))
