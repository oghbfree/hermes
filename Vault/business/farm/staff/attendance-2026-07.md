---
title: Staff Attendance Log — July 2026
month: 2026-07
farm: Senya Beraku
---

# Staff Attendance Log — July 2026

**Schedule:**
- **Ben**: Expected daily (7 days/week)
- **Eastwood**: Expected Mon/Wed/Fri (minimum 2×/week)

**Legend:** ✅ Present | ❌ Absent (no check-in) | ⚠️ Late/Partial | 📵 No check-in by 8:00 AM | 🔄 Made up later

---

## July 2026

| Date | Day | Ben | Eastwood | Notes |
|------|-----|-----|----------|-------|
| 2026-07-01 | Wed | ⏳ Awaiting check-in | ⏳ Awaiting check-in | **Eastwood's 2nd consecutive scheduled day** (Mon 6/29 missed, Wed 7/1 today). **Ben daily.** Per daily log: "awaiting morning check-in" — no check-in received by 8:00 AM. |
| 2026-07-02 | Thu | | (off) | |
| 2026-07-03 | Fri | | | Eastwood scheduled |
| 2026-07-04 | Sat | | (off) | |
| 2026-07-05 | Sun | | (off) | |
| 2026-07-06 | Mon | | | Eastwood scheduled |
| 2026-07-07 | Tue | | (off) | |
| 2026-07-08 | Wed | | | Eastwood scheduled |
| 2026-07-09 | Thu | | (off) | |
| 2026-07-10 | Fri | | | Eastwood scheduled |
| 2026-07-11 | Sat | | (off) | |
| 2026-07-12 | Sun | | (off) | |
| 2026-07-13 | Mon | | | Eastwood scheduled |
| 2026-07-14 | Tue | | (off) | |
| 2026-07-15 | Wed | | | Eastwood scheduled |
| 2026-07-16 | Thu | | (off) | |
| 2026-07-17 | Fri | | | Eastwood scheduled |
| 2026-07-18 | Sat | | (off) | |
| 2026-07-19 | Sun | | (off) | |
| 2026-07-20 | Mon | | | Eastwood scheduled |
| 2026-07-21 | Tue | | (off) | |
| 2026-07-22 | Wed | | | Eastwood scheduled |
| 2026-07-23 | Thu | | (off) | |
| 2026-07-24 | Fri | | | Eastwood scheduled |
| 2026-07-25 | Sat | | (off) | |
| 2026-07-26 | Sun | | (off) | |
| 2026-07-27 | Mon | | | Eastwood scheduled |
| 2026-07-28 | Tue | | (off) | |
| 2026-07-29 | Wed | | | Eastwood scheduled |
| 2026-07-30 | Thu | | (off) | |
| 2026-07-31 | Fri | | | Eastwood scheduled |

---

## Attendance Summary — July 2026 (as of 2026-07-01 08:00 AM)

| Staff | Scheduled Days | Present | Absent | Late/Partial | No Check-in | Attendance Rate |
|-------|----------------|---------|--------|--------------|-------------|-----------------|
| **Ben** | 1 (today) | 0 | 0 | 0 | 1 (today — awaiting) | 0% (0/1 logged) |
| **Eastwood** | 1 (today, Wed) | 0 | 0 | 0 | 1 (today — no check-in by 8 AM on scheduled Wed) | **⚠️ AT RISK — 2nd consecutive scheduled day** |

---

## 🚨 Escalation Log

| Date | Staff | Issue | Action Taken | Resolved |
|------|-------|-------|--------------|----------|
| 2026-06-29 | Eastwood | No morning check-in by 8:00 AM on scheduled Monday | Check WhatsApp "Farm Ops" for 6:30 AM check-in. **If no check-in by end of day: ALERT H — Eastwood missing 1 scheduled day. Next scheduled day: Wed 2026-07-01. If missing Wed too → 2 consecutive scheduled days missed → trigger backup protocol.** | **PENDING** — Awaiting WhatsApp verification |
| **2026-07-01** | **Eastwood** | **No morning check-in by 8:00 AM on scheduled Wednesday (2nd consecutive scheduled day)** | **Check WhatsApp "Farm Ops" for morning check-in. If no check-in by end of day: 🚨 ALERT H — Eastwood missing 2 consecutive scheduled days. Last contact: [last check-in date]. Backup: Ben calls replacement / you authorize temp hire.** | **PENDING** — Awaiting WhatsApp verification |

---

## Notes

- **2026-07-01 (Today, Wednesday)**: Daily log 2026-07-01.md shows "Morning Check (6:30) ⚠️ MISSING" and "Staff: [awaiting morning check-in]". **No clear WhatsApp check-in from Eastwood by 8:00 AM on his scheduled Wednesday**. Per `farm-cron-jobs.md` Job #9: if missing 2+ consecutive scheduled days, alert H with backup protocol. **This is the 2nd consecutive scheduled day missed** (Mon 2026-06-29 + Wed 2026-07-01).
- **Ben**: Expected daily. Daily log shows "awaiting morning check-in" — status pending.
- **Eastwood**: Expected Mon/Wed/Fri. Today is Wednesday (scheduled day). **No verified check-in by 8:00 AM**. Status: 📵 No check-in by 8:00 AM on scheduled day. **This is the 2nd consecutive scheduled day missed** (Mon 6/29 + Wed 7/1).
- **Kalidou**: Removed (keys retrieved) — no longer on roster.

---

## ⚠️ Active Alert Status

| Staff | Consecutive Scheduled Days Missed | Next Scheduled Day | Alert Threshold | Action if Threshold Met |
|-------|----------------------------------|-------------------|-----------------|------------------------|
| **Eastwood** | **2** (Mon 2026-06-29 + Wed 2026-07-01 — no check-in either day) | Fri 2026-07-03 | 2 consecutive scheduled days | 👤 **STAFF ABSENT**: Eastwood missing 2 days. Last contact: [last check-in date]. Backup: [Ben calls replacement / you authorize temp hire] |

*Per `farm-cron-jobs.md` Job #9 escalation protocol.*
*Log format per `farm-cron-jobs.md` Job #9 (Staff Accountability Check). Update daily via cron job `farm-staff-check` (Mon/Wed/Fri 8:00 AM). Manual updates as needed.*