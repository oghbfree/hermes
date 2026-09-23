# Security Audit — 22 September 2026

**Date:** 22/09/2026 (DMY dd/mm/yy)
**Run by:** internal cron / Hermes Agent (default profile) — security-policy-check
**Overall:** **STABLE / MODERATE** — Telegram gateway healthy, live token valid, credential exposure clean (backup `.env` = 0), **no active compromise / no token rejection**. One **NEW credential FAIL this cycle: Nous Portal refresh token terminally invalid** (`invalid_grant`) — auxiliary client offline; needs re-auth. Carried items: dual-`.env` divergence, 3 stale home-workspace `.env`-reader one-offs, 26 silent cron deliveries.

**Report path:** `C:\Users\User\.hermes\workspace\Vault\System\Assistant\SECURITY_AUDIT_2026-09-22.md`
**Telegram delivery target:** Topic 20 (`-1003784520976:20`, "Memory Review") — **verified reachable** (probe delivered, msg_id 11402; chat supergroup + forum enabled; live token valid → @Ogaitchhermesbot id 8277244378).

---

## Summary
- **Telegram gateway — HEALTHY.** PID `15220` alive (327 MB). Gateway state `running`; Telegram platform `connected` (polling). Fresh logs 06:18 today. **No `InvalidToken` / `rejected by the server`** in live logs (0 matches) → **no token rejection / no compromise**.
- **Live Telegram token — VALID** (`getMe` ok → @Ogaitchhermesbot). Home-root `~/.hermes/.env` copy still **revoked** (13-char stub, getMe **HTTP 404**) → dual-`.env` divergence persists (carried ≥4 cycles).
- **Credential exposure — CLEAN (PASS):** backup `.env` = **0** across all roots (backups/state-snapshots/hermes-backup/.openclaw); no `bws_cache.json`/`.secret_cache`; workspace AGENTS.md UTF-8 no BOM; main `~/.hermes/AGENTS.md` absent.
- **`google_token.json` ACL — PASS:** `SYSTEM:(I)(F)`, `BUILTIN\Administrators:(I)(F)`, `User:(I)(F)` only. No Everyone/Users.
- **NEW / ESCALATION — Nous Portal refresh token INVALID.** `invalid_grant` / "Invalid refresh token" at 05:46 today; `active_provider: nous` but credential pool terminally invalid → auxiliary Nous client **unavailable**. Promotional-model cost coverage down. Requires interactive re-auth (`hermes auth add nous` / `hermes model`). Prior cycle was only "expiry within 24h" (auto-refresh possible); this is now **failed refresh**, no auto-recovery.
- **Channel integrity — Telegram GOOD, WhatsApp disabled by config** (`platforms.whatsapp.enabled: false`). WhatsApp `disconnected` in gateway_state but this is intentional, not an unpaired failure.
- **One transient Telegram network oscillation** on 21/09 23:02–23:28 (dual-stack / IPv4 literal flapping, ConnectError/ConnectTimeout) — auto-recovered via sticky IP `149.154.166.110/.167.220`; no persistent outage, no crash (gateway-exit-diag clean, 0 exceptions).

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
| Stale home-root `~/.hermes/.env` token | **FAIL (carried, ≥4 cycles)** — revoked 13-char stub (getMe 404) |
| Home-workspace `.env`-reader one-offs | **FAIL (carried)** — 3 scripts: `tmp_send_afternoon_health.py`, `tmp_send_evening_checkin_0809.py`, `tmp_send_evening_checkin_1209.py` |
| `_tg_send.py` (live root) | **WARN** — documented generic Telegram sender that reads live `.env`; keep (legit utility) but it is a token-touchpoint |

### 2. Channel Integrity — Telegram GOOD, WhatsApp disabled
- **Telegram gateway** — ✅ **HEALTHY** (PID 15220 running, connected, logs fresh 06:18).
- **Live Telegram token** — ✅ valid (`getMe` ok).
- **Topic 20** — ✅ **verified reachable** (delivery probe msg_id 11402).
- **Chat `-1003784520976`** — ✅ supergroup forum (`type: supergroup`, `is_forum: true`).
- **No gateway crash:** `gateway-exit-diag.log` clean — 0 `asyncio.run.exception` / `ModuleNotFoundError`.
- **Cron delivery** — **56 jobs**: **30** target Telegram (6→topic 20, else → 14,4,26,1,2,16,28,8,10 + 2 DMs), **13 `local`** + **13 `origin`** silent (backup/DB-sync legit local; reminders/checkins silent → carried debt).
- **WhatsApp** — explicitly **disabled by config** (`enabled: false`), 18/09. Not a failure.

