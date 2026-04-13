# SKILL: Internal Security Watchdog

## DESCRIPTION
Executed every 2 hours. This is an internal-only audit skill designed to protect the integrity of the OpenClaw workspace, prevent credential leakage, and ensure data privacy compliance.

## CAPABILITIES
- Workspace File Auditing
- API Token Detection & Redaction
- Data Leakage Verification
- High-Priority Alerting

## WORKFLOW

### 1. Internal Log Audit
- Scan the `\tmp\openclaw\` directory for recent logs.
- Use regex to detect exposed API keys (e.g., `sk-...`, `ghp_...`, `tg_...`).
- **ACTION**: If found, redact the log file immediately and flag as CRITICAL.

### 2. Workspace Integrity Scan
- Check for unauthorized file creations or modifications in the `memory/` and `skills/` directories since the last check.
- Verify that no private files (Health Logs, Financials) have been accessed by external tools.

### 3. Outbound Channel Verification
- Audit the last 2 hours of the Telegram delivery log.
- **CRITERIA**: Confirm 100% of messages were sent ONLY to Group `-1003620024352`.
- **CRITERIA**: Confirm sensitive data topics (Health/Finance) were not cross-posted to public threads.

### 4. Documentation
Append the results to `memory/logs/SECURITY_LOG_$(date +%Y-%m).md` using this format:
- `[Timestamp]` | `[Check Name]` | `[Status: PASS/FAIL]` | `[Action Taken]`

### 5. Escalation Logic
- **IF ALL PASS**: Do not post to Telegram (keep the channel quiet).
- **IF ANY FAIL**: 
    - Log as **CRITICAL**.
    - **POST ALERT** to Telegram Topic 141 (#urgent) with details of the failure and the specific file/log affected.

## GUIDELINES
- **Strict Privacy**: Do not send the contents of the logs over Telegram. Only send the *fact* that a failure occurred and which file requires manual attention.
- **Persona**: The Librarian (Security Focus) - Vigilant, silent unless there is a problem.
- **Environment**: This skill must run in an isolated session to prevent the audit itself from leaking data.