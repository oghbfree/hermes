# SKILL: System Health & Cron Auditor

## DESCRIPTION
Executed daily at 9:00 AM. This skill acts as the system's "Check Engine" light. It audits the internal state of all defined crons, identifies failures or missed windows, and provides a clear diagnostic report to the user.

## CAPABILITIES
- JSON State Parsing (jobs.json)
- Error Log Analysis
- System Status Reporting

## WORKFLOW

### 1. The Audit
Read the system's core scheduling file: `C:\Users\User\.openclaw\cron\jobs.json` (or equivalent path for your installation).
For each cron entry, extract:
- `name`
- `lastRunStatus`
- `lastRunAtMs`
- `consecutiveErrors`

### 2. Failure Detection
- **MISSED**: If `nextRunAtMs` is in the past and `lastRunAtMs` hasn't updated.
- **FAILED**: If `lastRunStatus` is "error".
- **CRITICAL**: If `consecutiveErrors` > 0.

### 3. Documentation
Generate the report table:

# 🛠️ DAILY CRON STATUS REPORT | $(date +%F)

| Cron Name | Scheduled | Status | Notes |
| :--- | :--- | :--- | :--- |
| [Name] | [Time] | [✅ OK / ❌ FAIL / ⚠️ MISSED] | [Error Message snippet if applicable] |

### 4. Alerting Logic
If any cron has a "FAIL" or "MISSED" status:
1. Prepend the Telegram message with: "🚨 **ATTENTION REQUIRED: SYSTEM FRICTION DETECTED**"
2. Specifically list the `lastError` for any failed jobs so the user knows exactly what to fix (e.g., "Module Not Found" or "Unauthorized ChatId").

### 5. Notification
Post the report to **Telegram Topic 2 (#cron-status)**.

## GUIDELINES
- **Persona**: The Librarian (Technical Auditor).
- **Precision**: Do not guess; use the timestamps in the JSON to verify execution.
- **Actionable**: If a job fails, the "Notes" column must include the specific error message from the `state` object.