# Security Audit Report — 2026-07-17

**Generated:** 2026-07-17 21:35 UTC  
**Scope:** Internal system audit — credential exposure, channel integrity, recent security events  
**Classification:** INTERNAL — CONFIDENTIAL

---

## Executive Summary

**OVERALL: CRITICAL FAIL** — 7 CRITICAL/FAIL findings, 5 WARN findings

| Category | CRITICAL | FAIL | WARN | PASS |
|----------|----------|------|------|------|
| Credential Exposure | 2 | 2 | 2 | — |
| Channel Integrity | 2 | 2 | 2 | 1 |
| Security Events | 1 | 1 | 2 | — |

**Immediate Action Required:** Telegram bot token **revoked** (HTTP 404 on `getMe`). All Telegram delivery (gateway, cron, direct API) is non-functional. Rotate via @BotFather immediately.

---

## 1. Credential Exposure

### 1.1 Backup `.env` Proliferation — **FAIL (Persistent)**
- **Found:** 13 `.env` files outside canonical `~/.hermes/.env`:
  - `~/.hermes/backups/backup_20260716_230410/.env` (1)
  - `~/hermes-backup/` — 10 files across backup snapshots
  - `~/.openclaw/.env` (1)
- **Risk:** Each contains raw API keys for OpenRouter, Telegram, Firecrawl, Brave, xAI, Google, BWS, etc.
- **Trend:** Down from 49 (2026-07-11) → 57 (2026-07-15) → **13 today** (cleanup in progress but incomplete).
- **Remediation:** Delete all non-canonical `.env` copies. Migrate OpenClaw secrets to Hermes encrypted store.

### 1.2 Telegram Bot Token **REVOKED** — **CRITICAL**
- **Evidence:** Direct `GET https://api.telegram.org/bot<TOKEN>/getMe` → `{"ok":false,"error_code":404,"description":"Not Found"}`
- **History:** `errors.log.1` shows 7× `telegram.error.InvalidToken: The token was rejected by the server` on 2026-06-10
- **Impact:** **ALL** Telegram delivery vectors fail — gateway polling, cron `sendMessage`, direct API Patterns A/B. Gateway shows "Connected" but token is dead.
- **Classification:** Credential compromise or user-initiated rotation via @BotFather. Treat as security event.

### 1.3 Workspace Scripts Reading `.env` Directly — **FAIL (Regression)**
- **Found:** 20+ Python scripts in `~/.hermes/workspace/` reading `.env` via `Path.home() / '.hermes' / '.env'` or `dotenv`
- **Examples:** `send_cron_report.py`, `send_daily_report.py`, `send_health_summary.py`, `tg_send.py`, `check_telegram_bot.py`, `morning_checkin.py`, `send_telegram_*.py`, `tmp_*.py`
- **Risk:** Tokens leak to process table, shell history, logs. Created during gateway-outage delivery attempts.
- **Remediation:** Delete all `send_*.py`, `tmp_*.py`, `check_*.py` in workspace. Use Hermes `send_message` tool or gateway.

### 1.4 Google OAuth Token — **WARN (Broad Scopes)**
- **File:** `~/.hermes/google_token.json`
- **Contents:** `refresh_token`, `client_secret`, `access_token` with scopes: Gmail (modify/read/send), Drive, Sheets, Calendar, Contacts, Docs
- **ACL Check Needed:** Run `icacls google_token.json` — must show only Owner/SYSTEM/Administrators `(I)(F)` with no "Everyone" or "BUILTIN\Users"
- **Expiry:** Access token expired 2026-07-15; refresh token valid. Auto-refresh expected.

### 1.5 Bitwarden Cache — **WARN (Not Found)**
- **Expected:** `~/.hermes/cache/bws_cache.json`, `~/.hermes/cache/.secret_cache`
- **Status:** Neither file exists in either `~/.hermes` or `AppData/Local/hermes`
- **Note:** Previously found with 10+ plaintext service keys (2026-07-07 audit). Current absence is PASS but verify no recreation.

### 1.6 Hermes `.env` Location Mismatch — **WARN**
- `hermes status` / `hermes doctor` report `.env` **not found** (looks at `AppData/Local/hermes/.env`)
- Actual `.env` exists at `~/.hermes/.env` (C:\Users\User\.hermes\.env)
- **Cause:** Dual Hermes roots. Canonical path unclear.
- **Action:** Consolidate to single authoritative location.

---

## 2. Channel Integrity

### 2.1 Telegram Adapter vs. Token Validity — **CRITICAL FAIL**
| Signal | Status | Notes |
|--------|--------|-------|
| `hermes status` | ✓ Gateway running (PID 13808) | Python 3.11 (uv) |
| Gateway log | ✓ "Connected to Telegram (polling mode)" | Last: 2026-06-18 |
| **Direct `getMe` API** | **✗ HTTP 404 Not Found** | **Token revoked** |
| Cron delivery | ✗ `getaddrinfo failed` + InvalidToken | All 34 active jobs failing |

