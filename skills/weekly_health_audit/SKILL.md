# SKILL: Weekly Health Intelligence Audit

## DESCRIPTION
Executed every Sunday at 09:00 AM. This skill performs a longitudinal analysis of health data for both the user (H) and Mum (Comfort). It identifies correlations between nutrition, medication, and physical/mental states.

## CAPABILITIES
- Data Aggregation (7-day window)
- Pattern Recognition (Energy/Mobility Trends)
- Clinical Risk Assessment

## WORKFLOW

### 1. Data Retrieval
- **User (H)**: Read `workspace/health/*.md` for the last 7 days.
- **Mum (Comfort)**: Read `workspace/health/mum/*.md` for the last 7 days.

### 2. The "Crunch" (Analysis)
For each profile, determine:
- **Best/Worst Day**: Based on mood, energy, and symptom severity.
- **Symptom Tracking**: Identify recurring issues (e.g., "headaches 3/7 days").
- **Medication Audit**: Percentage of doses successfully taken.
- **Correlation**: (e.g., "Mum's confusion increases on days with lower fluid intake").

### 3. Reporting (Multi-Topic Delivery)
1. **Topic 50 (H Health)**: Post the "H WEEKLY HEALTH" summary.
2. **Topic 51 (Mum Health)**: Post the "MUM WEEKLY HEALTH" summary.
3. **Topic 141 (Urgent)**: **ONLY** post if a "Red Zone" is identified (e.g., 3+ days of severity >4, or zero medication compliance).

### 4. Archiving
Save the full detailed markdown reports to:
- `workspace/health/weekly/H-$(date +%F).md`
- `workspace/health/weekly/MUM-$(date +%F).md`

## GUIDELINES
- **Agent**: Use "Cruncher" for analytical depth.
- **Disclaimer**: Maintain a note that this is an AI-generated summary for tracking and not medical advice.
- **Error Handling**: If files are missing for >2 days of the week, note "Insufficient Data" in the report and alert Topic 2.