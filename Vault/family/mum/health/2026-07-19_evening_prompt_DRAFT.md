# Evening Check-in Prompt — DRAFT (not yet posted)

**Date:** 2026-07-19
**Target:** Telegram topic 4 (Health Log Mum), chat `-1003784520976`
**Status:** ⚠️ NOT POSTED — cron session lacked a terminal/exec tool and the bot token
is stored in a secret file (`~/.hermes/.env`) blocked from read tools.

---

## Message to post

🌆 Good evening — Comfort (Mum) evening check-in

Hope the evening is calm and comfortable. A few quick things to help us keep track of her day:

🍽️ Dinner — has she eaten? What did she have?
💊 Evening medications — taken? Any missed or skipped?
🤕 Any pain, discomfort, or issues to note?
⚡ Energy & mood — how is she feeling tonight?
📝 Overall — how was her day today?

Thank you for looking after her! 🙏

---

## How to post (where a terminal is available)

A ready-to-run script is at:
`~/.hermes/workspace/Vault/family/mum/health/evening_checkin_2026-07-19.py`

Run:
```
python ~/.hermes/workspace/Vault/family/mum/health/evening_checkin_2026-07-19.py
```
It reads `TELEGRAM_BOT_TOKEN` from `~/.hermes/.env` and posts the above to topic 4.
