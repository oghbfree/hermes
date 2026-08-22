# 2Real Customer Interactions — Learning Log

This is the feedback loop. Every inbound customer WhatsApp (walk-in shop + Jiji)
is handled here: log the enquiry, the reply I sent in H's voice, and the outcome.
Over time this makes replies sharper, prices tighter, and closings faster.

## SOP (how I respond)
1. Inbound message arrives (dm_policy: open -> reaches me).
2. Classify: greeting | availability | price-quote | delivery | after-hours | negotiation | close.
3. Pull real price from inventory_agent.json (Zobaze) if the item is a known SKU.
   - Known SKU -> quote real price, leave small mobile room ([Y]).
   - Unknown item (NOT in Zobaze) -> reply: "That one's not in our system yet — we may just not have had time to add it. Let me check manually and revert to you." It may simply not be entered yet, NOT necessarily unavailable. Flag H to input/price/stock it in Zobaze; log + update. NEVER invent a price.
4. Reply in first person, formal-but-direct, NO bot prefix, NO metadata.
5. Append the interaction below. Ask H for a quick :+1:/-1 so I can tune.
6. If H corrects wording or price, update the reply bank (2real-whatsapp-replies.md).

## Open questions to resolve with H
- Auto-send vs draft-for-approval on first price quotes (recommended: auto-ack +
  holding reply for unknown items, real quote only from inventory).
- How to capture outcome (sale closed / ghosted / negotiated down).

---

## Log (newest first)

<!-- format:
### [DATE] [source: walk-in|jiji] — [classification]
- Enquiry: "..."
- Reply sent: "..."
- Outcome: pending | closed | ghosted | corrected
- Lesson: ...
-->

<!-- No real customer interactions logged yet. This file will populate as the WhatsApp
     gateway receives live inquiries. All test data from July 2026 has been cleared
     to ensure only real data is tracked. -->