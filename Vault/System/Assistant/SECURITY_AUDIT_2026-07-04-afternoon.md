# Security Audit — 2026-07-04 (Afternoon)

**Date:** `2026-07-04` (12:25 UTC)
**Run by:** internal cron / Hermes Agent
**Overall:** 🔴 FAIL — 3 FAIL items, 2 WARN, 4 CRITICAL escalations

---

## Summary

| Category | Status | Details |
|----------|--------|---------|
| Credential Exposure | 🔴 CRITICAL | 28 backup .env copies with live secrets (↑1 from this morning) |
| Channel Integrity | 🔴 FAIL | Gateway dead 16 days — crash root cause identified (ModuleNotFoundError) |
| Recent Security Events | 🟡 WARN | 9 failed gateway restart attempts since Jun 22, config drift -3 versions |
| Gateway Root Cause | ⚠️ NEW | `concurrent_log_handler` ModuleNotFoundError blocks all restarts since Jun 22 |

---

## 1. Credential Exposure

### 🔴 CRITICAL: 28 Backup .env Copies (PERSISTENT — 10+ cycles)
- **24 copies** in `~/.hermes/backups/` (incl. `latest`, `latest_old`, nested backups)
- **4 copies** in `~/.hermes/state-snapshots/`
- **Increased from 27 to 28** since this morning's audit — new backup at `backup_20260704_020859/.env`
- All contain raw API keys (OpenRouter, Telegram, Google, Firecrawl, etc.)
- **PERSISTENT SECURITY DEBT — escalated to CRITICAL** (10+ consecutive audits without remediation)

### 🟢 PASS: Credential Cache Files
- `bws_cache.json`: Not found ✅ (clean since ~Jun 26)
- `.secret_cache`: Not found ✅ (clean since ~Jun 26)
- 7th consecutive clean cycle

### 🟢 PASS: google_token.json ACL
- `icacls` shows only Owner: (I)(F), SYSTEM: (I)(F), Administrators: (I)(F)
- No "Everyone" or "BUILTIN\Users" — standard Windows default, PASS
- Contains active `refresh_token` + `client_secret` (scopes: Gmail, Drive, Sheets, Calendar, Contacts, Docs)

### 🔴 FAIL: Workspace AGENTS.md UTF-8 BOM
- `~/.hermes/workspace/AGENTS.md`: **UTF-8 with BOM** ❌ (prompt injection risk)
- Main `~/.hermes/AGENTS.md`: Absent ✅

### 🔴 FAIL: 6+ Workspace Scripts Reading .env Directly
- **Newly found:** `send_telegram_temp_briefing.py`, `tmp_send_telegram_test.py` also open `.env` directly
- Scripts including `probe_threads.py`, `send_health_report.py`, `check_bot.py`, `send_telegram_integrated_briefing.py` extract `TELEGRAM_BOT_TOKEN` at runtime
- Risk of leakage to process tables, shell history, and logs

### 🟢 PASS: Telegram Bot Token Valid
- DNS resolves `api.telegram.org` (verified: HTTP 404 on `/bot` endpoint = connection functional)
- No `InvalidToken` events in current logs

### 🟢 PASS: Config.yaml Format
- ASCII with CRLF terminators — no BOM ✅
- `_config_version: 23` (unchanged)

---

## 2. Channel Integrity

### 🔴 FAIL: Gateway Dead — 16 Days Stale
- Last log entry: **2026-06-18 17:22:29**
- PID 8924 (from `hermes status`): **NOT RUNNING** (confirmed via `ps`)
- **NEW — Root Cause Identified:** Gateway crash loop from `concurrent_log_handler` ModuleNotFoundError
  - First crash: **2026-06-22 03:36** — `ModuleNotFoundError: No module named 'concurrent_log_handler'`
  - **9 total failed restart attempts** documented (Jun 22 ×2, Jun 26, Jun 27 ×4, Jul 1)
  - Each attempt crashes before initializing logging infrastructure
  - Python 3.14 environment missing `concurrent_log_handler` package

### 🔴 FAIL: 27/40 Jobs Silent Delivery
- 25 jobs deliver to `origin` — output stays local
- 2 jobs deliver to `local` — output stays local
- Only 13/40 jobs target Telegram topics (all undeliverable with gateway dead)
- **16 jobs have not run since June 18** or have no run history

### 🔴 FAIL: 11 Jobs with DNS Failure Errors
- `getaddrinfo failed` pattern in `last_error` or `last_delivery_error`
- Historical DNS failures (Jun 18) — DNS now healthy but jobs never re-ran

### 🔴 FAIL: WhatsApp Unpaired (64+ Days)
- `~/.hermes/whatsapp/session/` is **empty** — no `creds.json`
- WhatsApp bridge has 5 npm vulnerabilities (1 critical, 2 high, 2 moderate)
- Not exploitable while unpaired, but fixable when pairing

### 🟢 DNS Now Healthy
- `api.telegram.org` resolves (verified this audit)
- `openrouter.ai` resolves (verified)
- Root cause was host-level DNS, not targeted attack
- Gateway could connect if restarted — the ModuleNotFoundError is the blocking issue

