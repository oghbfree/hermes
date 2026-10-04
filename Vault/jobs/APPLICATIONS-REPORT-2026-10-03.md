# Daily Applications Report — 2026-10-03

**Pull timestamp:** 2026-10-03T11:20Z
**Google Sheets auth:** ACTIVE — Token refreshed 2026-10-03 (previous token expired 2026-10-01)
**Sheets snapshot:** `sheets-raw-2026-10-03.json` (51 nurses, 2 financial literacy, 13 construction, 4 facilitators)
**Baseline for diff:** `sheets-raw-2026-09-24.json` (last reported pull)

---

## New Applications Since Last Reported Pull (2026-09-24)

| Role | New | Total Now | Notes |
|------|-----|-----------|-------|
| **Nurses** | 1 | 51 | Kpodo Faith (28/09) |
| **Financial Literacy** | 0 | 2 | No new submissions |
| **Construction** | 1 | 13 | Arthur Kofi Shadrack (26/09) |
| **Facilitators** | 1 | 4 | Courage Agbalekpor (26/09) |

> **3 new applications** since the last reported pull (2026-09-24, 9-day gap). All 3 arrived before the non-reported 2026-10-01 fetch and are captured by the last-reported-pull baseline. Pipeline total 67 → **70**.

---

## New Applicant Screening

### 🏥 Nurse — Kpodo Faith (28/09/2026)
- NMC registered ✅ (PIN 24FK02352005) | Diploma in general nursing
- Experience: **0–2 years** (below 3–5 yr threshold)
- Car ❌ | Driver's licence ❌ | Location: Teshie-Accra | Can do live-in or commute
- **Verdict:** NMC certified but below top-priority tier (no car/licence, <3 yrs). Solid backup candidate; does not change the 7-person top tier.

### 🏗️ Construction — Arthur Kofi Shadrack (26/09/2026)
- Trade: **Electrician** | 3–5 years experience | Foreman/Supervisor ✅
- Machines: Angle grinder, SDS rotary hammer, heat gun (3–5 yrs each) | Owns battery drill
- Location: Kasoa Iron City
- **Verdict:** Foreman experience but **3–5 yrs (below 6+ threshold)** — does not enter the 7-person top tier. Adds valuable electrical capability to the pool.

### 🤖 Facilitator — Courage Agbalekpor (26/09/2026)
- Bachelor's in IT | Taught children 7–14 ✅ | Coding **4/5** | No mBot experience ❌
- Availability: **Tuesday, Thursday only** (sessions are typically Mon–Fri 3–5pm)
- Accepts commission structure, Zobase clock-in, John Protocol inventory
- **Verdict:** Good teaching + coding background, but **no mBot + limited availability** — below the mBot priority filter. Enters the "coding 4+" secondary pool.

---

## Pipeline Totals (All Time)

| Role | Total Applicants | Priority-Filtered |
|------|------------------|-------------------|
| **Nurses** | 51 | 7 (NMC + 3–5 yrs exp) |
| **Facilitators** | 4 | 2 (mBot + coding 4+) |
| **Construction** | 13 | 7 (Foreman + 6+ yrs) |
| **Financial Literacy** | 2 | 2 (both strong) |
| **TOTAL** | **70** | — |

---

## Top Candidates (Priority Filters)

### 🏥 Nurses — NMC + 3–5 yrs experience (7, unchanged)
Charlotte Nortey (3–5, car ✅, licence ✅, 0545995731) — top pick.
Tetteh Dorcas Worlali, Helen Kwakye, Stella Gyapong, Mohammed Shaibu (car-less), Agartha Ampofowaa, Ida Abbey-Quaye — unchanged.

### 🏗️ Construction — Foreman + 6+ years (7, unchanged)
Awal Mohammed Hashim, Kwame Odoom, Derrick Amortey, Amane John, Amuzu David Lauren, Woedzagbagba Bright Kwame, Eric Otoo.

### 🤖 Facilitators — mBot + Coding 4+ (2, unchanged)
Eyiah Michael Osardu (5/5), Patrick Selorm Bediako (4/5). Courage Agbalekpor (coding 4/5, no mBot) is #3 secondary candidate.

### 💰 Financial Literacy — Both Strong (2, unchanged)
Felix Ayettey Boateng, Benjamin Lolo.

---

## Auth & Pipeline Health

- ✅ Google OAuth2 token refreshed successfully (2026-10-03; was expired since 2026-10-01)
- ✅ All 4 Google Sheets accessible
- ✅ Snapshot saved: `sheets-raw-2026-10-03.json`
- ✅ Priority counts verified against live data (7 / 7 / 2 / 2 — unchanged despite +3 pipeline)
- ✅ No auth errors or rate limits

---

## Next Scheduled Pull

Daily cron at 08:00 UTC.

---

## Files Updated

- `APPLICATIONS-REPORT-2026-10-03.md` (this file)
- `RECRUITMENT_SUMMARY.md` (pipeline totals / latest pull)
- `last-check-nurses.json`
- `last-check-facilitators.json`
- `last-check-construction.json`
- `last-check-financial-literacy.json`
- `sheets-raw-2026-10-03.json`