# Security Audit — 21 September 2026

**Date:** 21/09/2026 (DMY dd/mm/yy)
**Run by:** internal cron / Hermes Agent (default profile) — security-policy-check
**Overall:** **STABLE / LOW** — Telegram gateway healthy, live token valid, no credential exposure, no active compromise. One transient Vercel MCP 401 (20/09 22:29 → resolved 200 OK 21/09 05:48) auto-recovered. Persistent carried items: dual-`.env` divergence (stale revoked token in home root) and `.env`-reader scripts. **No active credential compromise.**

**Report path:** `C:\Users\User\.hermes\workspace\Vault\System\Assistant\SECURITY_AUDIT_2026-09-21.md`
**Telegram delivery target:** Topic 20 (`-1003784520976:20`, "Memory Review") — reachable (live token valid via getMe → @Ogaitchhermesbot id 8277244378; chat is supergroup with forum enabled; security-audit job deliver=`telegram:-1003784520976:20`).

---

## Summary
- **Telegram gateway — HEALTHY.** Connected (polling mode) since 19/09 22:38 auto-recovery; 20/09 20:29 one isolated "stuck probe 1/2" heartbeat (5 updates queued but not consumed) — transient, no crash. Logs fresh (07:04 today). **No `InvalidToken`/`rejected by the server` in live or rotated logs today.**
- **Live Telegram token — VALID** (`getMe` ok → @Ogaitchhermesbot id 8277244378) in the AppData live root. Home-root copy (`~/.hermes/.env`) returns **HTTP 404** — dual-`.env` divergence persists (stale/revoked artifact, carried ≥3 cycles).
- **Credential exposure — CLEAN (PASS):** backup `.env` = **0** across all roots (backups/state-snapshots/hermes-backup/.openclaw); no `bws_cache.json`/`.secret_cache`; workspace AGENTS.md UTF-8, no BOM, CRLF; main `~/.hermes/AGENTS.md` absent (cleaned).
- **`google_token.json` ACL — PASS:** only `NT AUTHORITY\SYSTEM:(I)(F)`, `BUILTIN\Administrators:(I)(F)`, `User:(I)(F)`. No Everyone/Users.
- **Vercel MCP — transient 401, auto-resolved.** One `401 Unauthorized` (20/09 22:29); subsequent 200 OK (20/09 04:46 & 21/09 05:48). OAuth self-healed; not persistent.
- **Nous Portal key expiry 07:21 today** (within 24h at run time) — auto-refresh enabled; monitor post-expiry (historically succeeds).

## Findings by Area

### 1. Credential Exposure — CLEAN
| Item | Status |
|------|--------|
| `bws_cache.json` / `.secret_cache` | **PASS** — absent |
| Backup `.env` (all roots) | **PASS** — 0 |
| AGENTS.md (workspace) | **PASS** — UTF-8, no BOM |
| Main `~/.hermes/AGENTS.md` | **PASS** — absent (removed) |
| `google_token.json` ACL | **PASS** — SYSTEM/Admins/User only |
| Live Telegram token (AppData root) | **PASS** — valid (@Ogaitchhermesbot) |
| Stale home-root `~/.hermes/.env` token | **FAIL (carried, ≥3 cycles)** — still holds revoked copy (getMe 404) |
| `.env`-reader scripts (workspace) | **FAIL/WARN (carried)** — ~6 authoritative readers in workspace + ~8 `tmp_*`/`*_send*` one-offs; token leak surface. |

### 2. Channel Integrity — Telegram GOOD, WhatsApp disabled by config
- **Telegram gateway** — ✅ **HEALTHY** since 19/09 22:38 (polling mode, fresh logs 07:04 today).
- **Live Telegram token** — ✅ valid (`getMe` ok).
- **Chat `-1003784520976`** — ✅ supergroup forum (`type: supergroup`, `is_forum: true`); topic 20 reachable.
- **No gateway crash signature:** `gateway-exit-diag.log` clean — 0 `asyncio.run.exception` entries.
- **Cron delivery** — **56 jobs**: **30** target Telegram (6→topic 20, rest → 14,4,26,1,2,16,28,8,10 + 2 DMs), **13 `local`** + **13 `origin`** silent (local backups/DB-sync legit; reminders/checkins silent → carried debt).
- **WhatsApp** — explicitly **disabled by config** (`platforms.whatsapp.enabled: false`, 18/09). Intentional, not unpaired failure.

### 3. Recent Security Events — No token rejection
- **No `InvalidToken` / `rejected by the server`** in today's live or rotated logs (0 matches).
- **One transient Vercel MCP 401** (20/09 22:29) — auto-resolved to 200 OK (21/09 05:48), OAuth refresh; not credential compromise.
- **No rogue logins, no BOM/invisible-char injection** in configs; AGENTS.md clean.

## FAIL Findings
| ID | Severity | Description | Persistent? |
|----|----------|-------------|-------------|
| 1 | **high (≥3 cycles, carried)** | **Dual-`.env` divergence** — stale home-root `~/.hermes/.env` still holds a revoked Telegram token (getMe 404); live AppData root valid. Retire stale root. | Yes |
| 2 | **medium (carried)** | **Silent cron delivery** — 26/56 (`local`/`origin`); reminders/checkins silent (backup/DB-sync intentional). | Yes |
| 3 | **medium (carried)** | **`.env`-reader scripts** — workspace one-offs (`tmp_*`, `*_send*`) read `.env` directly. Clean up. | Yes |

## CRITICAL Escalations
- None this cycle. No unresolved compromise.

## WARN Findings
1. **Nous Portal key expiry 07:21 today** — auto-refresh enabled; monitor post-expiry (historically succeeds).
2. **Transient Vercel 401** (20/09) — resolved; re-monitor if it recurs (was a prior sustained WARN 13–16/09).

## Remediation Priority
1. **HIGH** — Retire/neutralize stale home-root `~/.hermes/.env`; single authoritative `.env` in live AppData root.
2. **MED** — Delete one-off `.env` readers (`tmp_*`, `*_send*`); gate intake.
3. **MED** — Re-point 26 silent jobs (`local`/`origin`) to explicit topic targets where user-facing.
4. **LOW** — Monitor Nous key expiry; confirm WhatsApp deliberate-disable intent unchanged.

## Retention Note
7-day window (14–21/09): files exist 13,14,15,17,18,20,21/09. **Removed `SECURITY_AUDIT_2026-09-13.md`** (>7 days, oldest). Kept 14,15,17,18,20 + today (21/09). One file per day maintained. (No 16,19 files existed.)

## Trend Comparison (vs 20/09)
| Item | 20/09 (prior) | 21/09 (this run) | Trend |
|---|---|---|---|
| Gateway | UP (polling) | UP (polling, 1 transient stall auto-recovered) | Stable / good |
| Telegram token (live) | VALID (8277244…) | VALID (getMe ok) | Stable / good |
| Backup `.env` | 0 | 0 | Good |
| Caches | clean | clean | Good |
| AGENTS.md | no BOM | no BOM (main absent) | Good |
| google_token ACL | PASS | PASS | Good |
| Dual-`.env` divergence | present | present (stale revoked persists) | No change (carried) |
| Vercel MCP | RESOLVED (200 OK 20/09) | 1 transient 401 (20/09 22:29) → 200 OK (21/09) | Stable (auto-healed) |
| Nous key expiry | 21:29 (20/09) | 07:21 today | Stable (auto-refresh) |
| WhatsApp | disabled-by-config | disabled-by-config (confirmed) | Stable |

*Retention: removed 13/09 (7 days old); kept 14,15,17,18,20/09 + today.*
