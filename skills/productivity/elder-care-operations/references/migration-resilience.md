# Migration Resilience — Lessons Learned

## Cron Jobs Lost During Migration (May 2026)

**What happened:** When the platform migrated from `.openclaw` to `.hermes`, all cron jobs were lost. On May 18, H noticed jobs from May 16 had disappeared. Only 13 jobs existed (all created May 17-18), vs 30+ in the OpenClaw export.

**Root cause:** `hermes claw migrate` did not fully transfer cron jobs. Old jobs remained in `~/.openclaw/cron/jobs.json` but were not active.

## Recovery Process

1. **Locate old jobs:** `~/.openclaw/cron/jobs.json` (OpenClaw format) vs `~/.hermes/cron/jobs.json` (Hermes format)
2. **Compare:** Parse both files, diff job names/schedules to find missing
3. **Recreate:** Use `cronjob(action='create')` for each missing job
4. **WhatsApp jobs:** Create them anyway — they'll fail until WhatsApp is relinked, but will work when it comes back

## Full Recovered Inventory (34 jobs total)

### System/Operations (11)
daily-system-briefing (06:36), integrated-daily-synthesis (22:05), weekly-learning-review (Mon), monthly-evolution (1st), ghana-dashboard-inquiry (Mon-Sat), security-policy-check (6h), friday-content-2real (Fri), daily-backup (23:03), cron-status-report (09:00), github-memory-backup (Sun), nightly-consolidation (03:00)

### Health Checks (6)
H morning/afternoon/evening (topic 2), Mum morning/afternoon/evening (topic 4)

### Content (2)
sunday-content-engine, saturday-content-performance (topic 26)

### Kanban (3)
brain-dump-parser, tasks-queue-sync, tasks-md-to-kanban

### WhatsApp-Dependent (8) — fail until WhatsApp relinked
checkin-mum (Sun+Wed), checkin-dad (Sun+Thu), kanzoni-tuesday-check, sammy-morning-check, john-field-check, ebony-goodnight, janet-friday-checkin, jnr-payment-reminder

### Weekly (4)
health-weekly-synthesis, mum-health-weekly-review, health-analysis-weekly, job-applications-check

## Key Paths Changed

| Old | New |
|-----|-----|
| `~/.openclaw/workspace/memory/HEALTH_LOG_MUM_*.md` | `C:\Users\User\CARE_LOG_COMFORT_*.md` |
| `~/.openclaw/cron/jobs.json` | `~/.hermes/cron/jobs.json` |

## Topic ID Changes

| Old | New | Purpose |
|-----|-----|---------|
| Topic 50 | Topic 2 | H's health |
| Topic 51 | Topic 4 | Comfort's health |
| -1003620024352 | -1003784520976 | Main group |

## Prevention Checklist

After any migration or config reset:
1. `cronjob list` — verify all expected jobs exist
2. Check `last_run_at` for nulls on jobs that should have run
3. Verify delivery targets match current topic IDs
4. **Keep old `jobs.json`** until all jobs verified recreated
