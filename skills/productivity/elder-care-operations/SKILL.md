---
name: elder-care-operations
description: End-to-end elder care operations for H's elderly parents — Comfort Blankson (mum, 91, Ghana) and Robert Herbert-Blankson (dad, 92, UK). Covers cron-scheduled health check-ins, care log management, Telegram topic routing, escalation paths, carer coordination, weekly health synthesis, structured care documents, hospital correspondence logging, and clinical meal planning. Triggered when H discusses either parent's care, health logs, carer hiring, nurse management, hospital letters, elder care business planning, or meal/diet planning for elderly parents.
version: 2.0.0
---

# Elder Care Operations

> Consolidated from `elder-care-operations` (mum) and `elder-care-dad` (dad). Both parents' care operations are now in this single skill with labeled subsections.

## Parents Overview

| | Mum | Dad |
|---|---|---|
| **Name** | Comfort Blankson | Robert Herbert-Blankson |
| **Age** | 91 | 92 |
| **Location** | Weija, Ghana | London, UK |
|| **Care skill** | elder-care-operations (this) | elder-care-operations (this — see Dad section below) |
| **Care log path** | `C:\Users\User\CARE_LOG_COMFORT_YYYY-MM.md` | `C:\Users\User\CARE_LOG_DAD_YYYY-MM.md` |
| **Structured doc** | (create if needed) | `FAMILY_INSIGHTS_DAD.md` |
| **Telegram topic** | 4 (health-log-mum) | 1 (health-log-dad) |

## Patient Profile

- **Name:** Comfort Blankson (Ms Blankson)
- **DOB:** 28 Aug 1934 (91 years)
- **NHS Number:** 4661817400
- **Location:** Weija, Ghana
- **Source System:** EMIS / Patient Access
- **Conditions:** Diabetes (controlled, HbA1c 41), CKD Stage 3b (eGFR 41), Hypertension (fluctuating), Bilateral leg oedema, Obesity (BMI 39.2), Mental health plan, Housebound
- **Budget:** ~6,000 GHS/month
- **Latest clinical data:** See `references/medical-record-review-comfort.md` (updated May 2026 from NHS records)

## Telegram Topic Routing

| Topic | ID | Purpose |
|-------|----|---------|
| health-log | 2 | H's personal health (3 daily checks — NOT currently active) |
| health-log-mum | 4 | Comfort's clinical care log (3 daily checks + weekly review) |

**Group:** `-1003784520976` (Hermes agent group)

## Cron Job Registry

| Job Name | Schedule | Job ID | Delivery |
|----------|----------|--------|----------|
| mum-health-morning | `4 8 * * *` (08:04 daily) | `8ba8c0c6a82f` | `telegram:-1003784520976:4` |
| mum-health-afternoon | `0 13 * * *` (13:00 daily) | `1c2103c267a6` | `telegram:-1003784520976:4` |
| mum-health-evening | `0 19 * * *` (19:00 daily) | `7ffb54b79331` | `telegram:-1003784520976:4` |
| mum-health-weekly-review | `6 9 * * 0` (Sunday 09:06) | `4f60c03655d0` | `telegram:-1003784520976:4` |

**⚠️ H Health Checks — Delivery Target Issue:**
The H health check jobs (morning/afternoon/evening) are configured to deliver to `telegram:123286468:2` (Home chat topic 2), NOT to the Hermes supergroup. This means H doesn't see the prompts in the supergroup where he actually interacts. If H reports not seeing health check prompts, this is the first thing to check. To fix: update the cron jobs to deliver to `telegram:-1003784520976:2` (Hermes supergroup topic 2).

| Job Name | Schedule | Job ID | Current Delivery | Should Be |
|----------|----------|--------|-----------------|-----------|
| health-check-morning | `4 8 * * *` | `ecb431eb971d` | `telegram:123286468:2` | `telegram:-1003784520976:2` |
| health-check-afternoon | `0 13 * * *` | `7b6f47df6a9a` | `telegram:123286468:2` | `telegram:-1003784520976:2` |
| health-check-evening | `0 19 * * *` | `c4818bab761b` | `telegram:123286468:2` | `telegram:-1003784520976:2` |
| health-weekly-synthesis | `6 9 * * 0` | `e5d89d644d51` | `telegram:123286468:2` | `telegram:-1003784520976:2` |

