# Integrated Daily Synthesis — Cron Task Reference

**Cron job name:** `integrated-daily-synthesis`
**Schedule:** `5 22 * * *` (22:05 UTC+1 daily)
**Delivery:** Telegram topic 20 (briefing)
**Job ID:** `34314e3e73f8`

## Purpose
Compile a cross-domain daily synthesis covering health, business, team, security, and system health. This is the "end-of-day report" that ties together all operational threads.

## Data Sources (in order of reading)

1. **Health logs:**
   - H: `memories/health/H/HEALTH_LOG_YYYY-MM.md` (current month)
   - Comfort: `memories/health/mum/HEALTH_LOG_YYYY-MM.md` or latest dated file
   - Check cron output for delivery failures (DNS errors, connection errors)

2. **Business checkins:**
   - `memories/business/BUSINESS_CHECKINS_YYYY-MM.md`
   - Check WhatsApp gateway status from latest security audit or gateway_state.json

3. **Cron output files:**
   - `~/.hermes/cron/output/*/YYYY-MM-DD_*.md` (today's date)
   - Read all output files from the past 24 hours
   - Note: failed jobs have an `## Error` section instead of `## Response`

4. **Security audit:**
   - `memories/security/SECURITY_AUDIT_YYYY-MM-DD.md` (today's)
   - Or from the security-policy-check cron output

5. **System health:**
   - `~/.hermes/cron/jobs.json` — parse for job counts, success rates, errors
   - Disk: `df -h /c`
   - Session count: count `session_YYYYMMDD*` files

## Report Structure

```
# Integrated Daily Synthesis — YYYY-MM-DD (Day)

## 1. Health Status
  - H: responses, gap, clinical risk
  - Comfort: responses, gap, clinical risk
  - Trend analysis (compare to previous days)

## 2. Business Operations
  - WhatsApp status
  - 2Real Shop / Construction / Supply Chain
  - Content pipeline
  - Business checkin log

## 3. Team Status
  - Active team members and channel status
  - Recruitment pipeline
  - Communication assessment

## 4. Security Posture
  - FAIL items (carried + new)
  - Remediated items
  - Security trend

## 5. System Health
  - Cron execution summary (jobs fired, success rate, SLA)
  - Today's job log
  - System resources
  - Error log summary

## Priority Actions for Tomorrow
  - Top 5-7 actionable items, prioritized

## Learning Metrics & Key Insights
  - Quantitative snapshot (table comparing metrics over time)
  - Emerging patterns (2-3 paragraphs)
```

## Key Patterns to Track

| Metric | Where to Read | Trend Direction |
|--------|---------------|-----------------|
| Health responses | Cron output + health logs | ↑ Good |
| WhatsApp uptime | Gateway state + business log | ↑ Good |
| Cron SLA | jobs.json `last_status` | ↑ Good |
| Security FAIL count | Security audit | ↓ Good |
| Disk usage | `df -h` | ↓ Good |
| Session count | File count in sessions/ | ↓ Good |

## Pitfalls

- **Cron output files use local timestamps** — the filename timestamp may differ from the `Run Time` in the file header. Use the header.
- **Failed jobs have no `## Response` section** — they have `## Error` instead. Don't skip them; they're important signals.
- **New jobs won't have run yet** — jobs created today with no `last_run_at` are expected, not failures.
- **Health log gaps are normal** — don't flag every gap as a crisis. Look for patterns (3+ days = concerning).
- **DNS failures affect all Telegram deliveries simultaneously** — if one job fails with `getaddrinfo`, check others at the same time.
- **The synthesis replaces earlier versions** — if a nightly consolidation already ran, this synthesis should be more comprehensive and supersede it.

## File Output
Save to: `memories/insights/INTEGRATED_INSIGHTS_YYYY-MM-DD.md`
