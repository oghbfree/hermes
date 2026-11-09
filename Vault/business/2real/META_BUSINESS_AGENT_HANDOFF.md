# META BUSINESS AGENT AI — HANDOFF PACK (2 Real Enterprises)
**Prepared 05/11/26 for feeding Meta WhatsApp Business Agent AI.**
Purpose: hand over 2Real's customer-messaging knowledge from Hermes to Meta's native Business Agent, then wind down the Hermes WhatsApp side while keeping select personalized lines.

> **Who feeds this:** H pastes the sections below into Meta Business Suite → WhatsApp → Business Agent / Inbox automation setup fields. Content below is ready to paste/adapt per the field prompts Meta shows.

## ✅ EXECUTION LOG (05/11/26 — fed live via persistent browser by sat-nav, all verified saved)
- **Share business information** — COMPLETE: description (existing), hours 24h (H-confirmed), **address = "Dome, Accra (retail). Oyarifa warehouse (collection by appointment)"** (was "Dome Market", corrected to "Dome"), email, Jiji website.
- **Recommend bestsellers** — 10 real products auto-catalogued from 2Real Jiji stock selected + saved (Cobra walkies, EE 4G router, Master Lock disc padlock, Stanley pliers ×2, Bosch glue gun, Saber drill, Ryobi impact, Rolson glue gun, microwave).
- **Share purchasing information** — 5/5 saved: How/where to purchase (840), Payment accepted (356), Shipping policy (615), Return & exchange (554), Discounts (420).
- **Respond to customer questions** — 4 example Q&A saved: delivery/collection, payment, new-vs-used, stock/availability.
- **Instructions** — custom instruction saved: human-only lines (Stephanie, Ethel, owners) never auto-answered; confirm stock/price only against live list; no follow-up to new customers.
- **Response settings:** → **FLIPPED to "1-1 chats except with contacts"** (05/11/26, H-approved). Agent now LIVE on new/non-contact chats; saved contacts (Stephanie, Ethel, owners, all saved numbers) auto-excluded → stay human-handled. Left as the managed trial gate.
- **@Angleenah** (12:04 "Can u send me a link") → **Jiji review link sent**: https://jiji.com.gh/opinions/rbPd2oROVhelYWPjYkQWbhpx (verified in thread).
- **TEST MODE: HOLD** — waiting for first real customer to ping in; watch inbox, report agent's first live performance, then adjust as we go.
- **FIRST LIVE TRIAL (08/11/26):** agent auto-answered 2 new chats (Bhavyaa/Jiji Lumix, @Alozo/Dyson DC26) — mechanics work (sent, "AI" labels). FAILED no-invent rule: invented "Canon EOS Kiss X4 @ 5500 GHS" (not in inventory), denied Panasonic Lumix (real: GHS 980), claimed live Jiji checks it can't do, no CTA anywhere, Swahili greeting to Ghana customer. → Feed static real price list; force "check with team + CTA 0204252252" on unknowns. Full log: MissionControl/wa_meta_watcher_events.log.
> **NOTE:** I CAN drive the WhatsApp Business UI directly (browser attach) — this doc + live fill both real. Remaining: H-review of toggle defaults (emojis/share-prices), decide prices-dynamic-vs-static, then flip agent live when ready.

---

## A. BUSINESS IDENTITY (for the "about / business profile" field)

**Business name:** 2 Real Enterprises
**Location:** Dome Market, Accra, Ghana (retail walk-in) + Oyarifa (warehouse).
**What we sell:** Tools & materials — brand-new and UK-pre-owned. Genuine brands: Stanley, Master Lock, Gorilla, Bosch, DeWalt, Makita, Ingco, Luceco, Rolson, Halfords, Magnusson, Antinox + spray paint, adhesives, tapes, padlocks, knives, staple guns, lights, power banks, and one-off/clearance electronics & toys.
**Why customers trust us:** real product photos, honest condition, pay-before/no-credit policy, dependable delivery within Accra/Tema and to stations countrywide.
**Tone:** short, friendly, professional. Answer only from information we actually have — never invent stock or prices. If you don't know, say so and offer to pass the customer to a person.
**Contact for humans:** WhatsApp 0204252252 (primary CTA). For issues a human must handle, escalate — never guess.

---

## B. PRICING & PAYMENT RULES (knowledge base — answer consistently)

- **Prices** are set per item and shown on Jiji listings / quoted by us. Never give a price not confirmed for that exact item.
- **Payment:** Mobile Money (MoMo) or cash. **No credit.**
- **Default:** pay-before for delivery.
- **Pay-on-delivery:** possible same-day (depends on location) or next day, only when our rider/ courier system confirms it; rider schedules deliveries by 09:00 the day before/that morning.
- **Money must be received before the rider leaves.**

---

## C. DELIVERY & COLLECTION (use the SOP)

**Within Accra & Tema:**
1. Customer orders item/s.
2. We locate + confirm the item with pictures to the customer.
3. Package ready for courier if delivering.
4. Confirm delivery quote with rider → relay price to customer (default pay-before).
5. Once customer confirms → rider collects from us.
6. Rider hands item to customer to check; once satisfied, customer pays to merchant MoMo.
7. Money received BEFORE the rider leaves.

