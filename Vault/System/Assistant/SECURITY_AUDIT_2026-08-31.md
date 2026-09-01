# Security Audit — 31 August 2026

**Date:** 31/08/2026
**Run by:** internal cron / Hermes Agent (default profile)
**Overall:** **STABLE** — live gateway RUNNING (AppData root, PID 868, Python 3.11), Telegram token VALID (getMe `ok:true`, `Ogaitchhermesbot`), WhatsApp paired, logs fresh (11:18 today), Topic 20 confirmed supergroup forum. No compromise events. **Persisting debt:** live `.env`-reader scripts, dual-root credential divergence (home-root token now confirmed revoked via getMe 404), 25/55 cron jobs silent delivery, legacy google_token backup copies (9), Nous Portal expiry imminent.

**Report path:** `C:\Users\User\.hermes\workspace\Vault\System\Assistant\SECURITY_AUDIT_2026-08-31.md`
**Telegram delivery target:** Topic 20 (`telegram:-1003784520976:20`), verified `type: supergroup`, `is_forum: true` ("Agent Hermes").

---

## Summary

- **Channel health GREEN** — Gateway PID **868** running (gateway_state `running`, logged start 08-31 02:55, `replace=true`), Telegram `connected` (02:56), WhatsApp `connected`/paired (`platforms/whatsapp/session/creds.json` present). `gateway.log` fresh at **11:18 today**.
- **Runtime Telegram token VALID** — direct `getMe` against the AppData-root token returns `{"ok":true,"result":{"username":"Ogaitchhermesbot",...}}`. Topic 20 `getChat` returns `type: supergroup, is_forum: true`.
- **Home-root token (dormant root) REVOKED** — `~/.hermes/.env` token returns HTTP 404 on `getMe`; its `gateway_state.json` is stale from 08-22 (`startup_failed`, token rejected). This is the known dual-root divergence: scripts referencing home-root `.env` operate against a dead token. WARN (not the active path; no delivery impact taken there).
- **No InvalidToken/401 in active (AppData) current logs** — only reconnect churn from host-level DNS/IPv4 flakiness (08-26, 08-27, 08-29 `All connection attempts failed`), all self-recovered.
- **Credential caches CLEAN** — `bws_cache.json` / `.secret_cache` / provider caches absent.
- **Backup `.env` copies** — 0 in `~/.hermes/backups`, `~/.hermes/state-snapshots`, `~/hermes-backup`, `~/.openclaw`. PASS (sustained).
- **Legacy google_token copies** — 9 in `~/hermes-backup` + 2 in `~/.hermes/backups` (unchanged vs 28/08). WARN.
- **`google_token.json` ACL correct** (home root) — SYSTEM / Administrators / User `(I)(F)` only, no Everyone/Users group. PASS.
- **AGENTS.md** — main `~/.hermes/AGENTS.md` absent; workspace copy UTF-8 (no BOM). PASS.
- **Live `.env`-reader scripts (FAIL debt)** — workspace/scripts `send_ghana_report.py`, `memory_review_telegram.py`, `ghana_telegram_report.py`; Vault family health scripts; root `telegram_direct_send.py`, `telegram_create_topic.py`, `telegram_post_file.py`, `send_health_check.py`; AppData `_tg_send.py`. All parse `Path.home()/.hermes/.env` / AppData `.env` directly.
- **Cron delivery** — **55 jobs; 25 silent** (13 `local` + 12 `origin`), 30 explicit `telegram:` targets (Topic 20 present).
- **Nous Portal** — access/key expiry **2026-08-31 12:08:57** (~50 min from audit time) — WARN; refresh enabled.

## Findings by Area

### 1. Credential Exposure — PARTIAL (caches clean, backups clean; FAIL debt persists)

| Item | Status |
|------|--------|
| `bws_cache.json` / `.secret_cache` | **PASS** — absent |
| Backup `.env` (all trees) | **PASS** — 0 |
| `google_token.json` ACL (home root) | **PASS** — icacls SYSTEM/Administrators/User `(I)(F)` only |
| AGENTS.md BOM | **PASS** — workspace UTF-8 no BOM; main absent |
| Active runtime token (AppData root) | **PASS/VALID** — getMe `ok:true` (Ogaitchhermesbot) |
| Home-root `~/.hermes/.env` token | **WARN** — revoked (getMe HTTP 404); dormant/divergent root |
| Legacy google_token copies | **WARN** — 9 in `~/hermes-backup` + 2 in `~/.hermes/backups` (unchanged) |
| Live `.env`-reader scripts | **FAIL (PERSISTS)** — workspace/scripts + Vault family + root send_*.py + AppData `_tg_send.py` |