### 3. Recent Security Events — No token rejection
- **No `InvalidToken` / `Unauthorized` / `rejected by the server`** in live or rotated logs (0 matches).
- **NEW — Nous Portal terminal auth failure** at 05:46 (`invalid_grant`, "Invalid refresh token"). Escalated from prior "expiry within 24h, monitor". Requires interactive re-auth — promotional model cost coverage currently offline.
- **No rogue logins, no BOM/invisible-char injection** in configs; AGENTS.md clean.

## FAIL Findings
| ID | Severity | Description | Persistent? |
|----|----------|-------------|-------------|
| 1 | **high (NEW, escalation)** | **Nous Portal refresh token terminally invalid** — `active_provider: nous` but credential pool dead; auxiliary client offline. Re-auth required. | New this cycle |
| 2 | **high (≥4 cycles, carried)** | **Dual-`.env` divergence** — stale home-root `~/.hermes/.env` holds revoked Telegram token (getMe 404); live AppData root valid. Retire stale root. | Yes |
| 3 | **medium (carried)** | **Silent cron delivery** — 26/56 (`local`/`origin`); reminders/checkins silent (backup/DB-sync intentional). | Yes |
| 4 | **medium (carried)** | **3 stale mobile-`.env`-reader one-offs** in home-workspace (`tmp_send_*.py`). Delete. | Yes |

## CRITICAL Escalations
- None this cycle. No unresolved compromise / no token rejection.
- ⚠️ Nous escalation is the main new risk (functional credential, not leak) — non-interactive cron cannot re-auth.

## WARN Findings
1. **Nous Portal auth invalid** (see FAIL 1) — main operational impact: promotional-model coverage + auxiliary client down until re-auth.
2. **Telegram network oscillation** 21/09 23:02–23:28 (IPv4 literal flapping) — transient, auto-recovered via sticky IP; monitor if it recurs.
3. **Vercel MCP OAuth parked** (`OAuthNonInteractiveError`, 06:04 today) — needs interactive `hermes mcp login vercel`. Parking is safe (no credential leak).
4. **web_search backend `ddgs` not installed** — falls back to keyless rescue; operational, not credential.
5. **`_tg_send.py`** in live root — legitimate sender utility reading `.env`; token touchpoint (keep, but track).

## Remediation Priority
1. **HIGH (NEW)** — Re-auth Nous Portal interactively (`hermes auth add nous` / `hermes model`); restores auxiliary client + promo-model coverage. **Cannot be done from cron.**
2. **HIGH** — Retire/neutralize stale home-root `~/.hermes/.env`; single authoritative `.env` in live AppData root.
3. **MED** — Delete 3 stale `tmp_send_*.py` one-offs in home-workspace.
4. **MED** — Re-point 26 silent jobs (`local`/`origin`) to explicit topic targets where user-facing.
5. **LOW** — `hermes mcp login vercel` when interactive session available; install `ddgs` if keyless search fallback desired.

## Retention Note
7-day window (15–22/09): files exist 14,15,17,18,20,21 + today 22/09. **Removing `SECURITY_AUDIT_2026-09-14.md`** (>7 days, oldest). Kept 15,17,18,20,21 + today. One file per day.

## Trend Comparison (vs 21/09)
| Item | 21/09 (prior) | 22/09 (this run) | Trend |
|---|---|---|---|
| Gateway | UP (polling) | UP (PID 15220, connected) | Stable / good |
| Telegram token (live) | VALID | VALID | Stable / good |
| Backup `.env` | 0 | 0 | Good |
| Caches | clean | clean | Good |
| AGENTS.md | no BOM (main absent) | no BOM (main absent) | Good |
| google_token ACL | PASS | PASS | Good |
| Dual-`.env` divergence | present | present (stale revoked persists) | No change (carried) |
| **Nous Portal** | expiry within 24h (auto-refresh) | **refresh token INVALID (invalid_grant)** | **NEW FAIL — escalation** |
| Vercel MCP | 200 OK (resolved) | OAuth parked (non-interactive) | WARN (needs interactive login) |
| WhatsApp | disabled-by-config | disabled-by-config (confirmed) | Stable |
| Topic 20 | documented reachable | **probe-confirmed (msg 11402)** | Verified good |

*Retention: removed 14/09 (7 days old); kept 15,17,18,20,21/09 + today.*