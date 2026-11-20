# Security Audit — 2026-11-19

**Generated:** 2026-11-19 07:00 by Hermes security-audit cron (*security-policy-check* job)
**Scope:** Credential exposure · Channel integrity · Recent security events
**Overall: 🟡 STABLE (WARNs persist; 1 channel-state change — WhatsApp adapter now explicitly disabled).** Telegram fully healthy: live 46-char token VALID via direct `getMe` (@Ogaitchhermesbot); gateway up (PID 25084), polling confirmed healthy (11-19 01:11, generation 1). **WhatsApp state CHANGE:** `platforms.whatsapp.enabled: false` in config.yaml now explicitly disables the adapter despite a live creds.json (11-18 10:40) — adapter will not start (was reported ACTIVE on 11-17). **Nous Portal still revoked/logged-out (persistent, unremediated).** No backup-`.env` copies (0), no credential caches, no current-window InvalidToken, no provider-key failures, no breach markers. Remaining WARNs: dual-root token divergence, 24/55 silent cron targets, 2 dead-thread jobs, multiplex duplicate-credential, `.env`-reader runtime scripts, `allow_all_users`, cron receipt recovery backlog (483 deferred — growing).

---

## 1. Credential Exposure

| Check | Status | Detail |
|-------|--------|--------|
| Telegram bot token (live, AppData root) | ✅ PASS | `getMe` → `{"ok":true}` (@Ogaitchhermesbot, 46-char live token, id 8277244378). Valid via direct API. |
| Stale token (`~/.hermes/.env`) | ⚠️ WARN | Still holds dead placeholder (prefix 827724). Live gateway uses AppData root. Persistent dual-root divergence debt. |
| Backup `.env` copies | ✅ PASS | **0** across `~/.hermes` + AppData backups, state-snapshots, `~/hermes-backup`, `~/.openclaw`. Sustained clean. |
| Credential caches | ✅ PASS | No `bws_cache.json`, `.secret_cache`, or token-cache files in either root. |
| `.env`-reader scripts | ⚠️ WARN | 4 runtime cron senders (`ghana_telegram_report.py`, `memory_review_telegram.py`, `h_evening_checkin_send.py`, `mum_evening_checkin.py`) read `.env` at runtime — transient process-state exposure, none at rest. Plus historical dated checkin scripts (Aug–Sep) under Vault/family/*/health. |
| `google_token.json` ACL | ✅ PASS | SYSTEM / Administrators / User only (F). |
| `.env` ACL (both roots) | ✅ PASS | SYSTEM / Administrators / User only (F). |
| `auth.json` ACL | ✅ PASS | SYSTEM / Administrators / User only (F). |
| AGENTS.md BOM / invisible chars | ✅ PASS | workspace AGENTS.md: UTF-8, no BOM. Main `~/.hermes/AGENTS.md` absent. |
| `allow_all_users` (config.yaml) | ⚠️ WARN | `allow_all_users: true` grants every sender on every platform access; bridged to `GATEWAY_ALLOW_ALL_USERS`. Confirm intentional. |

## 2. Channel Integrity

| Channel | Status | Detail |
|---------|--------|--------|
| Gateway process | ✅ PASS | Running (PID **25084**, python 3.14.9). Telegram polling healthy (11-19 01:11, generation 1). No crash-loop signatures — gateway-exit-diag last entry 11-16 clean. Serves 5 profiles (coach, content-buddy, harold, sat-nav, taiwah). |
| Telegram adapter | ✅ PASS | Valid token; polling confirmed healthy. Transient IPv4 flakiness this morning (sticky 149.154.166.110 timeouts at 05:39/05:59/06:32, each recovered to api.telegram.org or alternate IP) — host-level network blips, recovered, not an outage. |
| **WhatsApp** | ⚠️ **STATE CHANGE (adapter OFF)** | `platforms.whatsapp.enabled: false` in config.yaml now explicitly disables the adapter (`credentials found in the environment (WHATSAPP_ENABLED) will NOT start its adapter`). A live creds.json exists (11-18 10:40, 3.4 KB) but the adapter is disabled, so WhatsApp will not deliver. Was reported **ACTIVE** on 11-17 — intentional disable or regression, needs confirmation. |
| Topic 20 (Memory Review) | ✅ PASS | Supergroup forum target; 5 jobs deliver to thread 20 (this job included). Token valid → delivery will succeed. |
| Cron silent delivery | ⚠️ WARN | **24/55** jobs deliver to `origin` (16) or `local` (8) — output never reaches a user; 31 topic-targeted. Persistent. |
| Defunct-thread jobs (`telegram:123286468`) | ⚠️ WARN | **2** jobs (Mom Morning + Mom Evening Exercise Reminders) still target a dead DM thread. Not remediated (persistent). |
| Multiplex duplicate-credential | ⚠️ WARN | Gateway status flags default/content-buddy and default/sat-nav sharing the same `TELEGRAM_BOT_TOKEN`. Persistent. |
| Cron receipt recovery | ⚠️ WARN (GROWING) | **483 deferred receipts** total; today (07:02) 3+ admissions JSON receipts repeatedly deferred. Scheduled-delivery bookkeeping backlog — monitor; may transiently delay cron runs. |

## 3. Recent Security Events

- ✅ **No `InvalidToken` / Telegram token rejection** this window — validated live via `getMe` (2026-11-19). Historical only (Oct 1/6/13 old-root rejections of the dead 827724 token, out of window / stale root).
- ✅ **No provider 401/403/402/429 / InvalidKey failures** today (0 in gateway.log for 11-18/19; API calls via openrouter completing normally).
- ✅ **No breach / unauthorized-access markers** today (none in gateway.log/errors.log for 11-18/19).
- ⚠️ **Nous Portal still revoked/logged-out (PERSISTENT — not remediated).** `status --full`: "Nous Portal detected refresh-token reuse and revoked this session." External process called the OAuth refresh endpoint without persisting the rotated token. No operational Model impact (default runs on custom/OpenRouter). Requires `hermes auth add nous`; audit `auth.json` access before restore.
- ⚠️ Host-level network flakiness (Telegram IPv4 re-walks, recovered) — consistent with DNS/networking, not a targeted event.

---

## Trend vs 2026-11-17

| Item | 11-17 | 11-19 | Direction |
|------|-------|-------|-----------|
| Telegram token (live) | PASS | PASS | No Change |
| Gateway | PASS (PID 25084) | PASS (PID 25084) | Stable |
| **WhatsApp** | PASS (**ACTIVE**) | **⚠️ adapter OFF** (`platforms.whatsapp.enabled:false`) | **CHANGE (disabled)** |
| Nous Portal | logged out/revoked | logged out/revoked | **Unremediated** |
| Multiplex dup-credential | WARN | WARN | No Change |
| Dual-root token divergence | WARN | WARN | No Change (persistent) |
| Backup `.env` copies | PASS (0) | PASS (0) | No Change |
| `.env`-reader scripts | runtime remain | runtime remain | No Change |
| Cron silent delivery | 24/54 | 24/55 | No Change (persistent) |
| `telegram:123286468` thread loss | WARN (2) | WARN (2) | Not remediated |
| Cron receipt recovery | WARN (minor, 10x) | WARN (**483 deferred, growing**) | **WORSENED** |
| `google_token.json` ACL | PASS | PASS | No Change |

**Persistent security debt (3+ cycles):** dual-root token divergence, 24/55 silent cron targets, `telegram:123286468` thread loss. **Unremediated event:** Nous Portal revocation. **Change:** WhatsApp adapter now explicitly disabled in config.

## 🔧 Remediation Priority
1. **Confirm WhatsApp disable intent** — `platforms.whatsapp.enabled: false` turns the adapter off despite live creds.json. If intentional (held bridge), fine; if accidental regression from 11-17 ACTIVE, re-enable. Highest-priority change this cycle.
2. **Restore Nous Portal** — `hermes auth add nous`; audit what external process calls the refresh endpoint (persistent).
3. **Delete stale `~/.hermes/.env` placeholder token** → single authoritative AppData root (persistent debt).
4. **Resolve multiplex duplicate-credential** — give content-buddy/sat-nav own tokens or route via `gateway.profile_routes`.
5. Fix the 2 Mom exercise-reminder jobs to the Nursing coord thread (424) — `123286468` target is dead.
6. Clear cron receipt-recovery backlog (483 deferred admissions JSONs).
7. Re-review 24/55 silent cron targets (`origin`/`local`).

## Retention Note
Rolling 7-day window enforced. Kept 11-12 → 11-19 (7). Deleted 11-11 (outside window).

---
*Generated 2026-11-19 by Hermes security-audit cron.*