**Finding:** Adapter connectivity ≠ token validity. Gateway maintains TCP connection but Telegram rejects auth. **Token validation MUST precede any delivery attempt.**

### 2.2 Gateway Crash Loop — **FAIL (Historical, Recovered?)**
- **Evidence:** 7 entries in `gateway-exit-diag.log` with `asyncio.run.exception` + `ModuleNotFoundError: concurrent_log_handler` (Python 3.14 venv)
- **Timeline:** 2026-06-22 → 2026-07-01 (daily crashes)
- **Current:** PID 13808 running on Python 3.11 (uv) — appears stable since ~2026-07-01
- **Log Staleness:** `gateway.log` last entry 2026-06-18 — **30 days stale** but PID alive with ESTABLISHED TCP to 149.154.166.110
- **Classification:** **UNSTABLE** — recovery not sustained >1 hour of warm logs. Monitor for relapse.

### 2.3 Cron Delivery Target Audit — **FAIL (59% Silent Failure)**
| Deliver Target | Count | % | Reaches User? |
|----------------|-------|----|---------------|
| `origin` | 25 | 59% | **NO** — stays local |
| `local` | 2 | 5% | **NO** — stays local |
| `telegram:-1003784520976:2` | 3 | 7% | Topic 2 (Health) — blocked by token |
| `telegram:-1003784520976:4` | 3 | 7% | Topic 4 (Mum) — blocked by token |
| `telegram:-1003784520976:16` | 4 | 9% | Topic 16 — blocked by token |
| `telegram:-1003784520976:26` | 3 | 7% | Topic 26 (Content) — blocked by token |
| `telegram:-1003784520976:28` | 1 | 2% | Topic 28 — blocked by token |

**Total jobs:** 42 (34 active) — **27 jobs (64%) never reach user** due to `origin`/`local`; remaining 8 blocked by revoked token.

### 2.4 Topic 20 (Memory Review) — **PASS (Exists)**
- Verified in `channel_directory.json`: Thread ID 20, name "Memory Review", supergroup with forum enabled.

### 2.5 WhatsApp Bridge — **FAIL (65+ Days Down)**
- `~/.hermes/whatsapp/session/creds.json` **missing** — not paired
- Bridge deps present but non-functional since ~2026-05-10
- **Action:** Manual QR re-pair required.

### 2.6 Host-Level DNS Failure — **WARN**
- Correlated `getaddrinfo failed` for `api.telegram.org` AND `openrouter.ai` in same windows (2026-06-18)
- Indicates host network/DNS issue, not targeted attack.
- **Mitigation:** Gateway fallback IPs (149.154.166.110) partially work but flaky.

---

## 3. Recent Security Events

### 3.1 Telegram Token Revocation — **CRITICAL SECURITY EVENT**
- **Date:** ~2026-06-10 (first `InvalidToken` in logs)
- **Confirmation:** 2026-07-17 direct API `getMe` → HTTP 404
- **Root Cause Unknown:** User rotation via @BotFather? Telegram security action? Credential leak?
- **Impact:** Total Telegram comms blackout. All cron deliveries, gateway polling, health checks, business ops silent.
- **Required:** Immediate rotation via @BotFather. Audit all systems using old token.

### 3.2 Gateway Crash Loop (7 Crashes) — **FAIL**
- **Pattern:** `ModuleNotFoundError: concurrent_log_handler` on Python 3.14
- **Window:** 2026-06-22 to 2026-07-01
- **Resolution:** Apparent migration to Python 3.11 (uv) PID 13808
- **Status:** No crashes logged since 2026-07-01 but log stale — **verify sustained operation**

### 3.3 Multi-Provider Credential Rejections — **WARN**
- **xAI/Grok:** 400 Invalid API Key (historical)
- **OpenRouter:** 402 Payment Required / rate limit (2026-06-18)
- **Firecrawl:** 402 Insufficient balance (historical)
- **Classification:** Individual provider issues — not systemic credential compromise.

### 3.4 Workspace Script Proliferation — **FAIL (Self-Inflicted)**
- **Count:** 20+ `send_*.py`, `tmp_*.py`, `check_*.py` created during gateway outages
- **Pattern:** Each reads `.env` directly → token leakage
- **Recurrence:** Regression observed 2026-07-11, 2026-07-13, 2026-07-15 — **persistent security debt**

---

## 4. Configuration Hygiene

