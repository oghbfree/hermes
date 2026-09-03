# Security Audit — 01 September 2026

**Date:** 01/09/2026
**Run by:** internal cron / Hermes Agent (default profile)
**Overall:** **STABLE** — live gateway RUNNING (AppData root, PID 14576, Python 3.11, v0.20.6), Telegram token VALID (`getMe` ok:true, `Ogaitchhermesbot`), WhatsApp connected, active logs fresh (07:04 today). No compromise events. **Persisting debt:** live `.env`-reader scripts, dual-root credential divergence (home-root token revoked via getMe 404), 25/55 cron jobs silent delivery, legacy google_token copies (9+2). **New this cycle:** Vercel MCP 401 Unauthorized (provider credential/auth).

**Report path:** `C:\Users\User\.hermes\workspace\Vault\System\Assistant\SECURITY_AUDIT_2026-09-01.md`
**Telegram delivery target:** Topic 20 (`telegram:-1003784520976:20`), verified present in home channel_directory (supergroup forum "Agent Hermes").

---

## Summary

- **Channel health GREEN** — Gateway PID **14576** running (AppData root, gateway_state `running` since 05:10 today), Telegram `connected` (polling, confirmed 05:10), WhatsApp `connected`/reconnected (05:13). `gateway.log` fresh at 06:43 today.
- **Runtime Telegram token VALID** — direct `getMe` against the AppData-root token returns `{"ok":true,...,"username":"Ogaitchhermesbot"}`.
- **Home-root token (dormant root) REVOKED** — `~/.hermes/.env` token returns HTTP 404 on `getMe`; its `gateway_state.json` is `startup_failed` (token rejected). Known dual-root divergence, not the active path. WARN.
- **No InvalidToken/401 in active (AppData) current logs** — Telegram token clean. One provider signal: **Vercel MCP HTTP 401** (08-29, 09-01) — provider auth/config issue, WARN.
- **Credential caches CLEAN** — `bws_cache.json` / `.secret_cache` / provider caches absent.
- **Backup `.env` copies** — 0 across `~/.hermes/backups`, `~/.hermes/state-snapshots`, `~/hermes-backup`, `~/.openclaw`. PASS (sustained).
- **Legacy google_token copies** — 9 in `~/hermes-backup` + 2 in `~/.hermes/backups` (unchanged). WARN.
- **`google_token.json` ACL correct** — SYSTEM / Administrators / User `(I)(F)` only, no Everyone/Users group. PASS.
- **AGENTS.md** — main `~/.hermes/AGENTS.md` absent; workspace copy UTF-8, no BOM, no zero-width/RTL chars. PASS.
- **Live `.env`-reader scripts (FAIL debt)** — ~17 live files: workspace/scripts `send_ghana_report.py`, `memory_review_telegram.py`, `ghana_telegram_report.py`; `Vault/business/2real/.../ghana_telegram_report.py`; `Vault/family/mum/health/*checkin*.py`; root `send_health_check.py`, `telegram_direct_send.py`, `telegram_create_topic.py`, `telegram_post_file.py`, `scripts/test_paths.py`, `_token_test_2026-08-25.py`, `tmp_afternoon_send.py`; AppData `_tg_send.py`. All parse `/path/.hermes/.env` / AppData `.env` directly.
- **Cron delivery** — **55 jobs; 25 silent** (13 `local` + 12 `origin`), 30 explicit `telegram:` targets (Topic 20 present, 6 jobs + security-policy-check target it).
- **Nous Portal** — access/key expiry **2026-09-01 07:46:42** (~36 min from audit time) — WARN; refresh enabled.

## Findings by Area

### 1. Credential Exposure — PARTIAL (caches clean, backups clean; FAIL debt persists)
| Item | Status |
|------|--------|
| `bws_cache.json` / `.secret_cache` | **PASS** — absent |
| Backup `.env` (all trees) | **PASS** — 0 |
| `google_token.json` ACL | **PASS** — SYSTEM/Administrators/User `(I)(F)` only |
| AGENTS.md BOM / invisible chars | **PASS** — UTF-8 no BOM |
| Active runtime token (AppData) | **PASS/VALID** — getMe ok `Ogaitchhermesbot` |
| Home-root `~/.hermes/.env` token | **WARN** — revoked (getMe HTTP 404); dormant divergent root |
| Legacy google_token copies | **WARN** — 9 (hermes-backup) + 2 (internal backups), unchanged |
| Live `.env`-reader scripts | **FAIL (PERSISTS)** — workspace/Vault/root + AppData `_tg_send.py` |

