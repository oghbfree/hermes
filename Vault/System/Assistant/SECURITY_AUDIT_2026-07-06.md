# Security Audit — 2026-07-06

**Date:** `2026-07-06`
**Run by:** internal cron / Hermes Agent
**Overall:** 🔴 FAIL — 3 FAIL items, 2 WARN, 2 CRITICAL escalations

---

## Summary

| Category | Status | Details |
|----------|--------|---------|
| Credential Exposure | 🔴 CRITICAL | 29 backup .env copies with live secrets (UP from 28) |
| Channel Integrity | 🔴 FAIL | Gateway dead 17.6 days — `concurrent_log_handler` crash, PID 8924 zombie |
| Recent Security Events | 🟡 WARN | 7 failed gateway restarts since Jun 22, no new attempts since Jul 1, config drift v29→v32 |

---

## 1. Credential Exposure

### 🔴 CRITICAL: 29 Backup .env Copies (PERSISTENT — 11+ cycles)
- **25 copies** in `~/.hermes/backups/` (incl. `latest`, `latest_old`, nested backups)
- **4 copies** in `~/.hermes/state-snapshots/`
- **Worsening: increased from 28 to 29** — new backup copy at `backup_20260706_070708`
- All contain raw API keys (OpenRouter, Telegram, Google, Firecrawl, Brave, xAI, etc.)
- **PERSISTENT SECURITY DEBT — escalated to CRITICAL (11 cycles)**

### 🟢 PASS: Credential Cache Files
- `bws_cache.json`: Not found ✅ (clean — 8th consecutive cycle)
- `.secret_cache`: Not found ✅ (clean)

### 🟢 PASS: google_token.json ACL
- `icacls` shows only Owner: (I)(F), SYSTEM: (I)(F), Administrators: (I)(F)
- No "Everyone" or "BUILTIN\Users" — standard Windows default, PASS

### 🔴 FAIL: Workspace AGENTS.md UTF-8 BOM
- `~/.hermes/workspace/AGENTS.md`: **UTF-8 with BOM** ❌ (prompt injection risk, blocks cron content scanning)
- Main `~/.hermes/AGENTS.md`: Absent ✅ (no file at this location)

### 🟢 PASS: Telegram Bot Token Valid
- DNS resolves `api.telegram.org` ✅
- No `InvalidToken` events in current logs ✅

### 🟢 PASS: No Workspace Scripts Directly Reading .env
- No offending scripts detected

---

## 2. Channel Integrity

### 🔴 FAIL: Gateway Dead — 17.6 Days Stale
- **Last log entry: 2026-06-18 17:22:29** (17.6 days ago — worsened from 17)
- **PID 8924 still exists** (python.exe, ~248MB) but is a **zombie process** — no log activity since June 18
- **Root cause: `concurrent_log_handler` ModuleNotFoundError** (Python 3.14 venv missing package)
- **7 total failed restart attempts** (Jun 22 ×2, Jun 26 ×1, Jun 27 ×4)
- **Last attempt: 2026-07-01 22:06 UTC** — **5 days without recovery attempt**
- Gateway auto-recovery is **not possible** — manual fix required

### 🔴 FAIL: 27/40 Jobs Silent Delivery
- 25 jobs deliver to `origin` — output stays local
- 2 jobs deliver to `local` — output stays local
- Only 13/40 jobs target Telegram topics (all currently undeliverable)
- Affected: mum-health, dad-health, health-check, content-engine, job-applications

### 🔴 FAIL: WhatsApp Unpaired (66+ Days)
- `~/.hermes/whatsapp/session/` **empty** — no `creds.json`
- npm dependencies: 1 critical, 2 high vulnerabilities (Baileys, protobufjs, ws)
- Not exploitable while unpaired but 66+ days without recovery attempt

### 🟢 DNS Healthy
- `api.telegram.org` resolves ✅ (149.154.166.110)
- `openrouter.ai` resolves ✅

---

## 3. Recent Security Events

### 🔴 FAIL: Gateway Crash Loop — ModuleNotFoundError (Jun 22–Present)
- **7 failed restart attempts** with identical crash signature
- Each crash: `ModuleNotFoundError: No module named 'concurrent_log_handler'`
- Python 3.14 environment — missing `concurrent_log_handler` package
- **Fix:** `pip install concurrent-log-handler && hermes gateway run --replace`
- **5 days since last attempt** (Jul 1) — no auto-recovery possible

