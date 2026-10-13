# 2Real Campaign Launch Playbook — FB Marketplace + WhatsApp Catalog

**Owner:** H (CEO) · **Prepared:** 11 Oct 26 · **CTA everywhere:** WhatsApp 0204252252
**Grounding:** daily-sales-log.md (through 10/10/26), jiji-ghana-optimisation, ads playbook, content engine (4:30 run)

---

## PART 1 — WHEN TO START (optimum timing)

### The decision: sequence, don't launch both at once
Launch **WhatsApp Catalog FIRST**, then **FB Marketplace** 1–2 weeks later. Rationale:
- WhatsApp Catalog is **zero-cost, instant, uses your existing WhatsApp base** and the documented 500-ads Status pipeline. Fastest first win.
- FB Marketplace needs listing photos + a small boost budget + a cadence to maintain. Higher setup cost — do it second, once WhatsApp is producing.

### Optimum launch windows (grounded in your real sales data)
| Signal | What your data shows | Action |
|---|---|---|
| **Strong days** | Tue (3,090), Wed (2,170), Sat (1,620), Sun Jiji (1,120) | Launch campaigns so they're live + boosted **before the weekend** |
| **Weekend retail** | Sat 10/10 = 1,620; Sunday Jiji works | **Launch Thursday/Friday** so the Sat–Sun push is live |
| **Payday cycle** | Ghana monthly payday ~25th–month-end | **Schedule campaign kickoff to land the week after payday** (highest disposable income) |
| **Content readiness** | 4:30 run produces the weekly batch | **Launch at the START of a fresh content week** so catalog + content stay in sync |
| **Container/walk-in** | Mon 05/10 caught container traffic (630) | Monday = restock/refresh listings day |

### Recommended launch date
**Launch WhatsApp Catalog: Thursday 15 Oct 26** (payday-week, live for the Sat 17/10 weekend push — the weekend special reel is already queued for the 4:30 run).
**Launch FB Marketplace: Thu 22 or Thu 29 Oct** (after WhatsApp is producing; reuse the same weekend-special assets).

---

## PART 2 — HOW TO LAUNCH & PROCEED

### A. WhatsApp Catalog (launch first)

**Setup (day 1–2):**
1. Populate the Catalog from **Jiji = source of truth** (`jiji_listings_full.json`, active status only) — NOT Zobaze.
2. Group by category: Adhesives / Power Tools / Mechanic's Tools / Office & IT / Consumables.
3. Every item: real Jiji price, real photo from Jiji listing, CTA **WhatsApp 0204252252**.
4. Turn on the WhatsApp auto-responder (the 2-layer inquiry hook already handles price/stock replies).

**Launch cadence (the 500-ads Status pipeline):**
- **60% product posts** (item + price + CTA)
- **20% social proof** ("Just sold 3 of these — 2 left")
- **10% bundle deals** ("Any 3 spray paints for GHS 80")
- **10% new arrivals / restock alerts**
- Every Status → "DM or order on Jiji: [link]" → TOP+-boosted listing.

**Proceed rules:**
- Post 2–3 Status ads/day, timed to **peak WhatsApp usage** (12–2pm lunch, 6–9pm evening).
- **Bulk-buyer broadcast** (0245849519, the 1,870 mechanic) — add to a broadcast list, send value-first "what's on YOUR bench" restock alerts.
- Track: catalog views → WhatsApp DMs → sales logged in `customer_leads.json`.

### B. FB Marketplace (launch second)

**Setup:**
1. Listings must **match on-disk captions** (Jiji prices) — the weekly batch stills are the listing photos.
2. Use the **weekend-special composite** (5-product layout, anchor price GH¢600) as the hero listing.
3. CTA **WhatsApp 0204252252** in every description.

**Launch cadence:**
- Post the weekly batch as listings each **Monday** (refresh) + **Thursday** (weekend push).
- **Boost the weekend special** with a small budget (start GHS 50–100/day, Sat–Sun only).

**Proceed rules (from the ads playbook):**
- **Creative is the targeting** — target broadly (Accra region), let the listing photos/headlines do the work. Don't stack interests.
- **Statics beat video** on Meta in 2026 — your stills are the right asset; don't over-invest in video.
- **Scale +20% max per move**, wait 3–5 days between increases. Never +30% (resets learning).
- **Kill rule:** if a listing gets impressions but 0 chats after 24h of boost → fix price/description/photo, don't keep boosting.

---

## PART 3 — THE WEEKLY CAMPAIGN LOOP (runs continuously)

```
MON  Restock/refresh listings + Monday container-traffic status
TUE  Content engine 4:30 batch lands → stage weekend assets
WED  WhatsApp Status ads (product + social proof mix)
THU  Launch/boost weekend special (FB boost + Status countdown)
FRI  Peak push — bundle deals + urgency
SAT  Weekend special live (biggest retail day)
SUN  Jiji Sunday push + recap; log all sales
```

**Cadence guardrails:**
- Content engine (4:30) owns generation. Kofi stages copy. Taiwah drafts in-character. sat-nav builds/QC.
- **Jiji = source of truth** for every price/stock claim. Never quote Zobaze.
- **CTA 0204252252 everywhere.**
- Every sale logged in `daily-sales-log.md` + `customer_leads.json`.
- **Add trending sound at publish** for all reels (in-app, platform library).

