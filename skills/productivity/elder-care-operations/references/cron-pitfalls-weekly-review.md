# Cron Job Pitfalls — Elder Care Weekly Review

## `send_message` Tool Does Not Exist

**Symptom:** The weekly review cron prompt (dad-health-weekly-review, job `4f3e7b73e103`) says "Use send_message to post the weekly report to telegram:-1003784520976:1" — but `send_message` is not an available tool in this environment.

**What actually happens:** The cron system delivers the agent's final response automatically to the configured Telegram destination. The agent should just produce the report as its final text output.

**Action required:** Update the cron job prompt to remove the `send_message` instruction. Until then, agents should ignore that step.

## `elder-care-dad` Skill Not Found

**Symptom:** The cron prompt says "Read the elder-care-dad skill for full context" but `elder-care-dad` was consolidated into `elder-care-operations`. The skill loading fails silently.

**Fix:** Update cron job prompts to reference `elder-care-operations` instead, or rely on the agent reading the care log and FAMILY_INSIGHTS_DAD.md directly.

## Care Log Fields All Blank

**Symptom:** Every field in the weekly care log shows "—" (unfilled template). All check-in templates exist but no data was entered by carers/family.

**What to report:** This IS the finding. Do NOT suppress the report with `[SILENT]`. Report:
- Compliance rate: 0%
- Which days/fields are affected
- Systemic recommendations (carer assignment, alternative reporting channel)

## File Paths (Confirmed May 2026)

| Person | Care Log | Structured Doc |
|--------|----------|----------------|
| Dad | `C:\Users\User\CARE_LOG_DAD_YYYY-MM.md` | `C:\Users\User\.hermes\workspace\FAMILY_INSIGHTS_DAD.md` |
| Mum | `C:\Users\User\CARE_LOG_COMFORT_YYYY-MM.md` | (create if needed) |

## Weekly Report Format

```
📊 [Person]'s Weekly Health Review — [date range]
🔴 Red Flags / 🟡 Watch / 🟢 Good
📈 Trends summary
💡 Recommendations
```

- Be concise and actionable
- Include specific data completeness metrics
- Flag medication compliance gaps (especially DAPT for dad)
- Note upcoming appointments
