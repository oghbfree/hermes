# Security Audit — 15 August 2026 (Evening re-run)

**Date:** 15/08/2026 (18:06 GMT)
**Run by:** internal cron / Hermes Agent
**Overall:** FAIL (persistent credential-leak debt; **gateway still DOWN — regression persists**; Telegram token valid; WhatsApp down; 30/56 cron jobs silent)
**Report path:** `C:\Users\User\.hermes\workspace\Vault\System\Assistant\SECURITY_AUDIT_2026-08-15-evening.md`

---

## Summary

- **Telegram bot token VALID** — direct `getMe` → `ok:true`, `@Ogaitchhermesbot`, `has_topics_enabled`. `getChat` confirms `-1003784520976` is a **supergroup with `is_forum:true`**; **Topic 20 ("Memory Review") confirmed present** in `channel_directory.json` (`-1003784520976:20`). No `InvalidToken`/`Unauthorized` in current window.
- **Gateway STILL DOWN — REGRESSION persists ⚠️** — `hermes gateway status` → "No gateway process detected"; `gateway_state.json` PID **5596 is dead** (stale, no live process). `gateway.log` last written **08-14 09:44** (~33h stale), ending in "Connected to Telegram (polling mode)" then no further activity — the instance appears to have **exited without a clean recorded shutdown**. Compare prior audit 08-14 06:04 (gateway alive PID 18368). No live gateway process in tasklist (only H Hermes.exe desktop + python PIDs, unrelated).
- **Persistent credential-leak debt (3+ cycles, escalate):** **25 backup `.env` copies** (14 `~/.hermes/backups` + 10 `~/hermes-backup` + 1 `~/.openclaw`, unchanged), plaintext cache **`bws_cache.json`** present (1224B, 08-14), and ~33 live `.py` env-readers (4 `~/.hermes/*.py` + ~28 workspace + 3 vault mum-health scripts). **No remediation this cycle.**
- **Channels affected:** WhatsApp non-functional (`fatal`/`whatsapp_not_paired`, no `creds.json`, ~70 days); **30/56 cron jobs silent delivery** (16 `origin` + 14 `local`); 26 explicitly Telegram-targeted.
- No NEW credential compromise indicator; permission control blocked unauthorized user `5146706699` (08-13, working as intended).

## Findings by Area

### 1. Credential Exposure — **FAIL**

| Item | Status |
|------|--------|
| Backup `.env` copies | **FAIL** — **25 total** (14 `~/.hermes/backups`, 0 `state-snapshots`, 10 `~/hermes-backup`, 1 `~/.openclaw`) — unchanged, persistent debt |
| Plaintext cache `bws_cache.json` | **FAIL** — present (`~/.hermes/cache/bws_cache.json`, 1224B, 08-14), plaintext secrets surviving `.env` rotation |
| Live `.env`-reading scripts | **FAIL** — ~33 live scripts consult `.env`/`getenv`/`os.environ` (4 `~/.hermes/*.py`: send_health_check, telegram_create_topic, telegram_direct_send, telegram_post_file; ~28 workspace: check_*/send_*/tg_*/tmp_*; 3 vault mum-health evening/morning check scripts) |
| Dual `.env` roots | **WARN** — `~/.hermes/.env` (24.9KB) + `AppData/Local/hermes/.env` (552B) — divergence risk |
| `google_token.json` ACL | **PASS** — icacls: SYSTEM/Administrators/User `(I)(F)` only; no Everyone/Users |
| `.secret_cache` | **PASS** — absent |
| AGENTS.md BOM | **PASS** — main `~/.hermes/AGENTS.md` absent; workspace copy no BOM |

Verdict: **FAIL** (backup copies, plaintext cache, env-readers all persist unchanged).

### 2. Channel Integrity — **FAIL**

- **Telegram (token)** — ✅ **PASS**: token valid via `getMe`; supergroup + forum confirmed; topics enabled.
- **Gateway process** — ❌ **FAIL / REGRESSION**: no process detected; PID 5596 dead; log stale ~33h (last 08-14 09:44), no clean shutdown recorded. Same conclusion as 08-15 morning run.
- **WhatsApp** — ❌ **FAIL**: `fatal`/`whatsapp_not_paired`; no `creds.json`; requires manual QR re-pair.
- **Cron delivery** — ⚠️ **WARN**: jobs.json (56 total) → 26 explicit `telegram:` topic targets, **16 `origin` + 14 `local` = 30 silent** (unchanged).
- **Topic 20** — ✅ **PASS**: present in `channel_directory.json` (`-1003784520976:20`, "Agent Hermes / topic 20").

### 3. Recent Security Events — **PASS**