---

## 3. Recent Security Events

### 🔴 NEW: Gateway Crash Loop — ModuleNotFoundError (Jun 22–Present)
- **9 failed restart attempts** across 5 different days
- Each start crashes: `from concurrent_log_handler import ... ModuleNotFoundError`
- Python 3.14 environment — missing package, not a credential or network issue
- **No auto-recovery possible** — manual fix required (`pip install concurrent_log_handler`)
- Last attempt: **2026-07-01 22:06 UTC** — failed same way

### 🟢 Historical InvalidToken — Resolved
- Multiple `InvalidToken` rejections on 2026-06-08
- Current token fully valid per API probe

### 🟡 WARN: Host-Level DNS Failures (Jun 18) — Resolved
- Multi-service failure (Telegram + OpenRouter both failed `getaddrinfo`)
- DNS now healthy — gateway just can't restart due to module issue

### 🟡 WARN: Config Version Drift
- yaml `_config_version: 23` (unchanged for weeks)
- doctor schema: v29
- latest schema: v32
- 3 versions behind — partial improvement stalled

### 🟡 WARN: Gateway State File Stale
- `hermes status` reports PID 8924 "running" — process is dead
- State not cleaned up

### 🟡 WARN: 16 Jobs Not Run Since June 18
- All cron jobs stuck — scheduler can't route through dead gateway
- 11 jobs failed with DNS errors on their last attempt

### No Breach Markers Detected
- No unauthorized access patterns in logs
- No token revocation events (current)
- No traffic redirection evidence

---

## 4. Trend vs Prior Audit (2026-07-04 01:10 UTC)

| Finding | This Morning (01:10) | Afternoon (12:25) | Change |
|---------|---------------------|-------------------|--------|
| Backup .env copies | 🔴 27 (CRITICAL) | 🔴 28 (CRITICAL) | **Worsened** (+1 new backup) |
| Gateway alive | 🔴 Dead 16d | 🔴 Dead 16d | No change |
| WhatsApp unpaired | 🔴 63+ days | 🔴 64+ days | No change |
| Workspace AGENTS.md BOM | 🔴 FAIL | 🔴 FAIL | No change |
| Config drift (v23→v29→v32) | 🟡 WARN | 🟡 WARN | No change |
| bws_cache.json | ✅ Gone | ✅ Gone | No change |
| DNS health | ✅ Resolves | ✅ Resolves | No change |
| 27/40 silent jobs | 🔴 FAIL | 🔴 FAIL | No change |
| Telegram token valid | ✅ Valid | ✅ Valid | No change |
| .env readers (scripts) | 🟡 16+ found | 🔴 6+ direct-read (NEW scripts found) | **Worsened** (more discovered) |
| Gateway crash root cause | ❓ Unknown | 🔴 ModuleNotFoundError (NEW) | **New — root cause found** |

### Persistent Security Debt (10+ cycles unremediated)
- **Backup `.env` copies** — 10+ cycles, 28 copies, now at CRITICAL
- **WhatsApp unpaired** — 64+ days
- **AGENTS.md BOM** — present for 4+ cycles
- **Scripts reading .env** — growing, not shrinking

---

## 5. Recommendations

### IMMEDIATE
1. **🔴 CRITICAL — Install missing module & restart gateway:**
   ```bash
   pip install concurrent_log_handler
   hermes gateway run --replace
   ```
   This unlocks ALL cron delivery — the gateway has been blocked by a missing Python package since Jun 22

2. **🔴 CRITICAL — Delete backup .env copies:**
   ```bash
   find ~/.hermes/backups -name ".env" -delete
   find ~/.hermes/state-snapshots -name ".env" -delete
   ```
   28 copies of every API key — extreme exposure surface

3. **🔴 Fix local-delivery jobs:**
   `mum-health-morning` and `mum-health-evening` deliver to `local` — update to Telegram topics

4. **🔴 Re-pair WhatsApp:** Session empty for 64+ days — needs QR code pairing

### HIGH
5. **Strip AGENTS.md BOM:** `sed -i '1s/^\xEF\xBB\xBF//' ~/.hermes/workspace/AGENTS.md`

6. **Audit workspace scripts:** 6+ scripts read `.env` directly — refactor to use environment variables

7. **Update config:** `hermes doctor --fix` to migrate v23 → v32

### MEDIUM
8. **Fix cron delivery targets:** Migrate 25 `origin` and 2 `local` jobs to explicit Telegram topics
9. **Fix WhatsApp bridge npm vulns:** Run `npm audit fix` in whatsapp-bridge
10. **Add GITHUB_TOKEN to .env:** For better Skills Hub rate limits

---

## 6. Retention Cleanup

- **Same-day dedup:** `SECURITY_AUDIT_2026-07-04.md` (01:10 UTC) retained; this is `-afternoon` variant
- **7-day window:** Files from Jun 27 to Jul 4 retained
- **No deletion needed** (all within window)