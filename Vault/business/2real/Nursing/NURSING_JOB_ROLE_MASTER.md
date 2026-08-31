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

- [ ] ✅ **60-day review done — 17 Aug 26** (see `STEPHANIE_REVIEW_60DAY_2026-08-17.md`)
- [ ] **90-day / probation-end review — due 8 Sep 2026** (in new house): probation → 1-yr fixed term, salary GH¢ 2,000→2,500, expanded "run the whole house" role + pay discussion, travel notice, backup/escalation chain
- [ ] Buy **large-print Bible** for Stephanie (from 60-day review)
- [ ] Follow-ups for Stephanie: report detail/accuracy, garlic per protocol, mushroom tea frequency, water intake, daily elevation, compression-stocking logging, log room visits, more proactive + forward-planning
- [ ] Confirm `stephanie-nurse-wellbeing-checkin` delivery target (currently `local`)
- [ ] Move: Mum relocation + packing list (see `kanban`/`maa-joyce-checklist`); confirm move date for review alignment
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
