# Security Audit — 18 September 2026

**Date:** 18/09/2026 (DMY dd/mm/yy)
**Run by:** internal cron / Hermes Agent (default profile) — security-policy-check
**Overall:** **STABLE / LOW** — **Telegram gateway healthy**, no credential exposure, no active compromise. Two config-level WARNS appeared this cycle (`allow_all_users: true` confirmed; WhatsApp now **explicitly disabled** with creds.json present). Persistent carried item: dual-`.env` divergence (stale revoked token in home root). **No active credential compromise.**

**Report path:** `C:\Users\User\.hermes\workspace\Vault\System\Assistant\SECURITY_AUDIT_2026-09-18.md`
**Telegram delivery target:** Topic 20 (`-1003784520976:20`, "Memory Review") — reachable (chat=supergroup, `is_forum:true` confirmed via getChat; token valid; security-audit job deliver=`telegram:-1003784520976:20`).

---

## Summary
- **CRITICAL PRIOR (15/09) — STILL RESOLVED.** Live-root Telegram token `8277244…` is **valid** (`getMe` ok → @Ogaitchhermesbot, id 8277244378). Gateway connected today 04:29 (`Connected to Telegram (polling mode)`), housekeeping + kanban dispatcher running, ESTABLISHED TCP to Telegram API (149.154.167.92:443). Live log fresh (04:51 today); one transient IP fail 04:51 auto-recovered via `api.telegram.org`. **No `InvalidToken`/rejection in today's live or rotated logs** (agent.log.1/errors.log.1 clean of token events).
- **Credential exposure — CLEAN (PASS):** backup `.env` = **0** across all 6 roots (backups/hermes-backup/state-snapshots/.openclaw/AppData backups/snapshots); no `bws_cache.json`/`.secret_cache`; AGENTS.md no BOM (UTF-8, CRLF); no other raw API keys found hardcoded in config (only masked `fc-…**52e6` values).
- **WhatsApp — STATUS CHANGE (IMPROVED): now explicitly disabled** in config `platforms.whatsapp.enabled: false`; `creds.json` now present (2951 B, 15/09) but adapter won't start by config. Log warns env `WHATSAPP_ENABLED` no longer overrides explicit disable → **config/env drift WARN**; resolve intent (enable+pair, or remove env key). Prior 100+ cycle "unpaired/unconnectable" FAIL is now a **deliberate disable** — reclassify.
- **New this cycle — Vercel MCP 401 Unauthorized (WARN):** recurring `POST https://mcp.vercel.com → 401` on 13, 14, 15, 16/09 in rotated agent.log.1 — Vercel MCP credential rejected. Individual provider credential; WARN (not multi-provider). Verify/refresh Vercel MCP token.
- **Config hardening WARN — `allow_all_users: true`** at config lines 616 (whatsapp), 718 (api_server) + `GATEWAY_ALLOW_ALL_USERS: true` (839) — grants every sender on every platform access. Flag for review; restrict to allow-list if inbound surface matters.
- **Nous Portal key expiry 07:29 today (~19 min)** — auto-refresh enabled; transport healthy (gateway up). Monitor post-expiry.

## Findings by Area

### 1. Credential Exposure — CLEAN
| Item | Status |
|------|--------|
| `bws_cache.json` / `.secret_cache` | **PASS** — absent |
| Backup `.env` (all 6 roots) | **PASS** — 0 |
| AGENTS.md (workspace) | **PASS** — UTF-8, no BOM |
| Active Telegram token (live root) | **PASS** — `8277244…` valid (@Ogaitchhermesbot) |
| Stale home-root `~/.hermes/.env` token | **FAIL (carried, ≥3 cycles)** — still holds revoked `827724…1UJE` (returns getMe 404) + other valid keys |
| Raw keys in config.yaml | **PASS** — only masked `fc-3a3…52e6`; no `sk-`/`xai-`/full tokens |
| `.env`-reader scripts (workspace/home-root) | **FAIL/WARN (carried)** — 29 live Python files read `.env` directly (operational care/send/checkin scripts + one-off `tmp_send_*`/`_token_test`); token leak surface |

