# Security Audit — Internal System

**Date:** 2026-07-13
**Run by:** internal cron / Hermes Agent
**Overall:** **FAIL**

---

## Summary

- **CRITICAL:** Telegram bot token invalidated (`InvalidToken: Not Found` in rotated logs) — Telegram delivery completely offline.
- **CRITICAL:** 49 `.env` backup copies containing live API keys found across backup trees (34 in `~/.hermes/backups`, 4 in `~/.hermes/state-snapshots`, 10 in `~/hermes-backup`, 1 in `~/.openclaw`).
- **CRITICAL:** 23 active cron jobs reading `.env` directly via `dotenv`/`open('.env')` in workspace scripts — tokens leak to process tables, shell history, logs.
- **CRITICAL:** WhatsApp bridge unpaired for 40+ days (no `creds.json`); platform non-functional.
- **HIGH:** Gateway crash loop — 7 `ModuleNotFoundError: concurrent_log_handler` crashes in Python 3.14 venv; gateway restarts but Python 3.14 environment broken.
- **HIGH:** Multi-service DNS failure (Telegram `api.telegram.org`, fallback IPs) — host-level network/DNS issue affecting all cron deliveries.
- **HIGH:** 25 cron jobs use `deliver: origin` (silent local-only delivery); 2 use `deliver: local`; only 13 target explicit Telegram topics — most cron output never reaches user.
- **MEDIUM:** `~/.hermes/workspace/AGENTS.md` contains UTF-8 BOM — blocks cron execution (prompt injection guard).
- **MEDIUM:** Nous Portal token expired/not logged in — all Nous-managed tools unavailable.

---

## Findings by Area

### 1. Credential Exposure

| Check | Result | Evidence |
|-------|--------|----------|
| `~/.hermes/.env` | PASS (protected from `read_file`) | Defense-in-depth blocks direct read; `hermes status` shows keys masked |
| `~/.hermes/config.yaml` | PASS | Uses `${VAR}` references, no hardcoded secrets |
| `~/.hermes/auth.json` | PASS | No plaintext tokens found |
| Backup `.env` copies | **FAIL (49 files)** | 34 in `~/.hermes/backups/`, 4 in `~/.hermes/state-snapshots/`, 10 in `~/hermes-backup/`, 1 in `~/.openclaw/` — all contain live OpenRouter, Telegram, Google, Firecrawl, Brave, xAI keys |
| Credential cache (`bws_cache.json`) | PASS (not present) | File not found |
| `google_token.json` permissions | PASS | `icacls` shows Owner/SYSTEM/Administrators only (F); no Everyone/Users |
| Workspace scripts reading `.env` directly | **FAIL (23 scripts)** | `~/.hermes/workspace/*.py` and `~/.hermes/workspace/scripts/*.py` use `dotenv`/`open('.env')` — tokens leak to process table, shell history, logs |
| AGENTS.md BOM | **FAIL** | `~/.hermes/workspace/AGENTS.md` has UTF-8 BOM (`U+FEFF`) — blocks cron execution |

### 2. Channel Integrity

| Platform | Status | Details |
|----------|--------|---------|
| **Telegram** | **FAIL** | `InvalidToken` in `agent.log.1` (token `8277...ugM8` rejected by Telegram); `getMe` would return 404. Gateway shows "connected" but token invalid. DNS resolution fails for `api.telegram.org` (Errno 11001) and fallback IPs (149.154.167.220, 149.154.166.110) also fail — host-level DNS/network issue. |
| **WhatsApp** | **FAIL** | Unpaired 40+ days: no `creds.json` at `~/.hermes/whatsapp/session/`; gateway startup fails with "WhatsApp enabled but not paired" |
| **Webhooks / Other** | N/A | Discord, Signal, Slack, Email, SMS not configured |
| **Cron Delivery Targets** | **FAIL** | 25 jobs `deliver: origin` (reply to trigger context — silent in cron), 2 jobs `deliver: local` (in-session only), 13 jobs target Telegram topics but DNS blocks delivery |

### 3. Recent Security Events