**⚠️ Migration Risk:** Cron jobs are lost during platform migrations (`.openclaw` → `.hermes`). If health checks stop, check `cronjob list` first — jobs may need recreation. Always verify after any migration or config reset.

**⚠️ Job Recreation (May 18, 2026):** The health check jobs above were recreated at 15:51 UTC on May 18. Old job IDs may still appear in historical logs. Always verify current IDs via `cronjob list`. The H health checks (topic 2) were also recreated with new IDs: `ecb431eb971d` (morning), `7b6f47df6a9a` (afternoon), `c4818bab761b` (evening).

## Care Log File

**Path:** `C:\Users\User\.hermes\workspace\CARE_LOG_COMFORT_YYYY-MM.md` (monthly files, workspace root)

**Also check:** `memories/health/mum/health-log.md` — this is where some care entries may be logged via Telegram topic 4 responses. The root CARE_LOG file is the canonical structured document; the memories/ path may have raw Telegram entries.

**Format:** See `references/care-log-template.md` for the full template.

**Sections per day:**
- Morning Check (breakfast, vitals, mood, mobility, meds)
- Afternoon Check (lunch, midday vitals, activity, meds)
- Evening Check (dinner, evening vitals, day summary, meds, sleep)
- Daily Summary (energy, pain, sleep, bowel/bladder, skin, notes)

## Check-In Templates

### Morning (08:04)
- Breakfast (what eaten/drank, appetite level)
- Morning Vitals (BP, pulse, temp, O2 sat)
- Mood & Cognition
- Mobility (independent? pain on movement?)
- Morning Medications

### Afternoon (13:00)
- Lunch (what eaten/drank, appetite, fluid intake)
- Midday Vitals (BP, pulse, temp)
- Mood & Energy
- Afternoon Activity
- Midday Medications

### Evening (19:00)
- Dinner (what eaten/drank, appetite)
- Evening Vitals (BP, pulse, temp, O2 sat)
- Day Summary (mood, pain, bowel/bladder)
- Mobility Today (any falls/near-misses)
- Evening Medications (any missed doses?)
- Sleep Readiness

## Red Flags — Immediate Escalation

- Vitals outside normal range (BP >160/100 or <90/60, pulse >100 or <50, temp >38°C)
- Missed medications (especially diabetes/BP meds)
- Inability to get out of bed
- Acute pain or distress
- Fall or injury
- Inability to eat/drink all day
- Confusion or cognitive decline

## Escalation Path

1. **Nurse contact:** Via WhatsApp or SMS (⚠️ WhatsApp bridge has been unreliable — verify before relying on it)
2. **H notification:** Immediate Telegram message to main topic if red flags detected
3. **Emergency:** Local emergency services in Weija, Ghana

## Carer Candidates (as of May 2026)

| Name | Phone | Status |
|------|-------|--------|
| Emmanuella | +233 24 742 3073 | Ranked #1 — has equipment, can cook, mum liked her |
| Priscilla | +233 24 094 5922 | Ranked #2 — professionalism flag from John |

**Note:** WhatsApp bridge has been down 15+ days (as of May 14). Cannot message carers via WhatsApp until re-linked.

## Weekly Review Format (Sunday 09:06)

Generated by `mum-health-weekly-review` cron (also covers H and Dad). See `references/weekly-health-analysis-template.md` for the full template and data source guide.

Key requirements:
- Must cover **all three people** (H, Comfort, Dad) with separate data completeness tables
- Must scan integrated synthesis files as supplementary data source for free-text health mentions
- Must include week-over-week trend comparison
- Must distinguish between delivery failure vs. response failure vs. capture failure

## Pitfalls

