# JOHN — OFFICE JOB SPEC: 2 REAL ENTERPRISES
**Role:** Office Operations Coordinator (Oyarifa Home Office)  
**Location:** Home Office (Upstairs) / Stock Room (Downstairs) — Oyarifa  
**Reports To:** H (Owner)  
**Effective Date:** 2026-07-14  
**Review Cadence:** Weekly (Sundays 20:00) with H via WhatsApp call  
**Status:** ACTIVE — replaces prior broad "Operations Manager" scope

---

## 1. CORE MANDATE
**Own the office.** Single-threaded focus on:  
**Every call/enquiry logged → Every order collated → Every customer expectation managed → Every item confirmed (in stock or sourced) → Every order processed → Every sale logged → Every delivery tracked.**

No Akoma Robotics. No farm. No construction. No nursing recruitment. No facilitator coordination.  
**2 Real Enterprises only. Office + stock room. Full stop.**

---

## 2. PHYSICAL SETUP
| Zone | Location | Purpose | Your Desk |
|------|----------|---------|-----------|
| **Office** | Upstairs (Home Office) | Calls, laptop, Zobaze, Jiji dashboard, WhatsApp Business, order tracking spreadsheet, customer comms | **Your station** — laptop, headset, printer, stock sheets, delivery log |
| **Stock Room** | Downstairs | Physical inventory, packing, dispatch handover to riders | You go down → verify stock → pack → hand to rider → log dispatch |

**Rule:** Laptop stays upstairs. Stock stays downstairs. You move between them with intent — no loitering.

---

## 3. DAILY RHYTHM (NON-NEGOTIABLE)

| Time | Action | Output |
|------|--------|--------|
| **06:30** | Open laptop → Open Zobaze POS → Open Jiji seller dashboard → Open WhatsApp Business → Open **Daily Tracker Sheet** (Google Sheet: `2REAL_DAILY_TRACKER`) | Dashboard ready |
| **06:35–07:00** | **Morning Sweep** — Check overnight Jiji messages, WhatsApp enquiries, missed calls → Log every single one in **Enquiry Log** tab | 0 unread enquiries |
| **07:00–07:30** | **Stock Reconcile** — Walk downstairs → Spot-check top 20 SKUs against Zobaze → Note discrepancies → Update **Stock Availability** tab | Stock sheet current |
| **07:30–12:00** | **Active Enquiry Window** — Answer calls, reply WhatsApp, manage Jiji chats → For each: log → check stock → quote → confirm → process order → log sale → arrange delivery | All enquiries handled, orders in system |
| **12:00–13:00** | Lunch / Break | — |
| **13:00–16:00** | **Order Fulfilment Window** — Pack confirmed orders → Hand to riders → Log dispatch → Track deliveries → Confirm receipt → Log completion | Dispatch log complete |
| **16:00–17:00** | **Jiji Dominance Block** — Refresh top 20 listings, reply to all chats < 5 min, relist expired, adjust prices per Zobaze, push WhatsApp Status | Jiji dashboard green |
| **17:00–17:30** | **Daily Close-Out** — Update Daily Tracker: Enquiries | Sales | Dispatches | Deliveries | Stock Gaps → Send daily summary to H (WhatsApp) | Daily summary sent |
| **17:30** | Laptop shut. Day done. | — |

**No exceptions. No "I'll do it later."** If it's not in the tracker, it didn't happen.

---

## 4. CORE WORKFLOWS (STANDARD OPERATING PROCEDURES)

### 4.1 ENQUIRY LOGGING (Every Single One)
**Trigger:** Phone rings / WhatsApp pings / Jiji chat / Missed call  
**Action (within 2 min):**
1. Open **Enquiry Log** tab
2. Log: `Date/Time | Channel (Call/WhatsApp/Jiji/Walk-in) | Customer Name | Phone | Product/Enquiry | Urgency (Hot/Warm/Cold)`
3. Tag source: `Jiji` / `WhatsApp` / `Call` / `Walk-in` / `Referral`
4. **Immediate reply** (template): *"Thanks for reaching 2 Real Enterprises. I'm checking stock/price now — back in 5 mins."*

