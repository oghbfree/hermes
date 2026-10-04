---
title: SOP — Messaging & Routing
date: 2026-10-03
tags: [sop, system, routing]
---

# SOP — Messaging & Routing
> Which message goes where; how agents send.

## Channels
- **WhatsApp:** H's number +233 20 425 2252 (owner). Staff/brand groups: WhatsApp Business. External voice rules in [[AGENTS_READ_FIRST]].
- **Telegram forum:** chat `-1003784520976` — topic 1 home channel · **topic 4 = Mum health** · topic 424 = nursing coordination · #urgent = urgent. Gateway bot: @Ogaitchhermesbot.
- **Send mechanics:** `hermes send --to telegram:<chat>:<topic> --file <txt>` · MEDIA: prefix for attachments · scripts `~/.hermes/telegram_direct_send.py` (token from `.env`, never echoed).

## Data flow
- Stephanie's daily reports (topic 4) → **@SATNAV** → **@harold** (local agent) → masters in `family/mum/health/` same day. Handoff brief: `family/mum/health/HAROLD_HANDOFF_MUM_HEALTH.md`.
- H questions in topic 4 route to the mum-health session; deep work (doctor summaries, research, consolidation) stays with Hermes sessions.

## Cron
- Live store: `AppData/Local/hermes/cron/` (the `.hermes/cron` + `workspace/cron` copies are stale — never edit).
- Delivery targets per job follow this SOP's channel table. Changes via `hermes cron` CLI, then verify by reading back jobs.json.
- **Never** contact anyone via cron/campaign without H's explicit instruction naming person + message.
