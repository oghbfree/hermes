---
title: Farm Cron Jobs — Automated Operations
created: 2026-06-29
linked_workflow: FARM_WORKFLOW.md
---

# 🤖 Farm Cron Jobs — Automated Operations

All jobs use `workdir: "C:/Users/User/.hermes/workspace/Vault/business/farm"` and deliver to `telegram:-1003784520976:14` (Agent Hermes thread) unless noted.

---

## 1. Morning Prompt — Farm Lead Check-In
**Job ID**: `farm-morning-prompt`
**Schedule**: `30 6 * * *` (6:30 AM daily)
**Prompt**:
> You are the morning prompt for the Senya Beraku farm lead (Ben/Eastwood).
> 
> **SEND THIS EXACT MESSAGE to WhatsApp group "Farm Ops" (or individual):**
> 
> ```
> 🌅 FARM MORNING CHECK — {{date}}
> Reply with:
> 1. Pond level (cm):
> 2. Drains: flowing / blocked at [where]:
> 3. Goats: present / missing — last seen:
> 4. Crops waterlogged: [beds] — action taken:
> 5. Pump: off / running [hrs]:
> 6. Staff present: [names]
> 7. Today's priority task:
> ```
> 
> Log their reply to `farm/daily/{{date}}.md` under "## Morning Check".
> If no reply by 8:00 AM, alert H on Telegram: 📵 **NO MORNING CHECK** — Farm lead silent. Call now.

---

## 2. Evening Log Compilation
**Job ID**: `farm-evening-log`
**Schedule**: `30 18 * * *` (6:30 PM daily)
**Prompt**:
> Compile the daily farm log to Obsidian.
> 
> **Steps**:
> 1. Read WhatsApp messages from "Farm Ops" group since 6:00 AM today.
> 2. Extract: morning check, midday harvest/sales, evening check, notes.
> 3. Write/append to `farm/daily/{{date}}.md` using the template in FARM_WORKFLOW.md.
> 4. If morning or evening check missing, add **⚠️ MISSING** flag in log.
> 5. Deliver summary to Telegram: "✅ Daily log saved: {{date}} — Harvest: X kg, Sales: GHS Y, Pond: Z cm, Issues: [list]"

---

## 3. Weekly Review (Sunday)
**Job ID**: `farm-weekly-review`
**Schedule**: `0 9 * * 0` (Sunday 9:00 AM)
**Prompt**:
> Generate the weekly farm review.
> 
> **Read**: All `farm/daily/YYYY-MM-DD.md` from past 7 days.
> **Write**: `farm/weekly/YYYY-WW.md` with:
> 
> ```markdown
> # Weekly Farm Review — Week {{week_num}} ({{date_start}} to {{date_end}})
> 
> ## 📊 Harvest Summary
> | Crop | Total kg | Avg Price (GHS/kg) | Revenue (GHS) |
> |------|----------|-------------------|---------------|
> | Tomato | | | |
> | Pepper | | | |
> | Plantain (bunches) | | | |
> | Coconut (pcs) | | | |
> | Other | | | |
> **Total Revenue**: GHS
> 
> ## 💰 Expense Summary
> | Category | Amount (GHS) |
> |----------|-------------|
> | Labor | |
> | Feed | |
> | Fuel | |
> | Inputs (seeds, organic spray) | |
> | Repairs | |
> | Training | |
> **Total Expenses**: GHS
> 
> ## 💧 Water System
> - Pond level trend: Start {{start_cm}} cm → End {{end_cm}} cm
> - Rainfall total: {{total_mm}} mm
> - Drainage issues: [list]
> - Irrigation hours: {{hrs}}
> 
> ## 🐐 Livestock
> - Goats: [status, health, feed, housing progress]
> - Missing/stolen: [incidents]
> 
> ## 🐝 Apiary
> - Hive inspections: [count]
> - Honey harvest: [kg]
> - Training progress: [Kanzoni/Kwasi]
> 
> ## 🌱 Crop Health
> - Waterlogging incidents: [beds, severity, action]
> - Pest/disease: [crop, issue, treatment]
> - Mulch coverage: [beds done / total]
> 
> ## 👥 Staff Performance
> - Ben: [days present, tasks completed, issues]
> - Eastwood: [days present, tasks completed, issues]
> - Kalidou replacement: [status]
> 
> ## 🎯 Next Week Priorities
> 1. [Priority 1]
> 2. [Priority 2]
> 3. [Priority 3]
> 
> ## 🚨 Escalations to H
> - [Any item needing owner decision/funds]
> ```
> 
> Deliver the review to Telegram thread 14 (Agent Hermes).

---

