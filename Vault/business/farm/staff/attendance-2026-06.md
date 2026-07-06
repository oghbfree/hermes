---
title: Staff Attendance Log — June 2026
month: 2026-06
farm: Senya Beraku
---

# Staff Attendance Log — June 2026

**Schedule:**
- **Ben**: Expected daily (7 days/week)
- **Eastwood**: Expected Mon/Wed/Fri (minimum 2×/week)

**Legend:** ✅ Present | ❌ Absent (no check-in) | ⚠️ Late/Partial | 📵 No check-in by 8:00 AM | 🔄 Made up later

---

## June 2026

| Date | Day | Ben | Eastwood | Notes |
|------|-----|-----|----------|-------|
| 2026-06-01 | Mon | | | |
| 2026-06-02 | Tue | | (off) | |
| 2026-06-03 | Wed | | | |
| 2026-06-04 | Thu | | (off) | |
| 2026-06-05 | Fri | | | |
| 2026-06-06 | Sat | | (off) | |
| 2026-06-07 | Sun | | (off) | |
| 2026-06-08 | Mon | | | |
| 2026-06-09 | Tue | | (off) | |
| 2026-06-10 | Wed | | | |
| 2026-06-11 | Thu | | (off) | |
| 2026-06-12 | Fri | | | |
| 2026-06-13 | Sat | | (off) | |
| 2026-06-14 | Sun | | (off) | |
| 2026-06-15 | Mon | | | |
| 2026-06-16 | Tue | | (off) | |
| 2026-06-17 | Wed | | | |
| 2026-06-18 | Thu | | (off) | |
| 2026-06-19 | Fri | | | |
| 2026-06-20 | Sat | | (off) | |
| 2026-06-21 | Sun | | (off) | |
| 2026-06-22 | Mon | | | |
| 2026-06-23 | Tue | | (off) | |
| 2026-06-24 | Wed | | | |
| 2026-06-25 | Thu | | (off) | |
| 2026-06-26 | Fri | | | |
| 2026-06-27 | Sat | | (off) | |
| 2026-06-28 | Sun | | (off) | |
|| **2026-06-29** | **Mon** | **✅ Present** | **📵 No check-in by 8:00 AM** | **Morning check noted "Ben on-site, Eastwood [present/absent]" — ambiguous status. No clear WhatsApp check-in from Eastwood by 8:00 AM on scheduled day.** |
| 2026-06-30 | Tue | | (off) | |

---

## Attendance Summary — June 2026 (as of 2026-06-29)

| Staff | Scheduled Days | Present | Absent | Late/Partial | No Check-in | Attendance Rate |
|-------|----------------|---------|--------|--------------|-------------|-----------------|
| **Ben** | 29 (daily) | 1 (today) | 0 | 0 | 0 | 100% (1/1 logged) |
| **Eastwood** | ~13 (Mon/Wed/Fri) | 0 logged | 0 logged | 0 | 1 (today — no check-in by 8 AM on scheduled Mon) | **⚠️ AT RISK** |

---

## 🚨 Escalation Log

| Date | Staff | Issue | Action Taken | Resolved |
|------|-------|-------|--------------|----------|
| 2026-06-29 | Eastwood | **No morning check-in by 8:00 AM on scheduled Monday** | Check WhatsApp "Farm Ops" for 6:30 AM check-in. **If no check-in by end of day: ALERT H — Eastwood missing 1 scheduled day. Next scheduled day: Wed 2026-07-01. If missing Wed too → 2 consecutive scheduled days missed → trigger backup protocol.** | **PENDING** — Awaiting WhatsApp verification |

---

## Notes

- **2026-06-29 (Today, Monday)**: Daily log notes "Ben on-site, Eastwood [present/absent]" — **status ambiguous**. **No clear WhatsApp check-in from Eastwood by 8:00 AM on his scheduled Monday**. Per `farm-cron-jobs.md` Job #9: if missing 2+ consecutive scheduled days, alert H with backup protocol. **Next escalation point: Wednesday 2026-07-01** (Eastwood's next scheduled day). If no check-in Wed → 2 consecutive scheduled days missed → alert H with backup protocol.
- **Ben**: Expected daily. Daily log confirms "Ben on-site" for morning check. ✅ Present.
- **Eastwood**: Expected Mon/Wed/Fri. Today is Monday (scheduled day). **No verified check-in by 8:00 AM**. Status: 📵 No check-in by 8:00 AM on scheduled day.
- **Kalidou**: Removed (keys retrieved) — no longer on roster.

---

## ⚠️ Active Alert Status

| Staff | Consecutive Scheduled Days Missed | Next Scheduled Day | Alert Threshold | Action if Threshold Met |
|-------|----------------------------------|-------------------|-----------------|------------------------|
| **Eastwood** | **1** (Mon 2026-06-29 — no check-in) | **Wed 2026-07-01** | 2 consecutive scheduled days | 👤 **STAFF ABSENT**: Eastwood missing 2 days. Last contact: [last check-in date]. Backup: [Ben calls replacement / you authorize temp hire] |

*Per `farm-cron-jobs.md` Job #9 escalation protocol.*

*Log format per `farm-cron-jobs.md` Job #9 (Staff Accountability Check). Update daily via cron job `farm-staff-check` (Mon/Wed/Fri 8:00 AM). Manual updates as needed.*