# Security Audit — 14 August 2026

**Date:** 14/08/2026 (00:04 GMT)
**Run by:** internal cron / Hermes Agent
**Overall:** FAIL (persistent credential-leak debt; Telegram healthy, WhatsApp down)
**Report path:** `C:\Users\User\.hermes\workspace\Vault\System\Assistant\SECURITY_AUDIT_2026-08-14.md`

---

## Summary

- **Telegram channel healthy** — bot token **VALID** (direct `getMe` → `ok:true`, `@Ogaitchhermesbot`, topics enabled); gateway alive & connected (gateway_state PID 18460, ESTABLISHED TCP to Telegram API 149.154.166.110:443). Topic 20 ("Memory Review") confirmed present in `channel_directory.json` and chat verified `supergroup` + `is_forum:true` via `getChat`.
- **Persistent credential-leak debt (3+ cycles, escalate):** **25 backup `.env` copies** (14 `~/.hermes/backups` + 10 `~/hermes-backup` + 1 `~/.openclaw`, up from 22), plaintext credential cache **`bws_cache.json`** present, and **34 live workspace `.py` env-readers**. **No remediation this cycle.**
- **Channels affected:** WhatsApp non-functional (unpaired, no `creds.json`); **29/54 cron jobs silent delivery** (`origin`=15, `local`=14); 25 explicitly Telegram-targeted.
- No NEW credential compromise; no `InvalidToken`/`Unauthorized` in the current audit window (historical `InvalidToken` in rotated `agent.log.1`/`errors.log.2` from June 2026 only — token since recovered/rotated).

## Findings by Area

### 1. Credential Exposure — **FAIL**

| Item | Status |
|------|--------|
| Backup `.env` copies | **FAIL** — **25 total** (14 `~/.hermes/backups`, 0 `state-snapshots`, 10 `~/hermes-backup`, 1 `~/.openclaw`) — **INCREASED +3 vs 22**, persistent debt |
| Plaintext cache `bws_cache.json` | **FAIL** — present (`~/.hermes/cache/bws_cache.json`), plaintext secrets surviving `.env` rotation |
| Live `.env`-reading scripts | **FAIL** — 34 live workspace `*.py` consult `.env`/`getenv`/`Path.home` pattern (!incl. `scripts/memory_review_telegram.py`, `morning_checkin.py`, several `send_*.py`) |
| Dual `.env` roots | **WARN** — `~/.hermes/.env` (24KB) + `AppData/Local/hermes/.env` (399B) both exist |
| `google_token.json` ACL | **PASS** — icacls: SYSTEM/Administrators/User `(I)(F)` only; no Everyone/Users |
| `.secret_cache` | **PASS** — absent |
| AGENTS.md BOM | **PASS** — main `~/.hermes/AGENTS.md` absent; workspace copy UTF-8 (CRLF), no BOM |

Verdict: **FAIL** (backup copies increased + plaintext cache + env-reading scripts all persist).

### 2. Channel Integrity — **FAIL**

- **Telegram** — ✅ **PASS**: token valid via `getMe`; gateway PID 18460 live with ESTABLISHED TCP to Telegram; `gateway_state.json` shows telegram `connected` (updated 08-13 20:58); no InvalidToken in live logs; topic 20 verified in `channel_directory.json` + `getChat`.
- **WhatsApp** — ❌ **FAIL**: unpaired. No `creds.json`; `gateway_state.json` shows whatsapp `disconnected`/`needs_attention:true` retrying since 08-13 20:58.
- **Cron delivery** — ⚠️ **WARN**: jobs.json (54 total) → 25 explicit `telegram:` topic targets, **15 `origin` + 14 `local` = 29 silent**.
- **Topic 20** — ✅ **PASS**: present in channel_directory (`-1003784520976:20`, "Memory Review"); 3 jobs target it; chat verified supergroup+forum.

Verdict: **FAIL** (WhatsApp non-functional; 29/54 cron jobs silent).

### 3. Recent Security Events — **PASS**

- **No `InvalidToken` / token revocation in current window** — live gateway.log clean. Historical `InvalidToken` (Jun 08/09 2026, token `8277...ugM8`) only in rotated `errors.log.2` / `agent.log.1` / `gateway.log`; current token validated → resolved/rotated.
- **Repeated Telegram network/DNS failures** — 08-13 gateway.log shows repeated `getaddrindinfo failed` + fallback IP 149.154.166.110 failures, then successful reconnect. Host-level network/DNS instability, not compromise. Adapter recovered each time (`polling restarted after network error`).
- No `Unauthorized` / 401/403 in live gateway log beyond expected.
- **Blocked unauthorized user** — 08-13 19:04 gateway blocked unauthorized user `5146706699` (permission control working as intended).
- **Nous Portal refresh token rejected** — ❌ WARN: `This refresh token was already rejected; please re-authenticate` (`hermes portal`). Auth provider offline, not a compromise.
- `gateway-exit-diag.log` crash signature: 7 `asyncio.run.exception` entries (annotated), **all historical (June, `concurrent_log_handler` ModuleNotFoundError, Py3.14)**. Current gateway running clean — no active crash loop.
- Cron execution DB shows 725 failed / 215 completed / 60 unknown historically — dominated by config-drift model pinning and DNS getaddrinfo; not credential events.

