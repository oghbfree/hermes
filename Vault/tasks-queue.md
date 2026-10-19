# \# TASKS\_QUEUE

# 

# \_Managed by TodoScribe. Last updated: auto-stamped on each save.\_

# 

# \---

# 

# \## Active

# <!-- tasks go here -->

# 

# \## Waiting On

# <!-- WAITING tasks go here -->

# 

# \## Backlog

# <!-- lower priority items -->

# 

# \## Done

# <!-- completed tasks â€” cleared weekly -->

## Active

* [ ] **[business | HIGH]** — Bring all tools home
  → Notes: Consolidate tools from the shop to home (per H 19/10/26)
  → Due: 2026-10-19

* [ ] **[business | HIGH]** — Sell big items cheap
  → Notes: Clear rotation: sell the big items at discounted price to free space/cash
  → Due: 2026-10-19

* [ ] **[personal | HIGH]** — Buy petrol
  → Notes: Fuel for the Kia / travel
  → Due: 2026-10-19

* [ ] **[personal | HIGH]** — Put dP on car
  → Notes: Car maintenance - dP (display panel?) needs installation
  → Due: 2026-07-12

* [ ] **[personal | HIGH]** — Check steering wheel bolts
  → Notes: Safety check - bolts on steering wheel need tightening
  → Due: 2026-07-12

* [ ] **[property | MEDIUM]** — Erect shelves
  → Notes: Shelving installation needed
  → Due: not specified

* [ ] **[property | MEDIUM]** — Check upstairs items for warehouse
  → Notes: Sort through upstairs items to identify what can move to warehouse
  → Due: not specified

* [ ] **[business | MEDIUM]** — List love seat for sale online
  → Notes: Post love seat on marketplace (Jiji/FB Marketplace)
  → Due: not specified

* [ ] **[construction | MEDIUM]** — Speak to Patrick about moving wood step
  → Notes: Coordinate with Patrick to move wood step to dome
  → Due: not specified
  → Flags: [WAITING: Patrick]

* [ ] **[family | MEDIUM]** — Call Naa
  → Notes: Check-in call
  → Due: not specified
  → Flags: [WAITING: Naa]

* [ ] **[family | MEDIUM]** — Call Nicholas
  → Notes: Check-in call
  → Due: not specified
  → Flags: [WAITING: Nicholas]

* [ ] **[family | MEDIUM]** — Call Jnr
  → Notes: Check-in call
  → Due: not specified
  → Flags: [WAITING: Jnr]

* [ ] **[family | MEDIUM]** — Call H and N
  → Notes: Check-in call
  → Due: not specified
  → Flags: [WAITING: H and N]

* [ ] **[property | MEDIUM]** — Check air conditioning
  → Notes: Inspect A/C system
  → Due: not specified

* [ ] **[business | LOW]** — Contact Mike
  → Notes: Business follow-up
  → Due: not specified
  → Flags: [WAITING: Mike]

* [ ] **[business | LOW]** — Contact Henry
  → Notes: Business follow-up
  → Due: not specified
  → Flags: [WAITING: Henry]

* [ ] **[business | LOW]** — Contact Eric
  → Notes: Business follow-up
  → Due: not specified
  → Flags: [WAITING: Eric]

* [ ] **[business | LOW]** — Contact Verse
  → Notes: Business follow-up
  → Due: not specified
  → Flags: [WAITING: Verse]

* [ ] **[finance | HIGH]** — Deposit in bank
  → Notes: Bank deposit needed
  → Due: 2026-07-17
  → Flags: [REVIEW]

* [ ] **[property | MEDIUM]** — Get bolts for Mom's table
  → Notes: Hardware for Mom's table repair
  → Due: not specified
  → Flags: [WAITING: Mom]

* [ ] **[property | MEDIUM]** — Get screws for small hanger
  → Notes: Hardware for small hanger installation
  → Due: not specified

* [ ] **[personal | LOW]** — Fix golf bag
  → Notes: Golf bag repair needed
  → Due: not specified

* [ ] **[construction | MEDIUM]** — Weld big hanger
  → Notes: Welding required for big hanger
  → Due: not specified

