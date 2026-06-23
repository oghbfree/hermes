# APPLICATIONS REPORT - 2026-06-13

## Summary
- **Nurses**: ⚠️ Cannot check — auth expired (total last known: 35)
- **Financial Literacy**: ⚠️ Cannot check — auth expired (total last known: 1)
- **Construction**: ⚠️ Cannot check — auth expired (total last known: 7)
- **Facilitators/Robotics**: ⚠️ Cannot check — auth expired (total last known: 3)

---

## 🔑 KEY FINDINGS

### ⚠️ BLOCKED — Google OAuth2 Credentials Expired
- **Error**: `invalid_grant` on refresh_token
- **Since**: 2026-06-06 (7 days ago)
- **Impact**: All 4 recruitment sheets are inaccessible
- **New applications detected**: Unknown (cannot reach sheets)

---

## 📊 PIPELINE STATUS (Stale — Last Known 2026-06-02)

| Role | Status | Last Known Total | New Today | Blocked |
|------|--------|-----------------|-----------|---------|
| Nurses | ⚠️ Auth Dead | 35 | Unknown | ✅ Yes |
| Financial Literacy | ⚠️ Auth Dead | 1 | Unknown | ✅ Yes |
| Construction | ⚠️ Auth Dead | 7 | Unknown | ✅ Yes |
| Facilitators/Robotics | ⚠️ Auth Dead | 3 | Unknown | ✅ Yes |
| **TOTAL** | | **46** | **?** | |

---

## 📋 ALL-TIME NURSING SUMMARY (35 Total — Stale)

### By NMC Registration
- NMC Registered: 22 of 35 (62%)
- NMC Not Registered: 13 of 35

### By Driver Status
- Has licence: 4 of 35
- Has car: 1 of 35 (Charlotte Nortey)

### Top Candidates (All-Time)
1. **Charlotte Nortey** — Diploma Midwifery, NMC ✅, 3-5 yrs, Pokuase, **HAS CAR + LICENCE** — 0545995731
2. **Agartha Ampofowaa** — Diploma Midwifery, NMC ✅, 3-5 yrs, Accra — 0247260112
3. **Mohammed Shaibu** — BSc Nursing, NMC ✅, 3-5 yrs, Tamale, **HAS LICENCE** — 0597836125

---

## 🔧 ACTION REQUIRED
1. **⚠️ URGENT: Re-authorize Google OAuth2** — The `refresh_token` in `~/.hermes/google_token.json` has been returning `invalid_grant` since 2026-06-06. Need to re-authorize from scratch via Google OAuth2 consent flow to restore pipeline monitoring.
2. Priority outreach (when auth restored): Charlotte Nortey (driver + car, 0545995731) — requires WhatsApp
3. Review new candidates across all pipelines once sheets are accessible again

---

*Report generated: 2026-06-13*
*Google Sheets auth: ❌ EXPIRED (invalid_grant since 2026-06-06)*
*Last successful data pull: 2026-06-02*