Verdict: **PASS** (no unauthorized access / compromise indicators in window; network instability is DNS-based).

## FAIL Findings

| ID | Severity | Description | Evidence |
|----|----------|-------------|----------|
| 1 | critical | Plaintext credential cache `bws_cache.json` — holds plaintext secrets, survives `.env` rotation | `~/.hermes/cache/bws_cache.json` |
| 2 | high | **25** backup `.env` copies with raw API keys (**+3 vs prior, worsening**) | 14 `backups` + 10 `hermes-backup` + 1 `openclaw` |
| 3 | high | Live `.py` scripts read/consult `.env` directly (34 by targeted scope) | `workspace/*.py`, `~/.hermes/*.py` incl. `send_*`, `scripts/*` |
| 4 | medium | WhatsApp channel non-functional (unpaired, no creds.json) | `gateway_state.json` disconnected; no `creds.json` |

## WARN Findings

| ID | Description | Evidence |
|----|-------------|----------|
| 1 | Backup `.env` count increased 22 → 25 (regression, +3) | find across 4 trees |
| 2 | Dual `.env` roots — divergence risk | `~/.hermes/.env` + `AppData/Local/hermes/.env` |
| 3 | 29/54 cron jobs silent delivery (15 `origin` + 14 `local`) | `AppData/Local/hermes/cron/jobs.json` |
| 4 | Nous Portal refresh token rejected — auth offline | `hermes status` / `hermes doctor` |
| 5 | Repeated Telegram DNS/network failures (host-level, recovered) | live `gateway.log` 08-13 |

## Trend Comparison (vs 2026-08-13-evening)

| Item | 08-13 (16:35) | 08-14 (00:04) | Trend |
|---|---|---|---|
| Telegram token valid | ✅ | ✅ | No Change (good) |
| Gateway/Telegram online | ✅ PID 5060 | ✅ PID 18460 | No Change (good) |
| Topic 20 present | ✅ | ✅ (verified getChat supergroup+forum) | No Change (good) |
| WhatsApp paired | ❌ | ❌ | No Change (persistent) |
| Backup `.env` copies | 22 | **25** | **Worsened (+3)** |
| `bws_cache.json` | present | present | No Change (critical) |
| Live `.env` readers | ~41 | 34 (scope-dep) | No Change (persistent) |
| Cron silent delivery | 29/54 | 29/54 | No Change (persistent) |

## Remediation Priority

1. **CRITICAL** — Delete/purge `bws_cache.json` (plaintext secrets; survives `.env` rotation).
2. **HIGH** — Delete 25 backup `.env` copies (14+10+1); stop the backup stop growing.
3. **HIGH** — Purge/rewrite `.env`-reading scripts to Hermes-injected env.
4. **MEDIUM** — Re-point 29 silent `origin`/`local` cron jobs to explicit topic targets.
5. **MEDIUM** — Re-pair WhatsApp (manual QR); re-authenticate Nous Portal (`hermes portal`).

## Retention Note

- First run of 08-14. Rolling window contains 08-11 … 08-13-evening files; all within 7-day window. No deletions needed.
- 08-13 files: `-evening`, `-afternoon`, and base preserved as unique same-day runs.

## Attachments / Evidence

- `hermes status` (gateway running PID 18460, Telegram configured, Nous Portal rejected), direct `getMe` (`ok:true`, @Ogaitchhermesbot).
- `gateway_state.json` — telegram connected, whatsapp disconnected; PID 18460.
- Live `gateway.log` (08-13 DNS/network failures recovered; unauthorized user 5146706699 blocked).
- `icacls` google_token.json → SYSTEM/Administrators/User only (PASS).
- `channel_directory.json` + `getChat` (−1003784520976 supergroup, is_forum true; topic 20 present).
- `jobs.json`: 54 jobs, 25 topic-targeted, 29 silent (15 origin + 14 local).
- Report saved: `C:\Users\User\.hermes\workspace\Vault\System\Assistant\SECURITY_AUDIT_2026-08-14.md`

---

*Masked: all secrets represented by provider-prefix + truncated form. No full tokens echoed.*