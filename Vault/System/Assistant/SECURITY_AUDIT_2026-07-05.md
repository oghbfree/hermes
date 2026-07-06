# Security Audit — 2026-07-05

**Date:** `2026-07-05`
**Run by:** internal cron / Hermes Agent
**Overall:** 🔴 FAIL — 3 FAIL items, 2 WARN, 2 CRITICAL escalations

---

## Summary

| Category | Status | Details |
|----------|--------|---------|
| Credential Exposure | 🔴 CRITICAL | 28 backup .env copies with live secrets (unchanged from Jul 4) |
| Channel Integrity | 🔴 FAIL | Gateway dead 17 days — crash root cause: `concurrent_log_handler` ModuleNotFoundError |
| Recent Security Events | 🟡 WARN | 7 failed gateway restarts since Jun 22, no new attempts since Jul 1, config drift v29→v32 |

---

## 1. Credential Exposure

### 🔴 CRITICAL: 28 Backup .env Copies (PERSISTENT — 10+ cycles)
- **24 copies** in `~/.hermes/backups/` (incl. `latest`, `latest_old`, nested backups)
- **4 copies** in `~/.hermes/state-snapshots/`
- **No new copies since Jul 4** — count stable at 28
- All contain raw API keys (OpenRouter, Telegram, Google, Firecrawl, Brave, xAI, etc.)
- **PERSISTENT SECURITY DEBT — escalated to CRITICAL**

### 🟢 PASS: Credential Cache Files
- `bws_cache.json`: Not found ✅ (clean)
- `.secret_cache`: Not found ✅ (clean)
- 7th consecutive clean cycle

### 🟢 PASS: google_token.json ACL
- `icacls` shows only Owner: (I)(F), SYSTEM: (I)(F), Administrators: (I)(F)
- No "Everyone" or "BUILTIN\Users" — standard Windows default, PASS

### 🔴 FAIL: Workspace AGENTS.md UTF-8 BOM
- `~/.hermes/workspace/AGENTS.md`: **UTF-8 with BOM** ❌ (prompt injection risk, blocks cron jobs)
- Main `~/.hermes/AGENTS.md`: Absent ✅

### 🟢 PASS: Telegram Bot Token Valid
- DNS resolves `api.telegram.org` (149.154.166.110) ✅
- No `InvalidToken` events in current logs ✅

### 🟢 PASS: No Workspace Scripts Directly Reading .env
- No new offending scripts detected

---

## 2. Channel Integrity

### 🔴 FAIL: Gateway Dead — 17 Days Stale
- **Last log entry: 2026-06-18 17:22:29** (17 days ago)
- **PID 8924 still exists** (tasklist: python.exe, 82MB) but is a zombie — no log activity since June 18
- **Root cause: `concurrent_log_handler` ModuleNotFoundError** (Python 3.14 environment missing package)
- **7 total failed restart attempts** (Jun 22 ×2, Jun 26, Jun 27 ×4)
- **Last attempt: 2026-07-01 22:06 UTC** — no further attempts since

### 🔴 FAIL: 27/40 Jobs Silent Delivery
- 25 jobs deliver to `origin` — output stays local
- 2 jobs deliver to `local` — output stays local
- Only 13/40 jobs target Telegram topics (all currently undeliverable)
- Health-critical jobs affected: mum-health, dad-health, health-check, job-applications, content-engine

### 🔴 FAIL: WhatsApp Unpaired (65+ Days)
- `~/.hermes/whatsapp/session/` is **empty** — no `creds.json`
- WhatsApp bridge has 5 npm vulnerabilities (1 critical, 2 high, 2 moderate)
- Not exploitable while unpaired

### 🟢 DNS Healthy
- `api.telegram.org` resolves ✅ (149.154.166.110)
- `openrouter.ai` resolves ✅
- Root cause was host-level DNS, not targeted attack

---

## 3. Recent Security Events

### 🔴 FAIL: Gateway Crash Loop — ModuleNotFoundError (Jun 22–Present)
- **7 failed restart attempts** across 5 days
- Each crash: `from concurrent_log_handler import ... ModuleNotFoundError`
- Python 3.14 environment — missing `concurrent_log_handler` package
- **No auto-recovery possible** — manual fix: `pip install concurrent_log_handler && hermes gateway run --replace`
- **No new attempts since Jul 1** — 4 days without recovery attempt

