# SKILL: Weekly Learning & Systems Review

## DESCRIPTION
Executed every Monday at 9:00 AM. This skill performs a high-level audit of the previous week's data to extract permanent rules, identify recurring friction, and set the strategic direction for the new week.

## CAPABILITIES
- Multi-file Trend Analysis
- Pattern Extraction (Rules/Formulas)
- Strategic Planning
- Long-term Memory Archiving

## WORKFLOW

### 1. Evidence Collection
Scan the `memory/insights/` directory and read the last 7 files matching the pattern:
- `INTEGRATED_INSIGHTS_YYYY-MM-DD.md`
Also review:
- `tasks-queue.md` (for overdue or rolling items).

### 2. Analytical Processing
Compare the 7 days of insights to determine:
- **Health Trends**: Is energy rising or falling across the week?
- **Learning Patterns**: What new rules or formulas were captured most frequently?
- **Recurring Issues**: What "Blockers" or "Fails" appeared more than twice?
- **Key Wins**: The top 3 achievements of the week.

### 3. Documentation
Create a new file: `memory/analysis/WEEKLY_ANALYSIS_$(date +%Y-%m-%d).md` using this template:

# 📊 WEEKLY SYSTEM ANALYSIS | Week of $(date -d "7 days ago" +%F) to $(date +%F)

### 🏥 HEALTH TRENDS
[Summary of physical/mental state over the 7-day period]

### 💡 EVOLVED RULES & FORMULAS
[List any new permanent logic or "rules of thumb" discovered this week]

### 🏆 KEY WINS
[The three most impactful outcomes]

### 📉 RECURRING ISSUES & FRICTION
[List things that repeatedly slowed down the system or the user]

### 🎯 GOALS FOR NEXT WEEK
[Based on the patterns, what are the 3 strategic focus areas?]

---

### 4. System Update
If any "New Rules" were identified, append them to a master `memory/rules.md` file to ensure the agent's core personality and logic evolve.

### 5. Notification
Post a summary of "Key Wins" and "Goals for Next Week" to Telegram Topic 2.

## GUIDELINES
- **Tone**: Strategic, objective, and "Librarian-style" meticulousness.
- **Data Integrity**: Ensure the review spans exactly the last 7 days.
- **Format**: Use clean Markdown tables for health trends if possible.