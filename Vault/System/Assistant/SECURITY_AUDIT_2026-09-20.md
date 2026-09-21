# Security Audit — 20 September 2026

**Date:** 20/09/2026 (DMY dd/mm/yy)
**Run by:** internal cron / Hermes Agent (default profile) — security-policy-check
**Overall:** **STABLE / LOW** — Telegram gateway healthy, live token valid, no credential exposure, no active compromise. Vercel MCP 401 WARN **RESOLVED** this cycle (200 OK + OAuth token refreshed 20/09). Persistent carried items: dual-`.env` divergence (stale revoked token in home root) and `.env`-reader scripts. **No active credential compromise.**

**Report path:** `C:\Users\User\.hermes\workspace\Vault\System\Assistant\SECURITY_AUDIT_2026-09-20.md`
**Telegram delivery target:** Topic 20 (`-1003784520976:20`, "Memory Review") — reachable (live token valid via getMe → @Ogaitchhermesbot id 8277244378; chat is supergroup; security-audit job deliver=`telegram:-1003784520976:20`).

---

## Summary
- **Telegram gateway — HEALTHY.** Connected (polling mode) 19/09 22:38 after a transient 09-19 22:37 polling-stall auto-recovery (adapter rebuild, reconnect within ~1 min). Log fresh (20:31 today). One 20:29 "stuck probe 1/2" heartbeat (5 updates queued, not consumed) — transient, no crash. PID 15220 running. **No `InvalidToken`/`rejected by the server` anywhere** in live or rotated logs today.
- **Live Telegram token — VALID** (`getMe` ok → @Ogaitchhermesbot id 8277244378). Home-root copy (`~/.hermes/.env`) returns **HTTP 404** — dual-`.env` divergence persists (stale/revoked artifact).
- **Credential exposure — CLEAN (PASS):** backup `.env` = **0** across all roots (backups/state-snapshots/hermes-backup/.openclaw); no `bws_cache.json`/`.secret_cache`; no cache files found; AGENTS.md (workspace) UTF-8, no BOM, CRLF; main `~/.hermes/AGENTS.md` absent (cleaned).
- **`google_token.json` ACL — PASS:** only `NT AUTHORITY\SYSTEM:(I)(F)`, `BUILTIN\Administrators:(I)(F)`, `User:(I)(F)`. No Everyone/Users. Standard default, no exposure.
- **Vercel MCP — RESOLVED (was WARN):** 13–16/09 401 errors are gone; agent.log 20/09 shows `POST https://mcp.vercel.com → 200 OK` and Vercel OAuth token refreshed (20:29). No further 401s.
- **Nous Portal key expiry 21:29 today** — auto-refresh enabled; transport healthy. Monitor post-expiry (same pattern as prior cycles, auto-refresh historically succeeds).

## Findings by Area

### 1. Credential Exposure — CLEAN
| Item | Status |
|------|--------|
| `bws_cache.json` / `.secret_cache` | **PASS** — absent |
| Backup `.env` (all roots) | **PASS** — 0 |
| AGENTS.md (workspace) | **PASS** — UTF-8, no BOM |
| Main `~/.hermes/AGENTS.md` | **PASS** — absent (removed) |
| `google_token.json` ACL | **PASS** — SYSTEM/Admins/User only |
| Active Telegram token (live root) | **PASS** — valid (@Ogaitchhermesbot) |
| Stale home-root `~/.hermes/.env` token | **FAIL (carried, ≥3 cycles)** — still holds revoked copy (getMe 404) |
| `.env`-reader scripts (workspace/home) | **FAIL/WARN (carried)** — 5 in `~/.hermes`, 38 in workspace root, plus one-off `tmp_*`/`test_creds.py`/`tmp_send_*` persist; token leak surface. The broad scan count (181 across nested Vault subdirs incl. false positives from `open(`) overstates; the actionable surface is the workspace-root one-offs + direct readers. |

