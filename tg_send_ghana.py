import json, urllib.request, os

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

message = "[GHANA SUPPLIER DASHBOARD - Daily Status - June 9]\n\n"
message += "DASHBOARD SUPPLIERS (37 total)\n"
message += "- Inquiry Sent: 21 (#1-#22)\n"
message += "- Contacted: 1 (#10)\n"
message += "- CONFIRMED (stock): 1 (#25)\n"
message += "- QUOTED: 1 (#35 - 6,000 GHS)\n"
message += "- QUOTED IN PERSON: 3 (#38, #39, #40)\n"
message += "- Pending: 13 (#23-#24, #26-#34, #36-#37)\n"
message += "- Skip: 2 (#11 dup, #5 steering NOTED)\n\n"

message += "TODAY'S INQUIRY - #22 (+233 26 220 3611):\n"
message += '"Morning, I dey find Kia Rio dashboard. You get am for stock? I need price, whether na new or used, and how e take be. I ready to come collect if di price sweet me small. Kindly let me know ASAP."\n\n'

message += "!! WHATSAPP GATEWAY: DISCONNECTED (16+ days)\n"
message += "- 21 inquiries prepared since Apr 24 - 0 actually delivered\n"
message += "- Inquiry #22 queued, awaiting gateway reconnect\n\n"

message += "BEST PRICES (Dashboard - In Person):\n"
message += "- #38 Emmanuel (+233 24 417 4778): 5,000 GHS (Abossey Okai, 6/6/26)\n"
message += "- #39 Dan (+233 24 989 2219): 5,000 GHS (Abossey Okai, 6/6/26) [ALSO FITTER]\n"
message += "- #35 (+233 53 012 1872): 6,000 GHS (needs verification)\n\n"

message += "BEST PRICES (Steering - In Person):\n"
message += "- #40 Ebo (+233 55 613 6140): 1,700 GHS (Abossey Okai, 6/6/26)\n"
message += "- #2 (+233 53 093 9891): 2,000 GHS (rack + ends, NEW)\n\n"

message += "HOT LEAD: Dan (#39) is BOTH dashboard dealer AND RHD->LHD fitter\n\n"

message += "RED CRITICAL BLOCKERS:\n"
message += "1. WhatsApp gateway DOWN - 21 msgs undelivered (16+ days)\n"
message += "2. No supplier confirmed for BOTH steering conversion AND dashboard swap\n"
message += "3. Only 1 remote quote - in-person quotes now at 5k GHS\n"
message += "4. #25 confirmed stock, still no price\n\n"

message += "NEXT:\n"
message += "- Next run -> #23 (+233 54 251 7905)\n"
message += "- URGENT: Restore OpenClaw gateway (port 18789)\n"
message += "- Follow up #25 for price | Verify #35 quote\n"
message += "- Steering: Contact #3 and #4 for additional quotes\n"
message += "- Confirm with Dan (#39) on conversion + dashboard combo deal\n\n"

message += "[OK] Files updated: GHANA_SUPPLIER_RESEARCH.md (#22), supplier-tracker-state.json, daily report saved."

payload = json.dumps({
    "chat_id": "-1003784520976",
    "message_thread_id": 20,
    "text": message
}, ensure_ascii=False).encode("utf-8")

url = f"https://api.telegram.org/bot{token}/sendMessage"
req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json; charset=utf-8"}, method="POST")
with urllib.request.urlopen(req, timeout=15) as resp:
    result = json.loads(resp.read().decode("utf-8"))
    print(json.dumps(result, ensure_ascii=False, indent=2))
