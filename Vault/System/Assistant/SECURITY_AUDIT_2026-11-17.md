# Security Audit — 2026-11-17

**Generated:** 2026-11-17 07:00 by Hermes security-audit cron (*security-policy-check* job)
**Scope:** Credential exposure · Channel integrity · Recent security events
**Overall: 🟢 HEALTHY (stable WARNs; no new FAILs)** — Telegram fully healthy: live 46-char token VALID via direct `getMe` (@Ogaitchhermesbot); chat `-1003784520976` confirmed supergroup + forum. Gateway up and stable (PID 25084, no crash loop, multiple clean `--replace` restarts 11-16 evening). **WhatsApp ACTIVE (full recovery sustained)** — creds.json live (11-17 07:00, matching this-morning DM flush in gateway.log). Nous Portal **still revoked/logged-out (2nd consecutive cycle, not remediated)**. No backup-`.env` copies (0), no credential caches, no current-window InvalidToken, no provider-key failures, no breach markers. Remaining WARNs: dual-root token divergence, 24/54 silent cron targets, 2 dead-thread jobs, multiplex duplicate-credential (returned), `.env`-reader runtime scripts, `allow_all_users`.

---

## 1. Credential Exposure

| Check | Status | Detail |
|-------|--------|--------|
| Telegram bot token (live, AppData root) | ✅ PASS | `getMe` → `{"ok":true}` (@Ogaitchhermesbot, 46-char live token). Valid via direct API. |
| Stale token (`~/.hermes/.env`) | ⚠️ WARN | Still holds 13-char dead placeholder (prefix 827724) — dead. Live gateway uses AppData root. Persistent dual-root divergence debt (13+ cycles). |
| Backup `.env` copies | ✅ PASS | **0** across `~/.hermes` + AppData backups, state-snapshots, `~/hermes-backup`, `~/.openclaw`. Sustained clean. |
| Credential caches | ✅ PASS | No `bws_cache.json`, `.secret_cache`, or token-cache files in either root. |
| `.env`-reader scripts | ⚠️ WARN | No new at-rest leaks found in `workspace/*.py` (matches 11-16 set). Runtime cron senders (`ghana_telegram_report.py`, `memory_review_telegram.py`, `h_evening_checkin_send.py`, `mum_evening_checkin.py`) still read `.env` at runtime via `Path.home()/'.env'` — transient process-state exposure, none at rest. |
| `google_token.json` ACL | ✅ PASS | SYSTEM / Administrators / User only (F). No Everyone/Users. |
| `.env` ACL (both roots) | ✅ PASS | SYSTEM / Administrators / User only (F). |
| `auth.json` ACL | ✅ PASS | SYSTEM / Administrators / User only (F). |
| AGENTS.md BOM / invisible chars | ✅ PASS | workspace AGENTS.md: UTF-8, no BOM (CRLF). Main `~/.hermes/AGENTS.md` absent. |
| `allow_all_users` (config.yaml) | ⚠️ WARN | `GATEWAY_ALLOW_ALL_USERS: true` (+ `allow_all_users: true` x2) broadens attack surface; confirm intentional. |

## 2. Channel Integrity

| Channel | Status | Detail |
|---------|--------|--------|
| Gateway process | ✅ PASS | Running (PID **25084**, python 3.14.9). Clean `gateway.start` 11-16 20:48 (--replace). **0** `asyncio.run.exception` entries — no crash loop. Serves 5 profiles (coach, content-buddy, harold, sat-nav, taiwah). |
| Telegram adapter | ✅ PASS | Valid token; getChat confirms supergroup + forum. Transient IPv4 recovery 06:42 (149.154.166.110→.220) — host-level network blip, recovered, not a channel outage. |
| **WhatsApp** | ✅ **PASS (ACTIVE)** | creds.json live (**11-17 07:00**, 3.4 KB); gateway flushed WhatsApp agent DM this morning (06:39, 07:01, server_ack + delivered). **Full sustained recovery** — strong (held 11-15→16, now actively delivering). |
| Topic 20 (Memory Review) | ✅ PASS | Supergroup forum target; 5 jobs deliver to thread 20 (this job included). |
| Cron silent delivery | ⚠️ WARN | **24/54** jobs deliver to `origin` (16) or `local` (8) — output never reaches a user; 30 topic-targeted. Persistent (13+ cycles). |
| Defunct-thread jobs (`telegram:123286468`) | ⚠️ WARN | **2** jobs (Mom Morning + Mom Evening Exercise Reminders) still target a dead DM thread. Not remediated (persistent). |
| Multiplex duplicate-credential | ⚠️ WARN (RETURNED) | `hermes gateway status` again flags default/content-buddy/sat-nav sharing the same `TELEGRAM_BOT_TOKEN`. Was flagged 11-16 too; needs a fix decision (parked adapters only, non-blocking). |
| Cron receipt recovery | ⚠️ WARN (NEW-MINOR) | errors.log 05:50–05:59 today: repeated `Cron receipt recovery deferred: .../admissions/...json` (10x). Stuck scheduling receipt — monitor; may transiently delay a cron run. |

