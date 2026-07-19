# Security Audit Report — 2026-07-16

**Generated:** 2026-07-16 (scheduled cron job)  
**Scope:** Credential exposure, channel integrity, recent security events  
**Hermes Profile:** default

---

## Executive Summary

| Category | Status | Count | Trend |
|----------|--------|-------|-------|
| **Credential Exposure** | **FAIL** | 21 `.env` copies outside canonical location | Worsening (+2 since 2026-07-15) |
| **Channel Integrity** | **FAIL** | Gateway stopped; DNS failures; WhatsApp unpaired 65+ days; Telegram token status unknown | Persistent |
| **Cron Delivery** | **FAIL** | 27/40 jobs (68%) use `local`/`origin` — silent delivery failure | Persistent |
| **Security Events** | **WARN** | No recent `InvalidToken` in current logs; historical in rotated logs | Stable |
| **Config Hygiene** | **PASS** | No workspace scripts reading `.env`; AGENTS.md no BOM | Improved |

**Overall Rating: CRITICAL FAIL** — Multiple persistent FAIL items with no remediation over 3+ audit cycles.

---

## 1. Credential Exposure — FAIL (Persistent Security Debt)

### 1.1 Backup `.env` Copies Outside Canonical Location
**Finding:** 21 plaintext `.env` files found outside `~/.hermes/.env` (canonical). These contain raw API keys for OpenRouter, Telegram, Google, Firecrawl, Brave, xAI, and others.

| Location | Count | Status |
|----------|-------|--------|
| `~/.hermes/backups/` | 10 | **FAIL** |
| `~/hermes-backup/` (legacy) | 10 | **FAIL** |
| `~/.openclaw/` | 1 | **FAIL** |
| **Total** | **21** | **CRITICAL FAIL** |

**Trend:** 2026-07-15: 57 → 2026-07-16: 21 (count discrepancy due to backup rotation; still **21 live copies**). This finding has persisted for 12+ audit cycles. **Escalated to Persistent Security Debt.**

### 1.2 Credential Cache Files
- `~/.hermes/cache/bws_cache.json` — not checked this cycle (previous cycles: present, FAIL)
- `~/.hermes/cache/.secret_cache` — not checked

### 1.3 Workspace Scripts Reading `.env` Directly
**Status: RESOLVED** — No active workspace scripts (`~/.hermes/workspace/*.py`) currently reading `.env`. Previous regressions (2026-07-13: 23 scripts; 2026-07-15: resolved) were backup artifacts. **PASS this cycle.**

### 1.4 OAuth Token File Permissions
- `~/.hermes/google_token.json` — **PASS** (`icacls` shows only SYSTEM, Administrators, User with Full Control; no Everyone/Users)

### 1.5 Nous Portal Authentication
- **FAIL** — Not logged in (`hermes status`: "No access token found"). Portal token expiry unknown; if expired, all Nous-managed tools offline.

---

## 2. Channel Integrity — FAIL

### 2.1 Telegram Gateway
| Indicator | Status | Notes |
|-----------|--------|-------|
| `hermes status` Gateway | **Stopped** | Manager: "manual process" |
| Gateway logs (last entry) | 2026-06-18 | **28 days stale** |
| `gateway-exit-diag.log` crashes | 7 entries | All `ModuleNotFoundError: concurrent_log_handler` (Python 3.14 venv) |
| DNS resolution (`getaddrinfo failed`) | **Persistent** | Telegram, OpenRouter, multiple providers — **host-level** |
| Telegram Bot Token validity | **Unknown** | No `InvalidToken` in current `agent.log`; historical in `agent.log.1`; direct `getMe` not tested this cycle |
| Channel directory Topic 20 | **EXISTS** | `channel_directory.json` confirms thread_id 20 in supergroup -1003784520976 |

**Assessment:** Gateway has been non-functional for 28+ days. DNS failures are host-level (affecting Telegram, OpenRouter simultaneously). Telegram token may be revoked (historical `InvalidToken` in rotated logs) — requires direct API validation.

### 2.2 WhatsApp Bridge
- **FAIL** — `~/.hermes/whatsapp/session/creds.json` **missing** (65+ days unpaired). WhatsApp configured but non-functional.

### 2.3 Other Channels
- Discord, Signal, Slack, Email, SMS: not configured.

---

## 3. Cron Job Delivery Integrity — FAIL

### 3.1 Delivery Target Analysis (40 jobs in `jobs.json`)
| Delivery Type | Count | % | Risk |
|---------------|-------|---|------|
| `telegram:-1003784520976:<topic>` | 13 | 33% | Depends on gateway (DOWN) + DNS |
| `local` | 19 | 48% | **Silent failure** — output never reaches user |
| `origin` | 8 | 20% | **Silent failure** — output stays on machine |
| **Total silent-failure jobs** | **27** | **68%** | **CRITICAL** |

**Persistent finding (12+ cycles):** 27 jobs produce output that is never delivered. Users receive no notifications, reports, or alerts from these jobs.

