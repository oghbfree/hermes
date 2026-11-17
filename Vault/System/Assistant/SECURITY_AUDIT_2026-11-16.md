# Security Audit — 2026-11-16

**Generated:** 2026-11-16 07:00 by Hermes security-audit cron (*security-policy-check* job)
**Scope:** Credential exposure · Channel integrity · Recent security events
**Overall: 🟢 HEALTHY (two new/returning WARNs)** — Telegram fully healthy: live 46-char token VALID via direct `getMe` (@Ogaitchhermesbot); chat `-1003784520976` confirmed supergroup + forum. Gateway up (PID 28532). WhatsApp bridge held from 11-15 (creds.json present, agent DMs flushing in gateway.log). No backup-`.env` copies (0), no token exposure, no credential caches, no InvalidToken, no provider-key failures. NEW this cycle: **Nous Portal logged out/revoked** (401, refresh-token-reuse revocation) and the **multiplex duplicate-credential warning reappeared** across default/content-buddy/sat-nav. Remaining WARNs: dual-root token divergence, 24/54 silent cron targets, 2 dead-thread jobs.

---

## 1. Credential Exposure

| Check | Status | Detail |
|-------|--------|--------|
| Telegram bot token (live, AppData root) | ✅ PASS | `getMe` → `{"ok":true}` (@Ogaitchhermesbot, 46-char live token, prefix 8277). Valid via direct API. |
| Stale token (`~/.hermes/.env`) | ⚠️ WARN | Still holds 13-char dead placeholder (`getMe` → 404). Live gateway uses AppData root. Persistent dual-root divergence debt (12+ cycles). |
| Backup `.env` copies | ✅ PASS | **0** across `~/.hermes` + AppData backups, state-snapshots, `~/hermes-backup`, `~/.openclaw`. Sustained clean. |
| Credential caches | ✅ PASS | No `bws_cache.json`, `.secret_cache`, or token-cache files in either root. |
| `.env`-reader scripts | ⚠️ WARN | No new leaks in `workspace/*.py`. Runtime cron senders (`workspace/scripts/ghana_telegram_report.py`, `memory_review_telegram.py`, `h_evening_checkin_send.py`, `mum_evening_checkin.py`) still read `.env` at runtime via `Path.home()/'.env'` — tokens transiently enter process state, none at rest. |
| `google_token.json` ACL (both roots) | ✅ PASS | SYSTEM / Administrators / User only (F). No Everyone/Users. |
| `.env` ACL (both roots) | ✅ PASS | SYSTEM / Administrators / User only (F). |
| `auth.json` ACL | ✅ PASS | SYSTEM / Administrators / User only (F). |
| AGENTS.md BOM / invisible chars | ✅ PASS | workspace AGENTS.md: UTF-8, no BOM (CRLF). Main `~/.hermes/AGENTS.md` absent. |
| `allow_all_users` (config.yaml) | ⚠️ WARN | `GATEWAY_ALLOW_ALL_USERS: true` broadens attack surface; confirm intentional. |

## 2. Channel Integrity

| Channel | Status | Detail |
|---------|--------|--------|
| Gateway process | ✅ PASS | Running (PID **28532**, python 3.14.9, started 11-15 10:20 via clean `gateway.start`). gateway.log fresh (last write 06:56 today). 0 crash-loop entries. Serves 5 profiles (coach, content-buddy, harold, sat-nav, taiwah). |
| Telegram adapter | ✅ PASS | Valid token; getChat confirms supergroup + forum. Polling `getUpdates progressing` after transient timeouts 06:40–06:48 (recovered via sticky IPv4 149.154.166.110). Host-level network blips, not channel outage. |
| **WhatsApp** | ✅ **PASS (held)** | creds.json live (**11-16 07:02**, 3.4 KB); gateway flushing WhatsApp agent DMs today (06:55). Bridge stable since 11-15 recovery. |
| Topic 20 (Memory Review) | ✅ PASS | Supergroup forum target; 5 jobs deliver to thread 20 (this job included). Verified below by direct delivery. |
| Cron silent delivery | ⚠️ WARN | **24/54** jobs deliver to `origin` (16) or `local` (8) — output never reaches a user; 30 topic-targeted. Slight change from 25/56 (job count now 54). |
| Defunct-thread jobs (`telegram:123286468`) | ⚠️ WARN | **2** jobs (Mom Morning + Mom Evening Exercise Reminders) still target a dead DM thread. Not remediated (persistent). |
| Multiplex duplicate-credential | ⚠️ WARN (RETURNED) | `hermes gateway status` again flags default/content-buddy/sat-nav sharing the same `TELEGRAM_BOT_TOKEN`. Was reported resolved 11-15; warning present again this cycle. Non-blocking (parked adapters) but needs a fix decision. |

