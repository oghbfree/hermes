# 1b Setup Checklist — Meta Click-to-WhatsApp Ads (2Real Enterprises)

**Owner:** H (CEO) · **Prepared:** 12 Oct 26 · **CTA number:** WhatsApp **0204252252**
**Purpose:** Step-by-step setup for the FIRST paid WhatsApp ad campaign. Hand to whoever runs your Meta Ads Manager.
**Companion:** `campaign-launch-playbook.md` (Part 5 = strategy; this file = execution).

---

## PHASE 0 — PREREQUISITES (H only — needs Meta login)

- [ ] **Meta Business Manager account** exists and is verified
      → business.facebook.com → Settings → Business Info → verify business
- [ ] **Facebook Page** for 2Real Enterprises (the anchor for ads + Marketplace)
- [ ] **Ad account** created under the Business Manager
      → Business Settings → Accounts → Ad Accounts → Add → New ad account
- [ ] **Payment method** added to the ad account (MoMo / card)
      → Billing → Payment Settings → Add payment method
- [ ] **Two-factor authentication** enabled on the admin account (Meta requires it for ad spend)

---

## PHASE 1 — LINK WHATSAPP TO BUSINESS MANAGER (H only — the key step)

- [ ] Go to **Business Settings → Accounts → WhatsApp Accounts → Add**
- [ ] Enter **+233 20 425 2252** (the 2Real CTA number)
- [ ] Choose verification method — **SMS** or **voice call** — and enter the 6-digit code sent to that number
- [ ] Name the WhatsApp account: **"2 Real Enterprises"**
- [ ] Confirm the number shows **"Connected"** status
- [ ] (If the number is already on WhatsApp Business app) it stays usable — the Business Manager link enables CTWA ads
      → If not on WhatsApp Business app yet, install it first (free) and complete the Business profile

> ⚠️ **If 0204252252 is currently a plain WhatsApp/Business number, linking it to a Meta Business Manager for ads is non-destructive — chats keep working. Do NOT create a new number for ads; reuse 0204252252 so every conversation lands in one place.**

---

## PHASE 2 — BUILD THE CAMPAIGN (Ads Manager)

### Campaign level
- [ ] Ads Manager → **Create** → Choose objective: **Engagement → Messaging** (or "Conversations")
- [ ] **Messaging app:** WhatsApp
- [ ] Campaign name: `2REAL — CTWA — Weekend Special — Oct26`
- [ ] Budget: **Daily GHS 100** (start); set **Schedule: Sat + Sun only** for the test
- [ ] **No campaign budget optimisation** (CBO off) — control at ad-set level for the test

### Ad set level
- [ ] **Conversion location:** WhatsApp
- [ ] **Performance goal:** "Maximise number of conversations"
- [ ] **Audience:** Broad, no interest stacking
      - Location: **Accra Metropolitan + 40km radius** (covers Dome + Oyarifa + delivery zone)
      - Age: **25–55**
      - Language: English (Ghana)
      - Detailed targeting: **leave EMPTY** (creative is the targeting)
- [ ] **Placements:** Automatic (FB Feed, IG Feed, Reels, Stories) — **exclude Messenger**
- [ ] **Schedule:** Sat 00:00 → Sun 23:59 (Ghana time), recurring weekly

### Ad level (creative)
- [ ] **Format:** Single image (static beats video on Meta in 2026)
- [ ] **Creative:** the weekend-special still/composite from the current batch (already vision-QC'd)
- [ ] **Primary text:**
      ```
      🔧 This week's specials — real stock, real prices, ready now.

      • Direct Power Circular Saw 1200W — GHS 700
      • Bosch PST 650 500W — GHS 550
      • Ryobi 600W Jigsaw — GHS 600
      • Bauker Jigsaw 550W — GHS 500

      Dome walk-in or Oyarifa pickup • Accra delivery available.
      ```
- [ ] **Headline:** `Weekend Tool Specials — Order on WhatsApp`
- [ ] **Description:** `New stock • Quality checked • Fast delivery Accra`
- [ ] **CTA button:** **Send WhatsApp message**
- [ ] **Click destination:** `https://wa.me/233204252252` (pre-filled: "Hi 2Real, I saw your weekend special — ")
- [ ] Turn ON **"Send WhatsApp message"** deep link so the chat opens directly

> Ads Manager may auto-build the wa.me text from the linked number — if it asks for a WhatsApp message template, use a simple greeting: **"Hi! I want to order from the weekend special."**

---

## PHASE 3 — PRE-LAUNCH VERIFICATION

- [ ] **Auto-responder live** on 0204252252 (2-layer inquiry hook) — test by sending a WhatsApp to it yourself
- [ ] **Test the wa.me link** on your phone → confirm it opens a chat with 0204252252 with the pre-filled text
- [ ] **CTA 0204252252** matches every item/status/listing (no old 0233352252 anywhere)
- [ ] **Ad creative** shows the correct Jiji prices (verify against `jiji_listings_full.json`)
- [ ] **Payment method** is valid (no failed-payment warning in Billing)
- [ ] **Preview** the ad on Facebook feed + Instagram feed

---

## PHASE 4 — LAUNCH & MONITOR (first 72h)

- [ ] **Launch: Sat 17 Oct 00:00** (Ghana time) — first test run
- [ ] Check at **+24h:** impressions, chats opened, cost per chat
- [ ] **Kill rule:** any creative with ≥1,000 impressions and **0 chats** → pause it
- [ ] Check at **+72h (Mon):** total chats + any sales logged
- [ ] Log all chats→sales in `customer_leads.json`

### Success gates (from playbook)
| Metric | Target | Action if missed |
|---|---|---|
| Cost per chat | ≤ GHS 8 | Narrow audience, test new creative |
| Chats/day | ≥ 15 | Increase budget +20% only if ROAS > 3x |
| ROAS | ≥ 3x | Pause, re-target to repeat-buyer lookalike |

---

## PHASE 5 — SCALE (only after test passes)

- [ ] Scale **+20% max per move**, wait **3–5 days** between increases
- [ ] **Never +30%** (resets Meta's learning phase)
- [ ] Add a **retargeting ad set** — people who opened a chat but didn't buy (lookalike of purchasers)
- [ ] Rotate in the next batch of stills as they're produced (weekly 4:30 run)
- [ ] Move to **daily** running (not just Sat/Sun) once ROAS holds ≥3x for 2 weeks

---

## WHAT I (sat-nav) CAN DO vs WHAT NEEDS H

| Task | Who |
|---|---|
| Ad copy (primary text / headline / description) | ✅ sat-nav — draft ready |
| wa.me deep-link + pre-filled text | ✅ sat-nav |
| Creative selection + QC (weekend-special stills) | ✅ sat-nav |
| Campaign structure spec (budget/audience/objective) | ✅ sat-nav — in this file |
| Auto-responder verification | ✅ sat-nav |
| **Meta Business Manager login + account setup** | ❌ H only |
| **Link 0204252252 to Business Manager (SMS/voice code)** | ❌ H only (code goes to the phone) |
| **Add payment method** | ❌ H only |
| **Click "Publish" in Ads Manager** | ❌ H only |

---

## DELIVERABLES I CAN PREPARE NEXT (on request)
- [ ] Ready-to-paste ad copy — 3 variants (weekend-special, power-tools, adhesives) for A/B testing
- [ ] wa.me links per product category (pre-filled messages)
- [ ] Retargeting audience spec (purchaser lookalike build)
- [ ] Weekly ROAS tracker sheet (chats → sales → ROAS)