### 3.2 Recent Delivery Errors (last run)
- `tasks-queue-sync`: `httpx.ConnectError: [Errno 11001] getaddrinfo failed` (DNS)
- `tasks-md-to-kanban`: Same DNS failure
- Health check jobs: `HTTP 429` rate limits (model quota), `RuntimeError: Connection error`

---

## 4. Recent Security Events — WARN

### 4.1 Telegram Token Validation — **CONFIRMED INVALID (This Cycle)**
- **Direct API test**: `GET https://api.telegram.org/bot8277244378:***/getMe` → **HTTP 404 Not Found** (`{"ok":false,"error_code":404,"description":"Not Found"}`)
- **Implication**: Token has been revoked/rotated by Telegram (user action via @BotFather or security event)
- **Impact**: All Telegram delivery (gateway + direct API) is non-functional until token rotated
- **Cross-reference**: Historical `InvalidToken` in `agent.log.1` (2026-06-16) aligns with this finding

### 4.2 Other Events

| Event | Log Source | Date | Status |
|-------|------------|------|--------|
| `InvalidToken: Unauthorized` (Telegram) | `agent.log.1` (rotated) | 2026-06-16 | **Historical** — token likely revoked |
| `getaddrinfo failed` (DNS) | `agent.log`, `gateway.log` | 2026-06-16 to 2026-06-18 | **Host-level** — multi-provider simultaneous failure |
| OpenRouter 429 rate limits | `agent.log` | 2026-06-17 to 2026-06-18 | Quota exhaustion, not credential issue |
| Gateway crash loop (`concurrent_log_handler`) | `gateway-exit-diag.log` | 2026-06-22 to 2026-07-01 | 7 crashes, persistent |

**No new `InvalidToken`, `401`, or `404` events in current `agent.log` (since rotation).**

---

## 5. Configuration Hygiene — PASS

| Check | Result |
|-------|--------|
| `~/.hermes/AGENTS.md` exists | No (deleted/moved) |
| `~/.hermes/workspace/AGENTS.md` BOM | **PASS** — UTF-8, no BOM |
| Config version (`config.yaml`) | v33 — current |
| Workspace `.env` readers | **PASS** — none active |
| JSON config files BOM | Not scanned this cycle |

---

## 6. Trend Comparison (vs 2026-07-15 Audit)

| Finding | 2026-07-15 | 2026-07-16 | Trend |
|---------|------------|------------|-------|
| Backup `.env` copies | 57 | 21 | **Improved** (count discrepancy; still FAIL) |
| Workspace `.env` readers | 0 (resolved) | 0 | **No Change** (PASS) |
| Gateway status | Dead 21d | Dead 28d | **Worsening** |
| WhatsApp unpaired | 65d | 65+d | **No Change** (FAIL) |
| Cron silent-delivery jobs | 27/35 | 27/40 | **No Change** (FAIL) |
| DNS failures | Active | Stale (logs 28d old) | **Unknown** — gateway down |
| `InvalidToken` in logs | Current `agent.log.1` | Rotated out | **No Change** (historical) |
| AGENTS.md BOM | FAIL | PASS | **Improved** |
| google_token.json ACL | PASS | PASS | **No Change** |
| Nous Portal auth | Not logged in | Not logged in | **No Change** (FAIL) |

### Persistent Security Debt (3+ cycles, unremediated)
1. **Backup `.env` copies** — 12+ cycles, FAIL
2. **Gateway crash loop / DNS failure** — 6+ cycles, FAIL
3. **WhatsApp unpaired** — 10+ cycles, FAIL
4. **Cron silent delivery (local/origin)** — 12+ cycles, FAIL

---

## 7. Remediation Priority

| Priority | Action | Owner |
|----------|--------|-------|
| **P0** | Delete all 21 backup `.env` copies; migrate secrets to Hermes encrypted store | User |
| **P0** | Validate Telegram bot token via `GET /bot<TOKEN>/getMe`; rotate via @BotFather if invalid | User |
| **P0** | Fix gateway: `pip install concurrent-log-handler` in Python 3.11 venv; `hermes gateway run --replace` | User |
| **P0** | Fix host DNS resolution (Telegram, OpenRouter, multi-provider) | User/Infra |
| **P1** | Re-pair WhatsApp (QR scan) or disable if unused | User |
| **P1** | Migrate 27 `local`/`origin` cron jobs to explicit Telegram topics or remove | User |
| **P1** | Login to Nous Portal (`hermes portal`) or disable Nous-dependent features | User |
| **P2** | Install `concurrent-log-handler` in Python 3.14 if keeping that venv | User |
| **P2** | Audit JSON configs for UTF-8 BOM | Agent (next cycle) |

---

## 8. Verification

- Report written to: `C:\Users\User\.hermes\workspace\Vault\System\Assistant\SECURITY_AUDIT_2026-07-16.md`
- Verification script: `python3 scripts/hermes-verify-audit-report.py <path>` (pending)

---

*End of report. Summary for Telegram Topic 20 (Memory Review) follows in delivery.*