# Security Audit — Internal System

**Date:** 2026-07-19 (afternoon re-run)
**Run by:** internal cron / Hermes Agent (security-policy-check)
**Overall:** FAIL  *(key blocker from this morning — revoked Telegram token — is now RESOLVED)*
**Scope:** credential exposure · channel integrity · recent security events

---

## Executive Summary

The system remains in a **FAIL** posture, but the single most consequential blocker from the morning audit — a **revoked Telegram bot token (HTTP 404)** — is now **RESOLVED**: a direct `getMe` call returns `{"ok":true}` for the bot `Ogaitchhermesbot`, and the token is identical and valid in both `.env` roots. This means the required post to **topic 20 is now deliverable** via the direct API. The **gateway is still DOWN**, and its root cause is now precisely identified: the gateway's effective `.env` (`C:\Users\User\AppData\Local\hermes\.env`, 6 keys) lacks `GATEWAY_ALLOW_ALL_USERS` / `WHATSAPP_ALLOW_ALL_USERS` (present only in the main `~/.hermes/.env`, 31 keys), so it refuses to start against `config.yaml`'s `whatsapp: dm_policy: open`. Credential-exposure hygiene is unchanged: 21 plaintext `.env` backup copies, a plaintext `bws_cache.json` secret cache, and 22 live scripts reading `.env` directly.

---

## 1. Credential Exposure — FAIL

| Check | Result | Evidence |
|-------|--------|----------|
| Canonical `~/.hermes/.env` | EXISTS | `hermes status` sees it; 31 keys; standard ACL |
| Backup `.env` copies (plaintext API keys) | **21 FAIL** | `~/.hermes/backups`=5; `~/hermes-backup`=15; `~/.openclaw`=1; `state-snapshots`=0 |
| `bws_cache.json` (plaintext secret cache) | **FAIL** | `~/.hermes/cache/bws_cache.json` — `key` (len 54) + `secrets` (len 1112, ~11 plaintext secrets) + `fetched_at` |
| `.secret_cache` | not present | — |
| Active scripts reading `.env` directly | **22 FAIL** | `send_*.py`, `tg_*.py`, `check_*.py`, `tmp_*/temp_*` under `~/.hermes/` and `workspace/` |
| `AGENTS.md` BOM / invisible Unicode | **PASS** | main `~/.hermes/AGENTS.md` absent; workspace copy = UTF-8, no BOM, no zero-width/RTL |
| `google_token.json` ACL | **PASS** | `icacls`: SYSTEM (I)(F), Administrators (I)(F), User (I)(F) — no extra principals |
| Dual Hermes roots | **WARN (+root-caused)** | BOTH `~/.hermes/.env` (31 keys) AND `AppData\Local\hermes\.env` (6 keys) exist. AppData copy **lacks** `GATEWAY_ALLOW_ALL_USERS`/`WHATSAPP_ALLOW_ALL_USERS` → gateway refuses to start |

Live `.env` secrets are masked in all output (OpenRouter `sk-or-...72c1`; Telegram token valid this run). The 22 `.env`-reader scripts leak the bot token into process tables/logs each run — a persistent leak pattern. Operational delivery scripts were **not** deleted (they back other jobs); migrate to gateway/Hermes-native delivery.

---

## 2. Channel Integrity — FAIL (token recovered; gateway still down)

| Channel | State | Detail |
|---------|-------|--------|
| **Telegram token** | **VALID (recovered)** | `GET /bot<token>/getMe` → `{"ok":true}` (bot `Ogaitchhermesbot`, topics enabled). Identical & valid in both roots. Morning HTTP 404 is RESOLVED. |
| Topic 20 | EXISTS & valid | `channel_directory.json`: `-1003784520976:20` "Agent Hermes / topic 20". **0 cron jobs** target it → must deliver independently. |
| **Gateway** | **DOWN** | `gateway_state.json`: pid 16948 **dead**, `startup_failed` — *"whatsapp has dm_policy/group_policy set to 'open' but neither GATEWAY_ALLOW_ALL_USERS nor WHATSAPP_ALLOW_ALL_USERS is enabled"*. No ESTABLISHED Telegram TCP. Telegram adapter "connected" metadata is stale (2026-06-18). |
| WhatsApp | **UNPAIRED** | `~/.hermes/whatsapp/session/creds.json` MISSING (67+ days); `fatal` state. |
| Discord | PAUSED | `failed to reconnect` (stale 2026-05-30). |
| Nous Portal | LOGGED IN (WARN) | Access/Key exp `2026-07-19 13:41` — refreshed from 08:02; expires today, refresh active. |
| `gateway-exit-diag.log` | 7 crash entries | `ModuleNotFoundError: concurrent_log_handler` (Py3.14) dated 06-22→07-01; crash loop resolved; current down-state is the WhatsApp policy block. |

