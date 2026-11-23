# Security Audit — 2026-11-22

**Generated:** 2026-11-22 07:01 by Hermes security-audit cron (*security-policy-check* job)
**Scope:** Credential exposure · Channel integrity · Recent security events
**Overall: 🟡 STABLE** — Live Telegram token (AppData root) VALID via direct `getMe`; gateway PID 25084 alive with 2 ESTABLISHED TCP connections to Telegram. Topic 20 confirmed supergroup+forum (5 jobs target it). No current-window InvalidToken, no provider rejections, no breach markers, no backup-`.env` copies, no credential caches. Persistent WARNs unchanged: dual-root token divergence, 24/55 silent cron targets, 2 dead-thread jobs, Nous Portal revocation, WhatsApp adapter disabled, `allow_all_users: true`, `.env`-reader runtime senders, multiplex duplicate-credential.

---

## 1. Credential Exposure

| Check | Status | Detail |
|-------|--------|--------|
| Telegram bot token (live, AppData root) | ✅ PASS | `getMe` → `{"ok":true}` (@Ogaitchhermesbot, live token id 8277244378). Valid via direct API. |
| Stale token (`~/.hermes/.env`) | ⚠️ WARN | Dead placeholder (404 on getMe). Live gateway uses AppData root. Persistent dual-root divergence. |
| Backup `.env` copies | ✅ PASS | **0** across `~/.hermes/backups`, `state-snapshots`, `~/hermes-backup`, `~/.openclaw`. Sustained clean. |
| Credential caches | ✅ PASS | No `bws_cache.json` / `.secret_cache` in either root. |
| `.env`-reader scripts | ⚠️ WARN | **4** runtime workspace senders read tokens at process time (transient, none at rest): `workspace/scripts/{ghana_telegram_report, h_evening_checkin_send, memory_review_telegram, mum_evening_checkin}.py`. No independent leak scripts at rest. |
| `google_token.json` ACL | ✅ PASS | `icacls`: SYSTEM / Administrators / User (F) only. No Everyone/BUILTIN\Users. |
| AGENTS.md BOM / invisible chars | ✅ PASS | workspace AGENTS.md: UTF-8, no BOM. Main `~/.hermes/AGENTS.md` absent. |
| `allow_all_users` (config.yaml) | ⚠️ WARN | `allow_all_users: true` confirmed (lines 366, 876). Confirm intentional. |

## 2. Channel Integrity

| Channel | Status | Detail |
|---------|--------|--------|
| Gateway process | ✅ PASS | Running (PID **25084**), 2 ESTABLISHED TCP conns to Telegram (149.154.166.110:443). Serves coach, content-buddy, harold, sat-nav, taiwah. |
| Telegram adapter | ✅ PASS | Valid token via getMe; active live connections. Cold `gateway.log` (Oct 13 — new instance logs to AppData) shows 0 new crash signatures; live AppData logs fresh 2026-11-22. |
| **WhatsApp** | ⚠️ WARN | creds.json present (Nov 21, AppData root); adapter reported OFF (intent unconfirmed per 11-18 cycle). |
| Topic 20 (Memory Review) | ✅ PASS | `getChat` → `type: supergroup`, `is_forum: true`. **5 jobs** deliver to thread 20 (this job included). Token valid → delivery will succeed. |
| Cron silent delivery | ⚠️ WARN | **24/55** jobs → `origin` (16) or `local` (8); 31 telegram-targeted. Persistent, unchanged. |
| Defunct-thread jobs (`telegram:123286468`) | ⚠️ WARN | **2** jobs (`aebf7e736923`, `3ebd2dc4487c` — Mom Morning + Mom Evening) target dead DM thread. Not remediated. |
| Multiplex duplicate-credential | ⚠️ WARN | default/content-buddy and default/sat-nav share same `TELEGRAM_BOT_TOKEN`. Persistent. |

## 3. Recent Security Events

- ✅ **No `InvalidToken` / Telegram token rejection this window** — live token validated via `getMe` (2026-11-22). Historic InvalidToken entries present only in stale logs (Oct 13) — not current-window.
- ✅ **No provider 401/403/402/429 / InvalidKey failures** in 11/21–11/22 live logs.
- ✅ **No new unauthorized-access / breach markers** this window. (Prior blocked user 5146706699 was an Aug-13 event, correctly blocked.)
- ⚠️ **Nous Portal still revoked/logged-out (PERSISTENT — not remediated).** "Nous Portal detected refresh-token reuse and revoked this session." Requires `hermes auth add nous`.
- ℹ️ **Cron receipt recovery deferred** warnings in live logs (2026-11-22) — operational scheduler backlog, not a security event.

---

## Trend vs 2026-11-21

| Item | 11-21 | 11-22 | Direction |
|------|-------|-------|-----------|
| Telegram token (live) | PASS | PASS | No Change |
| Gateway | PASS (PID 25084) | PASS (PID 25084) | Stable |
| WhatsApp | ⚠️ adapter OFF | ⚠️ adapter OFF | No Change |
| Nous Portal | revoked | revoked | **Unremediated** |
| Multiplex dup-credential | WARN | WARN | No Change |
| Dual-root token divergence | WARN | WARN | No Change (persistent) |
| Backup `.env` copies | PASS (0) | PASS (0) | No Change |
| `.env`-reader scripts | runtime remain | runtime remain | No Change |
| Cron silent delivery | 24/55 | 24/55 | No Change (persistent) |
| `telegram:123286468` thread loss | WARN (2) | WARN (2) | Not remediated |
| Token-file ACLs | PASS | PASS | No Change |

**Persistent security debt (3+ cycles):** dual-root token divergence, 24/55 silent cron targets, `telegram:123286468` thread loss. **Unremediated event:** Nous Portal revocation. **Unconfirmed:** WhatsApp adapter disable intent.

## 🔧 Remediation Priority
1. **Confirm WhatsApp disable intent** — re-enable `platforms.whatsapp.enabled: true` if accidental (Mum/Dad check-in routing depends on it).
2. **Restore Nous Portal** — `hermes auth add nous`; identify external process hitting the refresh endpoint (cron receipts deferred may indicate scheduler self-heal touching it).
3. **Delete stale `~/.hermes/.env` placeholder token** → single authoritative AppData root.
4. **Resolve multiplex duplicate-credential** (content-buddy/sat-nav own tokens).
5. **Fix 2 Mom exercise-reminder jobs** to Nursing coord thread (424) — `123286468` is dead.
6. Re-review 24/55 silent cron targets (`origin`/`local`); audit `5128ceaa` batch-poster + `c3db50` checkin-mum timeouts.
7. Confirm `allow_all_users: true` is intentional.

## Retention Note
Rolling 7-day window enforced. Kept 11-15 → 11-22 (7 audits on record).

---
*Generated 2026-11-22 by Hermes security-audit cron.*