* [ ] **[business | MEDIUM]** — Call Julio to pick up heaters
  → Notes: Coordinate heater pickup with Julio
  → Due: not specified
  → Flags: [WAITING: Julio]

* [ ] **[personal | MEDIUM]** — Call Kwasi for iron and ironing board
  → Notes: Arrange iron and ironing board with Kwasi
  → Due: not specified
  → Flags: [WAITING: Kwasi]

---

Tasks Queue - Updated 2026-04-25 03:10

## Critical System Blockers (WhatsApp/Google/Vector DB)

* \[x] Configure memory embedding provider (currently 'google' unknown) to ensure vector DB sync works properly
* \[x] Configure Google Sheets authentication (missing sheets scope for oghbfree@gmail.com). Run: gog auth add oghbfree@gmail.com --services sheets
* \[ ] Link WhatsApp Web session: openclaw channels login --channel whatsapp --account 233204252252 (scan QR)



## Pending Actions from John's Meeting Notes

### High Priority (Starred Items)

* \[ ] **20% commission on sales** - Set up for 3rd parties
* \[ ] **Operational procedures** - Need to be documented and implemented
* \[ ] **VAT payment** - Outstanding, government has made adjustments
* \[x] **Tax Cron** - Need to set up automated tax tracking

### Medium Priority