**Cron delivery audit (jobs.json, 40 jobs):** `origin`=25, `local`=2, `telegram:`=13. **27 jobs (origin+local) are silent** — output never reaches a user. The 13 Telegram jobs target topics 16/26/4/2/28; **none target topic 20**. Gateway-dependent delivery (all 40 jobs) is blocked while the gateway is down; direct-API delivery to topic 20 works (token valid).

---

## 3. Recent Security Events — FAIL (mostly historical)

| Event | Source | Severity | Notes |
|-------|--------|----------|-------|
| **Telegram token REVOKED → RECOVERED** | this run `getMe` | **RESOLVED** | Morning audit saw HTTP 404; now `ok:true`. Either rotated via @BotFather or transient — verify with @BotFather if unexpected. |
| Historical `InvalidToken` | `errors.log.1` (2026-06-09) | HIGH (historical) | `token 8277...ugM8 rejected / Not Found` — predates current valid token |
| Active `InvalidToken` / breach markers | current `agent.log`/`errors.log` | NONE | No `breach`, `unauthorized access`, or live `InvalidToken` |
| Provider 401/403 rejections | current logs | NONE | No live provider HTTP rejections observed |
| Multi-service DNS failure | `gateway.log` (2026-06-18) | LOW/historical | `getaddrinfo failed` on Telegram — host-level, resolved |

---

## 4. FAIL Items & Trend (vs 2026-07-19 morning)

| ID | Finding | Morning | Afternoon | Trend |
|----|---------|---------|-----------|-------|
| F1 | Telegram token | CRITICAL (revoked 404) | VALID (ok:true) | **RESOLVED** |
| F2 | Gateway DOWN (WhatsApp policy) | CRITICAL | CRITICAL (root-caused) | No Change |
| F3 | WhatsApp unpaired | HIGH | HIGH | No Change (67+ days) |
| F4 | Backup `.env` copies | 16 | 21 | No Change |
| F5 | `.env`-reading scripts | 37 | 22* | No Change (still FAIL) |
| F6 | Dual Hermes roots | WARN | WARN (root-caused) | No Change |
| F7 | `google_token.json` ACL | PASS | PASS | Stable |
| F8 | `AGENTS.md` BOM | PASS | PASS | Stable |
| F9 | Cron origin/local silent | 27 | 27 | No Change |
| F10 | `bws_cache.json` plaintext | FAIL | FAIL | No Change |

\* Afternoon count uses the stricter live-tree scan (excludes Vault subdirs) vs morning's broader scan.

**Persistent security debt (≥3 cycles, escalated):** F2, F3, F4, F10 — carried many cycles with no remediation; continue escalation.

---

## 5. Required Actions

1. **Fix gateway start (root cause):** copy `GATEWAY_ALLOW_ALL_USERS`/`WHATSAPP_ALLOW_ALL_USERS` into the gateway's `AppData\Local\hermes\.env` (or set `whatsapp.dm_policy` to a restricted value in `config.yaml`). (F2)
2. **Pair WhatsApp** (QR re-scan) or disable the channel. (F3)
3. **Purge the 21 backup `.env` copies** outside `~/.hermes/.env`; add to backup exclusions. (F4)
4. **Clear `bws_cache.json`** or move secrets to an encrypted store. (F10)
5. **Migrate the 22 `.env`-reading scripts** to gateway/Hermes-native delivery. (F5)
6. **Consolidate dual `.env` roots** to one authoritative location. (F6)
7. **Verify the Telegram token rotation** with @BotFather if the morning revocation was unexpected (not a leak). (F1)

*Report generated non-destructively. No secrets printed. Temp scan scripts removed after run.*
