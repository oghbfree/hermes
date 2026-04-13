# SKILL: Integrated Daily Synthesis & Learning Capture

## DESCRIPTION
Executed at 10:00 PM daily. This is the system's "Closing Ceremony." It captures specific learning metrics from LEARNING_SYSTEM.md and synthesizes the day's health, business, and raw data into a permanent insight file.

## WORKFLOW

### 1. Data Aggregation
Read all logs from the current date:
- **Health**: `memory/health/LOG-$(date +%Y-%m).md`
- **Business**: `memory/business/BUSINESS_CHECKINS_$(date +%Y-%m).md`
- **System Logs**: `memory/logs/SECURITY_LOG_$(date +%Y-%m).md`
- **Learning Core**: `LEARNING_SYSTEM.md` (to access the Capture Template).

### 2. Learning Capture (The Merge)
Using the template from `LEARNING_SYSTEM.md`, document:
- **What Worked**: High-efficiency moments or successful system triggers.
- **What Failed**: Errors, model switches, or manual friction.
- **Rule Proposals**: Based on today's friction, propose 1 new rule for `memory/rules.md`.

### 3. Synthesis & Documentation
Create `memory/insights/INTEGRATED_INSIGHTS_$(date +%Y-%m-%d).md`:

# 🧩 DAILY INTEGRATED SYNTHESIS | $(date +%F)

### 🏥 HEALTH & VITALS
[Summary of AM/PM/EOD logs]

### 🎓 DAILY LEARNING CAPTURE
- **Key Insight**: [Single biggest takeaway]
- **Worked**: [Successes]
- **Failed**: [Friction/Errors]
- **Proposed Rule**: [Logic to prevent future failure]

### 💼 BUSINESS PULSE
[Status of Sammy/Kanzoni/Ghana interactions]

### 🚀 ACTION ITEMS FOR TOMORROW
[Top 3 priorities]

---

### 4. Cleanup & Notification
- Post the **Key Insight** and **Proposed Rule** to Telegram Topic 2.
- Redact any sensitive tokens found during the synthesis.