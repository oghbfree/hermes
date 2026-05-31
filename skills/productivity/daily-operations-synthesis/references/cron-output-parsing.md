# Cron Output Parsing Reference

**Last updated:** 2026-05-27

## [SILENT] vs Error vs send_message unavailable — 3-Way Distinction

When reading health-check cron output files, classify the outcome into one of three categories:

### 1. [SILENT] — No Data to Report
- **Output:** Agent responds with literal `[SILENT]`
- **Meaning:** Agent had nothing to report (empty data source, no responses captured)
- **Not a failure** — it means the data source was empty
- **Example:** mum-health-afternoon returning `[SILENT]` because no carer data exists
- **Report as:** `⚠️ SILENT`
- **Action:** Track as data gap, not delivery failure

### 2. Connection Error — Transient Network/API Failure
- **Output:** `## Error` section with `RuntimeError: Connection error`
- **Meaning:** Telegram API or network path failed during the 19:00 time window
- **Usually transient** — affects evening jobs simultaneously across multiple topics
- **Example:** Both health-check-evening (topic 2) AND mum-health-evening (topic 4) failing with Connection error on the same evening
- **Report as:** `❌ Connection error`
- **Action:** Track duration; if 3+ consecutive days, investigate network path

### 3. send_message Unavailable — Tool Not in Cron Context
- **Output:** `## Response` body contains phrases like "I don't have a `send_message` tool", "My available tools don't include Telegram", "no send_message tool available in my current toolset"
- **Meaning:** The cron session lacks the send_message tool entirely. The agent composed the prompt but couldn't deliver it.
- **Different from [SILENT]:** The agent had content to deliver but the mechanism was missing
- **Different from Connection error:** No network failure; the tool simply doesn't exist in this session
- **Example:** health-check-afternoon (13:02) responding "I don't have a `send_message` tool available"
- **Report as:** `❌ Failed — send_message unavailable`
- **Action:** Note in health summaries. This is a systemic cron delivery issue, not a per-job config problem.

### Classifying Any Health Check Output
1. Check for literal `[SILENT]` → Category 1
2. Check `## Error` section for `RuntimeError: Connection error` → Category 2
3. Check `## Response` body for "no send_message" / "don't have a send_message" / "tools don't include Telegram" → Category 3
4. If the `## Response` body contains the health check prompt text delivered as the agent's final response → **Success** (auto-delivered via cron's `deliver` field)

### Cron Output File Structure
Each file has this structure:
```
# Cron Job: <name>
**Job ID:** <id>
**Run Time:** <timestamp>
## Prompt
...
## Response
...
## Error        ← Only present if job failed
```

## Data Source Details

### Reading `~/.hermes/cron/jobs.json`

This file is large (~54KB, 1448+ lines). Key things to extract:

1. **Total enabled jobs:** Count `"enabled": true`
2. **Jobs that fired today:** Look for `"last_run_at"` with today's date (format: ISO 8601, e.g. `"2026-05-20T09:02:24.534002+01:00"`)
3. **Success count:** Count `"last_status": "ok"` among jobs that ran today
4. **Failure count:** Count `"last_status": "error"` among jobs that ran today (note: value is `"error"`, NOT `"failed"`)
5. **Failed job names:** grep for `"last_status": "error"` and get the nearest `"name"` field above it
6. **New jobs (never ran):** Jobs where `last_run_at` key is **absent entirely** (not `null`, not `"null"` — just missing). These haven't fired yet, not failures.
7. **Paused jobs:** Check for `"enabled": false` — these are intentionally disabled, not stuck.

**Parsing tips:**
- Use `grep -oP '"last_run_at":\s*"[^"]*"'` to extract all last_run_at timestamps
- Use `grep -oP '"last_status":\s*"[^"]*"' | sort | uniq -c` to get status counts
- Use `grep -oP '"enabled":\s*(true|false)' | sort | uniq -c` to check for paused jobs
- For MSYS bash: avoid `node -e` with inline Windows paths (gets mangled). Write a temp `.js` file instead.
- Python (`python3`) may not be on PATH in MSYS. Use `execute_code` for Python parsing.

### Reading Cron Output Files — Enumerate First

Cron output filenames use local time with dashes (e.g., `2026-05-27_19-00-44.md`). **Never guess filenames.** Use `terminal` with `ls` first, then iterate:

```bash
# List all job output directories
ls ~/.hermes/cron/output/

# List today's files for a specific job
ls ~/.hermes/cron/output/<job-id>/2026-05-27*
```

Then `read_file` each enumerated file. MSYS path resolution for wildcards in `read_file` is unreliable — always enumerate first.

### No `hermes cron logs` Subcommand

There is **no** `hermes cron logs` command. The available subcommands are:
`list, create, add, edit, pause, resume, run, remove, rm, delete, status, tick`

To inspect execution history:
- `hermes cron list` — shows last_run_at + last_status per job
- `hermes cron status` — checks if gateway scheduler is running (PID, next run)
- Read `~/.hermes/logs/agent.log` and `~/.hermes/logs/errors.log` directly for detailed execution logs
