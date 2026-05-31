# Skill Update Notes — 2026-05-28

## Session: nightly-consolidation (03:00 BST)

### Security Audit Persistence Gap (Recurring)
The May 28 00:04 security audit ran successfully but initially appeared missing from `workspace/memories/security/`. It was later confirmed present. The gap detection logic in nightly-consolidation is working but prone to false positives — the file may exist but not be found if search timing is off. **Recommendation:** Always verify with `ls` before concluding a gap exists.

### Request Dump Count Growth
- May 28 audit: 156 files
- May 29 consolidation: 164 files (+8 in ~22h)
- Growth rate: ~8 files/day → ~240/month
- Cleanup command that should be added to nightly-consolidation: `find ~/.hermes/sessions/ -name "request_dump_*.json" -delete`

### mum-health-morning Schedule Drift
The `mum-health-morning` cron (`4 8 * * *` = 08:04 UTC+1) produced output at 00:54 UTC+1 on May 29 — a 7-hour offset. This may indicate:
1. Cron schedule misconfigured (UTC vs local time confusion)
2. System timezone change
3. Job was manually triggered or backfilled

Monitor next 3 runs. If drift persists, check the cron job's timezone configuration. The `schedule_display` field in jobs.json shows `4 8 * * *` which is correct — the execution time is the anomaly.

### dad-health-morning Dual Failure Mode Confirmed
Both failure modes present in same run:
1. `elder-care-dad` skill not found (should be `elder-care-operations`)
2. `send_message` unavailable

Fixing only the skill name will NOT fully resolve this job — the send_message tool is also unavailable in cron context. The job needs to rely on auto-delivery (final response) rather than send_message, AND the skill reference needs updating.

### Connection Error Cluster (New Pattern)
See `skill-update-notes-2026-05-29.md` in the daily-operations-synthesis skill for full analysis.
