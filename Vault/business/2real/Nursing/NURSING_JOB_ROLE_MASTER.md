# NURSING JOB ROLE — MASTER INDEX & COORDINATION

> **Role:** Lead Carer / Nurse (Residential) for Mum — Comfort Blankson (91), Weija, Accra.
> **Employer:** Oman Herbert Blankson (2 Real Enterprises)
> **Current employee:** **Stephanie Yeboah Agyemang** (hired 2026, started Mon 8 June 2026)
> **Coordination topic:** Telegram **topic 424** (Agent Hermes — nursing/career role coordination here)
> **Last updated:** 17 Aug 2026 · **DMY dates** throughout

---

## 1. QUICK FACTS — STEPHANIE

| Field | Detail |
|-------|--------|
| Full name | Stephanie Yeboah Agyemang |
| Email | stephanieagyemang640@gmail.com |
| Mobile | +233 54 823 6698 (0548236698) |
| Qualification | Diploma in Nursing (NMC-certified nurse) |
| Role | Lead Carer / Nurse (Residential) — mum's nurse |
| Start date | Monday 8 June 2026 |
| Contract | 3-month trial → 1-year fixed term |
| Salary | GH¢ 2,000/mo (trial) → GH¢ 2,500 after review; paid end of month |
| Schedule | 6 days on / 1 day off (live-in, sleep-in from 21:00) |
| Clinical scope | Furosemide 20mg (STOP if BP <100 or >140) · BP/pulse/temp monitoring · swelling reduction |
| Previous (not hired) | Stephanie Yeboah Agyemang **(hired)** vs "Stephanie Avadane" (avadanestephanie@gmail.com, separate applicant) — do NOT confuse |

> ⚠️ **Two "Stephanie" applicants exist in the recruitment sheets.** The hired one is **Stephanie Yeboah Agyemang**. "Stephanie Avadane" is a different applicant (Degree in Nursing) — never treat them as the same person.

---

## 2. FILE MAP — EMPLOYMENT & PROCEDURE DOCUMENTS

**Canonical copies (source of truth):** `Vault/business/2real/Nursing/`
**Editable templates (source markdown):** `skills/productivity/elder-care-operations/templates/`

> **📋 To present to Stephanie — role & expectations (combined):** `Vault/business/2real/Nursing/STEPHANIE_ROLE_AND_EXPECTATIONS.md`
> *(Combines the daily routine + household duties + cooking + cleaning-standard + attitude into one document for managing expectations. The individual files below remain for reference.)*

| Document | PDF (Nursing/) | Source MD (templates/) |
|----------|----------------|-------------------------|
| Employment Offer Letter | `employment-offer-stephanie.pdf` | `employment-offer-stephanie.md` |
| Daily Routine & Timetable | `daily-routine.pdf` | `daily-routine.md` |
| Standard Operating Procedures (SOP) | `sop.pdf` | `sop.md` |
| Care Plan | `care-plan.pdf` | `care-plan.md` |
| Code of Conduct | `code-of-conduct.pdf` | `code-of-conduct.md` |
| Welcome Pack | `welcome-pack.pdf` | `welcome-pack.md` |
| Incident Report Form | `incident-report.pdf` | `incident-report.md` |
| CCTV & Privacy Consent | `cctv-consent.pdf` | `cctv-consent.md` |
| Driver Code of Conduct | `driver-code-of-conduct.pdf` | `driver-code-of-conduct.md` |
| Emergency Contacts | — | `emergency-contacts.md` |
| Day 1 Arrival Plan | — | `day-1-arrival-plan.md` |
| Budget (setup/operating) | — | `budget.md` |
| Maa Joyce relocation checklist | `maa-joyce-checklist.md` | — |

**Hiring poster:** `Nursing/whatsapp-message.txt` (WhatsApp recruitment ad; Google Form apply link)
**Recruitment pipeline:** `Vault/jobs/` (`RECRUITMENT_SUMMARY.md`, `jobs/nurses/`, `APPLICATIONS-REPORT-*.md`)

---

## 3. FILE MAP — CARE / CLINICAL DATA (MUM)

- **Medical master:** `Vault/family/mum/health/MUM_MEDICAL_MASTER.md`
- **Food master:** `Vault/family/mum/health/MUM_FOOD_MASTER.md`
- **Profile:** `Vault/family/mum/MUM_PROFILE.md`
- **Daily care reports:** `Vault/family/mum/health/YYYY-MM-DD_*report*.md` (from topic-4 reports)
- **Exercises:** `Vault/family/mum/exercises/`

> Health logging runs through the `elder-health-daily-logging` skill into topic 4; nursing role coordination & job-role docs sit in topic 424.

---

## 4. PREVIOUS SESSIONS (session IDs) — FINDING & EMPLOYING STEPHANIE

Useful to trace the full hire history. Locate in session DB via `@session:default/<id>`.

