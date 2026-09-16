# Security Audit — 15 September 2026

**Date:** 15/09/2026 (DMY dd/mm/yy)
**Run by:** internal cron / Hermes Agent (default profile) — `security-policy-check`
**Overall:** **CRITICAL — Telegram bot token REVOKED/INVALID, gateway DOWN.** Live gateway log (15/09 05:45) authoritatively shows the active Telegram token `827724…1UJE` **rejected by the server** — the **4th such rejection** (31 Aug, 05 Sep, 09 Sep, 15 Sep). Gateway exits on a non-retryable startup conflict; status `stopped`. This **corrects** the 14/09 audit's "gateway RECOVERED / token VALID" conclusion, which was contradicted by authoritative startup logs. ALL Telegram delivery is down — **including the directive's target, topic 20** — so no topic-20 post could be made this cycle. Credential exposure otherwise clean (backup `.env`=0, caches clear, token-file ACLs secure). **No other active credential compromise.**

**Report path:** `C:\Users\User\.hermes\workspace\Vault\System\Assistant\SECURITY_AUDIT_2026-09-15.md`
**Telegram delivery target:** Topic 20 (`-1003784520976:20`, "Memory Review") — **NOT REACHABLE** (token revoked).

---

## Summary

- **CRITICAL: Telegram bot token REVOKED/INVALID** — token `827724…1UJE` rejected by server at 05:45 today; same rejection on 31/08, 05/09, 09/09. **Escalated to CRITICAL** (credential loss + full Telegram outage). Requires new token via @BotFather → update `TELEGRAM_BOT_TOKEN`.
- **Gateway DOWN** — status `stopped`; last start (15/09 05:45) exited cleanly on the token-rejection conflict. Prior instance (PID 15860) exited UNCLEANLY 09/09 (last heartbeat 18/08).
- **WhatsApp not connectable** — adapter looks for `platforms\whatsapp\session\creds.json` (absent); session creds only exist at legacy `credentials\whatsapp\233204252252\creds.json` (May 15). Path/config mismatch → WhatsApp `failed to connect`. **FAIL.**
- **Credential exposure — CLEAN (PASS):** backup `.env` = **0** (backups/hermes-backup/state-snapshots/.openclaw); no `bws_cache.json`/`.secret_cache`; `google_token.json` + `auth.json` (both roots) ACL = Owner/SYSTEM/Administrators only; WhatsApp creds ACL = Owner/SYSTEM only; AGENTS.md no BOM, no zero-width chars.
- **14/09 "recovered/valid" finding was INCORRECT** — current live logs are authoritative; gateway has not had a healthy Telegram connection in this window.

## Findings by Area

### 1. Credential Exposure — CLEAN (caches/backups/ACLs); token-file access secure
| Item | Status |
|------|--------|
| `bws_cache.json` / `.secret_cache` | **PASS** — absent in both roots |
| Backup `.env` (backups/hermes-backup/state-snapshots/.openclaw) | **PASS** — 0 |
| AGENTS.md (workspace copy) | **PASS** — UTF-8, no BOM, no U+200B |
| `google_token.json` ACL | **PASS** — Owner/SYSTEM/Administrators only |
| `auth.json` ACL (both roots) | **PASS** — Owner/SYSTEM/Administrators only |
| WhatsApp `creds.json` ACL | **PASS** — Owner/SYSTEM only |
| **Active Telegram token** | **FAIL/CRITICAL** — `827724…1UJE` revoked/invalid |
| Live `.env`-reader scripts | **FAIL (carried debt)** — not re-scanned (cron secret-read gate blocks `.env` content access; scan_env_readers.py broken) |

### 2. Channel Integrity — BROKEN (Telegram + WhatsApp both down)
- **Telegram gateway** — ❌ **CRITICAL**: token rejection prevents connection; gateway `stopped`.
- **Active Telegram token** — ❌ CRITICAL: `827724…1UJE rejected by the server` (04× since 31/08). All Delivery Patterns (gateway polling, cron delivery, direct API) fail on this revoked token.
- **WhatsApp** — ❌ **FAIL**: creds exist only at legacy path; adapter's expected path missing → `failed to connect`.
- **Cron delivery** — ❌ all Telegram-targeted jobs fail while token revoked; **55 jobs** configured (44 active); silent/local-origin job share persisted as prior debt; job-state file not on disk (runtime-generated), delivery outcome governed by gateway = down.

