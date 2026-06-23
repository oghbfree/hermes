# DAILY PROCESSING REPORT — 2026-06-23 (Monday)

**Generated:** 2026-06-23 ~01:30 GMT+1
**Coverage:** 2026-06-22 00:00 → 2026-06-23 00:00
**Scope:** All Hermes artifacts modified in past 24 hours across both trees

---

## 1. INVENTORY SUMMARY

### Session Logs
**0 new session dumps** to archive in past 24 hours.  
**682 old session files** (>30 days) archived to `.hermes/sessions/.archive/`.  
**132 files** remain in `.hermes/sessions/` (≤30 days old).

### Cron Outputs
**3 cron output files** modified in past 24 hours:
- `cron/output/c9637a3c5a4f/2026-06-22_06-36-00.md` — Daily System Briefing (Jun 22, 06:36)
- `cron/output/e0194bbb8309/cron_status_report_2026-06-23.md` — Cron Status Report (Jun 23, 09:00)
- `cron/output/e0194bbb8309/cron_status_summary_2026-06-23.md` — Cron Status Summary (Jun 23, 09:00)

### Workspace Memories
**1 new master intelligence file:**
- `memories/insights/WEEKLY_LEARNING_2026-06-22.md` — Weekly synthesis for Jun 16–22

### Security Audits
**2 new audits:**
- `memories/security/SECURITY_AUDIT_2026-06-22.md` — Morning audit (06:09)
- `memories/security/SECURITY_AUDIT_2026-06-23.md` — Automated cron audit (01:24)

### Logs
- `logs/gateway-exit-diag.log` — Modified Jun 22 21:10 (touched, not new content)

---

## 2. MASTER FILES STATUS

| File | Status | Notes |
|------|--------|-------|
| `INTEGRATED_INSIGHTS_2026-06-23.md` | ✅ NEW | Generated from Jun 23 cron status report + security audit |
| `SECURITY_AUDIT_2026-06-23.md` | ⚠️ Stale | 7 FAIL / 8 WARN / 3 PASS — No remediation since creation |
| `WEEKLY_LEARNING_2026-06-22.md` | ✅ Current | Generated Jun 22; covers Jun 16–22 trends |
| `MEMORY.md` | ✅ Current | Canonical paths updated Jun 22 |
| `USER.md` | ✅ Current | User profile updated Jun 22 |

---

## 3. RECONCILE ACTIONS

### Security Audit File Sync
- Jun 23 audit saved to: `.hermes/memories/security/SECURITY_AUDIT_2026-06-23.md`
- No path inconsistency detected for this cycle.

### No Duplicate Memory Entries
- No duplicate or stale entries found in MEMORY.md or USER.md to prune.
- MEMORY.md already reflects canonical paths.

### Archive Actions
- 682 session files moved from `.hermes/sessions/` → `.hermes/sessions/.archive/`
- Files archived: all `session_*`, `request_dump_*`, and `.jsonl` files older than 30 days
- Remaining active sessions: 132 files

---

## 4. KEY FINDINGS FROM 24-HOUR PERIOD

### 🔴 CRITICAL: Security Debt Escalating
- **bws_cache.json**: 15+ plaintext API keys, world-readable (0644) — 2 consecutive audits
- **Sensitive files world-readable**: Persistent across 4+ audits (Jun 20–23)
- **WhatsApp bridge**: Unpaired 16+ days (fatal), enabled but non-functional
- **Direct .env reading scripts**: 10+ scripts in workspace leak tokens to process tables

### 🟡 WARN: DNS & Gateway Instability
- **Telegram DNS failures**: 5 jobs failed at 18:00–19:30 on Jun 22 with `getaddrinfo failed`
- **Gateway log stale**: Last entry Jun 18 17:22 (>5 days)
- **Gateway status mismatch**: `gateway_state.json` says running, `hermes gateway status` reports no process

### 🟡 WARN: Health Data Decay
- **H gap**: 12+ days without health log entries
- **Comfort gap**: 6+ days without care log entries

### 🟢 STABLE: Cron Reliability
- **Success rate**: 76.7% (23/30 runs) on Jun 22–23
- **Backup**: Daily backup ran Jun 22 23:25 successfully

---

## 5. CRON SLA SUMMARY

**Fleet:** 45 jobs | 45 enabled | 0 disabled
**24h Runs:** 30 | **Success:** 23 (76.7%) | **Failed:** 7

### Failed Runs
- Evening habit reflect — Connection error
- brain-dump-parser — Telegram DNS
- mum-health-evening — Telegram DNS
- health-check-evening — Telegram DNS
- nightly-consolidation — Request timed out
- dad-health-afternoon — Telegram DNS
- 2Real — Afternoon Follow-up — Telegram DNS

### Stale Jobs (>3 days)
- monthly-evolution — never ran
- Fluid CC Payment Reminder — never ran
- tax-monthly-checkin — never ran
- github-memory-backup — 8 days stale
- kanzoni-tuesday-check — 6 days stale
- janet-friday-checkin — 3 days stale

---

## 6. RECOMMENDATIONS

1. **🔴 IMMEDIATE**: Delete `bws_cache.json` — `rm ~/.hermes/cache/bws_cache.json`
2. **🔴 IMMEDIATE**: `chmod 600` on `.env`, `auth.json`, `google_token.json`, `config.yaml`
3. **🔴 IMMEDIATE**: Remove BOM from `AGENTS.md` — `sed -i '1s/^\xEF\xBB\xBF//' ~/.hermes/workspace/AGENTS.md`
4. **🟡 HIGH**: Fix Telegram DNS — configure static DNS (8.8.8.8, 1.1.1.1)
5. **🟡 HIGH**: Restart gateway and verify log rotation
6. **🟡 HIGH**: Re-pair WhatsApp or set `WHATSAPP_ENABLED=false`
7. **🟢 MEDIUM**: Implement circuit breakers for never-run / stale jobs
8. **🟢 MEDIUM**: Retry `nightly-consolidation`

---

*Report saved: `workspace/Daily/DAILY_PROCESSING_REPORT_2026-06-23.md`*
*Next processing run: 2026-06-24*