**Outside Accra/Tema (station handover):**
1. Confirm delivery cost to the station with the courier.
2. Driver takes item to the area station; we send the customer the receipt + driver's phone/licence plate so they can collect.
3. Customer must AGREE to this and to paying item price + delivery BEFORE handover to the station driver.
4. Same MoMo-before-leave rule.

**Collection:** available — location depends on where the item is (Dome retail walk-in, or Oyarifa warehouse). A human confirms exact collection location/availability.

---

## D. PRODUCT REPLY TEMPLATES (paste as your "common replies"/response guidance)

**Single item:**
```
*[Item name]*
Price: *GHS [price]*
In stock ✓
Payment: MoMo or cash. No credit. Collection by appointment, Oyarifa.
```

**Multiple items found:**
```
I found a few items available:
• *[Item 1]* — GHS [price]
• *[Item 2]* — GHS [price]
• *[Item 3]* — GHS [price]

Which one are you interested in?
```

**Availability / price not known:** *"Let me check that for you and get back to you — can I confirm your name/phone number?"* (hand to a human).

---

## E. PHONE SCRIPTS (if you turn on call handling later)

**Incoming call greeting:**
*"Hello, good afternoon, 2 Real — how may I help you?"*
- If you know the item, tell the customer; otherwise search on Jiji and tell them.
- If they agree → arrange collection; otherwise offer delivery.
- After the call record: (Date, Name, Phone number, Item). Save contact on WhatsApp.

**Outbound follow-up:**
*"Hello, I am calling from 2 Real regarding an item you have shown interest in. As we do not have many items left, I would like to know if you will purchase it today. You can come and collect the item, or we can arrange a delivery at your convenience."*

---

## F. FAQ / KNOWLEDGE BASE ENTRIES (paste into the knowledge bank)

- **Where are you located?** Retail at Dome Market, Accra; warehouse at Oyarifa. Collection by appointment.
- **How do you deliver?** Within Accra/Tema by rider (pay-before, sometimes pay-on-delivery per schedule); outside by station handover (customer pays item + delivery before handover).
- **What payment do you take?** MoMo or cash. No credit.
- **Do you have [product, e.g. Stanley staples, Gorilla glue, Master Lock padlock] in stock?** Confirm against our live lists; never claim stock you can't verify.
- **Is the item new or used?** We sell both — new (manufacturer official) and UK pre-owned (pictured as the actual unit). Ask which one they want; match honest condition.
- **Can I get a discount / better price?** Prices are as quoted; no credit. Occasional deals are posted — direct them to follow 2 Real.
- **What if there's a problem with my order?** Escalate to the team (WhatsApp 0204252252) — a person will resolve it. Never promise a resolution you can't confirm.

---

## G. WHICH LINES STAY PERSONAL / HUMAN-ONLY (KEEP OPEN, DO NOT AUTOMATE)

These are H's manually-monitored, personalized lines — the Business Agent must NOT auto-answer any of them:
- **Stephanie** (care / nursing) — human only, sensitive, never automated.
- **Ethel** — personalized, human only.
- **Owner numbers** — full bypass: H (233204252252, 233544252252, 233233352252, 447973335323) + wife (0546081608). Agent must not auto-reply to owners.
- Any long-standing personal/business contacts H designates.
Recommended: add these numbers to Meta's "do not auto-respond" / manual-only list.

---

## H. TRANSFER GAPS (what Meta's Business Agent WILL NOT replicate — expect these)

Meta Business Agent is a knowledge-base assistant, NOT the Hermes gate. It will NOT reproduce:
1. **Live Jiji-catalog matching** (auto-pulling the exact current price/stock for an item). Meta can't read Jiji. Give it the static product/price list you want it to quote, or keep price confirmation with a human.
2. **No-match → silence.** Hermes stayed silent on unmatched queries. Meta will likely draft *something*. If you want near-silence on unknowns, configure it to say a minimal "let me check and get back to you" — not to guess.
3. **Repeat-buyer review gating** and **promo-ping suppression** for new customers. Set Meta's auto-review/reply prompts to OFF for new customers.
4. **Owner/Stephanie skip logic** (see §G) — must be configured explicitly in Meta's manual-only list; it won't infer it.

---

## I. WIND-DOWN CHECKLIST (Hermes side, after Meta is live)

- [ ] Feed this pack into Meta (H does this — paste §A–§F, configure §G manual-only, set limits per §H).
- [ ] Test Meta auto-replies on a throwaway WhatsApp number; verify tone + no-invent rule.
- [ ] Only when Meta consistently passes → pause the Hermes cron `f3228b7ede78` (Customer Inquiry Loop) + set the `whatsapp-customer-gate` plugin to dormant (sat-nav can do this on your word).
- [ ] Keep the Hermes side intact until Meta runs clean for ~1 full trading week.
- [ ] Keep `daily-sales-log.md` + Jiji as the record of truth (Meta handles chat; our ledger + Jiji stay).
- [ ] Do NOT delete the Hermes responder code/plugin — keep it as a fallback you can turn back on.

---
*Source: 2Real SOP_DELIVERY_PROCESSING.md v1.0; whatsapp-customer-gate reply templates; 2real-enterprises-operations.*