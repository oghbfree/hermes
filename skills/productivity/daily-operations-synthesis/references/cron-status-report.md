# Cron Status Report — Data Gathering & Formatting

## Purpose

The `cron-status-report` cron (09:00 daily, job ID `e0194bbb8309`) produces a Daily Cron Status Report and posts it to Telegram Topic 28 (jobs).

## Data Gathering Order

1. **`hermes cron list`** — Full job list with `last_run_at` and `last_status` per job. Parse for: total count, success/fail counts, jobs with `error` status, jobs with no `last_run_at` (never run).
2. **`hermes cron status`** — Verify gateway scheduler is running.
3. **`agent.log` grep for `cron`** — Recent execution timeline. Look for `completed successfully` vs error patterns.
4. **`session_search` (if available)** — Search for recent cron session output. Note: `session_search` is often denied in cron context; use log files as fallback.
5. **Error log tail** — `tail -50 ~/.hermes/logs/errors.log` for recent error patterns.

## Report Format

```
📊 DAILY CRON STATUS REPORT — [Day, Date]

📈 OVERVIEW
• Total jobs: N (all active)
• Success rate (24h): ~XX%
• Failed jobs: N (persistent)
• Stuck/paused: N

✅ RECENT RUNS (last 24h)
[Table or list of completed jobs with timestamps]

❌ FAILED / ERRORS
[Each failed job: name, last run time, error message, days since failure]

⚠️ KNOWN ISSUES (Carried)
[Persistent infrastructure issues: WhatsApp, Discord, etc.]

📋 DAY-BY-DAY TREND
[Compact table: date | SLA | failed | notes]

🔧 ACTION NEEDED
[Numbered priority list]

Footer: Report generated | Next report time
```

## Key Metrics to Extract

| Metric | Source | How |
|--------|--------|-----|
| Total jobs | `hermes cron list` | Count lines with `[active]` |
| Success rate (24h) | `hermes cron list` | Count `last_status: ok` vs `error` among jobs that ran in last 24h |
| Failed jobs | `hermes cron list` | Filter `last_status: error` |
| Gateway status | `hermes cron status` | Check for `✓ Gateway is running` |
| WhatsApp status | Known issue (carried) | Cron list shows WhatsApp job failures; verify no change |

## Known Persistent Failures (Carry Forward Until Resolved)

As of May 27, 2026 — check each for resolution:

| Job | Error | First Seen | Last Seen |
|-----|-------|------------|-----------|
| saturday-content-performance | Provider returned error | Pre-May 23 | May 23 |
| health-check-evening | Connection error | May 25 | May 26 |
| mum-health-evening | Connection error | May 26 | May 26 |

If a job has run successfully since last report, remove it from this table.

## Delivery

The `cron-status-report` job's `deliver` field is set to `origin`. **Produce the report as your final response text** — the system handles delivery automatically. Do NOT attempt `hermes send`, `hermes telegram send`, or any CLI messaging variant — they will fail with "invalid choice." Do NOT attempt to use the Bot API directly from the cron session unless the job's deliver field explicitly targets a Telegram chat/topic.

If the deliver field is set to `origin`, the response goes to the originating platform session. If it's set to e.g. `telegram:-1003784520976:26`, it goes to that topic directly. Check the job's `deliver` field in `jobs.json` to confirm.

**`execute_code` is blocked in cron mode.** Do not attempt to use it for Bot API calls or any other purpose from a cron job. Use only standard tools (`terminal`, `read_file`, `search_files`, etc.).

As of May 31, 2026, this job's origin delivers to Telegram group `-1003784520976` thread `1`. If Topic 28/26 routing is needed, update the job's `deliver` field via `hermes cron edit e0194bbb8309` rather than trying to post manually.

## Distinguishing Error Types

| Type | Meaning | Action |
|------|---------|--------|
| `RuntimeError: Connection error` | Telegram API or network failure | Escalating pattern — investigate |
| `RuntimeError: Provider returned error` | LLM provider (OpenRouter) failure | Check provider billing/rate limits |
| `RuntimeError: ERROR` | Generic cron execution error | Check job prompt and tool availability |
| `skill not found, skipping` | Skill name mismatch in job config | Update job's `skills` field |
| No `last_run_at` | Job hasn't run yet (new or paused) | Verify schedule; not necessarily an error |
