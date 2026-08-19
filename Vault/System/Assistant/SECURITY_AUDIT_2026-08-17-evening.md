# Security Audit — 17 August 2026 (evening re-run)

**Date:** 17/08/2026 (19:18 GMT)
**Run by:** internal cron / Hermes Agent (default profile)
**Overall:** **FAIL** (persistent credential-leak debt; backup `.env` copies; WhatsApp non-functional). Telegram token **VALID**, gateway **UP**, delivery enabled. Consistent with the 12:05 same-day run — no new compromise.

**Report path:** `C:\Users\User\.hermes\workspace\Vault\System\Assistant\SECURITY_AUDIT_2026-08-17-evening.md`

> **Same-day re-run (evening).** Re-verifies the 06:11 and 12:05 runs with live checks: gateway process **PID 24152** alive (`tasklist`), **ESTABLISHED TCP** to Telegram `149.154.166.110:443` (2 conns), `hermes status` → Gateway `✓ running` PID 24152. Direct token `getMe` → `{"ok":true}`, `@Ogaitchhermesbot`. Gateway genuinely UP; token genuinely valid.

---

## Summary

- **Telegram bot token VALID** — direct `getMe` → `ok:true`, `@Ogaitchhermesbot`. Historical `InvalidToken` only (2026-06-09, resolved).
- **Gateway UP (confirmed)** — PID 24152 alive, live ESTABLISHED TCP to Telegram. Stale `gateway.log` (last write 08-14 09:44) is from a prior instance; the live PID writes differently.
- **Credential exposure PERSISTS** — **30 backup `.env` copies** (19 `~/.hermes/backups` + 10 `~/hermes-backup` + 1 `~/.openclaw`). Plaintext cache **`bws_cache.json`** present (1224B, 08-14, 15 service keys). **~25 live `.py` env-readers** (4 `~/.hermes/*.py` + 21 `workspace/*.py`).
- **Dual `.env` roots** — `~/.hermes/.env` + `AppData/Local/hermes/.env` both present.
- **Channels affected:** WhatsApp non-functional (unpaired, no `creds.json`, ~70+ days); **30/56 cron jobs silent delivery** (16 `origin` + 14 `local`); 3 jobs target topic 20.
- **No NEW credential compromise indicator.** Unauthorized user `5146706699` blocked 08-13 (permission control working).

## Findings by Area

### 1. Credential Exposure — **FAIL**

| Item | Status |
|------|--------|
| Backup `.env` copies | **FAIL** — **30 total** (19 backups, 0 state-snapshots, 10 hermes-backup, 1 openclaw) — unchanged |
| Plaintext cache `bws_cache.json` | **FAIL** — present (1224B, 08-14), 15 plaintext service keys (incl. GitHub PAT) |
| Live `.env`-reading scripts | **FAIL** — ~25 total: 4 `~/.hermes/*.py` (send_health_check, telegram_create_topic, telegram_direct_send, telegram_post_file) + 21 `workspace/*.py` (check_*, send_*, tg_*, tmp_*) |
| Dual `.env` roots | **WARN** — `~/.hermes/.env` + `AppData/Local/hermes/.env` divergence risk |
| `google_token.json` ACL | **PASS** — icacls: SYSTEM/Administrators/User `(I)(F)` only; no Everyone/Users |
| `.secret_cache` | **PASS** — absent |
| AGENTS.md BOM | **PASS** — main `~/.hermes/AGENTS.md` absent; workspace copy clean (UTF-8, no BOM) |

Verdict: **FAIL** (credential-leak debt persists, unchanged).

### 2. Channel Integrity — **FAIL** (partial)

- **Telegram (token)** — ✅ **PASS**: valid via `getMe`; Topic 20 ("Memory Review") present in `channel_directory.json`.
- **Gateway process** — ✅ **PASS (UP)**: PID 24152 alive, ESTABLISHED TCP to Telegram, `hermes status` running.
- **WhatsApp** — ❌ **FAIL**: no `creds.json`; manual QR re-pair required (~70+ days).
- **Cron delivery** — ⚠️ **WARN**: jobs.json (56 total) → 26 explicit `telegram:` topic targets (23 other + 3 topic20), **16 `origin` + 14 `local` = 30 silent** (unchanged).

