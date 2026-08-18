# JOBS MASTER — Recruitment & Job Vacancies Coordination

> **Purpose:** Single index for every job vacancy, job spec, and recruitment pipeline across 2 Real Enterprises / Akoma Robotics / family care.
> **Canonical pipeline dir:** `Vault/jobs/` ▪ **Telegram topic 28 = Jobs** (chat `-1003784520976`, thread `28`)
> **Last updated:** 18 Aug 2026 · **DMY dates** throughout

---

## 1. ACTIVE RECRUITMENT PIPELINES (Google-Form applicant tracking)

Driven by the `recruitment-tracking` skill + the **`job-applications-check`** cron (daily 08:00 → topic 28). Auth token + sheet snapshots + `last-check-*.json` live under `Vault/jobs/` (role subdirs `nurses/`, `construction/`, `facilitators/`, `financial-literacy/`).

| # | Role | Form | Pipeline |
|---|------|------|----------|
| 1 | Live-in Graduate Nurse (elderly care) | `forms.gle/n83KW2FoG5ffYSJL8` | 47 apps · 30 NMC · 7 priority |
| 2 | STEM / mBot Special-Education Facilitator | `forms.gle/4n1msAGrpEeDCErM7` | 3 apps · 2 priority |
| 3 | Financial Literacy Facilitator | `forms.gle/SjErZPvw2LMnb9HQ9` | 2 apps · both strong |
| 4 | Elite Construction Team (foremen, all trades) | `forms.gle/dFUQiMPwhQRrh1cP9` | 12 apps · 7 priority |

**Master summary:** `jobs/RECRUITMENT_SUMMARY.md` (64 applicants, updated 18 Aug 26)
**Daily reports:** `jobs/APPLICATIONS-REPORT-YYYY-MM-DD.md`
**Inbound routing:** `jobs/job-application-router.md` — WhatsApp job enquiry → matching Jiji listing → form link

