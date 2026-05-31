# Health Log Paths — Quick Reference

## H (Oman Herbert Blankson)

| Path | Role | Notes |
|------|------|-------|
| `C:\Users\User\.hermes\workspace\memories\health\H\HEALTH_LOG_YYYY-MM.md` | **Primary** — most up-to-date | Written by health-check cron jobs. Check this first. |
| `C:\Users\User\HEALTH_LOG_YYYY-MM.md` | Root copy — may lag | Older canonical path. May not have latest entries. |

**Always check both and use the most recent.** In practice, the `memories/health/H/` path is written to by the cron jobs and is the most current.

## Comfort Blankson (Mum)

| Path | Role | Notes |
|------|------|-------|
| `C:\Users\User\CARE_LOG_COMFORT_YYYY-MM.md` | **Primary** — monthly care log | Detailed carer logs. Check this first for Comfort data. |
| `C:\Users\User\.hermes\workspace\memories\health\mum\health-log.md` | Workspace copy | May be empty or outdated if carers aren't reporting via cron |
| `C:\Users\User\.hermes\workspace\memories\health\mum\YYYY-MM-DD.md` | Daily entries | Check for dated files |

## Dad (Robert Herbert-Blankson)

| Path | Role | Notes |
|------|------|-------|
| `C:\Users\User\CARE_LOG_DAD_YYYY-MM.md` | **Daily care log** — check-in templates | Carer-facing prompts delivered by cron. Has morning/afternoon/evening sections. Fields often blank if carers don't respond. |
| `C:\Users\User\.hermes\workspace\FAMILY_INSIGHTS_DAD.md` | Medical context | Conditions, medications, contacts, escalation paths. NOT the daily log. |

## Cron Jobs That Write to These Paths

| Job | Writes to | Frequency |
|-----|-----------|-----------|
| health-check-morning/afternoon/evening | `memories/health/H/HEALTH_LOG_YYYY-MM.md` | 3x daily |
| mum-health-morning/afternoon/evening | Telegram topic 4 (prompts); carer responses → `memories/health/mum/` | 3x daily |
| dad-health-morning/afternoon/evening | Telegram topic 1 (prompts); carer responses → `CARE_LOG_DAD_` | 3x daily |
