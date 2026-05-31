# Cron Health Audit Procedure

Procedure for auditing cron job execution health on this host. Used by the `cron-status-report` job (ID: `3d3e868ba056`, schedule: `0 9 * * *`, delivers to topic 20).

## Data Sources

### 1. Job List and State

```bash
hermes cron list
```

Returns all 25+ jobs with: ID, name, schedule, repeat count, next_run_at, last_run_at, last_status, last_error, deliver target.

Key fields:
- `last_status`: `ok` | `error` | null (never run)
- `last_error`: null or error string
- `last_run_at`: ISO timestamp of last execution

### 2. Execution Log (agent.log)

```bash
# All completions in a time window
grep "completed successfully\|Job.*failed" /c/Users/User/.hermes/logs/agent.log | grep "cron.scheduler"

# Full detail for one job
grep "cron_<job_id>" /c/Users/User/.hermes/logs/agent.log | tail -30
```

### 3. Error Log

```bash
tail -100 /c/Users/User/.hermes/logs/errors.log
grep -i "cron\|job\|runtime\|401\|timeout\|connection" /c/Users/User/.hermes/logs/errors.log | tail -30
```

### 4. Gateway Log (network issues)

```bash
grep -i "telegram\|network\|error\|restart" /c/Users/User/.hermes/logs/gateway.log | tail -30
```

### 5. Jobs State File

```bash
cat /c/Users/User/.hermes/cron/jobs.json
```

## Audit Steps

1. **Define window**: typically 24h, from last audit to now.
2. **Count executions**: grep agent.log for completions within window, group by job name.
3. **Cross-reference expected vs actual**: for each job due in the window, verify completion exists. If due but missing → SKIPPED. If `last_status: error` → FAILED.
4. **Calculate SLA**: `(completed) / (completed + failed) × 100%`. Exclude pending jobs from denominator.
5. **Categorize errors**: extract from `last_error` in jobs.json, ERROR lines in agent.log, stack traces in errors.log. Rate 🔴 CRITICAL / 🟡 WARNING / ℹ️ INFO.
6. **Compile report**: execution summary, error log, recovery actions.

## Jobs by Frequency

**Daily (18-20 runs/day):** cron-status-report, security-watchdog (4x/6h), daily-system-briefing, health-check-morning, mum-health-morning, job-applications-check, mum-health-afternoon, health-check-afternoon, mum-health-evening, health-check-evening, integrated-daily-synthesis, daily-backup, nightly-consolidation, ghana-supplier-outreach (Mon-Sat), workflow-48h-maintenance (every 48h)

**Weekly:** saturday-content-performance (Sat), weekly-learning-review (Mon), health-weekly-review-h (Sun), health-weekly-review-mum (Sun), github-memory-backup (Sun), sunday-content-engine (Sun), ghana-supplier-analysis (Mon), ghana-steering-verification (Wed), quarterly-synthesis (Thu)

**Monthly:** monthly-evolution (1st)

## Common Error Patterns on This Host

### OpenRouter 401
- `RuntimeError: Error code: 401 - Missing Authentication header`
- Credential pool exhausted. Check: `grep "exhausted\|401" ~/.hermes/logs/agent.log | tail -5`
- Remedy: Verify OPENROUTER_API_KEY in ~/.hermes/.env

### Telegram DNS Failures
- `[Errno 11001] getaddrinfo failed` for api.telegram.org
- Typically self-recovers in 5-40s. Low severity unless sustained >5 min.

### Memory Tool Unavailable in Cron
- `Memory is not available. It may be disabled in config or this environment.`
- Expected behavior. Write persistence to files, not memory tool.

### AGENTS.md BOM
- `Context file AGENTS.md blocked: invisible unicode U+FEFF`
- Save file as UTF-8 without BOM to fix.

### WhatsApp Bridge Exits
- `WhatsApp bridge process exited unexpectedly (code 1)`
- Gateway auto-recovers. Monitor frequency in gateway.log.

## Report Format

```
EXECUTION SUMMARY
- Jobs executed: N/M (X%)
- Completed: N | Failed: N | Pending: N
- SLA: X%

ERROR LOG
- Time | Job | Error | Impact | Severity

RECOVERY ACTIONS
- Per failure: specific remediation step
```

## Verification

- [ ] All expected jobs accounted for
- [ ] Each failure has a recovery action
- [ ] SLA calculated correctly
- [ ] Timestamps within window