## 3. Recent Security Events

- ✅ **No `InvalidToken` / Telegram token rejection** this window (validated live via `getMe`). Only historical 401 is 11-08 desktop.log `fleet-roster` — unrelated, outside window.
- ✅ **No provider 401/403/402/429 / InvalidKey failures** today (0 in gateway.log for 11-17).
- ✅ **No breach / unauthorized-access markers** today (none in gateway.log for 11-17).
- ⚠️ **Nous Portal still revoked/logged-out (PERSISTENT — 2nd cycle, not remediated).** `hermes status`: "Nous Portal detected refresh-token reuse and revoked this session." Root cause: an external process (monitoring/self-heal hook or another install sharing `~/.hermes/auth.json`) called the OAuth refresh endpoint without persisting the rotated token. No operational impact (model runs on OpenRouter/custom, not Nous) but credential-state drift. Requires `hermes auth add nous`; audit `auth.json` access before restore.
- ⚠️ Host-level network flakiness (Telegram IPv4 re-walk 06:42, recovered) — consistent with DNS/networking, not a targeted event.

---

## Trend vs 2026-11-16

| Item | 11-16 | 11-17 | Direction |
|------|-------|-------|-----------|
| Telegram token (live) | PASS | PASS | No Change |
| Gateway | PASS (PID 28532) | PASS (PID 25084) | Stable (restart 11-16) |
| WhatsApp | PASS (held) | PASS (**ACTIVE**) | **IMPROVED** |
| Nous Portal | logged out/revoked | logged out/revoked | **Unremediated (2nd cycle)** |
| Multiplex dup-credential | WARN (returned) | WARN | No Change |
| Dual-root token divergence | WARN | WARN | No Change (persistent, 13+) |
| Backup `.env` copies | PASS (0) | PASS (0) | No Change |
| `.env`-reader scripts | runtime remain | runtime remain | No Change |
| Cron silent delivery | 24/54 | 24/54 | No Change (persistent) |
| `telegram:123286468` thread loss | WARN (2) | WARN (2) | Not remediated |
| `google_token.json` ACL | PASS | PASS | No Change |
| Cron receipt recovery | — | WARN (minor) | **NEW-MINOR** |

**Persistent security debt (3+ cycles):** dual-root token divergence (13+), 24/54 silent cron targets, `telegram:123286468` thread loss. **Unremediated event:** Nous Portal revocation (2nd cycle). **Improvement:** WhatsApp now ACTIVE (full sustained bridge).

## 🔧 Remediation Priority
1. **Restore Nous Portal** — `hermes auth add nous`; audit what external process calls the refresh endpoint (unremediated 2nd cycle).
2. **Delete stale `~/.hermes/.env` placeholder token** → single authoritative AppData root (persistent debt, 13+ cycles).
3. **Resolve multiplex duplicate-credential** — give content-buddy/sat-nav own tokens or route via `gateway.profile_routes` (returned regression).
4. Fix the 2 Mom exercise-reminder jobs to the Nursing coord thread (424) — `123286468` target is dead.
5. Re-review 24/54 silent cron targets (`origin`/`local`).

## Retention Note
Rolling 7-day window enforced. Kept 11-11 → 11-17 (7). Deleted 11-08, 11-09, 11-10 (outside window).

---
*Generated 2026-11-17 by Hermes security-audit cron.*