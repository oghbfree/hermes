---
title: SOP — 2Real Enquiry Handling
date: 2026-10-03
tags:
  - sop
  - business
  - 2real
---

# SOP — 2Real Enquiry → Order Flow (WhatsApp / Jiji / Zobaze)
> Trigger: any customer enquiry on WhatsApp, Jiji chat, or walk-in.

## Flow (same-day, zero drift)
1. **Log every enquiry** — channel, name, SKU, quantity, urgency → Enquiry Log (tracker). No enquiry unanswered >2h in working hours.
2. **Stock check** — Zobaze POS first (authoritative), then physical stock room. Quote from Zobaze SKUs/pricing only — never quote from memory.
3. **Quote** — price + availability + delivery estimate in ONE message. Payment = MTN MoMo (exact number from tracker, never improvised).
4. **Out of stock?** — 24h sourcing SLA: 3 quotes, post in the sourcing WhatsApp group, H decides. Tell customer "checking, reply within 24h".
5. **Order confirmed** → Orders Log (ID, payment status, rider) → dispatch booking (Yango/Bolt/Uber) → photo of packed item to customer → delivery confirmation call → log delivery.
6. **Close of day** → [[SOP-2REAL-DAILY-CLOSE]] — sales log reconciliation vs Zobaze (zero variance).

## Never-do
- Never give discounts — only H approves ("let me check with the boss" is the full authority).
- Never share business strategy/financials/supplier terms with anyone.
- Never give staff options lists — give direct instructions.
- Scope: 2Real retail/wholesale ONLY — Akoma, farm, construction, recruitment, personal admin are excluded; refer back to H.

## Escalation → H WhatsApp immediately, with template
- Complaint/damage, payment dispute, rider failure, stock discrepancy >0, media/Jiji issue. Templates: `Vault/jobs/` desk quickref.

## Tools
Zobaze POS (stock+price truth) · Jiji seller dashboard (16:00 block, [[SOP-2REAL-JIJI-DOMINANCE]]) · WhatsApp Business · MoMo · tracker `Vault/jobs/2real-daily-tracker` template · daily sales → `business/2real/daily-sales-log.md`