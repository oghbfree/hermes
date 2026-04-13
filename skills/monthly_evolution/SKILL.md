# SKILL: Monthly Evolution & Macro-Review

## DESCRIPTION
Executed on the 1st of every month at 9:00 AM. This skill performs a high-level audit of the previous month's weekly analyses to document growth, pivot points, and overarching business/health trajectories.

## CAPABILITIES
- Macro-Data Synthesis
- Business Metric Tracking
- Evolution Journaling
- Strategic Goal Alignment

## WORKFLOW

### 1. File Retrieval
Scan the `memory/analysis/` directory and read all files from the previous month:
- `WEEKLY_ANALYSIS_YYYY-MM-DD.md`
- Identify any `INTEGRATED_INSIGHTS` that were flagged as "High Importance" during the month.

### 2. Macro-Analysis
Compare the four (or five) weekly reports to determine:
- **Health Evolution**: Is there a 30-day trend in energy or symptom management?
- **Learning Evolution**: Which new rules have become "habits" or "permanent logic"?
- **Business Progress**: Check the "Business Pulse" status from the daily briefings to see monthly movement on John, Sammy, Ghana Supplier, and Akoma Robotics.
- **Key Metrics**: Aggregate any quantitative data (e.g., FX trends, task completion rates).

### 3. Documentation
Create a new file: `memory/evolution/MONTHLY_EVOLUTION_$(date +%Y-%m).md` using this template:

# 🧬 MONTHLY EVOLUTION | $(date -d "last month" +%B %Y)

### 📈 BUSINESS PROGRESS & PULSE
[Status update on key business entities and supplier relations]

### 🏥 HEALTH EVOLUTION
[Macro-summary of physical/mental trends across 30 days]

### 📚 LEARNING EVOLUTION
[Summary of the most significant mindset or system logic shifts]

### 📊 KEY METRICS
[Consolidated data points: FX averages, completion rates, etc.]

### 🏆 BIGGEST WIN & 💀 BIGGEST FAILURE
- **Win**: [The standout achievement of the month]
- **Failure**: [The biggest lesson learned through a mistake]

### 🚀 GOALS FOR NEXT MONTH
[List top 5 strategic objectives for the new month]

---

### 4. Memory Consolidation
Archive the past month's `INTEGRATED_INSIGHTS` into a `memory/archive/$(date +%Y-%m)/` sub-folder to keep the active directory clean.

### 5. Notification
Post a "Monthly Evolution Snapshot" to Telegram Topic 2, highlighting the **Biggest Win** and the **Top 3 Goals** for the new month.

## GUIDELINES
- **Persona**: The Librarian - focused on long-term continuity and structural integrity.
- **Tone**: Professional, reflective, and high-level.
- **Data Range**: Ensure it covers from the 1st to the last day of the previous month.