* \[ ] **WhatsApp Broadcast blacklist** - Investigate why broadcasts are being blocked, test with small group
* \[ ] **iPhone 13 repairs** - Screen: 450, Back cover: 600, Battery: 250, Bypass: 600 (John's phone camera not good)
* \[x] **Jiji Pro Sales analysis** - Cost (1400gh/month for 1500gh credit) not working out, evaluate alternatives
* \[x] **Stanley blades** - Request 100 pieces for shopping list
* \[ ] **Nurses CV** - Send links/CV as requested

### Business Operations

* \[ ] **Akoma Robotics** - Zion Intl no demos, 50 out
* \[x] **Ring light for Jiji pics** - Need to stage products properly
* \[x] **Zobase links** - Ensure links on Jiji and WhatsApp
* \[ ] **FB Marketplace VPN issues** - Resolve
* \[x] **Web due** - Price, advertising for Akoma

### 2026-04-28 07:43 - WhatsApp Delivery Failures

* **Kanzoni check-in**: Failed  target 233248957794 not in allowFrom policy
* **Sammy morning strategy**: Failed  no active WhatsApp Web listener
* **Status**: WhatsApp gateway reconnected at 07:35 but Web listener still inactive
* **Blocked**: All WhatsApp outbound comms blocked until Web session is linked

### 2026-04-28 08:11 - Field Intel (John) Delivery Failed

* Skill: john\_field\_intel
* Target: 233233352252 (WhatsApp)
* Reason: No active WhatsApp Web listener
* WhatsApp gateway flapping (status 408)  reconnected at 08:05
* Status: All WhatsApp outbound blocked until Web session re-linked
2026-04-29 | 07:02 | Person: Sammy | Morning strategy | Status: FAILED - WhatsApp Web listener inactive
2026-04-29 | 08:00 | System: job\_application\_processor | Status: FAILED - Google Sheets auth missing
2026-04-29 | 08:19 | Person: John | Field intel | Status: FAILED - WhatsApp Web listener inactive
2026-04-30 | 08:02 | Person: John | Field intel | Status: FAILED - WhatsApp Web listener inactive (Day 3)

## Meeting Topics - 2026-05-05 Morning

* SOPs: ask where he saved the compiled SOPs
* Nurses: discuss/update
2026-05-05 | 22:07 | Cron: ebony-goodnight | Status: FAILED - No active WhatsApp Web listener on any account
2026-05-07 07:49 \[sammy-morning-check] FAILED - WhatsApp channel not connected (no active listener). Telegram alert sent.
2026-05-07 | 08:14 | Person: John | Field intel | Status: FAILED - No active WhatsApp Web listener (Day 8)

2026-05-07 | 09:51 | Cron: jnr-payment-reminder | Status: FAILED - Jnr (+447****5361) not in WhatsApp allowFrom policy. Telegram alert sent.

2026-05-08 | 15:45 | Cron: sammy-business-check-1600 | Status: SENT | Message: End-of-day business inquiry sent to Sammy (+233****2253) via WhatsApp. Awaiting reply.

## 2026-05-10 10:04 - Dad Checkin Failed
Job: checkin-dad - No active WhatsApp Web listeners.

2026-05-11 | 07:02 | Cron: sammy-morning-check | Status: FAILED - No active WhatsApp Web listener (Day 12)

---
## Cron Failure: john-field-check
**Time:** 2026-05-11 08:03 UTC
**Job:** f8b0ca3a-e434-45b7-84d6-3e524bd90e0c
**Status:** FAILED
**Reason:** No active WhatsApp Web listener (account: 233204252252)
**Action Required:** WhatsApp needs to be re-paired before this cron can execute.

## 2026-05-11 15:46:29 - SAMMY_EOD_CHECK_FAILED
- **Cron**: 8f2a7345-9474-4d1e-a0be-a3c9c3e47df2 (sammy_sales_check)
- **Error**: WhatsApp not connected (account: 233204252252)
- **Target**: Sammy (+233****2253)
- **Urgency**: RED FLAG — daily sales cycle disrupted
- **Action**: Re-link WhatsApp via CLI

2026-05-12 | 21:16 UTC | Cron: kanzoni-tuesday-check | Status: FAILED
Reason: +233****7794 not in WhatsApp allowFrom policy
Action: Alert sent to #urgent. Number needs allowlist update.

## Mum Check-In Failed (2026-05-13 12:19)
- **Cron:** checkin-mum (719215be)
- **Issue:** WhatsApp not paired (233204252252)
- Mum (Comfort) was due a check-in about health, mood, and needs

[2026-05-13 11:22 UTC] ? Cron John Field Check FAILED — WhatsApp listener not active (account 233204252252). Re-link required: openclaw channels login --channel whatsapp --account 233204252252.

2026-05-13 12:23 UTC | Cron: jnr-payment-reminder (2c464532) | Status: FAILED
Reason: WhatsApp Web not connected (no active listener on any account). Jnr (+447****5361) unreachable.
Action: Re-pair WhatsApp - openclaw channels login --channel whatsapp --account 233204252252

- [ ] **Sammy End-of-Day Check** (2026-05-13) — WhatsApp offline. Send Sammy: "Sammy, how was business today? Let me know the sales total and what moved well. Also confirm Zobase is updated."

2026-05-15 | 20:24 UTC | Cron: sammy-morning-check (bff58fed) | Status: FAILED
Reason: WhatsApp channel not connected (no active listener). Day 15+ of WhatsApp outage.
Target: Sammy (+233****2253)
Action: Re-link WhatsApp - openclaw channels login --channel whatsapp --account 233204252252
## [2026-05-15 20:37] FAILED: janet-friday-checkin (cron ab8cf20c) — WhatsApp channel unavailable. Target: Janet (+233****1608). Needs re-send when WhatsApp recovers.
Janet Friday check-in: +233****1575. Needs WhatsApp re-send. Queued 2026-05-15 20:37

---
## Brain Dump Extracted — 2026-06-04 05:05 UTC (Topic 8)

* [ ] **business | HIGH** — Send offer letter to Stephanie
  → Notes: Priority for today. Employment offer letter for Stephanie (nurse/care role).
  → Due: 2026-06-04

* [ ] **family | HIGH** — Check with Mum's UK doctor for odema prescription
  → Notes: Mum (Comfort) has swelling in feet/legs. Need prescription for odema management in Ghana.
  → Due: 2026-06-04

* [ ] **family | HIGH** — Order mattress from AliExpress for delivery
  → Notes: Mattress needed for Mum's room in Weija. Priority for today.
  → Due: 2026-06-04

* [ ] **business | MEDIUM** — Manually WhatsApp all suppliers from dashboard
  → Notes: Dashboard file needs to be retrieved. Then manually message all suppliers via WhatsApp.
  → Due: not specified

* [ ] **tech | MEDIUM** — Set up daily data scraping and briefing system
  → Notes: User wants examples of data to scrape, search queries to use, and daily briefing content based on business knowledge. Memory should be made available for this.
  → Due: not specified

* [ ] **tech | LOW** — Retrieve and review supplier dashboard file
  → Notes: Dashboard file needs to be located and reviewed before supplier outreach.
  → Due: not specified