- **Cron jobs don't survive migrations.** After any platform change, verify with `cronjob list`.
- **Care log file path changed** from `~/.openclaw/workspace/memory/CARE_LOG_COMFORT_YYYY-MM.md` to `C:\\Users\\User\\CARE_LOG_COMFORT_YYYY-MM.md`. Always use the new path.
- **Topic IDs changed** during migration. Old OpenClaw topic 51 → new topic 4. Always verify topic mapping in config.yaml.
- **WhatsApp is unreliable.** Never assume WhatsApp escalation will work. Have SMS fallback.
- **H sends terse, streaming intake drops.** H will send multiple short messages with food/vitals/meds mixed together (e.g. "Breakfast two boiled eggs and mushroom tea" then a separate message with vitals). Log each piece immediately as it arrives — don't wait for a complete structured entry or ask H to reformat. Fill in sections incrementally across messages.
- **Memory may be full.** If the memory tool reports capacity exceeded, write directly to the care log file via `patch` or `write_file` — do not skip logging. The care log file is the canonical record, not memory.
- **Weekly analysis data sources.** When compiling the weekly check, structured health check responses may be sparse or absent. ALWAYS also scan `memories/insights/INTEGRATED_INSIGHTS_YYYY-MM-DD.md` files from the past 7 days — these synthesis reports often contain free-text health mentions (meals, symptoms, energy) that bypass the structured check-in system. This is especially important for H, who frequently logs meals and symptoms via Telegram DM rather than structured forms.
- **AGENTS.md BOM issue in weekly sessions.** The weekly health analysis cron session may inherit the `AGENTS.md` invisible unicode (U+FEFF BOM) warning. This is a known issue and does NOT affect the actual file writes or Telegram delivery — proceed with the analysis regardless of this warning.
- **Health check jobs return [SILENT] — not errors:** The mum-health-morning, health-check-morning, dad-health-morning, dad-health-afternoon, and dad-health-evening jobs frequently return `[SILENT]` because `send_message` is unavailable in cron sessions. This is DIFFERENT from a delivery error — `[SILENT]` means the agent had no data source / no tool to deliver with. In the integrated synthesis, `[SILENT]` on health checks should be counted as "prompt NOT delivered" (delivery gap), not as a cron error. The jobs technically succeeded (`last_status: "ok"`) but the health prompt never reached Telegram. Track this as a health monitoring infrastructure gap, not a cron SLA failure.
- **Weekly review jobs can generate reports without send_message:** The weekly review jobs (mum-health-weekly-review, dad-health-weekly-review, health-analysis-weekly, health-weekly-synthesis) all ran successfully on 2026-05-24 (first-ever runs) and produced comprehensive reports despite `send_message` being unavailable. The cron system auto-delivers the agent's final response. This is the correct behavior — the report IS the delivery.
- **H health check cron jobs deliver to wrong channel.** The H health checks (morning/afternoon/evening/weekly) deliver to `telegram:123286468:2` (Home chat), not the Hermes supergroup where H interacts. H won't see them in the supergroup. Fix: update all 4 H health cron jobs to deliver to `telegram:-1003784520976:2`.
- **DNS resolution failures can block Telegram delivery.** On May 18, 2026, both evening health checks (H + Comfort) failed with `httpx.ConnectError: [Errno 11001] getaddrinfo failed` — the host could not resolve the Telegram API domain. This is a network/infrastructure issue, not a cron config issue. If health checks fail with DNS errors, check the host's DNS configuration (router/ISP). Monitor for recurrence — a single blip is transient; a pattern requires intervention.
- **New cron jobs have a "first run" gap.** When jobs are created mid-day, they won't fire until their next scheduled time. Don't assume a job has run just because it exists in jobs.json. Check `last_run_at` to confirm execution.
- **Cron delivery config pattern — `local` + `send_message` vs. direct `telegram:...` with thread_id.** Setting `deliver: "telegram:<chat_id>:<thread_id>"` on a cron job causes the system to try routing the agent's final response through that thread. If the thread_id doesn't exist on the target chat (e.g., thread 4 on `123286468` home chat instead of on `-1003784520976` group), the system logs `"configured thread_id X was not found; delivered without thread_id"` and the message lands in the wrong place or is silently dropped. **The fix:** Set `deliver: "local"` on the job and have the agent use `send_message` directly to `telegram:<group_id>:<topic_id>` in its prompt. This gives the job full control over routing and avoids the broken thread resolution. Apply this pattern to ALL health-check jobs (Mum, Dad, H) to prevent silent delivery failures.

## Related Files

- `references/care-log-template.md` — Full care log template with all sections and red flag criteria
- `references/migration-resilience.md` — Migration lessons learned, path/topic changes, prevention checklist
- `references/dns-failure-pattern.md` — DNS resolution failure pattern on Telegram API (May 2026), diagnosis steps, mitigation
- `references/medical-record-review-comfort.md` — Comfort's full clinical summary from NHS records (May 2026), lab values, trends, travel insurance risk assessment, clinical summary format guide
- `references/health-check-silent-pattern.md` — `[SILENT]` vs error distinction for health check cron jobs, affected jobs list, synthesis reporting guidance
- `references/meal-plan-template.md` — Weekly meal plan builder for elder care: clinical constraints, Dr Ferguson's alkaline protocol, Ghanaian cuisine adaptation, carer cooking instructions
- `references/dr-ferguson-meal-plan.md` — **Authoritative original document**: full 6-page transcription with handwritten overrides, allowed/banned food lists, plate diagram, detox cycle, herbal supplement protocol, daily schedule, Ghanaian compatibility table

