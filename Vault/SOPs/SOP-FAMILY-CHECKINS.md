---
title: SOP — Family Check-ins & Scheduled Messages
date: 2026-10-03
tags: [sop, family, cron]
---

# SOP — Family Check-ins & Scheduled Messages
> Trigger: cron check-ins (morning, goodnight, elder-care briefings) or H-requested messages.

## Active check-ins
- **Mum (Comfort, 92):** daily health logging per [[SOP-MUM-HEALTH-LOGGING]] · Telegram topic 4 · evening goodnight-call culture (protects her sleep → her BP).
- **Family goodnight (Ebony):** nightly warm WhatsApp message — scheduled, gentle, family tone.
- **Morning check-in (H):** scheduled morning briefing — system + day ahead, concise.
- **Elder care:** daily log verification + periodic weekly review briefings.

## Rules (all check-ins)
1. **Read before send:** real data from masters only — never canned content with stale numbers.
2. **One message, then stop** — no loops, no resends if unanswered.
3. Warm for family (Ebony, kids, mum); brief for ops (staff).
4. Delivery targets follow [[SOP-MESSAGING-ROUTING]]; cron edits verified by reading jobs.json back.
5. If a check-in fails (gateway/token), flag to H (#urgent if it's mum-care) — don't retry-loop.
