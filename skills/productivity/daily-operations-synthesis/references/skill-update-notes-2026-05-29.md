# Skill Update Notes — 2026-05-29

## New Patterns Detected This Session

### Connection Error Cluster Pattern (May 29)

**What happened:** 5 cron jobs failed simultaneously with `RuntimeError: Connection error` between 00:49-09:01 UTC+1:
- daily-backup
- security-policy-check
- Morning Priority Check-in
- tasks-queue-sync
- cron-status-report

**Diagnostic signal:** When 3+ jobs fail with the SAME error string within a 2-hour window, this is a **systemic connectivity failure** (OpenRouter API, TLS, or gateway network stack), NOT independent per-job failures. Check:
1. `~/.hermes/logs/gateway.log` for TLS/connection errors in that window
2. OpenRouter status page
3. Whether Interactive Brokers or other network-dependent services are also affected (shared network path)

**Cron SLA impact:** Systemic failures collapse SLA by 30-60 percentage points in a single day. Normal SLA variance is ±10% day-to-day. A drop >20% = systemic flag.

**Action:** Report as "🔴 Systemic Connection Failure — N jobs affected" in the Issues section. Don't list each job separately — group under the systemic cause.

### Backup Failure + Connection Error Coupling (May 29)

**What happened:** Daily backup (23:03) failed with Connection error — the first backup failure since May 23.

**Compound risk:** Backup failure during a connection error window means:
- No verified backup for the day
- If the connection issue also affected the workspace (Git push, file sync), there may be uncommitted changes at risk
- 5+ days without verified backup is a data loss window

**Action in consolidation:** When backup fails with Connection error, add a COMPOUND RISK note: "Backup failed during connection window — verify workspace sync status."

### Cron SLA Rapid Collapse Detection

| SLA Change | Interpretation |
|---|---|
| ±10% day-to-day | Normal variance |
| -10% to -20% | One job degraded — investigate specific job |
| **>-20% drop** | **Systemic failure** — cluster investigation needed |
| <50% for 2+ days | Persistent systemic issue |

**Threshold:** Flag as 🔴 Critical when SLA drops >20% from previous day AND 3+ jobs share the same error string.

### Request Dump Growth Rate (Tracking)

| Date | Count | Growth |
|---|---|---|
| May 28 audit | 156 | — |
| May 29 consolidation | 164 | +8 in ~22h |

**Projection:** At 8 files/day, ~240/month. These are security audit FAIL item #1 across 4+ consecutive audits. **Urgent:** Add `find ~/.hermes/sessions/ -name "request_dump_*.json" -delete` to nightly cleanup.

### dad-health-morning Failure Mode Update

Confirmed: `dad-health-morning` exhibits BOTH failure modes simultaneously:
1. `elder-care-dad` skill not found (config mismatch — should be `elder-care-operations`)
2. `send_message` tool unavailable in cron context

Both root causes must be fixed for this job to work. The skill name fix alone won't resolve it if send_message is also unavailable.

### mum-health-evening Pattern Confirmed

`mum-health-morning` on May 29 ran at 00:54 (not 08:04) — fired at wrong time. This suggests a timezone or schedule drift issue. The cron is `4 8 * * *` (08:04 UTC+1) but output shows 00:54 — off by ~7 hours. Monitor for schedule drift in future runs.
