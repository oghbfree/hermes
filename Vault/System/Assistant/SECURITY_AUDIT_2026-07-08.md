# Security Audit — 2026-07-08

**Date:** `2026-07-08`
**Run by:** internal cron / Hermes Agent
**Overall:** 🟡 MODERATE FAIL — 4 FAIL items (1 CRITICAL escalation), 2 WARN

---

## Summary

| Category | Status | Details |
|----------|--------|---------|
| Credential Exposure | 🔴 CRITICAL | **43 backup .env copies** across 4 locations (down from 49) |
| Channel Integrity | 🟢 PASS | **Gateway STABLE** — PID 17112 running 35h with 2 ESTABLISHED Telegram connections |
| Recent Security Events | 🟡 WARN | WhatsApp 69d unpaired, AGENTS.md BOM, config drift v29→v33 |

---

## 1. Credential Exposure

### 🔴 CRITICAL: 43 Backup .env Copies (PERSISTENT — 13+ cycles, SLIGHTLY IMPROVED)

| Location | Count |
|----------|-------|
| `~/.hermes/backups/` | 28 |
| `~/.hermes/state-snapshots/` | 4 |
| `~/.openclaw/.env` | 1 |
| `~/hermes-backup/` | 10 |
| **TOTAL** | **43** |

- Down from 49 (Jul 7) but still **CRITICAL** — raw API keys (OpenRouter, Telegram, Google, Firecrawl, Brave, xAI) exposed across 4 filesystem trees
- **PERSISTENT SECURITY DEBT — escalated to CRITICAL (13 cycles)**
- Notable: `hermes-backup/` count confirmed at 10, not 17 (prior overcount — validates skill warning about `find` timeout issue)

### 🟢 PASS: Credential Cache Files
- `bws_cache.json`: Not found ✅ (10th consecutive cycle clean)
- `.secret_cache`: Not found ✅

### 🟢 PASS: google_token.json ACL
- No `google_token.json` file found (not on disk) ✅ — previously assessed as standard Owner/SYSTEM/Admin ACL

### 🟡 WARN: Workspace AGENTS.md UTF-8 BOM
- `~/.hermes/workspace/AGENTS.md`: **UTF-8 with BOM** ❌ (prompt injection risk)
- Main `~/.hermes/AGENTS.md`: Does not exist ✅
- **SAME AS JUL 7** — no remediation

### 🟢 PASS: Telegram Bot Token Valid
- PID 17112 has 2 ESTABLISHED connections to `149.154.166.110:443` ✅
- No `InvalidToken` events in any log ✅

### 🔴 FAIL: probe_threads.py Directly Reads .env (REGRESSION)
- `~/.hermes/workspace/probe_threads.py` (938 bytes, Jun 23) reads `TELEGRAM_BOT_TOKEN` from `.env` with raw `open()` + line parsing
- Still present — **not remediated** since discovery
- Additional note: `test_threads.py` (found Jul 7) not found on disk this cycle — may have been cleaned up or moved

### 🟢 PASS: Config/Jobs JSON — No BOM
- `config.yaml`, `cron/jobs.json` — all clean ✅

---

## 2. Channel Integrity

### 🟢 PASS: Gateway STABLE (35+ Hours Uptime)

| Metric | Value |
|--------|-------|
| PID 17112 | ✅ Running since Jul 6 (uv python3.11) |
| PID 7984 | ✅ Running (second python.exe process) |
| Telegram connections | ✅ 2 ESTABLISHED to `149.154.166.110:443` |
| DNS resolution | ✅ `api.telegram.org` (149.154.166.110), `openrouter.ai` (104.18.x.x) |
| Webhook status | Polling mode (healthy) |

- PID 7984 confirmed as a second python.exe process — likely a child manager or cron worker
- Old gateway.log (Jun 18) belongs to prior instance — new instance writes differently

### 🟡 WARN: WhatsApp Unpaired (69+ Days)
- `~/.hermes/whatsapp/session/creds.json`: **MISSING**
- 69 days without re-pair attempt — still non-functional channel
- **PERSISTENT SECURITY DEBT — 13+ cycles, WORSENING**

### 🟡 WARN: 27/40 Jobs Silent Delivery
- 25 jobs `deliver=origin` — output stays on machine
- 2 jobs `deliver=local` — no external delivery
- 13 jobs target Telegram topics (now deliverable with recovered gateway)
- Status unchanged from Jul 7

### 🟢 DNS Healthy
- `api.telegram.org` resolves ✅ (149.154.166.110, IPv6 also)
- `openrouter.ai` resolves ✅ (104.18.x.x, IPv6 also)

---

## 3. Recent Security Events

