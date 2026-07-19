# Security Audit — Internal System

**Date:** 2026-07-19
**Run by:** internal cron / Hermes Agent (security-policy-check)
**Overall:** FAIL
**Scope:** credential exposure · channel integrity · recent security events

---

## Executive Summary

The system remains in a **FAIL** posture carried over from prior cycles. The single most consequential finding is a **revoked Telegram bot token** (confirmed by a direct `getMe` API call returning HTTP 404), which blocks *all* Telegram delivery — including this audit's required post to topic 20. The gateway is **currently down** because it refuses to start (WhatsApp `dm_policy/group_policy` set to `open` without the required allow-all opt-in). Credential-exposure hygiene is unchanged-to-worse: 16 plaintext `.env` backup copies across three trees, a plaintext `bws_cache.json` credential cache, and 37 live scripts that read `.env` directly. Positive movement: `AGENTS.md` no longer carries a BOM, and `google_token.json` (new this cycle) has a correct owner-only ACL.

---

## 1. Credential Exposure — FAIL

| Check | Result | Evidence |
|-------|--------|----------|
| Canonical `~/.hermes/.env` | EXISTS, standard ACL (Owner/SYSTEM/Administrators) | `hermes status` sees it |
| Backup `.env` copies (plaintext API keys) | **16 FAIL** | `~/.hermes/backups` = 5; `~/hermes-backup` = 10; `~/.openclaw` = 1 |
| `bws_cache.json` (plaintext secret cache) | **FAIL (NEW)** | `~/.hermes/cache/bws_cache.json` — keys `key` (617864...135\|) + `secrets` (FIRE...hN) + `fetched_at` |
| `.secret_cache` | not present | — |
| Active scripts reading `.env` directly | **37 FAIL** | `send_*.py`, `check_*.py`, `tg_*.py` across `~/.hermes/` and `~/.hermes/workspace/` (incl. Vault subdirs) |
| `AGENTS.md` BOM / invisible Unicode | **PASS** | main `~/.hermes/AGENTS.md` absent; workspace copy = UTF-8 text, **no BOM**, no zero-width/RTL chars |
| `google_token.json` ACL | **PASS (NEW)** | `icacls`: NT AUTHORITY\SYSTEM (I)(F), BUILTIN\Administrators (I)(F), DESKTOP-25Q3AQC\User (I)(F) — no extra principals |
| Dual Hermes roots | **WARN** | BOTH `~/.hermes/.env` AND `C:\Users\User\AppData\Local\hermes\.env` now exist → credential divergence risk |

Secrets in the live `.env` are masked in all tool output (OpenRouter `sk-or-...72c1`; Telegram token revoked; Google/Firecrawl/Brave/xAI keys present). The 37 active `.env` readers leak the bot token into process tables, shell history, and logs on every run — a persistent credential-leak pattern. Production delivery scripts were **not** deleted (they back other cron jobs); they should be migrated to the gateway/Hermes-native `send_message` to stop reading `.env` directly.

---

## 2. Channel Integrity — FAIL

| Channel | State | Detail |
|---------|-------|--------|
| **Telegram token** | **REVOKED** | `GET /bot<token>/getMe` → `{"ok":false,"error_code":404,"description":"Not Found"}`. Adapter "connected" ≠ token valid. |
| Topic 20 | EXISTS & valid | `channel_directory.json`: `-1003784520976:20` "Agent Hermes / topic 20", type group, thread_id 20. Target is fine; blocker is the revoked token. |
| **Gateway** | **DOWN** | Last start 2026-07-19 05:04:38 refused: *"whatsapp has dm_policy/group_policy set to 'open' but neither GATEWAY_ALLOW_ALL_USERS nor WHATSAPP_ALLOW_ALL_USERS is enabled"* → exit cleanly. No ESTABLISHED Telegram TCP (only TIME_WAIT). |
| WhatsApp | **UNPAIRED** | `~/.hermes/whatsapp/session/creds.json` MISSING (67+ days). Separately, its open policy also blocks gateway start. |
| Nous Portal | LOGGED IN (WARN) | Access/Key exp `2026-07-19 08:02:35` — expires today; flag if refresh then fails. |
| `gateway-exit-diag.log` | 7 crash entries | `ModuleNotFoundError: concurrent_log_handler` (Python 3.14) dated 06-22→07-01; recent starts (07-18/07-19) succeeded then exited cleanly — crash loop appears resolved; current down-state is the WhatsApp policy block, not the missing module. |