## 3. Recent Security Events

- ✅ **No `InvalidToken` / Telegram token rejection** this window. Live token accepted via direct `getMe`.
- ✅ **No provider 401/403/402/429 / InvalidKey failures** this window. OpenRouter reachable (models endpoint 200, key present).
- ✅ **No breach / unauthorized-access markers** (no "Blocked unauthorized user", no unexpected paired devices).
- ⚠️ **Nous Portal logged out / revoked (NEW).** `hermes status` reports: *"Nous Portal detected refresh-token reuse and revoked this session"*; `hermes auth status nous` → logged out (no access token). Root cause per status: an external process (monitoring/self-heal hook or another install sharing `~/.hermes/auth.json`) called the OAuth refresh endpoint without persisting the rotated token. No operational impact this cycle — model runs on OpenRouter, not Nous — but flag as credential-state drift requiring `hermes auth add nous` to restore.
- ⚠️ Host-level network flakiness (Telegram IPv4 timeouts/re-walks 06:40–06:48 today) — consistent with DNS/networking, not a targeted event.

---

## Trend vs 2026-11-15

| Item | 11-15 | 11-16 | Direction |
|------|-------|-------|-----------|
| Telegram token (live) | PASS | PASS | No Change |
| Gateway | PASS (PID 2272) | PASS (PID 28532) | Stable |
| WhatsApp | PASS (RECOVERED) | PASS (held) | No Change |
| Nous Portal | — (not noted) | **logged out/revoked** | **NEW WARN** |
| Multiplex dup-credential | RESOLVED | WARN (returned) | **REGRESSION** |
| Dual-root token divergence | WARN | WARN | No Change (persistent, 12+) |
| Backup `.env` copies | PASS (0) | PASS (0) | No Change |
| `.env`-reader scripts | runtime remain | runtime remain (workspace clean) | No Change |
| Cron silent delivery | 25/56 | 24/54 | No Change (count drift) |
| `telegram:123286468` thread loss | WARN (2) | WARN (2) | Not remediated |
| `google_token.json` ACL | PASS | PASS | No Change |

**Persistent security debt (3+ cycles):** dual-root token divergence (12+), 24/54 silent cron targets, `telegram:123286468` thread loss. **New this cycle:** Nous Portal revocation; **regression:** multiplex duplicate-credential warning returned.

## 🔧 Remediation Priority
1. **Restore Nous Portal** — `hermes auth add nous` (new event this cycle; revoke came from an external process reusing the refresh token). Audit what called it.
2. **Delete stale `~/.hermes/.env` placeholder** → single authoritative AppData root (persistent debt, 12+ cycles).
3. **Resolve multiplex duplicate-credential** — give content-buddy/sat-nav own tokens or route via `gateway.profile_routes` (returned regression).
4. Fix the 2 Mom exercise-reminder jobs to the Nursing coord thread (424) — `123286468` target is dead.
5. Re-review 24/54 silent cron targets (`origin`/`local`).

## Retention Note
Rolling 7-day window enforced. Prior files present: 11-07 … 11-12, 11-15 (7). This 11-16 audit added; oldest (11-06 absent) will drop on next rotation.

---
*Generated 2026-11-16 by Hermes security-audit cron.*