### 3. Recent Security Events — TOKEN REVOCATION CONFIRMED (no other breach)
- **`InvalidToken` / `rejected by the server`** — CONFIRMED `827724…1UJE` on 31/08, 05/09, 09/09, 15/09 (today). Treat as credential compromise → **rotate via @BotFather immediately**.
- **No other unauthorized access / provider key rejection** observed in this window (OpenRouter/xAI/Firecrawl keys report configured & healthy in `hermes status`).
- **Nous Portal access/key expiry 13:06 today (~1 hr at audit)** — auto-refresh enabled; **WARN** (unrelated to Telegram; this session operating normally).

## CRITICAL Escalations
| ID | Severity | Description | Persistent? |
|----|----------|-------------|-------------|
| 1 | **CRITICAL** (NEW escalation) | **Telegram bot token `827724…1UJE` revoked/invalid** — 4 rejections since 31/08; gateway down; all Telegram delivery (incl. topic 20) blocked. | Yes (≥3 cycles) |

## FAIL Findings
| ID | Severity | Description | Persistent? |
|----|----------|-------------|-------------|
| 1 | **CRITICAL (≥3 cycles, escalated)** | **Telegram token revoked** — `827724…1UJE` rejected; gateway down. | Yes |
| 2 | **high** | **WhatsApp unpaired/unconnectable** — creds at legacy path vs adapter's expected `platforms\whatsapp\session\creds.json`. | Yes (carried) |
| 3 | **high (≥3 cycles)** | **Dual-`.env` divergence** — active root vs stale home-root `~/.hermes/.env`; task scripts reference divergent root. | Yes |
| 4 | **high (≥3 cycles)** | **Live `.env`-reader scripts** (carried; not re-counted this cycle — gate-blocked). | Yes |
| 5 | **medium (≥3 cycles)** | **Silent cron delivery** (local/origin targets) — now all Telegram delivery down regardless. | Yes |

## WARN Findings
1. Nous Portal access/key expiry **13:06 today** (~1 hr at audit) — auto-refresh enabled; gateway down reduces refresh transport resilience.
2. WhatsApp credential path mismatch (legacy `credentials\whatsapp\…` vs `platforms\whatsapp\session\`).
3. Home-root `.env` stale/divergent — consolidate or retire.
4. Prior 14/09 audit's "recovered/valid" outcome contradicted — status/state-file optimism must be cross-checked against live startup logs.

## Remediation Priority
1. **CRITICAL** — Regenerate Telegram bot token via **@BotFather**, update to a **single** authoritative `TELEGRAM_BOT_TOKEN`, restart gateway. Required to restore all Telegram delivery (incl. topic 20) and to clear the credential-compromise flag.
2. **HIGH** — Move/copy WhatsApp session creds to `platforms\whatsapp\session\creds.json` (or point adapter at legacy path); re-pair if needed.
3. **HIGH** — Retire home-root `~/.hermes/.env`; reconcile dual roots; rewrite/gate `.env`-reader scripts.
4. **MED** — Re-point silent (local/origin) cron jobs to explicit topic targets; confirm Nous key auto-refresh.

## Trend Comparison (vs 14/09)
| Item | 14/09 (prior) | 15/09 (this run) | Trend |
|---|---|---|---|
| Gateway | "UP, both adapters connected" | **DOWN** — token rejection | **Worse / corrected** |
| Telegram token | "valid (bot-auth ops OK)" | **REVOKED** (`827724…1UJE` rejected) | **CRITICAL regression** |
| Backup `.env` | 0 | 0 | Good |
| Cache files | clean | clean | Good |
| Token-file ACLs | secure | secure | Good |
| WhatsApp | "connected & paired" | **unconnectable** (path mismatch) | **Worse** |
| Nous key exp | 09:21 (14/09) | 13:06 today | Stable (auto-refresh) |
| Cron silent | 25/55 | all Telegram delivery down (token) | Worse |

> **Methodological note:** Prior "recovered/valid" conclusions (14/09 & earlier) were based on `gateway_state.json`/state files that can be stale. This run uses the **authoritative startup log** (`gateway-exit-diag.log` + `gateway.log`), which shows token rejection — the getMe-equivalent check — and is definitive. **Do not rely on state files for token validity.**

## Retention Note
Retention applied against the directive path (`Vault\System\Assistant\`): rolling window kept ≤7 files (present: 09/06, 09/07, 09/11, 09/13, 09/14, 09/15 — 6 files; none older than 7 days; no duplicate same-day).

## Delivery
**Summary to Telegram topic 20 — NOT DELIVERED.** Telegram bot token `827724…1UJE` is revoked/invalid (confirmed 05:45 today). Per security-audit policy, delivery to Telegram is a **hard pre-requisite that fails outright** while the token is rejected; no sendMessage attempt was made with a known-bad token. Rotate the token via @BotFather, then re-run delivery. Report artifact saved to the directive path above.

---
*Masked: all secrets printed as provider-prefix + truncated. No full tokens echoed.*