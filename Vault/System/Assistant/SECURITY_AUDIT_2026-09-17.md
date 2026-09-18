# Security Audit — 17 September 2026

**Date:** 17/09/2026 (DMY dd/mm/yy)
**Run by:** internal cron / Hermes Agent (default profile) — security-policy-check
**Overall:** **IMPROVED / LOW** — **Telegram gateway RECOVERED.** The 15/09 CRITICAL (token revoked, gateway down) is **RESOLVED**: a valid token (`8277244…` @Ogaitchhermesbot) is now live in the active root and the gateway (PID 11700) is connected & polling Telegram healthily this morning (17/09 06:56 `getUpdates progressing`). No credential exposure this cycle. Residual debts: dual-`.env` divergence (stale revoked token in home root), WhatsApp still unpaired, silent cron delivery share. **No active credential compromise.**

**Report path:** `C:\Users\User\.hermes\workspace\Vault\System\Assistant\SECURITY_AUDIT_2026-09-17.md`
**Telegram delivery target:** Topic 20 (`-1003784520976:20`, "Memory Review") — reachable (token valid, forum supergroup confirmed; security-audit job deliver=`telegram:-1003784520976:20`).

---

## Summary
- **CRITICAL RESOLVED — Telegram token/gateway RECOVERED.** 15/09 found token `827724…1UJE` revoked (4× rejection: 31/08, 05/09, 09/09, 15/09) and gateway `stopped`. **Now**: live-root token `8277244…` is valid (`getMe` ok → @Ogaitchhermesbot, `has_topics_enabled:true`); gateway PID 11700 running with ESTABLISHED TCP to 149.154.166.110; `gateway.log` (live) shows `Connected to Telegram (polling mode)` at 06:56 today and `Telegram polling confirmed healthy: getUpdates progressing`. **No `InvalidToken`/rejection in today's live logs.** Matches memory note "TG OK ~16Sep (msg 11229)".
- **Credential exposure — CLEAN (PASS):** backup `.env` = **0** (backups/hermes-backup/state-snapshots/.openclaw); no `bws_cache.json`/`.secret_cache`; `google_token.json` + both `.env` ACLs = Owner/SYSTEM/Administrators only; AGENTS.md no BOM / no zero-width chars.
- **WhatsApp — FAIL (carried, 100+ cycles):** `creds.json` absent at adapter path `platforms\whatsapp\session\creds.json`; unpaired.
- **Nous Portal expiry 08:02 today (~1 hr)** — auto-refresh enabled; WARN.

## Findings by Area

### 1. Credential Exposure — CLEAN (caches/backups/ACLs)
| Item | Status |
|------|--------|
| `bws_cache.json` / `.secret_cache` | **PASS** — absent |
| Backup `.env` (backups/hermes-backup/state-snapshots/.openclaw) | **PASS** — 0 |
| AGENTS.md (workspace) | **PASS** — UTF-8, no BOM |
| `google_token.json` ACL | **PASS** — Owner/SYSTEM/Administrators only |
| `~/.hermes/.env` and `AppData\…\hermes\.env` ACLs | **PASS** — Owner/SYSTEM/Administrators only |
| **Active Telegram token (live root)** | **PASS** — `8277244…` valid (@Ogaitchhermesbot) |
| Stale home-root `~/.hermes/.env` token | **FAIL (carried)** — still holds revoked `827724…1UJE` + other valid keys |
| `.env`-reader scripts (workspace/home-root) | **FAIL/WARN (carried)** — operational care/send/checkin scripts + one-off `tmp_*`/`_token_test` files read `.env` directly |

### 2. Channel Integrity — Telegram GOOD; WhatsApp down
- **Telegram gateway** — ✅ **RECOVERED/GOOD**: PID 11700, ESTABLISHED TCP to Telegram API, polling confirmed healthy 06:56 today. Minor disconnect blips 06:44–06:56 (transient, reconnected).
- **Active Telegram token** — ✅ valid (`getMe` ok).
- **Chat `-1003784520976`** — ✅ type=supergroup, `is_forum:true` ("Agent Hermes") — topic posting valid. Topic 20 not in auto-built channel_directory (directory only registers recently-active topics); 6 jobs target it & it's historically confirmed — delivery will validate.
- **WhatsApp** — ❌ **FAIL (carried)**: `creds.json` absent at adapter path → unpaired, unable to connect.
- **Cron delivery** — **55 jobs (44 active)**: **30** target Telegram topics (6→topic 20, incl. security-audit; others→14,4,26,1,2,16,28,8,10, DMs); **25 silent** (13 `local`, 12 `origin` — local jobs like tasks-queue-sync/daily-backup are legit; several checkin/reminder jobs are silent → carried debt).

