# Staff Attendance Log — 2Real Enterprises
**Last Updated:** 27/11/26  
**Authoritative Record:** This file is the single source of truth for staff attendance

---

## 📝 HOW TO LOG (Via Telegram)

**Simple format:**
```
Kyei attended 9am-5pm shop cleaning + stock organizing
Sammy attended 10am-6pm Jiji listings + customer calls
```

**Or just hours:**
```
Kyei 9-5
Sammy 10-6
```

**I will parse and log automatically when you send these to Telegram.**

---

## 📊 ATTENDANCE RECORDS

### **Format:**  
`DATE | STAFF | HOURS | ACTIVITY | NOTES`

---

## November 2026

| DATE | STAFF | HOURS | ACTIVITY | NOTES |
|------|-------|-------|----------|-------|
| 27/11/26 Wed |  |  |  | *First entry - log starts today* |
| 18/11/26 Wed | Kyei | 1h | — | Agreement day 2 — H confirmed "today" |
| 17/11/26 Tue | Kyei | 1h | — | Agreement day 1 — H confirmed "worked yesterday" |

---

## October 2026

| DATE | STAFF | HOURS | ACTIVITY | NOTES |
|------|-------|-------|----------|-------|
| 22/10/26 Tue | Kyei | 1hr | Cleaning cables/laptop chargers | Pre-agreement trial — formal agreement started Nov 2026 |

---

## STAFF ROSTER

### **Active Staff:**

#### **1. Kyei** — Shop helper
**Agreement:** Verbal with H, week of 9–15 Nov 2026  
**Recorded:** 18/11/26  
**Reference:** `Vault/business/2real/staff/KYEI_WORK_AGREEMENT.md`  
**WhatsApp:** 0503344556 (233503344556@s.whatsapp.net)

**Weekly Schedule (16 hours total):**
- **Tue/Wed/Thu/Fri:** 1 hour each (4 hours)
- **Sat/Sun/Mon:** 4 hours each (12 hours)

**Pattern:** 1h on days H works, 4h on H's days off (Sun/Mon) + Saturday  
**Coverage role:** Kyei is the presence on Sunday and Monday when H isn't there

**Tasks:** Cleaning, organizing stock, inventory prep  
**Notes:** Visual learner - show don't tell

**⚠️ NOT YET CONFIRMED:** Pay rate, pay currency, payment day, formal scope of duties

**⚠️ IDENTITY:** Confirm WhatsApp number/chat for Kyei (staff). Two OTHER Kyeis exist:
- Anita Kyei (user_id 6454140) — job applicant, NOT staff
- Godfred Kyei (user_id 6739188) — Jiji buyer, NOT staff

#### **2. Sammy** — 2Real operations
   - Tasks: Jiji listings, customer inquiries, deliveries, shop operations
   - Notes: Primary shop operator

### **Inactive/Former Staff:**
- **John** — Field ops (now Akoma Robotics full-time)
- **Frederick** — Repair tech (availability unclear, no longer primary)

---

## USAGE PATTERNS TO TRACK

### **Kyei's Schedule:**
- **Weekly:** 16 hours (4 × 1h + 3 × 4h)
- **Light days (1h):** Tue, Wed, Thu, Fri — when H is working
- **Heavy days (4h):** Sat, Sun, Mon — Sat is work day, Sun/Mon are H's days off
- **Coverage:** Kyei provides presence on Sun/Mon when H isn't there

### **Expected Patterns:**
- Tue-Sat: Both working (H full day, Kyei 1h on Tue-Fri, 4h on Sat)
- Sun-Mon: Kyei only (4h each, H's days off)

### **Flags to track:**
- ⚠️ No-show without notice
- ⚠️ Late arrival (>30 min from scheduled start)
- ⚠️ Early departure
- ⚠️ Supervision gap issues (work not checked until next H workday)
- ✅ Extra hours beyond schedule
- ✅ Flexible coverage when needed

### **Monthly Summary:**
- Total days worked
- Total hours
- Attendance rate
- Key activities

### **Flags:**
- ⚠️ No-show without notice
- ⚠️ Late arrival (>30 min)
- ⚠️ Early departure
- ✅ Extra hours
- ✅ Weekend/Sunday work

---

## AUTOMATION RULES

### **When you send to Telegram:**
Pattern 1: `Kyei attended 9am-5pm [activity]`  
Pattern 2: `Kyei 9-5`  
Pattern 3: `Kyei attended today`  
Pattern 4: `Sammy 10-6 Jiji + deliveries`

**I will:**
1. Parse name, hours, activity
2. Log to this file
3. Confirm back to you

### **Daily reminder (optional):**
Could set up 7pm cron: "Log today's attendance? (Kyei, Sammy)"

---

## PAYROLL INTEGRATION

**⚠️ PAY DETAILS NOT YET CONFIRMED FOR KYEI:**
- Pay rate: *TBD*
- Pay currency: *TBD (GHS or £?)*
- Payment day: *TBD*
- Payment method: *TBD*

**DO NOT calculate wages until H provides rate.**

This log tracks **HOURS ONLY** until pay terms are confirmed.

### **When pay is confirmed:**
- Weekly hours × rate = pay
- Track here, calculate separately
- Payment records in separate file

### **This log feeds into:**
- Weekly pay calculations (once rate confirmed)
- Performance reviews
- Attendance patterns
- Hiring decisions

**Sammy arrangement:** *(to be confirmed)*

---

## NOTES

- **Source of truth:** This file only. No separate sheets.
- **Logging:** Via Telegram to sat-nav (I parse and append)
- **Review:** Weekly on Saturdays with sales review
- **Backup:** Part of daily GitHub backup (06:00 topic 20)