## Hospital Correspondence Protocol

When new hospital letters/documents arrive as images, follow the workflow at `references/hospital-correspondence-processing.md`.

For image enhancement of scanned/photographed documents (including music notation), use the pipeline at `references/image-enhancement-pipeline.md`.

## H's Medical Records

For H's full medical history, conditions, and exam results, see `references/medical-record-review-h.md`.

## Dad — Robert Herbert-Blankson

> Full dad-specific profile, cron jobs, contacts, medications, and red flags. This section is the canonical reference for dad's care — the former `elder-care-dad` skill has been consolidated here.

### Patient Profile

- **Name:** Prof Robert Herbert-Blankson
- **Age:** 92 (DOB 09/05/1934)
- **Location:** 40 Archdale Road, London SE22 9HJ
- **NHS Number:** 464 825 5879
- **Hospital MRN:** 38495304 (KCH)
- **Conditions:** Diabetes, PVD, right BKA, diabetic foot ulcer, bilateral hand OA, MGUS, hiatus hernia, gastric ulcer
- **Care provider:** Southwark Council Adult Social Care
- **Monthly cost:** ~£829.80 (non-residential)

### Primary Care Document

**Path:** `C:\Users\User\.hermes\workspace\FAMILY_INSIGHTS_DAD.md`

This is the single source of truth for dad's care. All hospital correspondence, medication changes, appointments, and care updates should be logged here.

### Telegram Topic Routing

| Topic | ID | Purpose |
|-------|----|---------|
| health-log-dad | 1 (Agent Hermes group) | Dad's health check-ins and care updates |

**Group:** `-1003784520976` (Hermes agent group)

### Dad Cron Job Registry

| Job Name | Schedule | Job ID | Delivery |
|----------|----------|--------|----------|
| dad-health-morning | `7 8 * * *` (08:07 daily) | `6b46477e2dae` | `telegram:-1003784520976:1` |
| dad-health-afternoon | `30 13 * * *` (13:30 daily) | `8b04e14f2ded` | `telegram:-1003784520976:1` |
| dad-health-evening | `30 19 * * *` (19:30 daily) | `d9aa7fcfaaea` | `telegram:-1003784520976:1` |
| dad-health-weekly-review | `30 9 * * 0` (Sunday 09:30) | `4f3e7b73e103` | `telegram:-1003784520976:1` |

### Dad Check-In Templates

These are **health data collection forms** delivered to Telegram Topic 1 for carers/district nurses to fill in. See the WhatsApp section below for **personal outbound messages TO Dad**.

**Morning (08:07):** Sleep quality, breakfast, morning vitals, mood/cognition, mobility (transfers, stump comfort), morning meds, overnight carer concerns.

**Afternoon (13:30):** Lunch, midday vitals, mood/energy, district nurse visit/wound status, midday meds, carer concerns.

**Evening (19:30):** Dinner, evening vitals, day summary (mood, pain, bowel/bladder), mobility (falls/near-misses), meds (missed doses?), skin check, sleep readiness.

### WhatsApp Outbound Messages TO Dad

These are **personal check-in messages sent directly to Dad via WhatsApp** (+447****4695), scheduled Sun & Wed 10:00 AM UK time. Tone: warm, caring. Keep concise — Dad is 92, wheelchair-bound, right BKA.

**Template — General Check-In:**
> "Good morning Dad! 🌞 Just checking in on you today. How are you feeling? How's your mobility been — any issues with the wheelchair or your stump? Is there anything you need or anything the carers should know about? Hope you're having a lovely [day]. Love you! ❤️"

**Template — Post-Incident Follow-Up:**
> "Hi Dad, just wanted to see how you're doing after [incident]. How are you feeling today? Any pain or discomfort? Let me know if you need anything. Love you! ❤️"

**Template — Weekend/Leisure:**
> "Morning Dad! 🌞 What are you up to today? Hope the carers are looking after you well. Anything you need? Have a wonderful [day]. Love you lots! ❤️"