### 🟢 Historical InvalidToken (Jun 8-9) — Resolved
- Token was rejected but replaced. Current token valid.
- No `InvalidToken` events in current or rotated logs

### 🟡 WARN: Config Version Drift
- Doctor reports v29 → v32 (3 versions behind)
- No change from prior audit

### 🟡 WARN: hermes status Reports 47 Jobs, jobs.json Has 40
- 7 job discrepancy — some jobs in-memory only
- Not security-critical but signals state drift

### 🟡 WARN: 16+ Jobs Not Run Since June 18
- All cron jobs blocked — scheduler can't route through dead gateway
- DNS failures on last execution for 11 jobs

### ✅ No Breach Markers Detected
- No unauthorized access patterns
- No token revocation events (current)
- No traffic redirection evidence

---

## 4. Trend vs Prior Audit (2026-07-05)

| Finding | Jul 5 | Jul 6 | Change |
|---------|-------|-------|--------|
| Backup .env copies | 🔴 28 (CRITICAL) | 🔴 **29** (CRITICAL) | 🔴 **Worsening (+1)** |
| Gateway dead days | 17 days | **17.6 days** | 🔴 Worsening |
| Gateway crash attempts | 7 (no new) | 7 (no new) | 🔴 No attempts (5 days idle) |
| WhatsApp unpaired | 65+ days | **66+ days** | 🔴 Worsening |
| AGENTS.md BOM | 🔴 FAIL | 🔴 FAIL | No change |
| Config drift v29→v32 | 🟡 WARN | 🟡 WARN | No change |
| bws_cache.json | ✅ Gone | ✅ Gone | No change |
| DNS health | ✅ Resolves | ✅ Resolves | No change |
| 27/40 silent jobs | 🔴 FAIL | 🔴 FAIL | No change |
| Telegram token | ✅ Valid | ✅ Valid | No change |
| Gateway crash root | 🔴 ModuleNotFoundError | 🔴 ModuleNotFoundError | No change |
| PID 8924 | Zombie | Zombie (248MB) | No change |

### Persistent Security Debt (11+ cycles unremediated)
- **Backup `.env` copies** — 29 copies, 11+ cycles, CRITICAL — **increasing**
- **WhatsApp unpaired** — 66+ days
- **AGENTS.md BOM** — 6+ cycles
- **Gateway crash loop** — 18 days without resolution
- **Config drift** — unchanged for weeks

---

## 5. Recommendations

### IMMEDIATE
1. **🔴 CRITICAL — Install missing module & restart gateway:**
   ```bash
   pip install concurrent-log-handler
   hermes gateway run --replace
   ```
   This fixes ALL cron delivery — the only blocker since Jun 22

2. **🔴 CRITICAL — Delete backup .env copies (now 29!):**
   ```bash
   find ~/.hermes/backups -name ".env" -delete
   find ~/.hermes/state-snapshots -name ".env" -delete
   ```
   **Count increased by 1 since last audit** — new copy every ~2 days

3. **🔴 Fix local-delivery jobs:** `mum-health-morning`, `mum-health-evening`, and 25 `origin` jobs never reach a user

4. **🔴 Re-pair WhatsApp:** Session empty for 66+ days — needs QR code pairing

### HIGH
5. **Strip AGENTS.md BOM:** `sed -i '1s/^\xEF\xBB\xBF//' ~/.hermes/workspace/AGENTS.md`
6. **Update config:** `hermes doctor --fix` to migrate v29 → v32

### MEDIUM
7. **Fix cron delivery targets:** Migrate `origin` jobs to explicit Telegram topics
8. **Add GITHUB_TOKEN to .env:** For better Skills Hub rate limits

---

## 6. Retention Cleanup

- **7-day window:** Keep files Jun 29 – Jul 6 only
- **Files to retain:**
  - `SECURITY_AUDIT_2026-06-29.md`
  - `SECURITY_AUDIT_2026-07-01.md`
  - `SECURITY_AUDIT_2026-07-02.md`
  - `SECURITY_AUDIT_2026-07-03.md`
  - `SECURITY_AUDIT_2026-07-04.md`
  - `SECURITY_AUDIT_2026-07-05.md`
  - `SECURITY_AUDIT_2026-07-06.md` (this report)
- **Files to delete (out of 7-day window):**
  - `SECURITY_AUDIT_2026-06-28.md`
  - `SECURITY_AUDIT_2026-07-04-afternoon.md` (duplicate — Jul 4 already kept)
- **Same-day dedup:** First Jul 6 audit — no duplicates yet