- **No `InvalidToken` / token revocation** in current window — live gateway.log/errors.log clean of telegram auth rejection. Historical `InvalidToken` only in rotated `agent.log.1` / `errors.log.2` (older, resolved).
- **Unauthorized user blocked (08-13 19:04)** — `[Telegram] Blocked unauthorized user 5146706699` — permission control functioning.
- Transient **OpenRouter 401 "Missing Authentication header"** (08-04) — credential pool marked key exhausted, auto-rotated; not a compromise (older, pre-window, resolved).
- **Nous Portal refresh token rejected** — ⚠️ WARN: `This refresh token was already rejected; please re-authenticate` (`hermes portal`). Auth provider offline, not a compromise.
- `gateway-exit-diag.log` — 7 `asyncio.run.exception` entries, all historical (June `concurrent_log_handler` ModuleNotFoundError, Py3.14); no fresh crash entries — current instance exited without a recorded traceback.

Verdict: **PASS** (no compromise indicators; gateway outage is a process-lifecycle regression, network failures DNS-based).

## FAIL Findings

| ID | Severity | Description | Evidence |
|----|----------|-------------|----------|
| 1 | critical | Plaintext credential cache `bws_cache.json` — holds plaintext secrets, survives `.env` rotation | `~/.hermes/cache/bws_cache.json` |
| 2 | high | **25** backup `.env` copies with raw API keys (unchanged, persistent debt) | 14 `backups` + 10 `hermes-backup` + 1 `openclaw` |
| 3 | high | Live `.py` scripts read/consult `.env` directly (~33 live) | `~/.hermes/*.py` (4), `workspace/*.py` (~28), vault mum-health (3) |
| 4 | medium | **Gateway DOWN (regression persists)** — no process; PID 5596 dead; log stale ~33h (since 08-14 09:44) | `hermes gateway status`, `gateway_state.json`, tasklist |
| 5 | medium | WhatsApp channel non-functional (unpaired, no creds.json, ~70 days) | `gateway_state.json` fatal/whatsapp_not_paired |

## WARN Findings

| ID | Description | Evidence |
|----|-------------|----------|
| 1 | Dual `.env` roots — divergence risk | `~/.hermes/.env` (24.9KB) + `AppData/Local/hermes/.env` (552B) |
| 2 | 30/56 cron jobs silent delivery (16 `origin` + 14 `local`) | jobs.json |
| 3 | Nous Portal refresh token rejected — auth offline | `hermes status` |
| 4 | Gateway outage is a functional regression affecting all cron delivery (only direct Bot-API delivery works) | gateway.log stale, no process |

## Trend Comparison (vs 2026-08-15 morning, 15:32)

| Item | 08-15 (15:32) | 08-15 (18:06) | Trend |
|---|---|---|---|
| Telegram token valid | ✅ (getMe ok:true) | ✅ (getMe ok:true + forum verified) | No Change (good) |
| Gateway online | ❌ DOWN (PID 5596 dead) | ❌ DOWN (no process) | No Change (regression persists) |
| Topic 20 present | ✅ | ✅ (supergroup+forum) | No Change (good) |
| WhatsApp paired | ❌ | ❌ | No Change (persistent ~70d) |
| Backup `.env` copies | 25 | 25 | No Change (persistent) |
| `bws_cache.json` | present | present | No Change (critical) |
| Live `.env` readers | ~29 | ~33 | No Change (persistent) |
| Cron silent delivery | 30/56 | 30/56 | No Change |
| InvalidToken in window | none | none | No Change (good) |

## Remediation Priority

1. **CRITICAL** — Delete/purge `bws_cache.json` (plaintext secrets; survives `.env` rotation).
2. **HIGH** — Restart gateway (`hermes gateway run --replace`) — DOWN for ~33h (regression from 08-14). Note: `gateway start/restart` is blocked by AGENTS.md rules → alert H via Telegram #urgent rather than auto-restart.
3. **HIGH** — Delete 25 backup `.env` copies (14+10+1); stop backup growth.
4. **HIGH** — Purge/rewrite .env-reading scripts to Hermes-injected env.
5. **MEDIUM** — Re-point 30 silent `origin`/`local` cron jobs to explicit topic targets.
6. **MEDIUM** — Re-pair WhatsApp (manual QR); re-authenticate Nous Portal (`hermes portal`).

## Retention Note

- Same-day re-run → `-evening` suffix used (morning 15:32 run = base `-15.md`).
- 5 files in vault path (08-11 … 08-15), all within 7-day window. No deletions required.

## Attachments / Evidence

- `hermes status` (Tel configured, Nous Portal rejected), direct `getMe` (`ok:true`, @Ogaitchhermesbot, topics enabled), `getChat` (supergroup, is_forum:true).
- `hermes gateway status` → "No gateway process detected"; `gateway_state.json` → pid 5596 (dead), telegram connected (stale), whatsapp fatal.
- `icacls` google_token.json → SYSTEM/Administrators/User only (PASS).
- `channel_directory.json` — topic 20 present.
- jobs.json: 56 jobs, 26 topic-targeted, 30 silent (16 origin + 14 local).
- Report saved: `C:\Users\User\.hermes\workspace\Vault\System\Assistant\SECURITY_AUDIT_2026-08-15-evening.md`

---

*Masked: all secrets represented by provider-prefix + truncated form. No full tokens echoed.*