**WhatsApp sending notes:**
- Requires OpenClaw gateway running (port 18789) — check gateway status first
- `send_message` tool may not be available in cron environments; if unavailable, draft the message, log the attempt to the care log, and report via Telegram
- On failure, append entry to `CARE_LOG_DAD_YYYY-MM.md` with: date/time, "WhatsApp Message Attempt — FAILED", bridge error, intended recipient, and full intended message text
- See `whatsapp-bridge-failure-protocol.md` for full failure handling procedure

### Dad Red Flags — Immediate Escalation

- Vitals outside normal range (BP >160/100 or <90/60, pulse >100 or <50, temp >38°C, O2 <92%)
- Missed DAPT doses (aspirin/clopidogrel) — graft thrombosis risk
- New/worsening foot ulceration or stump problems
- Signs of infection (redness, heat, swelling, discharge)
- Sudden cold/pale/paraesthetic leg (possible graft occlusion)
- DVT/PE symptoms: leg pain/swelling, chest pain, breathlessness
- Fall or injury
- Inability to eat/drink all day
- Acute confusion or behavioural change
- Skin breakdown

### Dad Escalation Path

1. **District nurse** — wound care, routine concerns
2. **GP (Dulwich Medical Centre)** — 020 8693 2727 — medication queries, non-urgent
3. **KCH Vascular (Mr Slim's team)** — graft/stump/foot concerns
4. **KCH A&E / 999** — acute vascular compromise, severe infection, DVT/PE
5. **H notification** — immediate Telegram to main topic for any red flag

### Dad Care Log

**Path:** `C:\Users\User\CARE_LOG_DAD_YYYY-MM.md` (monthly files)

Uses the same format as mum's care log — see `references/care-log-template.md`.

### Dad Key Contacts

| Role | Name | Contact |
|---|---|---|
| Vascular Surgeon | Mr Hani Slim (KCH) | 020 3299 9000 |
| Orthopaedic Surgeon | Mr A Saini (KCH T&O) | 020 3299 9000 |
| GP | Dulwich Medical Centre | 020 8693 2727 |
| Rehab Medicine | Dr Alifa Isaacs-Itua (Bowley Close) | 020 3049 7724 |
| Hand Therapy | KCH | 020 3299 8220 |
| Social Care | Southwark Council | 020 7525 1111 |
| Wife | Lily Herbert-Blankson | 07855 929714 |
| Daughter | Jane | 07860 945810 |
| Son (H) | Oman Herbert-Blankson | +233 20 425 2252 |

### Dad Medication Pitfalls

- **DAPT compliance is critical.** Aspirin + clopidogrel must not be stopped without vascular review — risk of graft thrombosis.
- **Oxycodone is a controlled drug.** Monitor usage, watch for sedation/confusion in a 92-year-old.
- **Gabapentin + indigestion remedies** — must be separated by 2 hours.
- **Lansoprazole** — must be taken 30-60 min before food, don't crush/chew.

### Southwark Council Invoicing

- Invoices arrive monthly, ~£829.80
- Reference: SF01051115
- Payment by cheque
- Log each invoice in **Section 10** (Financial Tracking) of `FAMILY_INSIGHTS_DAD.md`
- Cross-reference with CareGrid schedule in **Section 5**

### Care Log Append Gotcha (Dad)

The monthly care log (`CARE_LOG_DAD_YYYY-MM.md`) uses repeated identical section headers across entries. When using `patch` to append a new entry, the `old_string` MUST include enough unique context. If patch reports "N matches", widen the context or use the target entry's date+type header as an anchor. Alternatively, use `write_file` to rewrite the entire file — safer for this format. Always verify after patching.

### dad-health cron jobs reference wrong skill name

The `dad-health-morning`, `dad-health-afternoon`, `dad-health-evening`, and `dad-health-weekly-review` cron jobs all have `skills: elder-care-dad` in their job config. This skill name was consolidated into `elder-care-operations` and no longer exists as a standalone skill. The skill loading fails silently — the job runs but without skill context. H needs to update each job's `skills` field to `elder-care-operations`. Until then, dad health cron jobs run on the cron prompt alone without access to the richer templates and protocols in this skill.

### Weekly Review — No send_message Tool

**The weekly review cron prompt instructs the agent to use `send_message` to post the report, but `send_message` does NOT exist as a tool in this environment.** The cron system delivers the agent's final response automatically to the configured destination. The weekly review agent should:

1. Generate the report as its final response text (not try to call `send_message`)
2. NOT attempt `send_message` — it will fail with "Tool does not exist"
3. If the report genuinely has nothing new to say, respond with exactly `[SILENT]` to suppress delivery

Coaching the weekly cron job prompts to remove the `send_message` instruction is recommended. Until then, agents should ignore that step and just produce the report as their final output.

### Weekly Review — Blank Data Is a Finding

When all care log fields for the week are blank/unfilled (—), the review should **NOT** be marked `[SILENT]`. A week with zero recorded data is itself the most important finding. The report should:
- State clearly that no data was recorded and for how many days
- Flag the compliance gap as a Red Flag
- Still include the standard format sections (trends, recommendations)
- Treat blank templates as a system/process failure requiring intervention

### WhatsApp Check-In Failure Logging

When the WhatsApp bridge is down and a check-in cannot be sent to Dad, still append an entry to the care log with: date/time, "WhatsApp Message Attempt — FAILED", bridge error, intended recipient, and full intended message text.

### Home Instead Senior Care

Full documentation pack is in `FAMILY_INSIGHTS_DAD.md` Section 12. Quick-reference extract at `references/home-instead-quick-reference-dad.md`. Mum (Comfort Blackson) was also a signed Home Instead client (Service Agreement 10.3.2021, 21A Phillip Walk SE15 3NH).

## Cross-Reference

- For the integrated daily synthesis cron that covers health + business + security + system, see `daily-operations-synthesis`.

## Meal Planning & Nutrition

When H asks to create, adapt, or integrate meal plans for either parent (or household members like Ebony), follow the protocol at `references/meal-plan-template.md`.

**Key principles:**
- Clinical dietary constraints always come first (diabetes, CKD, HTN, obesity, chewing difficulty)
- Follow the specific dietary protocol the patient's doctor recommends (e.g., Dr Ferguson's alkaline/plant-based protocol for Mum)
- **When a doctor's original document is available, use `references/dr-ferguson-meal-plan.md` as the authoritative source. Handwritten overrides on the original ALWAYS take priority over printed text.**
- Adapt to local Ghanaian dishes where possible — many Ghanaian staples (kontomire, alefu, okro, light soups) are naturally alkaline-forming and low-acid
- When integrating a UK food haul: inventory all items, **check each ingredient against the protocol's allowed/banned lists**, and DO NOT use items that violate the protocol (no meat, no dairy, no tinned/smoked fish, no cheese, no nuts on Dr Ferguson's plan)
- Items that conflict with the patient's protocol may still be used for OTHER household members not on that protocol — cook separately
- Save completed meal plans to `MEAL_PLAN_<context>.md` in the workspace root
- Meal plans are distinct from health logs — DO NOT append to `CARE_LOG_COMFORT_`; keep as standalone files
- **Save the original doctor's document transcription** as a reference file under the skill's `references/` directory

