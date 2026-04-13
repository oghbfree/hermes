# SKILL: Geriatric Care Monitor (Comfort - Afternoon)

## DESCRIPTION
Executed daily at 1:00 PM. This skill tracks midday nutrition, hydration, and medication compliance for Comfort (91). It serves as the midday bridge to identify any "sundowning" or physical decline early in the day.

## CAPABILITIES
- Clinical Data Templating
- Historical Comparison
- Urgent Symptom Escalation

## WORKFLOW

### 1. Template Deployment
Post the following message to **Telegram Topic 51 (#health-log-mum)**:

"🍽️ **MUM AFTERNOON LOG - $(date +%F)**
*Comfort (91), Carer: H (Son)*

**Lunch:** **Drink:** **Medication taken:** [yes/no]
**Mobility:** [good/assisted/poor]
**Mood:** [good/low/confused]
**Symptoms:** [none/list]
**Severity:** [1-5]
**Notes:**"

### 2. Data Processing & Comparison
Upon response from the carer:
1. **Append**: Add the data to the existing file: `workspace/health/mum/$(date +%Y-%m-%d).md`.
2. **Medication Audit**: If "Medication taken" is `no`, flag this immediately for the user to check the prescription schedule.
3. **Change Detection**: Compare the "Mood" and "Mobility" against the **08:00 AM** entry. If there is a decline (e.g., went from 'good' to 'confused'), trigger an alert.

### 3. Alerting
If Severity is >= 4 OR there is a significant decline since morning:
- **Ping Telegram Topic 141 (#urgent)**: "⚠️ **MUM HEALTH UPDATE: MIDDAY DECLINE DETECTED**. Review afternoon log in Topic 51."

## GUIDELINES
- **Tone**: Diligent and observant.
- **Consistency**: Use the exact pipe-separated format for the final log to ensure the `nightly-consolidation` script can parse it.
- **Error Handling**: If the Telegram message fails to post, retry once, then alert Topic 141.