**Cron delivery audit (jobs.json, 40 jobs):** `origin` = 25, `local` = 2, `telegram:...` = 13. **27 jobs (origin+local) are silent** — output stays local and never reaches a user. The 13 Telegram jobs target topic 26. The security-audit job itself is `deliver: origin`. All Telegram-bound delivery (topic 20, topic 26, these 13 jobs) is **blocked by the revoked token**.

---

## 3. Recent Security Events — FAIL

| Event | Source | Severity | Notes |
|-------|--------|----------|-------|
| Telegram token revoked (HTTP 404) | direct `getMe` call (this run) | **CRITICAL** | Potential credential compromise — rotate via @BotFather before any Telegram use |
| Historical `InvalidToken` | `errors.log.1` (2026-06-09) | HIGH | `token 8277...ugM8 was rejected by the server` / `Not Found` |
| Telegram polling conflicts | `errors.log` (2026-06-12) | LOW | Multiple bot instances ("terminated by other getUpdates request") — transient, historical |
| Unauthorized access / breach markers | all logs | NONE | No `breach`, `unauthorized access`, or active `InvalidToken` in current `agent.log`/`errors.log` |
| Provider 401/403 rejections | current logs | NONE | Prior 402/403 grep matched normal token-count INFO lines, not HTTP errors; no live provider rejection observed |

---

## 4. FAIL Items & Trend (vs 2026-07-18)

| ID | Finding | 07-18 | 07-19 | Trend |
|----|---------|-------|-------|-------|
| F1 | Telegram token revoked | CRITICAL | CRITICAL | No Change (persistent, 8+ cycles) |
| F2 | Gateway DOWN (WhatsApp policy) | CRITICAL | CRITICAL | No Change (persistent) |
| F3 | WhatsApp unpaired | HIGH | HIGH | No Change (65→67+ days) |
| F4 | Backup `.env` copies | 5 (backups) | 16 (3 trees) | No Change / more exposed |
| F5 | Active `.env`-reading scripts | 18 | 37 | **Worsened** |
| F6 | Dual Hermes roots | FAIL (AppData missing) | WARN (both exist) | Changed — divergence risk |
| F7 | `google_token.json` | absent (PASS) | exists, ACL PASS | New / Improved |
| F8 | `AGENTS.md` BOM | FAIL | PASS | Improved |
| F9 | Cron origin/local silent | 11 | 27 | **Worsened** |
| F10 | `bws_cache.json` plaintext | not noted | FAIL | **New finding** |

**Persistent security debt (≥3 cycles, escalated):** F1, F2, F3, F4 — carried across many cycles with no remediation; continue escalation.

---

## 5. Required Actions

1. **Rotate the Telegram bot token via @BotFather** and update `~/.hermes/.env`; re-verify with `getMe`. (F1)
2. **Fix gateway start:** set WhatsApp `dm_policy`/`group_policy` to a restricted value, or enable `GATEWAY_ALLOW_ALL_USERS`/`WHATSAPP_ALLOW_ALL_USERS`. (F2)
3. **Pair WhatsApp** (QR re-scan) or disable the channel. (F3)
4. **Purge the 16 backup `.env` copies** outside `~/.hermes/.env`; add to backup exclusions. (F4)
5. **Delete/clear `bws_cache.json`** or move secrets to encrypted store. (F10)
6. **Migrate the 37 `.env`-reading scripts** to gateway/Hermes-native delivery. (F5)
7. **Consolidate dual `.env` roots** to one authoritative location. (F6)

*Report generated non-destructively. No secrets printed. Temp scan scripts removed after run.*
