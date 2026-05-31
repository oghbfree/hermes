# Nightly Consolidation — Environment Reference

## Telegram Group & Topic IDs

| Topic | ID | Purpose |
|-------|-----|---------|
| general | 1 | General operations, supplier outreach |
| health-log | 2 | H health checks (morning/afternoon/evening) |
| health-log-mum | 4 | Comfort health checks (morning/afternoon/evening) |
| briefing | 10 | Daily briefing + nightly synthesis |
| memory-review | 20 | Security audits, backups, cron status, nightly consolidation |
| content-calendar | 26 | Akoma/2Real content plans |
| jobs | 28 | Job applications |
| to-do-list | 8 | H's brain-dump task management (TASKS.md) |

**Group ID:** `-1003784520976`

## Key Cron Job IDs

| Job | ID | Schedule | Output Dir |
|-----|-----|----------|------------|
| nightly-consolidation | `661bee8a8f5c` | 0 3 * * * | `~/.hermes/cron/output/661bee8a8f5c/` |
| daily-system-briefing | `7ccae58aa436` | 36 6 * * * | `~/.hermes/cron/output/7ccae58aa436/` |
| cron-status-report | `3d3e868ba056` | 0 9 * * * | `~/.hermes/cron/output/3d3e868ba056/` |
| security-watchdog | `5cd8bc6aa0c2` | 4 */6 * * * | `~/.hermes/cron/output/5cd8bc6aa0c2/` |
| integrated-daily-synthesis | `1ce4c6b6f727` | 5 22 * * * | `~/.hermes/cron/output/1ce4c6b6f727/` |
| daily-backup | `c2d685f3b8e5` | 3 23 * * * | `~/.hermes/cron/output/c2d685f3b8e5/` |
| health-check-morning | `13e9ece3ec0a` | 1 8 * * * | `~/.hermes/cron/output/13e9ece3ec0a/` |
| mum-health-morning | `7f0d3305056f` | 4 8 * * * | `~/.hermes/cron/output/7f0d3305056f/` |
| health-check-afternoon | `7b7fc8c10d96` | 1 13 * * * | `~/.hermes/cron/output/7b7fc8c10d96/` |
| mum-health-afternoon | `4399b4d83d57` | 0 13 * * * | `~/.hermes/cron/output/4399b4d83d57/` |
| health-check-evening | `47e39f12d7fc` | 2 19 * * * | `~/.hermes/cron/output/47e39f12d7fc/` |
| mum-health-evening | `b84b006dcfbe` | 0 19 * * * | `~/.hermes/cron/output/b84b006dcfbe/` |
| ghana-supplier-outreach | `00d4f0e3d9aa` | 16 9 * * 1-6 | `~/.hermes/cron/output/00d4f0e3d9aa/` |
| job-applications-check | `dd6ee15aac71` | 0 8 * * * | `~/.hermes/cron/output/dd6ee15aac71/` |

## Intelligence File Paths

| File | Path |
|------|------|
| Daily synthesis | `~/.openclaw/workspace/memory/YYYY-MM-DD-synthesis.md` |
| Integrated insights | `~/.openclaw/workspace/memory/insights/INTEGRATED_INSIGHTS_YYYY-MM-DD.md` |
| Health log (H) | `~/.openclaw/workspace/memory/HEALTH_LOG_2026-MM.md` |
| Health log (Mum) | `~/.openclaw/workspace/memory/HEALTH_LOG_MUM_2026-MM.md` |
| Business check-ins | `~/.openclaw/workspace/memory/business/BUSINESS_CHECKINS_2026-MM.md` |
| Supplier analysis | `~/.openclaw/workspace/memory/procurement/GHANA_SUPPLIER_ANALYSIS_YYYY-MM-DD.md` |
| Security audit findings | `~/.hermes/skills/devops/system-security-audit/references/YYYY-MM-DD-HHMM-audit-findings.md` |
| Backup | `~/hermes-backup/YYYY-MM-DD/` |

## Known Persistent Issues (as of May 14, 2026)

| Issue | First Detected | Status |
|-------|----------------|--------|
| WhatsApp Web listener inactive | May 8 (Day 15+) | 🔴 Unresolved — user approved re-link May 12 |
| Health intake compliance = 0% | May 7-8 (7+ days) | 🔴 Unresolved — clinical risk HIGH for Mum (91, hip ache) |
| Google Sheets auth broken | May 11 (migration) | 🟡 Unresolved — 4 recruitment pipelines blind |
| Desktop `.env` with API keys | May 11 (5+ audits) | 🔴 Unresolved — BRAVE key + HOOKS token fully exposed |
| Google OAuth refresh_token exposed | May 14 (new audit format) | 🔴 Unresolved — persistent Sheets access |
| Conflicting Telegram bot tokens | May 14 (new audit format) | 🟡 Unresolved — two tokens across 3 environments |
| .env backup files with secrets | May 14 (new audit format) | 🟡 Unresolved |
| Empty cron prompts (supplier/steering jobs) | May 13 | 🟡 Configuration error — produces false successes |
| groq_key.txt in git history | May 11 (5+ audits) | 🔴 Unresolved |
| 185 .txt files in git | May 11 (5+ audits) | 🟡 Unresolved |

## Cron Jobs Added/Updated After May 11 Migration

| Job | ID | Schedule | Notes |
|-----|-----|----------|-------|
| workflow-48h-maintenance | `c35016e9d778` | every 2880m | Flags critical issues; runs ~every 48h |
| ghana-steering-verification | `4cadf4e4945e` | 11 11 * * 3 | Empty prompt — needs fix |

## Key File Paths (Verified May 14)

| File | Path | Last Verified |
|------|------|---------------|
| Integrated insights | `~/.openclaw/workspace/memory/insights/INTEGRATED_INSIGHTS_YYYY-MM-DD.md` | 2026-05-14 |
| Health log (H) | `~/.openclaw/workspace/memory/HEALTH_LOG_2026-05.md` | 2026-05-14 (last entry: May 8) |
| Health log (Mum) | `~/.openclaw/workspace/memory/HEALTH_LOG_MUM_2026-05.md` | 2026-05-14 (last entry: May 7) |
| Business check-ins | `~/.openclaw/workspace/memory/business/BUSINESS_CHECKINS_2026-05.md` | 2026-05-13 (last entry: May 11) |
| Daily notes | `~/.openclaw/workspace/memory/2026-05-13.md` | 2026-05-13 |

## Security Audit Methodology Note

The `security-watchdog` cron (ID: `5cd8bc6aa0c2`) changed audit methodology between the May 13 18:04 run and the May 14 00:12 run. The original format used a broad 9-category checklist (git history, tirith, sessions, permissions, etc.). The new format focuses on credential-exposure depth with 5 categories. **When comparing security scores across audit runs, compare the actual FAIL items, not the counts.** A shift from "9 FAIL" to "5 FAIL" with identical core findings is a methodology change, not remediation.

## User-Established Workflows (May 13 session)

- **Topic 8 (to-do-list)**: H sends raw brain-dumps → OWL parses into structured tasks → H says "save" → OWL writes to `TASKS.md`
  - Status: 40+ tasks parsed from first brain dump; **TASKS.md not yet saved** (awaiting H confirmation)
  - Path: `C:\Users\User\.hermes\workspace\TASKS.md`

## Upcoming First Executions

- **thursday-content-akoma** (Thu May 14, 09:09, Topic 26): First-ever execution. Verify prompt is populated.
