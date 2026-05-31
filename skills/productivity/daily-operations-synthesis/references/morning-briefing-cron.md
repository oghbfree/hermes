# Morning Briefing Cron — Reference

**Cron job name:** `daily-system-briefing`
**Schedule:** `36 6 * * *` (06:36 UTC+1 daily)
**Delivery:** Telegram topic 20 (briefing), via `origin` (auto-delivers to the topic where the job is configured)
**Job ID:** `c9637a3c5a4f`
**Created:** 2026-05-18T16:04:30 UTC+1

## Purpose

The morning briefing is the first thing H sees each day. It must be:
- **Scannable** — H hasn't had coffee. Use tables, emojis, compact sections.
- **Action-oriented** — TODAY'S PRIORITIES is the most important section.
- **Forward-looking** — Focus on what's happening today, not a deep retrospective.
- **Honest about gaps** — If health data is stale, say so plainly.

## Data Gathering Order

1. `~/.hermes/cron/jobs.json` — parse for SLA stats, pending first-runs
2. `~/.hermes/logs/gateway.log` (tail -50) — check Telegram/WhatsApp connectivity
3. `~/.hermes/logs/errors.log` (tail 20-30 lines) — recent errors
4. Health logs (both paths for H, memories/ path for Comfort)
5. `~/.hermes/workspace/memories/insights/INTEGRATED_INSIGHTS_YYYY-MM-DD.md` (yesterday's synthesis)
6. `df -h /c` — disk usage
7. Security audit output (latest)

## Key Differences from Nightly Synthesis

| Aspect | Morning Briefing | Nightly Synthesis |
|--------|-----------------|-------------------|
| Length | ~400-500 words | ~600-800 words |
| Health detail | Gap + risk only | Full trend analysis |
| Cron detail | SLA + pending first-runs | Full job log |
| Business detail | Status lines only | Detailed breakdown |
| Security detail | FAIL count + trend | Full tables |
| Key section | TODAY'S PRIORITIES | LEARNING METRICS |
| Team section | Omit or one-liner | Full table |
| Weekly overview | Include compact table | Omit |

## Common Data Sources

| Data | Path |
|------|------|
| H health log (canonical) | `C:\Users\User\HEALTH_LOG_YYYY-MM.md` |
| H health log (backup) | `memories/health/H/HEALTH_LOG_YYYY-MM.md` |
| Comfort health log | `memories/health/mum/health-log.md` |
| Comfort care log | `C:\Users\User\CARE_LOG_COMFORT_YYYY-MM-DD.md` |
| Yesterday's synthesis | `memories/insights/INTEGRATED_INSIGHTS_YYYY-MM-DD.md` |
| Cron jobs | `~/.hermes/cron/jobs.json` |
| Gateway log | `~/.hermes/logs/gateway.log` |
| Error log | `~/.hermes/logs/errors.log` |
| Security audit | `memories/security/SECURITY_AUDIT_YYYY-MM-DD.md` |

## Telegram Delivery

The job delivers to `origin` which resolves to the job's configured `origin` field:
```json
"origin": {
  "platform": "telegram",
  "chat_id": "-1003784520976",
  "chat_name": "Agent Hermes",
  "thread_id": "20"
}
```
Topic 20 = briefing topic. The system auto-delivers — do NOT call `send_message` in the cron response.