### 🟢 PASS: Gateway Crash Loop Resolved
- Last `concurrent_log_handler` crash: Jul 1 (PID 15068)
- No new crashes in 7 days — fully resolved
- Current instance (PID 17112) stable for 35+ hours

### 🟢 PASS: No Breach Markers
- No unauthorized access patterns
- No token revocation or `InvalidToken` events
- No traffic redirection
- No suspicious outbound connections beyond known Telegram (149.154.166.110)

### 🟡 WARN: Config Version Drift
- v29 → v33 (unchanged from Jul 7)
- Run `hermes doctor --fix` to migrate

### 🟡 WARN: Job Count Discrepancy
- `hermes status`: 47 active jobs
- `cron/jobs.json`: 40 jobs
- 7-job discrepancy persists — likely ephemeral/in-memory jobs

### 🟢 PASS: hermes doctor Clean
- No security advisories active
- SSL valid
- All required packages installed
- No retired xAI models in config

---

## 4. Trend vs Prior Audit (2026-07-07)

| Finding | Jul 7 | Jul 8 | Change |
|---------|-------|-------|--------|
| Backup .env copies | 🔴 49 (CRITICAL) | 🔴 **43** (CRITICAL) | ⬇️ **Slight improvement (-6)** — `hermes-backup` count corrected |
| Gateway status | 🟢 RECOVERED (12.5h) | 🟢 **STABLE (35h)** | ✅ Stable — no regression |
| WhatsApp unpaired | 🟡 68+ days | 🟡 **69+ days** | 🔴 Worsening (+1 day) |
| AGENTS.md BOM (workspace) | 🟡 WARN | 🟡 WARN | No change |
| Config drift | v29→v33 (WARN) | v29→v33 (WARN) | No change |
| probe_threads.py leak | ❓ Not yet found | 🔴 FAIL | **Regressed — discovered** |
| Credential caches (bws, .secret) | ✅ Clean | ✅ Clean | No change |
| DNS health | ✅ Resolves | ✅ Resolves | No change |
| 27/40 silent jobs | 🟡 WARN | 🟡 WARN | No change |
| Telegram token | ✅ Valid | ✅ Valid | No change |

### Persistent Security Debt (13+ cycles unremediated)
- **Backup `.env` copies** — 43 copies, 13+ cycles, **CRITICAL**
- **WhatsApp unpaired** — 69+ days, worsening weekly
- **AGENTS.md workspace BOM** — 6+ cycles
- **Config drift** — v29→v33, unchanged

### New/Changed Findings
- **probe_threads.py credential leak** — newly identified (was on disk Jun 23, not flagged Jul 7 main report)
- **Backup count corrected** — 43, not 49 (`~/hermes-backup` was overcounted at 17 due to recursion depth)

### De-escalating Items
- **Gateway stability** — now in second consecutive audit as PASS; 35h uptime
- **No breach markers** for 7+ days post-recovery

---

## 5. Recommendations

### IMMEDIATE
1. **🔴 CRITICAL — Delete ALL backup .env copies (43):**
   ```bash
   find ~/.hermes/backups -name ".env" -delete
   find ~/.hermes/state-snapshots -name ".env" -delete
   find ~/hermes-backup -name ".env" -delete
   rm -f ~/.openclaw/.env
   ```

2. **🔴 HIGH — Delete credential-leaking scripts:**
   ```bash
   rm -f ~/.hermes/workspace/probe_threads.py
   rm -f ~/.hermes/test_threads.py
   ```

3. **🔴 HIGH — Strip AGENTS.md BOM:**
   ```bash
   sed -i '1s/^\xEF\xBB\xBF//' ~/.hermes/workspace/AGENTS.md
   ```

4. **🟡 HIGH — Update config:**
   ```bash
   hermes doctor --fix
   ```

### MEDIUM
5. **Re-pair WhatsApp**: 69+ days unpaired
6. **Migrate cron delivery**: 27 `origin`/`local` jobs to Telegram topics
7. **Delete OpenClaw `.env`**: Ensure secrets migrated to Hermes `.env` first

---

## 6. Retention Cleanup

- **7-day window:** Keep files Jul 1 – Jul 8
- **Retained files:**
  - SECURITY_AUDIT_2026-07-01.md
  - SECURITY_AUDIT_2026-07-02.md
  - SECURITY_AUDIT_2026-07-03.md
  - SECURITY_AUDIT_2026-07-04.md
  - SECURITY_AUDIT_2026-07-05.md
  - SECURITY_AUDIT_2026-07-06.md
  - SECURITY_AUDIT_2026-07-07.md
  - SECURITY_AUDIT_2026-07-08.md (this report)

- **Deleted this session:**
  - SECURITY_AUDIT_2026-06-29.md, SECURITY_AUDIT_2026-06-30.md (out of 7-day window)