| Event | Count | Severity | Source |
|-------|-------|----------|--------|
| `InvalidToken: Not Found` / `The token was rejected by the server` | 6+ | **CRITICAL** | `agent.log.1` (rotated) — Telegram token revoked/rotated |
| `httpx.ConnectError: [Errno 11001] getaddrinfo failed` (Telegram DNS) | Continuous | **HIGH** | `gateway.log` — primary + fallback IPs fail |
| `ModuleNotFoundError: No module named 'concurrent_log_handler'` | 7 | **HIGH** | `gateway-exit-diag.log` — Python 3.14 venv missing dependency |
| WhatsApp "enabled but not paired" | 10+ gateway start attempts | **FAIL** | `gateway.log` — persistent since 2026-06-04 |
| Cron delivery failures (`getaddrinfo failed`) | 20+ jobs affected | **HIGH** | `jobs.json` `last_delivery_error` fields |
| AGENTS.md BOM blocking cron | Ongoing | **MEDIUM** | `errors.log` — `invisible_unicode_U+FEFF` blocks execution |

---

## FAIL Items

| ID | Severity | Description | Evidence / Source |
|----|----------|-------------|-------------------|
| 1 | CRITICAL | Telegram bot token invalidated — complete Telegram outage | `agent.log.1`: `InvalidToken: Not Found` |
| 2 | CRITICAL | 49 `.env` backup copies with live API keys across 4 backup trees | `find` results: 34+4+10+1 |
| 3 | CRITICAL | 23 workspace scripts read `.env` directly — credential leakage to process table/logs | `grep -r "\.env\|dotenv" ~/.hermes/workspace/` |
| 4 | CRITICAL | WhatsApp unpaired 40+ days — platform non-functional | `gateway.log`: "no creds.json" since 2026-06-04 |
| 5 | HIGH | Gateway crash loop: 7 `concurrent_log_handler` ModuleNotFoundError in Python 3.14 | `gateway-exit-diag.log`: 7 `asyncio.run.exception` entries |
| 6 | HIGH | Host-level DNS failure blocks all Telegram/API connectivity | `gateway.log`: primary + fallback IPs fail |
| 7 | HIGH | 27 cron jobs silently deliver locally (`origin`/`local`) — output never reaches user | `jobs.json` deliver field audit |
| 8 | MEDIUM | `AGENTS.md` UTF-8 BOM blocks cron job execution | `errors.log`: `invisible_unicode_U+FEFF` |
| 9 | MEDIUM | Nous Portal not logged in — all Nous tools unavailable | `hermes status`: `Nous Portal ✗ not logged in` |

---

## Recommended Remediations

1. **Immediate: Rotate Telegram bot token** via @BotFather; update `.env`; restart gateway.
2. **Delete all 49 backup `.env` copies** — retain only `~/.hermes/.env` as canonical.
3. **Refactor 23 workspace scripts** to use Hermes credential injection (`${VAR}` in config) or `hermes env` — never read `.env` directly.
4. **Remove UTF-8 BOM** from `~/.hermes/workspace/AGENTS.md`: `sed -i '1s/^\xEF\xBB\xBF//' ~/.hermes/workspace/AGENTS.md`.
5. **Fix Python 3.14 venv**: `pip install concurrent-log-handler` then `hermes gateway run --replace`.
6. **Diagnose host DNS**: `nslookup api.telegram.org`, check Windows DNS client, firewall, proxy/VPN.
7. **Pair WhatsApp** (`hermes whatsapp`) or disable `WHATSAPP_ENABLED=false` in `.env`.
8. **Re-route cron deliveries**: update 27 `origin`/`local` jobs to explicit `telegram:-1003784520976:<topic_id>` targets.
9. **Login to Nous Portal**: `hermes portal` to refresh token.
10. **Implement credential hygiene cron**: weekly scan for `.env` copies outside `~/.hermes/.env`.

---

## Attachments / Evidence

- `hermes status --all` output
- `hermes doctor` output
- `~/.hermes/cron/jobs.json` (delivery target audit)
- `~/.hermes/logs/gateway.log` (last 100 lines — DNS/connection failures)
- `~/.hermes/logs/gateway-exit-diag.log` (7 crash signatures)
- `~/.hermes/logs/agent.log.1` (InvalidToken events)
- `find` outputs for `.env` backup copies
- `icacls ~/.hermes/google_token.json` (ACL verification)
- `file ~/.hermes/workspace/AGENTS.md` (BOM detection)
- `cat ~/.hermes/channel_directory.json | grep thread_id` (Topic 20 confirmed)