> **Autism facilitator** (Kobena's school-support role) is a **separate** child-support role with its own form (`forms.gle/GJoGjx4mJSbh2Ca7A`); responses sheet not yet linked. Track separately from the STEM-facilitator pipeline.

---

## 2. JOB VACANCIES / JOB SPECS

| File | Role | Status |
|------|------|--------|
| `jobs/JOHN_OFFICE_JOB_SPEC_2026-07-14.md` | John — Office Operations Coordinator | Active |
| `jobs/JOHN_DESK_QUICKREF.md` | John — laminated desk card (= merged old REFERENCE) | Active |
| `jobs/AUTISM_FACILITATOR_JOB_SPEC.md` | Facilitator for child with autism | Recruiting |
| `jobs/JIJI_DOMINANCE_SOP.md` | 2Real Jiji ops SOP | Active |
| `jobs/farm/FARM_WORKER_JOB_POSTING.md` | Farm worker — bee drainage + pond dig (Senya) | Templated |
| `business/2real/Nursing/NURSING_JOB_ROLE_MASTER.md` | Stephanie — Lead Carer/Nurse for Mum (HIRED) | Hired |
| `business/2real/Nursing/STEPHANIE_DUTIES_AND_TASKS.md` | Stephanie — duties/task list | Hired |
| `archive/raw-data/akoma confidential/Manager docs/` | John/trainee-ops raw docs (JOB DESCRIPTION, john jd, manager package, TRAINEE EMPLOYMENT CONTRACT.pdf, NSS enrolment) | Reference |

---

## 3. AUTOMATION

| Job | Cron ID | Schedule | Delivery |
|-----|---------|----------|----------|
| `job-applications-check` | `2e2d1d6ece88` | Daily 08:00 | Telegram topic 28 (Jobs) |
| `stephanie-nurse-wellbeing-checkin` | `f747316d1579` | Tue 09:00 | `local` (review target) |

---

## 4. TELEGRAM TOPIC 28 — JOBS (recruitment pipeline)

The daily job-applications-check posts applicant/pipeline summaries here: chat `-1003784520976`, thread **28**. Previously delivered to the wrong topic (20); corrected to 28 on 5 Jun 26 and confirmed in topic map 22 Jun 26.

---

## 5. SESSION IDs (jobs / recruitment / topic 28)

Locate via `@session:default/<id>`.

| Session ID | Date | Relevance |
|-----------|------|-----------|
| `cron_2e2d1d6ece88_20260818_080039` | 18 Aug 26 | job-applications-check → topic 28 (msg 10596), 0 new apps |
| `cron_2e2d1d6ece88_20260817_080003` | 17 Aug 26 | job-applications-check → topic 28 (msg 10482), 64-app pipeline |
| `20260622_092336_f1b75a` | 22 Jun 26 | Set cron `2e2d1d6ece88` → `Vault/jobs/` + topic 28 |
| `20260622_051543_21c05bd2` | 22 Jun 26 | Confirmed topic 28 = Jobs in config |
| `20260605_041451_c85c5f20` | 5 Jun 26 | Fixed job-applications-check: topic 20 → **28** |
| `20260625_054313_a5873e0f` | 25 Jun 26 | job-applications-check → topic 28 (OK) |
| `20260712_081715_9ccb5749` | 12 Jul 26 | Cron report (job-applications-check connection errors — historical) |
| `20260714_052816_d5263235` | 14 Jul 26 | Integrated synthesis: Jobs Check → topic 28 ✅ |
| `20260714_052655_f661ae71` | 14 Jul 26 | Created John office job spec + desk refs + tracker template |
| `20260814_104852_89a839` | 14 Aug 26 | Created autism facilitator job spec + form |
| `20260712_094220_24c1404b` | 12 Jul 26 | Nurse application form link |
| `20260817_070037_785929` | 17 Aug 26 | Nursing role master consolidation (pattern for this) |
| `20260717_034556_8184631e` | 17 Jul 26 | Considering hiring manual worker "Verse" |
| `20260703_115413_5d806771` | 3 Jul 26 | Hasbunallah / female-driver recruitment incident |
| `20260814_043205_609af9` | 14 Aug 26 | Dad's affairs consolidation (closest merge template) |

---

## 6. CONSOLIDATION DONE — 18 Aug 26

- ✂️ Created this master index (`JOBS_MASTER.md`)
- 🗑️ Deleted stale `nurses/RECRUITMENT_SUMMARY.md` (June, 57 apps) — root summary (64) is canonical
- 🗑️ Deleted stale `nurses/last-check-*.json` ×4 (Jun 22) — root `last-check-*.json` (Aug 18) is canonical
- ✂️ Merged John desk refs: kept `JOHN_DESK_QUICKREF.md`, deleted duplicate `JOHN_DESK_REFERENCE.md`; footer now points to the full spec
- 📁 Relocated `memories/jobs/farm-worker-bee-pond-job.md` → `jobs/farm/FARM_WORKER_JOB_POSTING.md` (memories/ deprecated)
- ✂️ Removed the duplicate "JOB DESCRIPTION: TRAINEE OPERATIONS MANAGER" embedded ×2 inside `insights/business-insights.md` (authoritative doc remains at `archive/raw-data/akoma confidential/Manager docs/manager package job description.txt`)
- 🔗 Cross-linked `NURSING_JOB_ROLE_MASTER.md` ↔ this index

---

## 7. CROSS-LINKS

- **Pipelines:** `jobs/RECRUITMENT_SUMMARY.md` · role dirs `jobs/{nurses,construction,facilitators,financial-literacy}/`
- **Hires:** `business/2real/Nursing/NURSING_JOB_ROLE_MASTER.md`
- **Skill:** `recruitment-tracking` · **Cron skill:** `cronjob-repair` · **Delivery:** `cron-delivery-routing`