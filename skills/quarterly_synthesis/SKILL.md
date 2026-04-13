# SKILL: Quarterly Strategic Synthesis

## DESCRIPTION
Executed every Thursday (as per existing cron) to maintain a rolling quarterly perspective, or specifically at the end of a Quarter. This skill performs a "deep scan" of the last three months of evolution to filter out noise and extract the highest-level strategic signals.

## CAPABILITIES
- Strategic Pattern Matching
- Long-term Metric Aggregation
- System Logic Auditing
- Executive Goal Setting

## WORKFLOW

### 1. Archive Access
Scan the `memory/evolution/` directory and ingest:
- The last 3 `MONTHLY_EVOLUTION_YYYY-MM.md` files.
- The `memory/rules.md` master file (to see what was added vs. what was actually effective).

### 2. High-Level Audit
Evaluate the 90-day window for:
- **Strategic Progress**: Did the "Goals for Next Month" across the last 3 months actually result in a "Strategic Win"?
- **Health Progress**: Identify the dominant physical/mental state of the quarter.
- **Business Evolution**: Summarize the 90-day movement for John, Sammy, Ghana Supplier, Akoma Robotics, and 2Real Shop.
- **Key Insights**: What is the most profound lesson learned in the last 90 days?

### 3. Documentation
Create a new file: `memory/analysis/QUARTERLY_SYNTHESIS_$(date +%Y-Q$(expr $(date +%m) / 4 + 1)).md` using this template:

# 💎 QUARTERLY STRATEGIC SYNTHESIS | [Year]-Q[#]

### 🏗️ BUSINESS & STRATEGIC PROGRESS
[Summary of major project milestones and business entity status]

### 🩺 HEALTH & VITALITY PROGRESS
[90-day overview of wellness trends and energy baselines]

### 🧠 EVOLVED OPERATING SYSTEM
[List the most important rules/formulas that proved successful this quarter]

### 🏆 STRATEGIC WINS & ⚠️ STRATEGIC FAILURES
- **Wins**: [Major outcomes that moved the needle]
- **Failures**: [Systemic errors or missed strategic targets]

### 💡 THE QUARTERLY THEME
[One sentence defining the "lesson" or "focus" of the past 90 days]

### 🎯 GOALS FOR NEXT QUARTER
[3-5 high-level objectives for the upcoming 90 days]

---

### 4. System Optimization
- **Rule Pruning**: Identify any rules in `memory/rules.md` that were created but never mentioned in the Weekly or Monthly reports. Flag them for removal.
- **Archive Management**: Move the previous quarter's Weekly and Monthly files into a `memory/archive/[Year]/Q[#]/` folder structure.

### 5. Notification
Post a "Quarterly Strategic Overview" to Telegram Topic 2. Focus on the **Quarterly Theme** and **Goals for Next Quarter**.

## GUIDELINES
- **Tone**: Executive, ruthless on efficiency, and deeply analytical.
- **Perspective**: Do not focus on daily tasks; focus on milestones and identity shifts.
- **Format**: Use clear headers and concise bullet points.