### Dr Ferguson-Compliant Meal Plan Checklist
1. Check every ingredient against `references/dr-ferguson-meal-plan.md` allowed/banned lists
2. Handwritten overrides always apply — even across sessions, persistently
3. Separate patient portions from others at cooking stage
4. Use local Ghanaian vegetables generously (kontomire, alefu, okro, garden eggs, callaloo)
5. Include carer "how to think about every meal" checklist in the plan
6. Verify plate fits on 6-inch saucer, 7 spoons total

### Cron Job Pitfalls

When running as a cron job (especially the weekly review), be aware of tool and skill loading limitations. See `references/cron-pitfalls-weekly-review.md` for the full list. Key takeaways:
- `send_message` does not exist — just produce the report as your final response
- `elder-care-dad` standalone skill no longer exists — it's consolidated in this skill
- Blank care log fields are a finding, not a reason to go `[SILENT]`

### File Naming Convention for Weekly Reports

Weekly analysis files follow a predictable naming scheme so future sessions can discover them:
- H weekly: `memories/health/weekly/H-YYYY-MM-DD.md` (date = Sunday of the reporting week)
- Comfort weekly: `memories/health/weekly/MUM-YYYY-MM-DD.md`
- Dad weekly: `memories/health/weekly/DAD-YYYY-MM-DD.md` (if generated separately)