## 4. Pond Level Monitor (Twice Daily)
**Job ID**: `farm-pond-monitor`
**Schedule**: `0 6,18 * * *` (6:00 AM, 6:00 PM)
**Prompt**:
> Check farm pond level.
> 
> **If sensor data available** (future): Read sensor → log.
> **Current (manual)**: Prompt farm lead via WhatsApp:
> ```
> 🌊 POND CHECK — {{date}} {{time}}
> Reply: Pond level (cm):
> ```
> 
> **Thresholds**:
> - > 150 cm: **OVERFLOW RISK** → Alert H: "🌊 POND HIGH: {{level}} cm. Check overflow pipe. Dig emergency spillway if needed."
> - < 30 cm (dry season): **LOW** → Alert H: "💧 POND LOW: {{level}} cm. Conserve water. Prioritize high-value crops."
> 
> Log to `farm/daily/{{date}}.md` under "## Pond Level".

---

## 5. Market Price Fetch (Tue/Thu)
**Job ID**: `farm-market-prices`
**Schedule**: `0 7 * * 2,4` (Tue/Thu 7:00 AM)
**Prompt**:
> Fetch current Senya/Kasoa market prices for farm crops.
> 
> **Method**: Ask Eastwood/Ben to do quick market walk or call contacts.
> **Send WhatsApp to Farm Ops**:
> ```
> 💰 MARKET PRICE CHECK — {{date}}
> Reply with current prices (GHS):
> - Tomato (kg):
> - Pepper (kg):
> - Onion (kg):
> - Plantain (bunch):
> - Coconut (pc):
> - Maize (kg):
> - Sweet potato (kg):
> - Honey (kg):
> ```
> 
> Log to `farm/daily/{{date}}.md` and `farm/finance/prices.md`.
> Alert H if any crop price < production cost (estimated: tomato GHS 12/kg, pepper GHS 18/kg).

---

## 6. Apiary Check (Tuesday)
**Job ID**: `farm-apiary-check`
**Schedule**: `0 7 * * 2` (Tuesday 7:00 AM)
**Prompt**:
> Kanzoni Tuesday check-in — bee status.
> 
> **Send WhatsApp to Kanzoni** (+233 24 895 7794):
> ```
> 🐝 APIARY CHECK — {{date}}
> 1. Hives active: [count]
> 2. Honey ready to harvest: [kg / none]
> 3. Queen status: [seen / not seen / cells]
> 4. Pests: [wax moth / ants / beetles / none]
> 5. Water source: [ok / need refill]
> 6. Kwasi training needed: [yes / no — what topic]
> ```
> 
> Log to `farm/apiary/hive-LOG.md`.
> If no reply by 10:00, alert H.

---

## 7. Weekly Finance Summary (Friday)
**Job ID**: `farm-finance-weekly`
**Schedule**: `0 18 * * * * * 5` (Friday 6:00 PM)
**Prompt**:
> Weekly farm P&L summary.
> 
> **Read**: `farm/daily/` logs for Mon–Fri this week + `farm/finance/prices.md`.
> **Calculate**:
> - Revenue by crop (harvest kg × market price)
> - Expenses by category (from daily logs)
> - Net cash flow
> - Cash on hand (from Zobase / WhatsApp records)
> 
> **Deliver to Telegram**:
> ```
> 💰 FARM WEEKLY P&L — Week {{week_num}}
> Revenue: GHS {{revenue}}
> Expenses: GHS {{expenses}}
> Net: GHS {{net}}
> Cash: GHS {{cash}}
> 
> Top crop: {{crop}} (GHS {{amount}})
> Biggest cost: {{category}} (GHS {{amount}})
> 
> ⚠️ Flags: [any crop selling below cost, cash < 2 weeks expenses, unpaid labor]
> ```

---

## 8. Dry Season Prep Trigger (Annual)
**Job ID**: `farm-dry-season-prep`
**Schedule**: `0 9 1 11 *` (Nov 1, 9:00 AM)
**Prompt**:
> **DRY SEASON PREPARATION CHECKLIST ACTIVATED**
> 
> Create `farm/dry-season-prep-{{year}}.md` with:
> 
> ```markdown
> # Dry Season Prep — {{year}}
> 
> ## 🌊 Water Security
> - [ ] Pond at max capacity (target 150+ cm)
> - [ ] Pond shade cloth installed (reduce evap 60%)
> - [ ] Treadle pump tested + hose no leaks
> - [ ] Drip tape laid for 500 m² min
> - [ ] Mulch all beds 15 cm (cocoa husk / coir / grass)
> - [ ] Vetiver hedges established on all contours
> - [ ] Zai pits dug for tomato/pepper beds
> 
> ## 🐐 Livestock
> - [ ] Goat housing complete (raised slatted floor, shade, water tank, lock)
> - [ ] Dry season feed stockpiled (3 months: grass, moringa, leucaena, crop residue)
> - [ ] Mineral lick + deworming done
> 
> ## 🐝 Apiary
> - [ ] Hives strong (5+ frames brood) going into dry
> - [ ] Water stations at apiary (shallow, stones for bees)
> - [ ] Kwasi monthly visits scheduled
> 
> ## 🌱 Crops
> - [ ] Dry season nursery: tomato, pepper, onion, cabbage, lettuce
> - [ ] Early maize planted (irrigated)
> - [ ] Sweet potato vines multiplied for planting
> - [ ] Moringa/leucaena coppiced for mulch + fodder
> 
> ## 💰 Finance
> - [ ] 3 months operating cash reserved
> - [ ] Input procurement done (seeds, organic spray, drip parts)
> ```
> 
> Deliver checklist to Telegram with 🚨 **DRY SEASON PREP STARTED** — 90 days to ready.

