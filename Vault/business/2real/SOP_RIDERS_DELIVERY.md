# SOP: RIDERS & DELIVERY COORDINATION — 2 Real Enterprises

**Version:** 1.1 · **Absorbs:** SOP_DELIVERY_PROCESSING.md (base) + rider network + Yango/Uber + driver recruitment.
**Owner:** H · **CTA:** WhatsApp 0204252252

---

## 1. THE RIDER NETWORK (regulars)

| Rider | WhatsApp | Use for |
|-------|----------|---------|
| Bernard | +233 24 544 4141 | Standard Accra/Tema runs |
| Jerry | +233 54 041 8575 | Standard Accra/Tema runs |
| Eben | +233 24 757 5993 | Standard Accra/Tema runs |

- **Sunday-night availability check (auto):** the `2Real — Monday Rider Availability Check` cron
  fires **Sunday 19:00** → drafts a ready-to-send message for each rider asking if they're free
  **Monday 7:00–9:00 AM** + a rough price for within-Accra vs Accra→Tema. **H sends** the three
  messages from his phone (he is the only one with these contacts; the cron delivers drafts only).
- Collect their replies and note who's confirmed for the week — pick the cheapest/fastest confirmed.

## 2. THE DELIVERY FLOW (customer → rider / Yango / Uber)

1. **Customer says they want delivery** — get the item + price confirmed first.
2. **Pin the exact location** — within Accra/Tema, ask for the **nearest landmark** (e.g. "Kokomlemle, near Melcom," "Dome, by Total station"). A landmark, not just a town — riders navigate by landmarks in Accra.
3. **Get a price two ways (quote the lower):**
   - **Rider quote:** tell the rider the pickup (Oyarifa/Dome) + dropoff landmark → they give a price.
   - **Yango / Uber estimate:** input the trip in the app → **screenshot the result** → show/agree the fare.
4. **Relay the cost to the customer** — confirm they accept before dispatch.
5. **Dispatch** the confirmed rider (or book the Yango/Uber and confirm the driver takes it).
6. **On delivery: PAYMENT RULE DEPENDS ON RIDER TYPE (H's anti-loss policy, 19/10/26):**
   - **OUR OWN riders (Bernard, Jerry, Eben, Robert about the Oyarifa area): PAY ON DELIVERY IS ALLOWED.** They have patience to wait for the customer to pay before leaving, and they know us — they will hold the product until paid.
   - **Yango/Uber riders (no affiliation): PAY-BEFORE ONLY.** They have no patience/affiliation and may leave the product without payment, or not care if the customer is stealing. NEVER let a Yango/Uber rider take an item to collect payment at the door. The customer MUST pay (MoMo) BEFORE dispatch with any app rider.
   - **Default rule:** paid-in-full before dispatch for EVERY order; the ONLY exception is our own trusted riders who wait for payment on delivery (pay-before is the safe default; pay-on-delivery is a trust privilege for our own riders only).

## 3. RECRUITING DRIVERS (busy-season pipeline — Christmas)

**When a Yango/Uber driver delivers for us, recruit them.** We get busier around Christmas; building a
warm pool of known drivers now means dispatches don't stall in peak season.

**The one-liner (after a smooth delivery):**
> "You did well today, thanks. We deliver a lot around Christmas and we're building a list of reliable
> drivers — want me to add you? If you're free, we'll call you direct and you skip the app cut."

**Capture on a driver log** (`delivery-drivers.md`):
- Driver name · phone · app (Yango/Uber) · **home base location** (they asked you where they are so you
  can match to runs) · usual available hours · vehicle type · notes (reliability, took the run well).

**Why it matters:** app drivers on a *manual* referral run keep more of the fare (no app commission),
so they say yes — and you get a committed local fleet for the Christmas rush without surge pricing.

## 4. Sunday rhythm (tie-in)
- **Sunday 19:00** — rider availability check fires (this SOP's cron).
- Combine with the merged strategy's **Sunday = group adverts** — riders often have wide local networks;
  a rider who posts to a community group is a bonus distribution channel.

## Files
- Rider list + availability: keep in this doc.
- Driver recruitment log: `Vault/business/2real/delivery-drivers.md` (create on first recruit).
- Sales log: `daily-sales-log.md` (log delivery fees + rider used).