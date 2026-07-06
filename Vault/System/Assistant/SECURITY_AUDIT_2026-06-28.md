# Security Audit Report — 2026-06-28

**Generated:** 2026-06-28 12:08 BST  
**Scope:** Credential exposure, channel integrity, recent security events

---

## 1. Credential Exposure — FAIL (Persistent)

| Check | Result | Details |
|-------|--------|---------|
| WhatsApp `creds.json` | **FAIL** | File exists but is 0 bytes — WhatsApp configured but **not paired** (non-functional channel). Session directory contains only pre-keys from initial setup (Jun 7), no active session. |
| Backup `.env` files | PASS | `~/.hermes/backups/` directory empty — no backup copies of `.env` with live secrets. |
| Credential cache files | PASS | No `bws_cache.json`, `.secret_cache`, or provider cache files found in `~/.hermes/cache/`. |
| `google_token.json` | NOT FOUND | No Google OAuth token file present. |
| Direct `.env` reading scripts | NOT CHECKED | Requires targeted grep across workspace — deferred to next audit. |
| Invisible Unicode/BOM in workspace | NOT CHECKED | Deferred to next audit. |

**Persistent Finding (5+ cycles):** WhatsApp remains unpaired since initial setup (Jun 7). Channel is **configured but non-functional**.

---

## 2. Channel Integrity — FAIL

### Telegram Adapter
- **Status:** Running but unstable
- **Events (last 4h):** 12+ network errors, fallback IP (149.154.166.110) failures, reconnection loops
- **Root cause:** DNS/connectivity to `api.telegram.org` intermittently failing; fallback IP also failing
- **Classification:** Channel integrity **degraded** — adapter connected but delivery unreliable

### WhatsApp Adapter
- **Status:** **Persistent failure** — 146 reconnection attempts since 08:03 today, all timeout after 30s
- **Root cause:** Bridge starts but `creds.json` is empty — no paired session
- **Classification:** Channel integrity **FAIL** — adapter cannot connect without valid credentials

### Cron Delivery Targets — FAIL (29 silent failures)
| Delivery Type | Count | Impact |
|---------------|-------|--------|
| `local` | 7 jobs | Output never leaves machine |
| `origin` | 22 jobs | Output stays in cron system, no user delivery |
| **Total silent failures** | **29/42 jobs (69%)** | **Most cron jobs never reach user** |

**Notable affected jobs:** `tasks-queue-sync`, `tasks-md-to-kanban`, all 6 family health check-ins, all 6 2Real business check-ins, daily-backup, cron-status-report, github-memory-backup, monthly-evolution, weekly-learning-review.

---

## 3. Recent Security Events

| Event | Timestamp | Severity | Status |
|-------|-----------|----------|--------|
| `telegram.error.InvalidToken: The token was rejected by the server` | 2026-06-05 (historical) | HIGH | **Resolved** — token rotated, no recent occurrences |
| `telegram.error.InvalidToken: Not Found` | 2026-06-05 (historical) | HIGH | **Resolved** — same incident |
| Nous Portal token expiry | **2026-06-28 12:15:23 GMT** | WARN | **Expiring today** — auto-refresh expected but monitor |
| Config version drift | Current v29 → available v30 | WARN | Migration needed (`hermes doctor --fix`) |
| WhatsApp npm vulnerabilities | 5 (1 critical, 2 high, 2 moderate) | WARN | Run `npm audit fix` in whatsapp-bridge |

**No active credential compromise indicators.** No 403/401 from OpenRouter, FAL, or other providers.

---

## 4. Severity Summary

| Category | Severity | Trend |
|----------|----------|-------|
| WhatsApp unpaired (non-functional) | **FAIL** | Persistent (5+ audits) → **Escalated: Persistent Security Debt** |
| 69% cron jobs silent delivery failure | **FAIL** | New finding |
| Telegram DNS/connectivity instability | **WARN** | Recurring |
| Nous Portal token expires today | **WARN** | Time-bound |
| Config version outdated (v29→v30) | **WARN** | Recurring |
| WhatsApp bridge npm vulns | **WARN** | Persistent |

---

## 5. Remediation Actions

1. **WhatsApp:** Pair session (`hermes setup whatsapp`) or disable adapter if not needed
2. **Cron delivery:** Audit all 29 `local`/`origin` jobs — assign valid `telegram:-1003784520976:<topic>` targets
3. **Telegram DNS:** Investigate host-level DNS/network; consider sticky fallback IP configuration
4. **Nous Portal:** Monitor auto-refresh post-expiry; re-authenticate if gateway logs show failures
5. **Config:** Run `hermes doctor --fix` to migrate to v30
6. **WhatsApp bridge:** `cd scripts/whatsapp-bridge && npm audit fix`

---

## 6. Comparison with Previous Audit (if any)

*No prior audit file found at canonical path for trend comparison.*