**KPI:** 100% of enquiries logged within 5 minutes. Zero "I forgot to log it."

---

### 4.2 STOCK CHECK & QUOTE (In-Stock)
**Process:**
1. Enquiry comes in → Check **Zobaze POS** (laptop) for SKU, price, qty
2. If **in stock (≥1)**: Quote Zobaze price immediately → "In stock, ready today. GHS ___."
3. If **low stock (1–2)**: Quote but flag *"Limited stock — confirm now to reserve"*
4. If **out of stock (0)**: Trigger **Out-of-Stock Sourcing** (4.3)
5. Log quote sent in Enquiry Log with timestamp

**No discount without H approval. Ever.** Standard reply: *"Let me confirm with the boss on any flexibility — back in 10 mins."*

---

### 4.3 OUT-OF-STOCK SOURCING (24-Hour SLA)
**Trigger:** Customer wants SKU not in stock (Zobaze = 0)  
**Process:**
1. Log in **Sourcing Log** tab: `Date | Customer | SKU/Description | Urgency`
2. **You have 24 hours** to source 3 comparables:
   - UK eBay (search, screenshot, convert GBP→GHS at current rate + shipping + 25% margin)
   - Direct manufacturer/distributor (email/call, get proforma)
   - Ghana competitor (Jiji/Jumia/physical shop — photo + price)
3. Post all 3 in **2 Real Sourcing WhatsApp Group** (you + H) with screenshots/links
4. **H sets final price** → You relay to customer
5. On confirmation → Place order → Track → Update customer every 24h until delivery

**KPI:** 100% of out-of-stock requests have 3 quotes in WhatsApp group within 24h.

---

### 4.4 ORDER PROCESSING (In-Stock)
**Trigger:** Customer confirms "Yes, I'll take it" + pays (MoMo/cash)  
**Process:**
1. Log in **Orders Log** tab: `Order ID | Date | Customer | SKU | Qty | Price | Payment Ref | Status: CONFIRMED`
2. Go downstairs → Pull item from stock room → Verify SKU/condition
3. Pack → Photo of packed item + label → Send photo to customer WhatsApp
4. Call rider (Yango/Bolt/Uber) → Hand over → Get rider name/phone/plate
5. Update Orders Log: `Status: DISPATCHED | Rider: ___ | Time: ___ | Tracking: ___`
6. Notify customer: *"Your order is with rider [Name], plate [XX], ETA ___ mins. Track: [link]"*

---

### 4.5 DELIVERY TRACKING & CONFIRMATION
**Process:**
1. Track rider via app → Confirm drop-off
2. **Call customer within 30 min of drop-off:** *"Package delivered — everything good?"*
3. Log in **Deliveries Log**: `Order ID | Delivered Date/Time | Rider | Customer Confirmed (Y/N) | Notes`
4. If issue (damage/wrong item/return) → Escalate to H immediately with photos
5. Update Orders Log: `Status: COMPLETED` or `RETURN/PROBLEM`

**KPI:** 100% delivery confirmation calls made. Zero "customer didn't receive" surprises.

---

### 4.6 JIJI DOMINANCE (Daily 16:00–17:00 Block)
**Goal:** Own the first page for our top 20 SKUs. Every chat replied < 5 min. Zero expired listings.

**Daily Checklist (16:00 sharp):**
- [ ] Refresh all 20 priority listings (bump/relist)
- [ ] Reply to **every** unread chat — target < 5 min response
- [ ] Check competitor prices on top 20 SKUs → Adjust ours if >5% gap (log change)
- [ ] Push 3–5 items to WhatsApp Status (photos + prices + "DM to order")
- [ ] Screenshot Jiji dashboard (views, chats, leads) → Paste in Daily Tracker
- [ ] Flag any "Out of Stock" listings → Take down or mark "Pre-order"

**Weekly (Sunday):** Export Jiji analytics → Compare views/chats/conversion vs prior week → Note in Weekly Review.

---