### 3. Recent Security Events — Token revocation CONFIRMED & RESOLVED (no other breach)
- **`rejected by the server`** on `827724…1UJE` at 31/08, 05/09, 09/09, 15/09 — confirmed revocation; treated as credential compromise. **RESOLVED THIS CYCLE**: valid replacement token active; gateway healthy; **no `InvalidToken` in today's live logs.**
- **No other unauthorized access / provider key rejection** observed (OpenRouter/xAI/Firecrawl report configured & healthy).
- **Nous Portal access/key expiry 08:02 today (~1 hr)** — auto-refresh enabled; **WARN** (gateway now up, so refresh transport healthy).

## FAIL Findings
| ID | Severity | Description | Persistent? |
|----|----------|-------------|-------------|
| 1 | **high (≥3 cycles, carried)** | **Dual-`.env` divergence** — stale home-root `~/.hermes/.env` still holds revoked `827724…1UJE` + valid keys; live root has the valid token. Consolidate/retire stale root. | Yes |
| 2 | **high (carried)** | **WhatsApp unpaired/unconnectable** — `platforms\whatsapp\session\creds.json` absent; legacy creds only. | Yes (100+ cycles) |
| 3 | **medium (carried)** | **Silent cron delivery** — 25/55 jobs (`local`/`origin`) produce no user-visible output; reminders/checkins silent. | Yes |
| 4 | **medium (carried)** | **`.env`-reader scripts** — multiple operational scripts + one-off `tmp_*`/`_token_test` read `.env` directly (token leak surface). Clean up one-offs. | Yes |

## CRITICAL Escalations
- **None this cycle.** The 15/09 CRITICAL (Telegram token revoked / gateway down) was **RESOLVED** — valid token live, gateway recovered & polling. No new escalation.

## Retention Note
- Applied 7-day retention: **removed** `SECURITY_AUDIT_2026-09-06.md` and `..._2026-09-07.md` (>7 days). **Kept** 11, 13, 14, 15/09 + today. One file per day maintained.

## WARN Findings
1. Nous Portal key expiry **08:02 today** (~1 hr) — auto-refresh enabled; monitor post-expiry.
2. Stale home-root `.env` — revocation confusion risk (resolved toward live root this cycle); consolidate.
3. Channel directory does not list topic 20 (not authoritative — only recently-active topics registered).
4. Morning gateway disconnect blips (06:44–06:56) — transient; recovered & stable since.

## Remediation Priority
1. **HIGH** — Retire/neutralize stale home-root `~/.hermes/.env` (single authoritative `.env` in live root); remove the revoked `827724…1UJE` token artifact.
2. **HIGH** — Re-pair WhatsApp or restructure adapter path to locate existing creds; re-pair from dashboard if stale.
3. **MED** — Re-point the 25 silent (`local`/`origin`) cron jobs to explicit Telegram topic targets (or confirm they are intentionally local-only).
4. **MED** — Delete one-off `.env`-reading scripts (`tmp_tg20_send.py`, `tmp_*`, `_token_test_*`); keep intake gated.
5. **LOW** — Confirm Nous portal key auto-refresh succeeds past 08:02 expiry.

## Trend Comparison (vs 15/09)
| Item | 15/09 (prior) | 17/09 (this run) | Trend |
|---|---|---|---|
| Gateway | DOWN (token-reject conflict) | **UP/RUNNING** (PID 11700, polling OK) | **Improved / resolved** |
| Telegram token | REVOKED (`827724…1UJE`) | **VALID** (`8277244…` @Ogaitchhermesbot) | **Improved / resolved** |
| Backup `.env` | 0 | 0 | Good |
| Caches | clean | clean | Good |
| Token-file ACLs | secure | secure | Good |
| WhatsApp | unconnectable | unpaired (unchanged) | No change (carried) |
| Dual-`.env` divergence | present | present (stale revoked token persists) | No change (carried) |
| Nous key expiry | 13:06 (15/09) | 08:02 today | Stable (auto-refresh) |

*Retention: removed audits 06/09 & 07/09 (>7 days). Kept 11,13,14,15/09 + today.*