---

## PART 4 — MEASUREMENT & KILL RULES

| Metric | Health target | Action if failing |
|---|---|---|
| WhatsApp catalog views → DMs | >5% view-to-DM | Improve Status copy/photo, change timing |
| FB listing impressions → chats | 0 chats after 24h boost | Fix price/description/photo, stop boost |
| Weekend special ROAS | >2x on boosted spend | Scale +20%; else kill boost, test new creative |
| Bulk-buyer broadcast reply rate | >10% | Segment list, send value-first not sales-first |
| Blended daily revenue | ≥ GHS 1,000/day | Shift mix toward proven categories (adhesives, tools) |

**3-hour founder review (monthly):** H reviews the actual numbers — not agent summaries. Data → confidence → speed.

---

## READY-TO-RUN CHECKLIST (before Thu 15 Oct launch)
- [ ] WhatsApp Catalog populated from Jiji (active items only, real prices)
- [ ] Auto-responder live (2-layer inquiry hook)
- [ ] Weekend-special reel queued in 4:30 run (already done)
- [ ] Weekend-special still + composite ready (already done, vision-QC'd)
- [ ] Bulk-buyer broadcast list built (0245849519 + any repeat buyers)
- [ ] CTA 0204252252 confirmed on every item/status/listing
- [ ] FB Marketplace account/boost payment method ready (for the 22 Oct launch)

---

## PART 5 — 1b: PAID WHATSAPP ADS (Meta Click-to-WhatsApp)

### The direct answer: YES, WhatsApp has paid ads
Paid WhatsApp advertising = **Meta Click-to-WhatsApp ads** (run in Meta Ads Manager, NOT inside the WhatsApp app). You cannot "boost" a WhatsApp Status or catalogue item with money directly in WhatsApp — paid reach happens on Facebook/Instagram/Reels, and the ad's CTA button opens a WhatsApp chat with 2Real. This is separate from the free WhatsApp Business catalogue + Status pipeline (which your crons already run).

### What you need to start (setup checklist)
1. **Meta Business Manager** account (the FB page you post Marketplace listings from is the anchor).
2. **WhatsApp Business number linked** to the Business Manager — **0204252252** (the CTA number). Link it: Business Manager → WhatsApp accounts → add number → verify with the code sent to that number.
3. **A payment method** on the ad account (MoMo/card) + a **daily budget**.
4. **Ad creative** — reuse the weekend-special still/composite (statics beat video on Meta in 2026; your vision-QC'd stills are ready).

### Campaign structure (proven, cheap, Ghana-appropriate)
- **Objective:** "Conversations" (optimise for WhatsApp message opens) — this is the correct objective for Click-to-WhatsApp.
- **Budget:** start **GHS 50–100/day**, Sat–Sun only (matches your biggest retail days). ~GHS 1,200–2,400/month.
- **Audience:** broad, Accra region + 20–50km radius around Dome/Oyarifa. **No interest-stacking** — creative is the targeting.
- **Placement:** Facebook + Instagram feeds + Reels (auto). Skip Messenger.
- **CTA button:** "Send WhatsApp message" → opens chat with 0204252252 → your 2-layer auto-responder answers price/stock instantly (already built).
- **Creative rotation:** rotate the 4 batch stills; kill any ad with 0 chats after 24h.

### Expected economics (grounded in your data)
- Meta Click-to-WhatsApp in Ghana typically **GHS 2–8 per chat open** on a broad Conversations objective (cheap — it's an underused objective).
- At GHS 100/day you'd expect **~15–40 chats/day** → with your proven conversion (bulk buyer dropped 1,870; Eric bought 1,020), even a 10% chat→sale rate at GHS 600 avg ticket = **GHS 900–2,400 in sales for GHS 100 in ads** → **ROAS 9–24x**. Strong.
- **Kill rule:** if blended ROAS < 2x after 2 weeks, pause and re-target (narrow to repeat-buyer lookalike) rather than raise spend.

### 1b launch timing
- **Setup (week of 12 Oct):** link 0204252252 to Business Manager, add payment method.
- **First paid run:** **Sat 17 Oct** (weekend special live) — run GHS 100/day Sat+Sun as the test.
- **Scale:** +20% max per move, 3–5 days between. Only scale if ROAS > 3x.

### 1b vs the organic crons (don't confuse them)
| | Organic (running now) | Paid 1b (NEW) |
|---|---|---|
| Where | WhatsApp app catalogue + Status | Meta Ads Manager (FB/IG/Reels) |
| Cost | Free | GHS 50–100/day budget |
| Reach | Your existing contacts/followers | New audiences (paid) |
| CTA | Status → DM/Jiji link | Ad button → WhatsApp chat |
| Owner | WhatsApp Catalogue Poster cron (09:00) | Manual/agent-managed campaign |
| Start | Already live | Sat 17 Oct test run |

### 1b ready-to-run checklist
- [ ] 0204252252 linked to Meta Business Manager (WhatsApp account)
- [ ] Payment method on ad account
- [ ] Weekend-special still/composite as ad creative (ready)
- [ ] "Conversations" objective campaign built (GHS 100/day, Sat+Sun, Accra broad)
- [ ] Auto-responder confirmed live on 0204252252 (already built)
- [ ] ROAS tracked: chats → sales logged in customer_leads.json