The weekly cron for health-analysis-weekly should generate **separate reports for each person** when data exists, OR a single combined report that covers all three with clear sections.

### Weekly Analysis Scope — All Three People

**IMPORTANT**: The health-analysis-weekly cron covers **H, Comfort, AND Dad** — not just Comfort. Each weekly report must:

1. **Data completeness table** for each person (checks responded / checks sent / response rate)
2. **Week-over-week trend table** comparing current week to prior 3–4 weeks
3. **Red flags** specific to each person's conditions
4. **Root cause analysis** if data gaps exceed 3 consecutive days
5. **Actionable recommendations** ranked by severity (🔴 Critical / 🟡 Moderate / 🟢 Stable)

### Chronic Data Gap Patterns (as of May 2026)

- **Comfort**: 8+ day data gaps are chronic and recurring. Root cause is **carer response failure**, NOT delivery failure. Templates deliver 100% to Telegram Topic 4 but responses are never captured. The weekly report should flag this as a persistent pattern requiring systemic fix (alternative channel, carer assignment, phone-based check-in).
- **Dad**: Daily templates deliver to Telegram Topic 1 100%, but **all fields remain blank**. Carer response capture is not working. Different from Comfort's issue — Dad's carers in the UK (district nurses, home carers) may not have access to or awareness of the Telegram topic. Escalate to H for alternative reporting mechanism.
- **H (self)**: Partially logging health via free-text Telegram messages but **ignoring structured 3x/day forms**. Response rate ~5%. The system should adapt: either accept free-text as valid responses or simplify to a single daily prompt.

### Health Log File Locations (Confirmed May 2026)

| Person | Health/Care Log | Weekly Reports |
|--------|----------------|----------------|
| H | `C:\Users\User\.hermes\workspace\memories\health\H\HEALTH_LOG_YYYY-MM.md` | `memories/health/weekly/H-YYYY-MM-DD.md` |
| Comfort | `C:\Users\User\CARE_LOG_COMFORT_YYYY-MM.md` (root) | `memories/health/weekly/MUM-YYYY-MM-DD.md` |
| Dad | `C:\Users\User\CARE_LOG_DAD_YYYY-MM.md` (root) | `memories/health/weekly/DAD-YYYY-MM-DD.md` |

Also check for free-text health mentions in `memories/insights/INTEGRATED_INSIGHTS_YYYY-MM-DD.md` files — these often contain H's meal logging and symptom reports that bypass the structured health check-in system.

## H's Personal Health Records

When H sends medical documents (scans, photos of forms, lab results), follow this workflow:

### Medical Records Intake Workflow

1. **Extract data** from images using `vision_analyze` — read all text, values, and structured fields
2. **Log to health file** at `C:\Users\User\.hermes\workspace\memories\health\H\HEALTH_LOG_YYYY-MM.md`
3. **Structure by record type:**
   - Eye exams → prescription table, IOP, visual fields, external exam findings
   - Blood work → table with test/result/range/flag (✅ normal, ⚠️ abnormal)
   - Endoscopy/procedures → findings, diagnosis, recommendations
   - Known conditions → dedicated `## Known Conditions` section with diagnosis date, symptoms, complications to watch, status
4. **Update memory** with key facts (conditions, abnormal values, upcoming follow-ups)
5. **Flag anything urgent** — abnormal values, missed follow-ups, worsening symptoms

### H's Known Conditions (updated May 2026)

- **Achalasia** — diagnosed pre-2018, had dilatation, gastroscopy 12/2018 unremarkable, manometry status unknown. Watch for: dysphagia, regurgitation, weight loss, pulmonary aspiration. If rapid weight loss or worsening dysphagia → rule out secondary achalasia (tumor).
- **Pericarditis** — recurring. Usually resolves ~7 days with NSAIDs. ~30% recurrence rate. Watch for: cardiac tamponade (fluid compresses heart), constrictive pericarditis (scarring restricts heart) — both life-threatening → A&E immediately.

### H's Health Profile Summary

- **Myopia:** R -1.00/-0.25×145, L -0.50/-0.25×145 (Sep 2025)
- **IOP:** Normal (R: 11, L: 12)
- **Blood flags (Mar 2020, needs recheck):** MCV high (98.1), MCHC low (31.3), Lymphocytes low (1.18)
- **NHS Number:** 4326631864
- **GP:** The Dulwich Medical Centre
- **Allergies:** None known
- **Medications:** None regular
