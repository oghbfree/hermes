# APPLICATIONS REPORT - 2026-06-10

## Summary
- **Nurses**: ⚠️ **UNKNOWN** — credential expired, cannot fetch (total was 35)
- **Financial Literacy**: ⚠️ **UNKNOWN** — credential expired, cannot fetch (total was 1)
- **Construction**: ⚠️ **UNKNOWN** — credential expired, cannot fetch (total was 7)
- **Facilitators/Robotics**: ⚠️ **UNKNOWN** — credential expired, cannot fetch (total was 3)

**Cannot determine new applications — Google Sheets auth failure (4th consecutive failed check).**

---

## 🔑 KEY FINDINGS

### ❌ Google Sheets Auth Failure (ONGOING — 4 days)
- `refresh_token` returned `invalid_grant` — the OAuth2 token is permanently expired
- The existing `google_token.json` credentials cannot be refreshed automatically
- **Re-authorization from scratch required** to restore recruitment pipeline monitoring
- This is the **4th consecutive failed check** (2026-06-06, 2026-06-07, 2026-06-09, 2026-06-10)
- Pipeline has been blind since June 2 — any new applications since then are undetected

### Last Known State (2026-06-02 baseline — 8 days stale)
| Role | Last Known Total | Last New Applicant |
|------|-----------------|-------------------|
| Nurses | 35 | Laureen Baidoo (non-NMC, skipped) |
| Financial Literacy | 1 | — |
| Construction | 7 | — |
| Facilitators/Robotics | 3 | — |

---

## ⭐ Top Picks from Pipeline (All-Time, unchanged from last cycle)

1. **Charlotte Nortey** — Diploma Midwifery, NMC ✅, 3-5 yrs, Pokuase, **HAS CAR + LICENCE** — 0545995731 **[TOP TIER]**
2. **Mohammed Shaibu** — BSc Nursing, NMC ✅, 3-5 yrs, Tamale, **HAS LICENCE** — 0597836125
3. **Agartha Ampofowaa** — Diploma Midwifery, NMC ✅, 3-5 yrs, Accra — 0247260112
4. **Tetteh Dorcas Worlali** — Cert in Nursing, NMC ✅, 3-5 yrs, Madina — 0543168947

---

## 📊 PIPELINE STATUS

| Role | Status | Last Check | Last Total | Notes |
|------|--------|------------|------------|-------|
| Nurses | 🔴 Auth Failed | 2026-06-02 | 35 | Cannot read — token expired |
| Financial Literacy | 🔴 Auth Failed | 2026-06-02 | 1 | Cannot read — token expired |
| Construction | 🔴 Auth Failed | 2026-06-02 | 7 | Cannot read — token expired |
| Facilitators/Robotics | 🔴 Auth Failed | 2026-06-02 | 3 | Cannot read — token expired |

---

## 🔧 ACTION REQUIRED
1. **🚨 CRITICAL: Re-authorize Google Sheets credentials** — Go through OAuth2 flow to get a new refresh token. Until done, recruitment check runs will continue to fail. Pipeline has been blind for 8+ days.
2. Priority outreach remains: **Charlotte Nortey** (driver + car + NMC, 0545995731) — requires WhatsApp
3. **Manual check of Google Sheets strongly recommended** — there may be several days of unprocessed applications

---
*Report generated: 2026-06-10*
*Google Sheets auth: ❌ INVALID_GRANT — re-authorization required (4th consecutive failure)*
*Nursing sheet ID: 1JKAQMF1eUotpqp61Dd_0bbkteRe3oOB-oLwLMMdyOq4*
*Next scheduled check: 2026-06-11 (will fail until credentials fixed)*
