# Padlock → WhatsApp Ad — Launch Plan (Option 1, repeatable-offer variant)

**Status:** Building on existing verified photos (H chose #3 — build now, swap to new photos later).
**Budget:** GH₵ 100/week · **CTA (hard rule):** `0204252252` everywhere.
**Guardrails:** real product photos only · real prices from Jiji (source of truth) · CTA only 0204252252 · pay-before · no invented claims/statistics/testimonials.

---

## Why padlocks/security (the repeatable offer)

One-off inventory can't scale a single item — but you have **81 units of padlock/security stock** across Master Lock + Magnum + Rolson (verified in `inventory_agent.json`, and confirmed live on Jiji). Padlocks are:
- **Repeatable** — you can sell them all year as stock turns.
- **Universal need** — every household, trader, shop, gate owner in Accra needs one. Clear buyer identity.
- **Good ticket (GHS 700–980)** + **recognizable global brand** (Master Lock) = credibility in the ad itself.
- **Cheap to ship** (small, light) — you cross-sell Gorilla + spray paint in-chat to raise basket value.

---

## The creative (build on existing verified photos)

We build **ONE primary ad** now (repeatable + cheap to iterate). All 3 photos verified on disk.

### Ad 1 — Master Lock Long Padlock 50mm (GHS 700)
- **Image:** `photos/7571372.jpg` (real, 24 KB, existing) → *swap in H's new photo later if better*
- **Headline:** "Master Lock PADLOCKS — From GHS 100"
- **Primary (front-loaded hook):** "Master Lock padlocks & security locks — genuine UK stock. Models from GHS 100. Message us on WhatsApp and tell us what you need; we confirm stock + price & arrange collection from Dome."
- **CTA button:** **Send WhatsApp Message** → `0204252252`
- **Identity angle (Andromeda rule):** broad Ghana targeting; copy does the targeting (traders, shops, gates, landlords, motorbike owners).

### Backup/B-side creatives (swap-rotate weekly to feed the algorithm)
- **Ad 2 — Master Lock 2 Padlocks One Key Strength 4 140t (GHS 100)** → cheapest entry point = friction-free first chat. Image `photos/8646626.jpg`. Headline "PADLOCKS FROM GHS 100 — Master Lock".
- **Ad 3 — Master Lock Key Safe 5414D (GHS 650)** → security-conscious angle. Image `photos/14504270.jpg`.
- **Ad 4 — Master Lock Select Wall-Mounted Key Safe (GHS 980)** → premium/trades angle. Image `photos/16713224.jpg`.

> Rule: rotate 1 creative/week. Kill any creative at 2× its weekly budget share with zero WhatsApp start.

---

## The in-chat first reply (headline-mirror — the ad promise equals the chat intro)

When a buyer taps the ad → WhatsApp opens to `0204252252`. The first bot reply must answer the ad.
(Reuses the tightened auto-responder — confirm product-query routing is live before launch.)

- **If they ask about padlocks / "still available?":**
  > "2Real Enterprises. Yes — Master Lock padlocks from GHS 100. Which size are you after — a single 50mm padlock (GHS 700) or the 2-in-1 one-key set (GHS 100)? I'll confirm stock and arrange collection from Dome."
- **Cross-sell (once engaged, same chat — do NOT push before they answer):**
  > "Also in stock while you're here: Gorilla super-glue/tape from GHS 100 and Halfords spray paint from GHS 130 — worth grabbing with your lock."
- **Objection (pay-before / delivery):**
  > "Pay on confirmation by MoMo or cash at pickup. Small items we can send by Yango/Bolt — delivery at a small fee."
- **Generic (any ad message not matching):** "Thanks for reaching 2Real Enterprises! Which item are you asking about? I'll confirm availability."

---

## Budget & structure (GH₵ 100/week)

- **75% (GHS 75)** → single "Catalog → WhatsApp" campaign, objective **Conversations/Linked messages**, one ad set, Ghana broad, the 4 padlock creatives.
- **25% (GHS 25)** → reserve for the winning creative's scale + 1 new creative/week.
- **Cost-cap** per WhatsApp start (set a cap so we never blow the weekly envelope while learning).
- **Kill rule:** any creative >2× its budget share with zero WhatsApp start → swap it.
- **Scale rule:** when a creative demonstrably turns a WhatsApp chat into a sale (pay-before), shift budget to it and scale +20%/48h.

---

## Pre-launch checklist (hard)

- [ ] **CTA = `0204252252`** on every creative + in-chat (no other number).
- [ ] **Photos = real existing** `photos/<id>.jpg` (verified) — swap H's new shots in after if better.
- [ ] **Prices = live Jiji prices** re-verified the day of launch.
- [ ] **Auto-responder tightened + live** — confirms the ad's product, no canned "saved your number" pings.
- [ ] **FB account unlocked + verified** (H confirmed 02/11) before spend.
- [ ] No invented claim/stat/testimonial anywhere in copy or creative.
- [ ] Kill/scale rules above in place before the campaign goes live.

---

## Swap-to-new-photos path (when H shoots better shots)

Images are keyed by listing id (`photos/7571372.jpg` etc.). When H's new photos arrive:
1. Copy new file over the same id filename in `photos/`.
2. Re-render the same creative template (same copy — no cost).
3. Relaunch that creative. One-line swap, no restructure.

---

## Next action (on H's "go")
1. Stage the 4 verified photos + write the 4 creatives' final copy.
2. Have **content-buddy (Kofi)** apply the static template + spec-check (text <20% frame, spec sizes).
3. **Present the creatives for H's approval** (no posting).
4. On approval: build the campaign in Meta Ads Manager (or walk H through it), CTA→WhatsApp `0204252252`, GH₵ 100/wk cost-capped.