### 4.7 DAILY SALES LOGGING (Non-Negotiable)
**Every sale** (Jiji, WhatsApp, Walk-in, Referral) → Entered in **Zobaze POS** + **Daily Tracker → Sales Log** tab:
`Date | Order ID | Channel | Customer | SKU | Qty | Unit Price | Total | Payment Method | Rider | Status`

**Reconcile at 17:00:** Zobaze total = Tracker total. Discrepancy = find it before H sees it.

---

### 4.8 STOCK ROOM MANAGEMENT (Downstairs)
- **Weekly (Sunday 18:00):** Full cycle count of top 50 SKUs → Update Zobaze → Note variances
- **Daily (07:00):** Spot-check 20 SKUs (rotate)
- **Incoming stock:** You receive → Verify against PO → Update Zobaze → Shelve → Photo for records
- **Damaged/Expired:** Segregate → Photo → Log in **Write-Off Log** → Notify H before disposal
- **Layout:** Keep fast-movers at front, heavy/bulk at back, fragile on shelves. Label zones.

---

## 5. TOOLS & ACCESS (You Own These)

| Tool | Purpose | Your Responsibility |
|------|---------|---------------------|
| **Zobaze POS (Web)** | Inventory, pricing, sales entry | Daily entry, daily reconcile, stock accuracy |
| **Jiji Seller Dashboard** | Listings, chats, analytics | Daily dominance block, chat response, relist |
| **WhatsApp Business (2 Real line)** | Customer comms, orders, Status | 06:30–17:00 active, templates ready |
| **Google Sheets: `2REAL_DAILY_TRACKER`** | Single source of truth | Update live — Enquiries, Orders, Sales, Dispatch, Deliveries, Stock Gaps, Sourcing, Jiji Stats |
| **Yango/Bolt/Uber Apps** | Rider dispatch | Book, track, confirm |
| **MTN MoMo / Bank App** | Payment verification | Confirm every payment before dispatch |

**Laptop stays upstairs. Phone (WhatsApp/Jiji/Yango) goes with you downstairs.**

---

## 6. KPIs (Weekly Review with H — Sunday 20:00)

| KPI | Target | Measurement |
|-----|--------|-------------|
| **Enquiry Response Time** | < 5 min (WhatsApp/Jiji), < 2 rings (Call) | Tracker timestamp |
| **Enquiry Log Completeness** | 100% | Zero unlogged enquiries in weekly audit |
| **In-Stock Quote Accuracy** | 100% (Zobaze price) | Spot-check 10/week |
| **Out-of-Stock Sourcing SLA** | 3 quotes in 24h | Sourcing Log timestamp |
| **Order-to-Dispatch Time** | < 2 hours (in-stock) | Orders Log timestamps |
| **Delivery Confirmation Rate** | 100% customer call-back | Deliveries Log |
| **Sales Log Reconciliation** | Zobaze = Tracker (zero variance) | Sunday reconcile |
| **Jiji Response Time** | < 5 min avg | Jiji dashboard |
| **Jiji Listing Freshness** | 0 expired priority listings | Sunday audit |
| **Stock Count Accuracy** | ≤ 2% variance on top 50 | Weekly cycle count |

---

## 7. ESCALATION PROTOCOL

| Situation | Action | Timeline |
|-----------|--------|----------|
| Customer complaint (damage/wrong/late) | Photo → WhatsApp H immediately → Log in Tracker | < 15 min |
| Stock discrepancy > 2 units on fast-mover | Stop sales on that SKU → Count → WhatsApp H | < 30 min |
| Rider no-show / lost package | Call rider → Escalate to platform → WhatsApp H | < 15 min |
| Customer requests discount > 5% | "Let me check with boss" → WhatsApp H | < 10 min |
| Jiji account issue / listing removed | Screenshot → WhatsApp H → Jiji support | < 30 min |
| Payment dispute / MoMo failed | Screenshot → WhatsApp H → Do not dispatch | Immediate |

**Default:** When in doubt, WhatsApp H. Document in Tracker. Do not guess.

---

## 8. WHAT YOU DO NOT DO (Explicit Exclusions)