---

## 9. Staff Accountability Check (Mon/Wed/Fri)
**Job ID**: `farm-staff-check`
**Schedule**: `0 8 * * 1,3,5` (Mon/Wed/Fri 8:00 AM)
**Prompt**:
> Staff presence verification.
> 
> **Check**: WhatsApp "Farm Ops" for morning check-ins from Ben/Eastwood on scheduled days.
> - Ben: expected daily
> - Eastwood: expected Mon/Wed/Fri (2x/week minimum)
> 
> **If missing 2+ consecutive scheduled days**:
> Alert H: 👤 **STAFF ABSENT**: {{name}} missing {{days}} days. Last contact: {{date}}. Backup: [Ben calls replacement / you authorize temp hire].
> 
> Log to `farm/staff/attendance-{{year}}-{{month}}.md`.

---

## 10. Goat Search Alert (Until Resolved)
**Job ID**: `farm-goat-search`
**Schedule**: `0 8,12,16 * * *` (8 AM, 12 PM, 4 PM daily — **pause when goats found**)
**Prompt**:
> Goat search follow-up.
> 
> **Send to Eastwood/Ben/WhatsApp group**:
> ```
> 🐐 GOAT SEARCH — {{date}} {{time}}
> Any sightings? Checked: [locations]
> Police/unit committee notified: [yes/no]
> Finder's fee offered: GHS 50
> ```
> 
> If found: **PAUSE THIS JOB** and log to `farm/livestock/goats.md`.
> If not found after 7 days: Alert H with escalation options (replace, insurance claim, community meeting).

---

## 📋 Cron Creation Commands

Run these via `cronjob` tool or Hermes CLI:

```bash
# All jobs use workdir: "C:/Users/User/.hermes/workspace/Vault/business/farm"
# Deliver to: telegram:-1003784520976:14 (Agent Hermes thread)

# 1. Morning Prompt
hermes cron create --name "farm-morning-prompt" --schedule "30 6 * * *" --prompt "@farm-cron-jobs.md#1" --workdir "C:/Users/User/.hermes/workspace/Vault/business/farm" --deliver "telegram:-1003784520976:14"

# 2. Evening Log
hermes cron create --name "farm-evening-log" --schedule "30 18 * * *" --prompt "@farm-cron-jobs.md#2" --workdir "C:/Users/User/.hermes/workspace/Vault/business/farm" --deliver "telegram:-1003784520976:14"

# 3. Weekly Review
hermes cron create --name "farm-weekly-review" --schedule "0 9 * * 0" --prompt "@farm-cron-jobs.md#3" --workdir "C:/Users/User/.hermes/workspace/Vault/business/farm" --deliver "telegram:-1003784520976:14"

# 4. Pond Monitor
hermes cron create --name "farm-pond-monitor" --schedule "0 6,18 * * *" --prompt "@farm-cron-jobs.md#4" --workdir "C:/Users/User/.hermes/workspace/Vault/business/farm" --deliver "telegram:-1003784520976:14"

# 5. Market Prices
hermes cron create --name "farm-market-prices" --schedule "0 7 * * 2,4" --prompt "@farm-cron-jobs.md#5" --workdir "C:/Users/User/.hermes/workspace/Vault/business/farm" --deliver "telegram:-1003784520976:14"

# 6. Apiary Check
hermes cron create --name "farm-apiary-check" --schedule "0 7 * * 2" --prompt "@farm-cron-jobs.md#6" --workdir "C:/Users/User/.hermes/workspace/Vault/business/farm" --deliver "telegram:-1003784520976:14"

# 7. Finance Weekly
hermes cron create --name "farm-finance-weekly" --schedule "0 18 * * 5" --prompt "@farm-cron-jobs.md#7" --workdir "C:/Users/User/.hermes/workspace/Vault/business/farm" --deliver "telegram:-1003784520976:14"

# 8. Dry Season Prep
hermes cron create --name "farm-dry-season-prep" --schedule "0 9 1 11 *" --prompt "@farm-cron-jobs.md#8" --workdir "C:/Users/User/.hermes/workspace/Vault/business/farm" --deliver "telegram:-1003784520976:14"

# 9. Staff Check
hermes cron create --name "farm-staff-check" --schedule "0 8 * * 1,3,5" --prompt "@farm-cron-jobs.md#9" --workdir "C:/Users/User/.hermes/workspace/Vault/business/farm" --deliver "telegram:-1003784520976:14"

# 10. Goat Search (pause when resolved)
hermes cron create --name "farm-goat-search" --schedule "0 8,12,16 * * *" --prompt "@farm-cron-jobs.md#10" --workdir "C:/Users/User/.hermes/workspace/Vault/business/farm" --deliver "telegram:-1003784520976:14"
```

---

*Created 2026-06-29. Add to cron via tool or CLI. Each job references FARM_WORKFLOW.md for context.*