### 3. Recent Security Events — **PASS**

- No `InvalidToken` / token revocation in current window; historical only (June, resolved).
- **Unauthorized user blocked (08-13)** — `[Telegram] Blocked unauthorized user 5146706699` — permission control functioning.
- No multi-provider simultaneous failure; no breach markers.
- **Nous Portal refresh token rejected** — ⚠️ **WARN**: `This refresh token was already rejected` — auth provider offline, not a compromise.
- **SQLite WAL-reset corruption warning** — ⚠️ **WARN**: SQLite 3.50.4 linked; recommend `hermes update` for 3.51.3+.

## FAIL Findings

| ID | Severity | Description | Evidence |
|----|----------|-------------|----------|
| 1 | critical | Plaintext credential cache `bws_cache.json` (15 service keys, incl. GitHub PAT) | `~/.hermes/cache/bws_cache.json` |
| 2 | high | **30** backup `.env` copies with raw API keys (unchanged, persistent) | 19 backups + 10 hermes-backup + 1 openclaw |
| 3 | high | Live `.py` scripts read `.env` directly (~25 total) | `~/.hermes/*.py` (4), workspace `send_*/check_*` (21) |
| 4 | medium | WhatsApp channel non-functional (unpaired, ~70+ days) | no `creds.json` |

## WARN Findings

| ID | Description |
|----|-------------|
| 1 | Dual `.env` roots — divergence risk |
| 2 | 30/56 cron jobs silent delivery (16 `origin` + 14 `local`) |
| 3 | Nous Portal refresh token rejected — auth offline |
| 4 | SQLite 3.50.4 WAL-reset corruption bug — upgrade to 3.51.3+ |

## Trend Comparison (vs 2026-08-17 12:05 same-day)

| Item | 12:05 run | This run (19:18) | Trend |
|---|---|---|---|
| Telegram token valid | ✅ | ✅ | No Change (good) |
| Gateway online | ✅ UP (PID 24152) | ✅ UP (PID 24152) | No Change (good) |
| WhatsApp paired | ❌ | ❌ | No Change (~70d) |
| Backup `.env` copies | 30 | **30** | No Change |
| `bws_cache.json` | present | present | No Change (critical) |
| Live `.env` readers | ~30 | ~25 | No Change |
| Cron silent delivery | 30/56 | 30/56 | No Change |
| InvalidToken in window | none | none | No Change (good) |

## Remediation Priority

1. **CRITICAL** — Delete/purge `bws_cache.json` (plaintext secrets; survives `.env` rotation).
2. **HIGH** — Delete 30 backup `.env` copies; stop backup growth.
3. **HIGH** — Purge/rewrite `.env`-reading scripts to Hermes-injected env.
4. **MEDIUM** — Upgrade SQLite to 3.51.3+ (`hermes update`).
5. **MEDIUM** — Re-pair WhatsApp (manual QR); re-authenticate Nous Portal.
6. **MEDIUM** — Re-point 30 silent `origin`/`local` cron jobs to explicit topic targets.

## Retention Note

- Same-day re-run → `-evening` suffix (06:11 base + 12:05 afternoon + this 19:18 evening = 3 files today; keep latest/evening only).
- Vault path now: 08-11, 08-12, 08-13, 08-14, 08-15, 08-15-evening, 08-17-afternoon, 08-17-evening (8 files). Same-day dedup applies — retain 08-17-evening as today's canonical.

## Attachments / Evidence

- `hermes status` → Gateway `✓ running` PID 24152; Nous Portal rejected.
- Direct `getMe` → `ok:true`, `@Ogaitchhermesbot`.
- `tasklist`/`netstat` → PID 24152 alive; 2 ESTABLISHED TCP to Telegram `149.154.166.110:443`.
- `icacls` google_token.json → SYSTEM/Administrators/User only (PASS).
- jobs.json (live): 56 jobs, 26 topic-targeted, 30 silent (16 origin + 14 local), 3 topic20.
- `bws_cache.json` — 15 plaintext secret keys.
- InvlaidToken events: historical 2026-06-09 only.

---

*Masked: all secrets represented by provider-prefix + truncated form. No full tokens echoed.*