### 2. Channel Integrity — GOOD (gateway stable)
- **Telegram (gateway)** — ✅ PASS: PID 14576 running, `connected`, logs fresh.
- **Telegram (token, active)** — ✅ PASS: getMe ok; Topic 20 present (home cdir). Note: AppData `channel_directory.json` does not enumerate topic 20 (home cdir does) — catalog inconsistency, not an integrity failure.
- **WhatsApp** — ✅ PASS: state `connected`/reconnected (05:13).
- **Cron delivery** — ⚠️ WARN: 55 jobs → 25 silent (13 `local` + 12 `origin`), 30 telegram-targeted.

### 3. Recent Security Events — NO COMPROMISE (one new WARN)
- **No** new `InvalidToken` / `Revoked` / Telegram `401` in active (AppData) logs this window — token clean.
- **NEW:** Vercel MCP **HTTP 401 Unauthorized** (08-29 10:59, 09-01 05:28) — provider access-token/auth configuration issue, not Telegram/WhatsApp. WARN.
- **Access control good:** adapter blocked unauthorized user `5146706699` in chat (08-13) — allowlist enforcement recorded.
- Home-root token revoked steps (08-22, 08-31 `The token ...1UJE was rejected`) — dormant root, no active impact.
- Nous Portal token expiry ~07:46 today (~36 min) — refresh enabled, assess next cycle.

## FAIL Findings
| ID | Severity | Description | Persistent? |
|----|----------|-------------|-------------|
| 1 | high | **Live `.py` scripts read `.env` directly** (workspace/scripts, Vault family health, root send_*.py, AppData `_tg_send.py`, incl. `_token_test` / `tmp_*` one-offs) — leak tokens to process table/history/logs | Yes (3+ cycles) |
| 2 | high | **Credential divergence: dual `.env` roots** — AppData holds VALID token; home-root `~/.hermes/.env` REVOKED (getMe 404) but referenced by task scripts | Yes (3+ cycles) |
| 3 | medium | **25/55 cron jobs silent delivery** (13 `local` + 12 `origin`) | Yes (3+ cycles) |

## WARN Findings
*(No WhatsApp outage — online and connected; Topic 20 present; no config drift; no DNS instability; no health-log gaps this cycle.)*
| ID | Description |
|----|-------------|
| 1 | **NEW: Vercel MCP HTTP 401** (08-29, 09-01) — provider auth/config; verify access token |
| 2 | Nous Portal access/key expiry ~07:46 today (~36 min) — confirm auto-refresh |
| 3 | 9 legacy `google_token.json` (hermes-backup) + 2 (internal) not purged — unchanged |
| 4 | Home-root `.env` token revoked — dormant root should be consolidated or retired |
| 5 | AppData `channel_directory.json` does not enumerate topic 20 (home cdir does) — catalog drift |

## CRITICAL Escalations
None — no findings escalated this cycle.

## Trend Comparison (vs 31/08 audit)
| Item | 31/08 | This run (01/09) | Trend |
|---|---|---|---|
| Gateway | ✅ running (PID 868) | ✅ running (PID 14576) | Stable |
| Telegram token valid (active) | ✅ getMe ok | ✅ getMe ok | Stable |
| WhatsApp | ✅ paired | ✅ connected/reconnected | Stable |
| `bws_cache` / caches | clean | clean | Good (sustained) |
| Backup `.env` | 0 | 0 | Good (sustained) |
| Legacy google_token copies | 9 + 2 | 9 + 2 | No Change |
| Live `.env` readers | present | present (~17) | No Change (debt) |
| Home-root token | revoked (404) | revoked (404) | No Change |
| Vercel MCP auth | — | **401 (new)** | Degraded (new) |
| Cron silent | 25/55 | 25/55 | No Change |

**Persistent security debt (3+ cycles):** live `.env`-reader scripts; dual-root credential divergence; silent cron delivery.

## Remediation Priority
1. **HIGH** — Rewrite/retire `.env`-reader scripts (workspace + Vault + `_tg_send.py`); delete dated one-offs (`_token_test_2026-08-25.py`, `tmp_afternoon_send.py`, `test_paths.py`, root `send_health_check.py`).
2. **HIGH** — Align home-root `~/.hermes/.env` `TELEGRAM_BOT_TOKEN` with valid AppData token, or retire the stale root (token revoked).
3. **MED** — Purge legacy `google_token.json` (9 hermes-backup + 2 internal).
4. **MED** — Re-point 25 silent cron jobs to explicit topic targets; reconcile AppData channel_directory vs home cdir.
5. **MED** — Investigate Vercel MCP 401 (provider access token/credential).
6. **LOW** — Confirm Nous Portal auto-refresh at ~07:46 today.

## Delivery
Summary posted to Telegram topic 20 via the live gateway (running, connected, token valid).

## Retention Note
Report retained in `Vault/System/Assistant/` per job directive; rolling 7-day window enforced.

---
*Masked: all secrets shown as provider-prefix + truncated form. No full tokens echoed.*