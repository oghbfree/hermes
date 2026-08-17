# Security Audit — 15 August 2026

**Date:** 15/08/2026 (15:32 GMT)
**Run by:** internal cron / Hermes Agent
**Overall:** FAIL (persistent credential-leak debt; **gateway DOWN** — regression; Telegram token valid; WhatsApp down, 30/56 cron jobs silent)
**Report path:** `C:\Users\User\.hermes\workspace\Vault\System\Assistant\SECURITY_AUDIT_2026-08-15.md`

---

## Summary

- **Telegram bot token VALID** — direct `getMe` → `ok:true`, `@Ogaitchhermesbot`, `has_topics_enabled:true`. No `InvalidToken`/`Unauthorized` in live or rotated logs.
- **Gateway DOWN — REGRESSION** ⚠️ — `hermes gateway status` reports **no gateway process detected**; `gateway_state.json` PID 5596 is **dead** (`tasklist` no match). Gateway log last written **10:15 today** (stale ~5h), ending in repeated `[Telegram] ... All connection attempts failed` polling reconnect failures. Prior audit (08-14 06:04) had gateway alive (PID 18368). Last `gateway.start` recorded 08-14 09:44 (PID 5596, Python 3.14.3). No live ESTABLISHED TCP to Telegram (only TIME_WAIT).
- **Topic 20 ("Memory Review") present** — `-1003784520976:20` confirmed in `channel_directory.json`.
- **Persistent credential-leak debt (3+ cycles, escalate):** **25 backup `.env` copies** (14 `~/.hermes/backups` + 10 `~/hermes-backup` + 1 `~/.openclaw`, unchanged), plaintext cache **`bws_cache.json`** present, and **~29 live operational `.py` env-readers** (root workspace `send_*`/`tg_*`/`check_*`, `scripts/`, `~/.hermes/*.py`) plus additional skill/archive helper hits. **No remediation this cycle.**
- **Channels affected:** WhatsApp non-functional (`fatal`/`whatsapp_not_paired`, no `creds.json`); **30/56 cron jobs silent delivery** (16 `origin` + 14 `local`); 26 explicitly Telegram-targeted.
- No NEW credential compromise indicator; no unauthorized-access events in current window.

## Findings by Area

### 1. Credential Exposure — **FAIL**

| Item | Status |
|------|--------|
| Backup `.env` copies | **FAIL** — **25 total** (14 `~/.hermes/backups`, 0 `state-snapshots`, 10 `~/hermes-backup`, 1 `~/.openclaw`) — unchanged, persistent debt |
| Plaintext cache `bws_cache.json` | **FAIL** — present (`~/.hermes/cache/bws_cache.json`), plaintext secrets surviving `.env` rotation |
| Live `.env`-reading scripts | **FAIL** — ~29 live operational scripts consult `.env`/`getenv`/`os.environ` (root workspace send/tg/check scripts, `scripts/`, `Vault/2real`, `~/.hermes/*.py`: care_checkin, send_health_check, telegram_create_topic, telegram_direct_send, telegram_post_file); plus skill/archive helper hits (legitimate) |
| Dual `.env` roots | **WARN** — `~/.hermes/.env` (24.9KB) + `AppData/Local/hermes/.env` (552B) both exist — divergence risk |
| `google_token.json` ACL | **PASS** — icacls: SYSTEM/Administrators/User `(I)(F)` only; no Everyone/Users |
| `.secret_cache` | **PASS** — absent |
| AGENTS.md BOM | **PASS** — main `~/.hermes/AGENTS.md` absent; workspace copy UTF-8 CRLF, **no BOM** |

Verdict: **FAIL** (backup copies, plaintext cache, and env-reading scripts all persist unchanged).

### 2. Channel Integrity — **FAIL**

- **Telegram (token)** — ✅ **PASS**: token valid via `getMe`; topics enabled.
- **Gateway process** — ❌ **FAIL / REGRESSION**: no process detected (PID 5596 dead), log stale since 10:15 with `All connection attempts failed` reconnect loop. Last `gateway.start` 08-14 09:44 (Python 3.14.3). `gateway-exit-diag.log` shows 7 `asyncio.run.exception` (all historical June `concurrent_log_handler` ModuleNotFoundError); no fresh crash entries — the instance appears to have exited without a clean recorded shutdown.
- **WhatsApp** — ❌ **FAIL**: `fatal`/`whatsapp_not_paired`; no `creds.json`; requires manual QR re-pair.
- **Cron delivery** — ⚠️ **WARN**: jobs.json (56 total) → 26 explicit `telegram:` topic targets, **16 `origin` + 14 `local` = 30 silent** (unchanged).
- **Topic 20** — ✅ **PASS**: present in `channel_directory.json` (`-1003784520976:20`, "Agent Hermes / topic 20").

### 3. Recent Security Events — **PASS**