### 🟢 Historical InvalidToken (Jun 8-9) — Resolved
- Token was rejected but replaced. Current token valid.
- No `InvalidToken` events in current or rotated logs

### 🟡 WARN: Config Version Drift
- `_config_version: 23` (unchanged)
- doctor schema: v29
- latest schema: v32
- 3 versions behind — still unresolved

### 🟡 WARN: hermes status Reports 48 Jobs, jobs.json Has 40
- Discrepancy of 8 jobs — 10 jobs in-memory only (ephemeral/session-based)
- Not security-critical but indicates state drift

### 🟡 WARN: 16+ Jobs Not Run Since June 18
- All cron jobs stuck — scheduler can't route through dead gateway
- DNS failures on last attempt for 11 jobs

### ✅ No Breach Markers Detected
- No unauthorized access patterns in logs
- No token revocation events (current)
- No traffic redirection evidence

---

## 4. Trend vs Prior Audit (2026-07-04 Afternoon)

| Finding | Jul 4 (Afternoon) | Jul 5 | Change |
|---------|-------------------|-------|--------|
| Backup .env copies | 🔴 28 (CRITICAL) | 🔴 28 (CRITICAL) | No change |
| Gateway dead days | 16 days | **17 days** | 🔴 Worsening |
| Gateway crash attempts | 9 | 7 (no new) | No new attempts |
| WhatsApp unpaired | 64+ days | **65+ days** | 🔴 Worsening |
| Workspace AGENTS.md BOM | 🔴 FAIL | 🔴 FAIL | No change |
| Config drift (v23→v29→v32) | 🟡 WARN | 🟡 WARN | No change |
| bws_cache.json | ✅ Gone | ✅ Gone | No change |
| DNS health | ✅ Resolves | ✅ Resolves | No change |
| 27/40 silent jobs | 🔴 FAIL | 🔴 FAIL | No change |
| Telegram token valid | ✅ Valid | ✅ Valid | No change |
| Gateway crash root cause | 🔴 ModuleNotFoundError | 🔴 ModuleNotFoundError | No change |
| PID 8924 | Dead | **Zombie** (tasklist shows it) | 🔴 Finding refined |

### Persistent Security Debt (10+ cycles unremediated)
- **Backup `.env` copies** — 28 copies, 10+ cycles, CRITICAL
- **WhatsApp unpaired** — 65+ days
- **AGENTS.md BOM** — 5+ cycles
- **Gateway crash loop** — 13 days without resolution
- **Config drift** — unchanged for weeks

---

## 5. Recommendations

### IMMEDIATE
1. **🔴 CRITICAL — Install missing module & restart gateway:**
   ```bash
   pip install concurrent_log_handler
   hermes gateway run --replace
   ```
   This fixes ALL cron delivery — the only blocker since Jun 22

2. **🔴 CRITICAL — Delete backup .env copies:**
   ```bash
   find ~/.hermes/backups -name ".env" -delete
   find ~/.hermes/state-snapshots -name ".env" -delete
   ```
   28 copies of every API key — extreme exposure surface

3. **🔴 Fix local-delivery jobs:** `mum-health-morning`, `mum-health-evening`, and 25 `origin` jobs never reach a user

4. **🔴 Re-pair WhatsApp:** Session empty for 65+ days — needs QR code pairing

### HIGH
5. **Strip AGENTS.md BOM:** `sed -i '1s/^\xEF\xBB\xBF//' ~/.hermes/workspace/AGENTS.md`
6. **Update config:** `hermes doctor --fix` to migrate v23 → v32

### MEDIUM
7. **Fix cron delivery targets:** Migrate `origin` jobs to explicit Telegram topics
8. **Add GITHUB_TOKEN to .env:** For better Skills Hub rate limits

---

## 6. Retention Cleanup

- **7-day window:** Keep files Jun 28 – Jul 5 only
- **Files retained:**
  - `SECURITY_AUDIT_2026-06-28.md`
  - `SECURITY_AUDIT_2026-06-29.md`
  - `SECURITY_AUDIT_2026-07-01.md`
  - `SECURITY_AUDIT_2026-07-02.md`
  - `SECURITY_AUDIT_2026-07-03.md`
  - `SECURITY_AUDIT_2026-07-04.md`
  - `SECURITY_AUDIT_2026-07-04-afternoon.md`
  - `SECURITY_AUDIT_2026-07-05.md` (this report)
- **No same-day dedup needed** (first Jul 5 audit)
- **No old files outside 7-day window in this directory**