### 4.1 AGENTS.md BOM Check — **PASS**
- `~/.hermes/AGENTS.md` — **not present** (deleted/moved)
- `~/.hermes/workspace/AGENTS.md` — UTF-8 text, **no BOM**, no zero-width/RTL chars
- **Status:** Clean. No prompt-injection vector from BOM.

### 4.2 Config Version — **PASS**
- `hermes doctor`: Config version v33 (current). No drift.

### 4.3 JSON Config BOM Scan — **NOT CHECKED**
- Recommend: `find ~/.hermes -name "*.json" -exec file {} \; | grep BOM`

---

## 5. Trend Comparison (vs. 2026-07-15 Audit)

| Finding | 2026-07-15 | 2026-07-17 | Trend |
|---------|------------|------------|-------|
| Backup `.env` copies | 57 | 13 | **Improved** (cleanup active) |
| Workspace `.env` readers | 23 | 20+ | **No Change** (persistent regression) |
| Telegram token | Revoked (401) | Revoked (404) | **Worsened** (now 404 Not Found) |
| Gateway crash loop | 21 days | Recovered (unstable) | **Improved** |
| WhatsApp paired | No (65d) | No (65d) | **No Change** |
| Cron silent delivery (`origin`/`local`) | 27/40 | 27/42 | **No Change** |
| AGENTS.md BOM | Present | Absent | **Resolved** |

**Persistent Security Debt (3+ cycles unremediated):**
1. Backup `.env` proliferation — **ESCALATED to CRITICAL**
2. Workspace direct `.env` readers — **ESCALATED to CRITICAL**
3. WhatsApp bridge down — **ESCALATED to CRITICAL**
4. Cron `origin`/`local` silent failures — **ESCALATED to CRITICAL**

---

## 6. Remediation Priorities

### P0 — Immediate (Today)
1. **Rotate Telegram bot token** via @BotFather → update `~/.hermes/.env` → restart gateway
2. **Delete all non-canonical `.env`** files (13 identified)
3. **Delete all `send_*.py`, `tmp_*.py`, `check_*.py`** in `~/.hermes/workspace/`
4. **Verify gateway sustained operation** — watch `gateway.log` for 1+ hour of warm entries

### P1 — This Week
5. **Audit `google_token.json` ACL** with `icacls`; restrict if over-permissive
6. **Fix cron delivery targets** — change `origin`/`local` to explicit Telegram topics
7. **Re-pair WhatsApp** — manual QR flow
8. **Consolidate Hermes roots** — single `.env` location

### P2 — Ongoing
9. **Automate credential hygiene** — pre-commit hooks, cron cleanup job
10. **Add token validity pre-check** to all delivery paths (gateway, cron, direct API)
11. **Monitor gateway PID/log freshness** — alert on >1h staleness

---

## 7. Audit Artifacts

- **Report Path:** `C:\Users\User\.hermes\workspace\Vault\System\Assistant\SECURITY_AUDIT_2026-07-17.md`
- **Verification:** Run `python3 scripts/hermes-verify-audit-report.py <path>` after write
- **Retention:** Keep latest 7 daily audits; deduplicate same-day runs
- **Cleanup:** Remove `send_audit_*.py`, `tmp_*.py` created during this audit

---

## 8. Telegram Summary (Topic 20 — Memory Review)

🔴 **SECURITY AUDIT 2026-07-17 — CRITICAL FAIL**

**Credential Exposure:**
• 13 `.env` copies in backups (down from 57, still FAIL)
• 20+ workspace scripts leak tokens via direct `.env` reads (REGRESSION)
• **Telegram bot token REVOKED** — HTTP 404 on getMe (CRITICAL SECURITY EVENT)
• Google OAuth token broad scopes — verify Windows ACL

**Channel Integrity:**
• Gateway PID 13808 "running" but token dead — ALL Telegram delivery FAILS
• 27/42 cron jobs (64%) use `origin`/`local` — never reach user
• 7 gateway crashes (concurrent_log_handler) — recovered to Python 3.11 but logs 30d stale → UNSTABLE
• WhatsApp unpaired 65+ days
• Host DNS failures correlate across Telegram + OpenRouter

**Security Events:**
• InvalidToken in logs since 2026-06-10 — confirmed revoked 2026-07-17
• Multi-provider quota/auth failures (xAI, OpenRouter, Firecrawl) — individual, not systemic
• Workspace script proliferation during outages — self-inflicted leakage

**Trend:** Backup `.env` cleanup progressing. Token revocation worsened. Silent cron delivery persistent. Gateway recovery unproven.

**P0 Actions:** Rotate Telegram token @BotFather → purge backup `.env` → delete workspace leaker scripts → verify gateway 1h+ warm logs.

**Report:** `Vault/System/Assistant/SECURITY_AUDIT_2026-07-17.md`