| Excluded Area | Owner | Your Action If It Comes Up |
|---------------|-------|----------------------------|
| Akoma Robotics (school enquiries, mBot, curriculum) | John (separate role) / H | "That's handled by the Akoma team — let me give you their number" |
| Farm operations (Senya, coconuts, irrigation) | Ben | Redirect to Ben |
| Construction projects | Construction PM | Redirect |
| Nursing/Financial Literacy recruitment | Recruitment team | Redirect |
| H's personal admin / family / travel | H / EA | Not your remit |
| Supplier negotiation (beyond sourcing quotes) | H | You source 3 quotes; H decides & negotiates |
| Major capital purchases | H | You research; H approves |

**If it's not in Sections 3–7, it's not your job.** Politely redirect.

---

## 9. WEEKLY REVIEW TEMPLATE (Sunday 20:00 — Send to H by 19:30)

```
## 2 REAL WEEKLY OFFICE REVIEW — Week Ending [DATE]

### 📊 ENQUIRIES
- Total logged: ___
- By channel: Call ___ | WhatsApp ___ | Jiji ___ | Walk-in ___ | Referral ___
- Conversion rate (enquiry → sale): ___%
- Avg response time: ___ min

### 💰 SALES
- Orders processed: ___
- Revenue (GHS): ___
- Top 5 SKUs: 1) ___ 2) ___ 3) ___ 4) ___ 5) ___
- Zobaze ↔ Tracker variance: ___ (target 0)

### 📦 DELIVERIES
- Dispatched: ___
- Delivered & confirmed: ___
- Issues/Returns: ___ (details)
- Avg dispatch-to-delivery: ___ hrs

### 📈 JIJI DOMINANCE
- Priority listings active: ___/20
- Avg chat response: ___ min
- Leads from Jiji: ___
- Conversion Jiji lead → sale: ___%
- Price adjustments made: ___

### 📦 STOCK
- Top 50 cycle count variance: ___%
- Stock-outs this week: ___ (SKUs)
- Sourcing requests: ___ | Completed: ___ | Pending: ___
- Write-offs: ___ GHS

### ⚠️ ISSUES / ESCALATIONS
1. ___
2. ___

### 🎯 NEXT WEEK FOCUS (Top 3)
1. ___
2. ___
3. ___
```

---

## 10. ONBOARDING CHECKLIST (First 3 Days)

| Day | Task | Done? |
|-----|------|-------|
| **Day 1** | Laptop set up: Zobaze, Jiji, WhatsApp Web, Google Sheets (`2REAL_DAILY_TRACKER`), Yango/Bolt/Uber apps | ☐ |
| **Day 1** | Walk stock room with H — learn layout, top 50 SKU locations, labelling system | ☐ |
| **Day 1** | Practice full cycle: Enquiry → Quote → Order → Dispatch → Delivery confirm (test order) | ☐ |
| **Day 2** | Run morning sweep solo → H spot-checks tracker at 07:30 | ☐ |
| **Day 2** | Run Jiji dominance block solo → H reviews dashboard at 17:00 | ☐ |
| **Day 3** | Full day solo → H reviews Daily Tracker at 17:30 | ☐ |
| **Day 3** | Sunday Weekly Review — you draft, H reviews | ☐ |

**Sign-off:** _________________ (John) _________________ (H)  Date: ___________

---

## 11. ACCOUNTABILITY

- **Daily Tracker** is the single source of truth. H has view access 24/7.
- **Sunday 19:30** — Weekly Review in H's WhatsApp. No exceptions.
- **Monthly (1st of month)** — Deep dive: trends, SKU profitability, channel mix, Jiji ROI.
- **Missed KPI 2 weeks in a row** → Formal performance conversation with H.
- **This spec replaces all prior "Operations Manager" scope for 2 Real.** Akoma/farm/construction/recruitment are separate roles.

---

**Document Version:** 1.0  
**Created:** 2026-07-14  
**Next Review:** 2026-07-21 (Sunday Weekly Review)  
**Location:** `/c/Users/User/.hermes/workspace/Vault/jobs/JOHN_OFFICE_JOB_SPEC_2026-07-14.md`