| Session ID | Date | Topic |
|-----------|------|-------|
| `20260605_050156_268dddf2` | 5 Jun 26 | CCTV setup, employment docs sent to Stephanie |
| `20260607_130851_e056d490` | 7 Jun 26 | ZOSI spec + meeting Stephanie's family before start |
| `20260608_045614_b7b15c1c` | 8 Jun 26 | Stephanie arrival/Day-1 prep checklist |
| `20260608_053240_9309464b` | 8 Jun 26 | Stephanie starts (nurse Agyemang); nurse workflow design |
| `20260609_052803_dfe3c7ca` | 9 Jun 26 | Add Stephanie to topic 4; fix muм health-log crons |
| `20260702_213435_6ad63e8e` | 2 Jul 26 | Stephanie June pay alignment (started 8/6/26, ~23 days) |
| `20260704_133552_e9f37611` | 4 Jul 26 | Mum's ankle-pump exercise routine |
| `20260719_141744_1ad63e` | 19 Jul 26 | Created `stephanie-nurse-wellbeing-checkin` cron |
| `20260806_164308_51e45610` | 6 Aug 26 | Recorded cash payment to Stephanie (2000, 1/8/26) |
| `20260811_031410_c34b10` | 11 Aug 26 | Mum health-log backfill from Stephanie's topic-4 reports |

*(Hiring-phase search sessions from April–May 2026 are recorded in `Vault/jobs/nurses/` APPLICATIONS-REPORT files rather than dedicated chat sessions.)*

---

## 5. CRON / AUTOMATION

| Job | ID | Schedule | Delivery | Status note |
|-----|----|----------|----------|-------------|
| `stephanie-nurse-wellbeing-checkin` | `f747316d1579` | Tue 09:00 | `local` | Weekly nurse wellbeing + procedures reminder |
| mum health crons (morning/afternoon/evening/weekly) | see `elder-care-operations` skill | daily | topic 4 | Run separately |

> ⚠️ **Finding:** `stephanie-nurse-wellbeing-checkin` is configured to deliver to `local` (output stays on machine). For the Tuesday wellbeing reminder to reach Stephanie or surface to H, delivery should be set to an explicit target (e.g. topic 424 or WhatsApp). Confirm before changing.

---

## 6. OPEN ACTIONS / WATCHLIST

- [ ] ✅ **60-day review done** (see `STEPHANIE_REVIEW_60DAY_2026-08-17.md`)
- [ ] ⚠️ **TRIAL EXTENDED +1 month — performance-based** (see `STEPHANIE_TRIAL_EXTENSION.md`). Permanent contract NOT signed in Sep. 7 items to fix: report detail/accuracy (incl. Dr Morris meds = 3 elements + masseuse info), mushroom tea on schedule+logged, push water, daily elevation+Epsom soaks, Furosemide refusal logging + BP stop-rule (10-8 refused; 144 reading), forward-planning+meal prep+expiry checks, more room visits+logging
- [ ] **Speak to Stephanie** — over a month overdue (said would after paying her)
- [ ] Decide **firm review date** (~2 weeks) + **salary step** (2,000→2,500: moves with extension or gated?)
- [ ] **CCTV still not installed** in new house (consent in place; install pending)
- [ ] H **on the fence** — Mum gives mixed messages re Stephanie; reconcile
- [ ] Buy **large-print Bible** for Stephanie (from 60-day review)
- [ ] Confirm `stephanie-nurse-wellbeing-checkin` delivery target (currently `local`)
- [ ] House move maintenance/repairs (see `NEW_HOUSE_MAINTENANCE.md`)
- [ ] Cross-check any future nurse hiring against this master so Stephanie stays the canonical carer

---

## 7. CROSS-LINKS

- **Up:** `[[family/mum]]` care · `[[jobs]]` recruitment
- **Recruitment index:** `jobs/JOBS_MASTER.md` (all pipelines + every job spec)
- **Siblings:** `jobs/RECRUITMENT_SUMMARY.md` · `family/mum/health/MUM_MEDICAL_MASTER.md`
- **Skill:** `elder-care-operations` (templates live there)
- **Stephanie duties/task list:** `Vault/business/2real/Nursing/STEPHANIE_DUTIES_AND_TASKS.md` (household duties, cooking = copper pots only + Himalayan salt + local rice, daily window/radio checks, packing/move checklist)
- **Stephanie morning routine (new house):** `Vault/business/2real/Nursing/STEPHANIE_MORNING_ROUTINE.md` (compound cleaning, security morning→evening, sofa/cushion setup, no-flies, bins, windows/doors)
- **Stephanie 60-day review (17 Aug 26):** `Vault/business/2real/Nursing/STEPHANIE_REVIEW_60DAY_2026-08-17.md`
- **New-house security/camera (17 Aug 26):** `Vault/business/2real/Nursing/NEW_HOUSE_SECURITY_CAMERA.md` — VM380 Pro solar camera (installed by Frederick), MTN SIM GH¢25 (15 sim/7 data/3 airtime)
- **Trial extension (record & message):** `Vault/business/2real/Nursing/STEPHANIE_TRIAL_EXTENSION.md` — performance-based +1 month, 7 items, context (CCTV pending, H on fence, spoken-to gap)
- **Task bank (keep occupied):** `Vault/business/2real/Nursing/STEPHANIE_TASK_BANK.md` — cooking/baking from scratch, making/mending, deep-clean, security, records/planning
- **New-house maintenance/repairs:** `Vault/business/2real/Nursing/NEW_HOUSE_MAINTENANCE.md` — main gate (welder+key), stiff front door, water-heater refit (plumber), ask re mosquito nets