### 2. Channel Integrity — Telegram GOOD; WhatsApp intentionally off
- **Telegram gateway** — ✅ **HEALTHY**: connected polling mode 04:29 today; PID with ESTABLISHED TCP to Telegram; log fresh (04:51). One transient IP fail 04:51 auto-`recovered` via hostname path.
- **Active Telegram token** — ✅ valid (`getMe` ok).
- **Chat `-1003784520976`** — ✅ type=supergroup, `is_forum:true ("Agent Hermes") — topic posting valid; topic 20 confirmed exist (`:20` thread_id; 6 jobs target it incl. security-audit).
- **WhatsApp** — ⚠️ **explicitly disabled** (`platforms.whatsapp.enabled: false`) with `creds.json` present. Drift: env `WHATSAPP_ENABLED` still set → adapter won't start. Decide explicitly: (a) enable+pair, (b) remove env key.
- **Cron delivery** — **55 jobs (44 active)**: **30** target Telegram topics (6→topic 20; 14;4;26;1;2;16;28;8;10; DMs), **25 silent** (13 `local` + 12 `origin` — local sync/backups legit; checkin/reminder silent → carried debt).
- **Vercel MCP** — ⚠️ **401 Unauthorized** on mcp.creds → channel integrity warn (credential).

### 3. Recent Security Events — No token rejection today (4× confirmed 31/08–15/09, RESOLVED)
- **`rejected by the server` on `827724…1UJE`** at 31/08, 05/09, 09/09, 15/09 — continued-treat as historical compromise **RESOLVED**; valid replacement (8277244…) active since ~16/09.
- **No `InvalidToken`** in today's live/rotated logs (clean).
- **recurring Vercel MCP 401** 13–16/09 (above) — WARN.
- **No other unauthorized access / breach markers** — no rogue logins, no zero-width/BOM injection in configs; AGENTS.md clean.

## FAIL Findings
| ID | Severity | Description | Persistent? |
|----|----------|-------------|-------------|
| 1 | **high (≥3 cycles, carried)** | **Dual-`.env` divergence** — stale home-root `~/.hermes/.env` still holds revoked `827724…1UJE` + valid keys; live root has valid token. Retire stale root. | Yes |
| 2 | **high (carried)** | **WhatsApp off + drift** — disabled-by-config prevents adapter; creds present; env-key orphaned. | Yes (evolved) |
| 3 | **medium (carried)** | **Silent cron delivery** — 25/55 (`local`/`origin`); reminders/checkins silent. | Yes |
| 4 | **medium (carried)** | **`.env`-reader scripts** — 29 live + one-offs (`tmp_send_*`, `_token_test_*`) read `.env` directly. Clean up one-offs. | Yes |

## CRITICAL Escalations
- None this cycle. 15/09 CRITICAL (telegram token revoked/gateway down) remains **RESOLVED** — valid token live, gateway healthy, no new escalation.

## WARN Findings
1. **`allow_all_users: true`** (2× config + env override) — config-hardening; restrict to allow-list if inbound surface matters.
2. **Vercel MCP 401 Unauthorized** (13,14,15,16/09) — verify/refresh credential.
3. **WhatsApp config/env drift** — decide enable+pair vs disable+remove env key.
4. **Nous Portal key expiry 07:29 today** (~19m) — auto-refresh monitor.

## Remediation Priority
1. **HIGH** — Retire/neutralize stale home-root `~/.hermes/.env`; remove revoked token artifact (single authoritative `.env` in live root).
2. **HIGH** — Resolve WhatsApp intent: enable+pair OR remove `WHATSAPP_ENABLED` env/disable (currently dangling).
3. **MED** — Refresh Vercel MCP token; investigate 401 root cause (credential rotation or expired).
4. **MED** — Review `allow_all_users: true` → restrict to allowed sender allow-list.
5. **MED** — Delete one-off `.env` readers (`tmp_send_*`, `_token_test_*`); gate intake; re-point 25 silent jobs.

## Retention Note
- Applied 7-day retention: **kept** 11, 13, 14, 15, 17/09 + today (18/09). Oldest 11/09 = 7 days. One file per day maintained at `Vault\System\Assistant\`. No files removed this cycle (none older than 7 days). Note: file names in this dir use DMY; a stray `SECURITY_AUDIT_2026-09-09.md` was placed at a wrong sub-path earlier this run and relocated to the correct `Vault\System\Assistant\SECURITY_AUDIT_2026-09-18.md`.

## Trend Comparison (vs 17/09)
| Item | 17/09 (prior) | 18/09 (this run) | Trend |
|---|---|---|---|
| Gateway | UP (PID 11700, polling OK) | UP (connected 04:29, ESTABLISHED TCP; fresh log) | Stable / good |
| Telegram token | VALID (`8277244…`) | VALID (`getMe` ok) | Stable / good |
| Backup `.env` | 0 | 0 | Good |
| Caches | clean | clean | Good |
| AGENTS.md | no BOM | no BOM | Good |
| WhatsApp | unpaired/unconnectable | **explicitly disabled** + creds present | **Changed / config intent** |
| Dual-`.env` divergence | present | present (stale revoked persists) | No change (carried) |
| Vercel MCP 401 | — (new) | present 13–16/09 | **New WARN** |
| allow_all_users | — | present (2× + env) | **New WARN** |
| Nous key expiry | 08:02 (17/09) | 07:29 today | Stable (auto-refresh) |

*Retention: kept 11,13,14,15,17/09 + today (all within 7-day window; 11/09 oldest = 7 days).*