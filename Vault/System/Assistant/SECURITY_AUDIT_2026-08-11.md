# Security Audit — 11 August 2026

**Date:** 11/08/2026
**Scope:** Credential exposure, channel integrity, recent security events
**Report path:** `C:\Users\User\.hermes\workspace\Vault\System\Assistant\SECURITY_AUDIT_2026-08-11.md`

---

## Executive Summary

**Overall status: FAIL** (persistent findings remain, though Telegram channel is healthy and token is valid).

The gateway is **ALIVE and healthy** (PID 13760, active logs in `AppData/Local/hermes/logs/`, established TCP to Telegram). The Telegram bot token is **VALID** (direct `getMe` → `ok:true`, bot `@Ogaitchhermesbot`). No credential compromise detected. WhatsApp remains in a persistent reconnect-fail loop. Credential-leak debt (backup `.env` copies, `.env`-reading scripts) persists.

---

## 1. Credential Exposure

| Finding | Severity | Status |
|---|---|---|
| Backup `.env` copies | **FAIL** | 20 total (9 in `~/.hermes/backups`, 10 in `~/hermes-backup`, 1 in `~/.openclaw`) — improved from 42 |
| Workspace scripts reading `.env` directly | **FAIL** | Multiple: `send_telegram_report.py`, `send_telegram_temp_briefing.py`, `check_*.py`, `send_daily_report.py`, etc. leak token to process/log |
| Dual `.env` roots | **WARN** | `~/.hermes/.env` (full, 24KB) + `AppData/Local/hermes/.env` (399B) both exist — divergence risk |
| Cache credential files | **WARN** | `bws_cache.json` present (masked key found) |
| Secret cache | **PASS** | `.secret_cache` absent |
| AGENTS.md BOM | **PASS** | Workspace AGENTS.md is clean UTF-8, no BOM; main `~/.hermes/AGENTS.md` absent |

**No raw secrets printed. All tokens masked.**

---

## 2. Channel Integrity

| Channel | Status | Detail |
|---|---|---|
| **Telegram** | ✅ **PASS** | Token valid (getMe ok). Gateway PID 13760 live, ESTABLISHED TCP to `149.154.167.92:443` & `149.154.166.110:443`. Active logs fresh (06:04 today). |
| **WhatsApp** | ❌ **FAIL** | Persistent reconnect loop — attempt 171 failing (every 5 min). `creds.json` exists (Jul 21) but bridge fails to connect. Non-functional though configured. |
| **Cron delivery** | **WARN** | 25/40 jobs `deliver=origin` (silent), 2 `local`, 13 topic-targeted (topics 2,4,16,26,28). |
| Topic 20 | ✅ **PASS** | Confirmed exists in channel_directory (id `-1003784520976:20`) |

**Gateway note:** Older `~/.hermes/logs/` is stale (last entry Aug 4); authoritative live logs are at `AppData/Local/hermes/logs/`. Previous `gateway-exit-diag` crash entries (Aug 4 SystemExit 78) superseded by healthy Aug 11 instance.

---

## 3. Recent Security Events

| Event | Severity | Assessment |
|---|---|---|
| WhatsApp unauthorized-user warnings (Jul 19-20) | INFO | `lid` users rejected (Vasty Sounds, OG H-B) — expected access control, not breach |
| Firecrawl 402 **Payment Required / insufficient funds** | **WARN** | Recurring Aug 10-11 — billing/quota (Nous portal subscription), not credential compromise |
| Stream drop / peer closed (OpenRouter) | WARN | Transient network, retried successfully |
| Inference config drift (job unpinned) | WARN | Guard rails blocked spend — safe behavior |
| **Telegram token revocation** | ✅ **PASS** | NOT revoked — `getMe` returns `ok:true`. No InvalidToken in current or rotated (`errors.log.1`) logs |

**No unauthorized access, breach, or token-compromise indicators found in the audit window.**

---

## 4. Trend Comparison vs Prior Audits

| Item | 2026-07-31 | 2026-08-11 | Trend |
|---|---|---|---|
| Telegram token valid | ✅ | ✅ | No Change (good) |
| Gateway/Telegram online | ✅ | ✅ | No Change (good) |
| Backup `.env` copies | ~40 | **20** | **Improved** |
| WhatsApp functional | ❌ | ❌ | No Change (persistent debt) |
| Workspace `.env` readers | ⚠️ | present | Not Remediated (persistent debt) |
| Firecrawl billing (402) | — | WARN | New (WARN) |

---

## 5. Required Actions

1. **Delete 20 backup `.env` copies** (9+10+1) — highest-priority credential cleanup.
2. **Purge `.env`-reading workspace scripts** (`send_telegram_*.py`, `check_*.py` etc.) or rewrite to use Hermes-injected env.
3. **Re-pair WhatsApp** via the bridge (manual QR) to restore channel.
4. **Consolidate dual `.env` roots** — single authoritative location.
5. **Resolve Firecrawl billing** (insufficient Nous subscription balance) if web tools needed.

---

*Audit performed autonomously as scheduled cron. No secrets disclosed in any output.*
