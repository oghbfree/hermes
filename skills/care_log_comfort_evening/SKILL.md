# SKILL: Geriatric Care Monitor (Comfort - Evening)

## DESCRIPTION
Executed daily at 7:00 PM. This skill captures the final health status of Comfort (91) for the day. It focuses on dinner intake, evening medication, and identifying any "sundowning" symptoms before sleep.

## CAPABILITIES
- Clinical Data Finalization
- End-of-Day Health Summary
- Critical Symptom Escalation

## WORKFLOW

### 1. Template Deployment
Post the following message to **Telegram Topic 51 (#health-log-mum)**:

"🌙 **MUM EVENING LOG - $(date +%F)**
*Comfort (91), Carer: H (Son)*

**Dinner:** **Drink:** **Medication taken:** [yes/no]
**Mobility:** [good/assisted/poor]
**Mood:** [good/low/confused]
**Symptoms:** [none/list]
**Severity:** [1-5]
**Notes:**"

### 2. Record Finalization
Upon response from the carer:
1. **Append**: Add the data to the existing daily file: `workspace/health/mum/$(date +%Y-%m-%d).md`.
2. **Medication Cross-Check**: Verify if medications were marked 'yes' in all three logs (Morning, Afternoon, Evening).
3. **Daily Trend Audit**: Compare the Evening mood/severity against the Morning/Afternoon entries.

### 3. Reporting & Alerting
- **If Severity is >= 4**: Immediately mirror to Telegram Topic 141 (#urgent).
- **Final Sync**: Mark the daily health file as "READY FOR CONSOLIDATION" so the Librarian includes it in the nightly system update.

## GUIDELINES
- **Tone**: Attentive and thorough.
- **Data Integrity**: This log is the "Closing Entry." Ensure H includes any specific observations about her readiness for sleep or nighttime restlessness in the Notes.
- **Error Handling**: Standard escalation to Topic 141 if Telegram delivery fails.