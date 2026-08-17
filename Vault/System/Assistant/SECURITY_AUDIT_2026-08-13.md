# Security Audit — 13 August 2026

**Date:** 13/08/2026
**Run by:** internal cron / Hermes Agent
**Overall:** FAIL (persistent credential-leak debt; channels: Telegram OK, WhatsApp down)
**Report path:** `C:\Users\User\.hermes\workspace\Vault\System\Assistant\SECURITY_AUDIT_2026-08-13.md`

---

## Summary

- **Telegram channel healthy** — bot token **VALID** (direct `getMe` → `ok:true`, bot `@Ogaitchhermesbot`); gateway alive (PID 13760, ESTABLISHED TCP to `149.154.166.110:443`), live logs fresh 00:05 today. No credential compromise detected.
- **Persistent credential-leak debt (3+ cycles, escalate):** **22 backup `.env` copies** (+2 vs 08-12), plaintext credential cache **`bws_cache.json`** (15 live secrets, unchanged), and **46 live scripts** (41 workspace + 5 `~/.hermes/`) reading `.env` directly — **increasing**.
- **Channels affected:** WhatsApp permanently unpaired (reconnect attempt **509**, up from 442); **29/49** cron jobs silent delivery (`origin`=15, `local`=14); **32 jobs in error** `last_status` (per jobs.json, undercharged against 21 ok).
- No NEW credential compromise; no `InvalidToken`/`Unauthorized` in the current audit window.

## Findings by Area

### 1. Credential Exposure — **FAIL**

| Item | Status |
|------|--------|
| Backup `.env` copies | **FAIL** — **22 total** (11 `~/.hermes/backups`, 0 `state-snapshots`, 10 `~/hermes-backup`, 1 `~/.openclaw`) — **increasing** (+2 vs 08-12) |
| Plaintext cache `bws_cache.json` | **FAIL** — exists (1224B, 04/08), **15 secret keys** (Firecrawl, OpenRouter, Telegram, FAL, xAI, Google, GOG, Groq, Brave, Whisper, Tavily, GitHub PAT, Apify) — none printed |
| Workspace/root `.env` readers | **FAIL** — **41** workspace `.py` + **5** `~/.hermes/*.py` (`care_checkin.py`, `send_health_check.py`, `telegram_create_topic.py`, `telegram_direct_send.py`, `telegram_post_file.py`) — **increasing** |
| Dual `.env` roots | **WARN** — `~/.hermes/.env` + `AppData/Local/hermes/.env` (399B) both exist |
| `google_token.json` ACL | **PASS** — only SYSTEM/Administrators/User `(I)(F)`, no Everyone/Users |
| `.secret_cache` | **PASS** — absent |
| AGENTS.md BOM | **PASS** — main `~/.hermes/AGENTS.md` absent; workspace copy UTF-8 (CRLF), no BOM |

Verdict: **FAIL** (backup copies + plaintext cache + env-reading scripts all persist/grow).

### 2. Channel Integrity — **FAIL**

- **Telegram** — ✅ **PASS**: token valid via `getMe`, PID 13760 live, ESTABLISHED TCP to Telegram. No InvalidToken in live logs.
- **WhatsApp** — ❌ **FAIL**: unpaired. Reconnect loop at **attempt 509** (08-13 00:05), no `creds.json`. Bridge finds the target but never completes pairing.
- **Cron delivery** — ⚠️ **WARN**: jobs.json (54 total) → 15 `origin` (silent), 14 `local` (silent), 25 explicit `telegram:` topic targets. **29/49 targetable jobs never reach a user.** 32 jobs `last_status=error` vs 21 ok — delivery contention.
- **Topic 20** — ✅ **PASS**: exists in channel_directory (`-1003784520976:20`, thread_id 20).

Verdict: **FAIL** (WhatsApp non-functional; 29/49 cron jobs silent; high error count).

### 3. Recent Security Events — **PASS**

- **No `InvalidToken` / token revocation in current window** — live gateway.log & errors.log show 0. No `Unauthorized` / HTTP 401/403.
- Nous Portal refresh token rejected — **WARN**: `This refresh token was already rejected; please re-authenticate` (`hermes portal`). Auth provider offline, not a compromise.
- Transient host-level network: Telegram primary DNS failure (`Errno 11001 getaddrinfo failed` 08-12 20:52, recovered via fallback IP) + OpenRouter `APIConnectionError`/HTTP 10054 forced-close (08-12 21:28) — channel-integrity, not attack.
- No breach / unusual-access indicators.