### 2. Channel Integrity — Telegram GOOD, WhatsApp configured (not verified this cycle)
- **Telegram gateway** — ✅ **HEALTHY** since 19/09 22:38 (connected polling mode, fresh log 20:31, PID 15220).
- **Active Telegram token** — ✅ valid (`getMe` ok).
- **Chat `-1003784520976`** — ✅ supergroup forum; topic 20 reachable (6 jobs deliver there incl. security-audit).
- **No gateway crash signature:** `gateway-exit-diag.log` clean today — 0 `asyncio.run.exception` entries on 20/09 (none found).
- **Cron delivery** — **56 jobs**: **30** target Telegram topics (6→topic 20, rest → 14,4,26,1,2,16,28,8,10 + 2 DMs), **13 `local`** + **13 `origin`** silent (local backups/DB-sync legit; checkin/reminder silent → carried debt).

### 3. Recent Security Events — No token rejection today
- **No `InvalidToken` / `rejected by the server`** in today's live or rotated `agent.log.1`/`errors.log.1` (clean).
- **No 401/403/Unauthorized** today (prior Vercel 401 resolved).
- **No rogue logins, no BOM/invisible-char injection** in configs; AGENTS.md clean.
- **Transient gateway polling stall 19/09 22:37** — auto-recovered 22:38 (adapter rebuild); not credential-related, network/verifier transient.

## FAIL Findings
| ID | Severity | Description | Persistent? |
|----|----------|-------------|-------------|
| 1 | **high (≥3 cycles, carried)** | **Dual-`.env` divergence** — stale home-root `~/.hermes/.env` still holds a revoked Telegram token (getMe 404); live root valid. Retire stale root. | Yes |
| 2 | **medium (carried)** | **Silent cron delivery** — 26/56 (`local`/`origin`); reminders/checkins silent. | Yes |
| 3 | **medium (carried)** | **`.env`-reader scripts** — workspace/home one-offs (`tmp_send_*`, `test_creds.py`, `tmp_*`) read `.env` directly. Clean up one-offs. | Yes |

## CRITICAL Escalations
- None this cycle. No unresolved compromise.

## WARN Findings
1. **Nous Portal key expiry 21:29 today** — auto-refresh monitor (historically succeeds).
2. **WhatsApp** configured — status shows "✓ configured"; not re-verified via config line this cycle (config read gated). Prior audit flagged deliberate-disable intent; confirm state if WhatsApp reliability matters.

## Remediation Priority
1. **HIGH** — Retire/neutralize stale home-root `~/.hermes/.env`; single authoritative `.env` in live root.
2. **MED** — Delete one-off `.env` readers (`tmp_send_*`, `test_creds.py`, `test_sheets.py`); gate intake.
3. **MED** — Re-point 26 silent jobs (`local`/`origin`) to explicit topic targets.
4. **LOW** — Monitor Nous key expiry; confirm WhatsApp intent.

## Retention Note
Applied 7-day retention at `Vault\System\Assistant\`: existing files 11,13,14,15,17,18,20/09. **Removed `SECURITY_AUDIT_2026-09-11.md`** (now >7 days, oldest). Kept 13,14,15,17,18 + today (20/09). One file per day maintained. (No 09/16, 09/19 file existed.)

## Trend Comparison (vs 18/09)
| Item | 18/09 (prior) | 20/09 (this run) | Trend |
|---|---|---|---|
| Gateway | UP (polling) | UP (polling, 1 transient stall 19/09 auto-recovered) | Stable / good |
| Telegram token | VALID (8277244…) | VALID (getMe ok) | Stable / good |
| Backup `.env` | 0 | 0 | Good |
| Caches | clean | clean | Good |
| AGENTS.md | no BOM | no BOM (main absent) | Good |
| google_token ACL | PASS | PASS | Good |
| Dual-`.env` divergence | present | present (stale revoked persists) | No change (carried) |
| Vercel MCP 401 | WARN (13–16/09) | **RESOLVED** (200 OK 20/09 + OAuth refresh) | **Improved** |
| Nous key expiry | 07:29 (18/09) | 21:29 today | Stable (auto-refresh) |
| WhatsApp | disabled-by-config | configured (not re-verified) | Unchanged |

*Retention: removed 11/09 (7 days old); kept 13,14,15,17,18/09 + today.*