- **No `InvalidToken` / token revocation** in current window — live gateway log and rotated `errors.log.1`/`agent.log.1` all clean (0 matches). Current token validated → resolved.
- **Repeated Telegram network/DNS failures** — gateway log shows `All connection attempts failed` / `getaddrinfo failed` polling failures; host-level network/DNS instability (known), not compromise.
- **No unauthorized-access / blocked-user events** in current gateway log window.
- **Nous Portal refresh token rejected** — ⚠️ WARN: `This refresh token was already rejected; please re-authenticate` (`hermes portal`). Auth provider offline, not a compromise.

Verdict: **PASS** (no compromise indicators; failures are network/DNS and process-lifecycle based).

## FAIL Findings

| ID | Severity | Description | Evidence |
|----|----------|-------------|----------|
| 1 | critical | Plaintext credential cache `bws_cache.json` — holds plaintext secrets, survives `.env` rotation | `~/.hermes/cache/bws_cache.json` |
| 2 | high | **25** backup `.env` copies with raw API keys (unchanged, persistent debt) | 14 `backups` + 10 `hermes-backup` + 1 `openclaw` |
| 3 | high | Live `.py` scripts read/consult `.env` directly (~29 operational + skill/archive hits) | root workspace `send_*`/`tg_*`/`check_*`, `~/.hermes/*.py` (5) |
| 4 | medium | **Gateway DOWN (regression)** — no process detected, PID 5596 dead, log stale since 10:15 | `hermes gateway status`, `tasklist`, gateway.log |
| 5 | medium | WhatsApp channel non-functional (unpaired, no creds.json, ~69 days down) | `gateway_state.json` fatal/whatsapp_not_paired |

## WARN Findings

| ID | Description | Evidence |
|----|-------------|----------|
| 1 | Dual `.env` roots — divergence risk | `~/.hermes/.env` (24.9KB) + `AppData/Local/hermes/.env` (552B) |
| 2 | 30/56 cron jobs silent delivery (16 `origin` + 14 `local`) | jobs.json |
| 3 | Nous Portal refresh token rejected — auth offline | `hermes status` |
| 4 | Repeated Telegram DNS/network failures (host-level, recovered) | gateway.log |

## Trend Comparison (vs 2026-08-14 morning)

| Item | 08-14 (06:04) | 08-15 (15:32) | Trend |
|---|---|---|---|
| Telegram token valid | ✅ | ✅ (getMe ok:true) | No Change (good) |
| Gateway online | ✅ PID 18368 | ❌ **DOWN** (PID 5596 dead) | **Worsened (regression)** |
| Topic 20 present | ✅ | ✅ | No Change (good) |
| WhatsApp paired | ❌ | ❌ | No Change (persistent) |
| Backup `.env` copies | 25 | 25 | No Change (persistent) |
| `bws_cache.json` | present | present | No Change (critical) |
| Live `.env` readers | 43 | ~29 operational (scope) | No Change (persistent) |
| Cron silent delivery | 30/56 | 30/56 | No Change |
| InvalidToken in window | none | none | No Change (good) |

## Remediation Priority

1. **CRITICAL** — Delete/purge `bws_cache.json` (plaintext secrets; survives `.env` rotation).
2. **HIGH** — Restart gateway (`hermes gateway run --replace`) — currently DOWN (regression from 08-14).
3. **HIGH** — Delete 25 backup `.env` copies (14+10+1); stop backup growth.
4. **HIGH** — Purge/rewrite `.env`-reading scripts to Hermes-injected env.
5. **MEDIUM** — Re-point 30 silent `origin`/`local` cron jobs to explicit topic targets.
6. **MEDIUM** — Re-pair WhatsApp (manual QR); re-authenticate Nous Portal (`hermes portal`).

## Retention Note

- First audit on 2026-08-15 (no same-day suffix). Prior latest 08-14-morning.
- Rolling window 08-11 … 08-15; 11 files currently in vault path. Retention policy (7 days max, one per day) applied.

## Attachments / Evidence

- `hermes status` (Telegram configured, Nous Portal rejected), direct `getMe` (`ok:true`, @Ogaitchhermesbot).
- `hermes gateway status` → "No gateway process detected"; `gateway_state.json` → pid 5596 (dead), telegram connected (stale), whatsapp fatal.
- `tasklist /FI "PID eq 5596"` → no match; gateway.log mtime 10:15 today, reconnect failures.
- `icacls` google_token.json → SYSTEM/Administrators/User only (PASS).
- `channel_directory.json` — topic 20 present.
- jobs.json: 56 jobs, 26 topic-targeted, 30 silent (16 origin + 14 local).
- Report saved: `C:\Users\User\.hermes\workspace\Vault\System\Assistant\SECURITY_AUDIT_2026-08-15.md`

---

*Masked: all secrets represented by provider-prefix + truncated form. No full tokens echoed.*