Verdict: **PASS** (no unauthorized access / compromise indicators).

## FAIL Findings

| ID | Severity | Description | Evidence |
|----|----------|-------------|----------|
| 1 | critical | Plaintext credential cache `bws_cache.json` — 15 live secrets, survives `.env` rotation | `~/.hermes/cache/bws_cache.json` |
| 2 | high | **22** backup `.env` copies with raw API keys (+2 vs 08-12) | 11 `backups` + 10 `hermes-backup` + 1 `openclaw` |
| 3 | high | **46** live `.py` scripts read `.env` directly (41 workspace + 5 `~/.hermes/`) | `send_*.py`, `check_*.py`, `tg_*.py`, `telegram_*.py`, `care_checkin.py` |
| 4 | medium | WhatsApp channel non-functional (unpaired, reconnect loop attempt 509) | live `gateway.log` |

## WARN Findings

| ID | Description | Evidence |
|----|-------------|----------|
| 1 | Dual `.env` roots — divergence risk | `~/.hermes/.env` + `AppData/Local/hermes/.env` |
| 2 | 29/49 cron jobs silent delivery (15 `origin` + 14 `local`) | `AppData/Local/hermes/cron/jobs.json` |
| 3 | 32 cron jobs `last_status=error` (per jobs.json) vs 21 ok | `jobs.json` |
| 4 | Nous Portal refresh token rejected — auth offline | `hermes status` |
| 5 | Transient host network: Telegram DNS fail + OpenRouter connection reset (08-12) | `errors.log` |

## Trend Comparison (vs 2026-08-12)

| Item | 08-12 | 08-13 | Trend |
|---|---|---|---|
| Telegram token valid | ✅ | ✅ | No Change (good) |
| Gateway/Telegram online | ✅ | ✅ | No Change (good) |
| Backup `.env` copies | 20 | **22** | **Worsening** (persistent debt) |
| `bws_cache.json` secrets | 15 | 15 | No Change (critical debt) |
| Live `.env` readers | ~25–38 | **46** | **Worsening** (persistent debt) |
| WhatsApp functional | ❌ | ❌ | No Change (attempt 442→509) |
| Cron silent delivery | ~25/40 | 29/49 | No Change (persistent) |
| Jobs in error | — | 32 | New observation (delivery contention) |

## Remediation Priority

1. **CRITICAL —** Delete/purge `bws_cache.json` (15 plaintext secrets; survives `.env` rotation).
2. **HIGH —** Delete 22 backup `.env` copies (11+10+1).
3. **HIGH —** Purge/rewrite 46 `.env`-reading scripts to Hermes-injected env.
4. **MEDIUM —** Re-point 29 silent `origin`/`local` cron jobs to explicit topic targets; investigate 32 error-state jobs.
5. **MEDIUM —** Re-pair WhatsApp (manual QR); re-authenticate Nous Portal.

## Retention Note

- Report dir holds 08-11, 08-11-afternoon, 08-12, 08-12-afternoon, 08-12-evening (all within 7-day window). No deletions needed. No same-day dupes (first run today).
- AppData `memories/security/` mirror absent — no migration needed.

## Attachments / Evidence

- CLI outputs: `hermes status --all` (gateway alive PID 13760, Telegram configured), direct `getMe` (`ok:true`, @Ogaitchhermesbot).
- Log files scanned: `AppData/Local/hermes/logs/gateway.log` (fresh 00:05 08-13), `errors.log` (fresh 00:06), `gateway-exit-diag.log` (7 historical crash entries).
- Config scanned: `AppData/Local/hermes/cron/jobs.json` (54 jobs), `channel_directory.json` (topic 20 present), cache files, back-up trees.
- Report saved: `C:\Users\User\.hermes\workspace\Vault\System\Assistant\SECURITY_AUDIT_2026-08-13.md`

---

*Masked: all secrets represented by provider-prefix + truncated form. No full tokens echoed.*