### 2. Channel Integrity — GOOD (gateway stable)

- **Telegram (gateway)** — ✅ PASS: PID 868 running, `connected`, logs fresh (11:18 today).
- **Telegram (token, active)** — ✅ PASS: getMe `ok:true`; topic 20 `getChat` supergroup+forum.
- **WhatsApp** — ✅ PASS: creds.json present, state `connected`.
- **Cron delivery** — ⚠️ WARN: 55 jobs → 25 silent (13 `local` + 12 `origin`), 30 telegram-targeted.

### 3. Recent Security Events — NO COMPROMISE (one WARN)

- **No** new `InvalidToken` / `Unauthorized` / `Revoked` / `401` in active (AppData) logs this window.
- Recurrent Telegram reconnect cycles (08-26/27/29, `All connection attempts failed`, IPv4 path failures) = host-level DNS/network flakiness, self-recovered by sticky-IPv4 fallback. Transient, not credential.
- **Home-root token revoked** confirms the dormant `~/.hermes/.env` is dead (getMe 404) — distinct from the active AppData token which is healthy. Divergence risk, not an active compromise.
- Nous Portal token expiry ~12:08 today (~50 min) — refresh enabled, assess at next cycle.

## FAIL Findings

| ID | Severity | Description | Evidence |
|----|----------|-------------|----------|
| 1 | high | **Live `.py` scripts read `.env` directly** (workspace/scripts, Vault family health, root send_*.py, AppData `_tg_send.py`) — leak tokens to process table/history/logs | grep `env_path`/`open(.env)` across live trees |
| 2 | high | **Credential divergence: dual `.env` roots** — AppData holds the VALID token; home-root `~/.hermes/.env` is REVOKED (getMe 404) and referenced by task scripts | status + getMe on both tokens |
| 3 | medium | **25/55 cron jobs silent delivery** (13 `local` + 12 `origin`) | jobs.json delivery audit |

## WARN Findings

| ID | Description |
|----|-------------|
| 1 | 9 legacy `google_token.json` + 2 in `~/.hermes/backups` not purged (unchanged) |
| 2 | Nous Portal token expiry ~12:08 today (≈50 min) — verify auto-refresh succeeds |
| 3 | Host-level Telegram DNS/IPv4 flakiness recurring (08-26/27/29) — self-recovering but disruptive |
| 4 | Home-root `.env` token revoked — dormant root should be consolidated or retired |

## Trend (vs 28/08 audit)

| Item | 28/08 | This run (31/08) | Trend |
|---|---|---|---|
| Gateway | ✅ running (PID 19936) | ✅ running (PID 868) | Stable |
| Telegram token valid (active) | ✅ (polling gen 5) | ✅ (getMe ok) | Stable |
| WhatsApp | ✅ paired | ✅ paired | Stable |
| `bws_cache` | absent | absent | Good (sustained) |
| Backup `.env` (all trees) | 0 | 0 | Good (sustained) |
| Legacy google_token copies | 9 | 9 + 2 internal | Slightly degraded (internal copies reappeared) |
| Live `.env` readers | present | present (+AppData `_tg_send.py`) | No Change (debt) |
| Home-root token state | "truncated/corrupt" | **revoked (getMe 404)** | Deteriorated (dormant root dead) |
| Cron silent | 25/57 | 25/55 | No Change |

**Persistent security debt (3+ cycles):** live `.env`-reader scripts; dual-root credential divergence; silent cron delivery.

## Remediation Priority

1. **HIGH** — Rewrite/retire `.env`-reader scripts (workspace + Vault + `_tg_send.py`) to use Hermes-injected env or `hermes send`; delete root `send_*.py`.
2. **HIGH** — Align home-root `~/.hermes/.env` `TELEGRAM_BOT_TOKEN` with the valid AppData token, or retire the stale root entirely (its token is revoked).
3. **MED** — Purge remaining legacy `google_token.json` from `~/hermes-backup` and `~/.hermes/backups`.
4. **MED** — Re-point 25 silent cron jobs to explicit topic targets.
5. **LOW** — Confirm Nous Portal auto-refresh at ~12:08 today; monitor host DNS/IPv4 flakiness.

## Delivery

Summary posted to Telegram topic 20 via the live gateway (running, connected, token valid) + verified `getChat` supergroup/forum.

## Retention Note

Report retained in `Vault/System/Assistant/` per job directive. Rolled off `SECURITY_AUDIT_2026-08-21.md` (>7-day window) and deduped same-day variants; keeping one file/day, rolling 7-day window (22, 23, 24, 28, 31).

---

*Masked: all secrets shown as provider-prefix + truncated form. No full tokens echoed.*