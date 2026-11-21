# Security Audit — 2026-11-20

**Generated:** 2026-11-20 07:03 by Hermes security-audit cron (*security-policy-check* job)
**Scope:** Credential exposure · Channel integrity · Recent security events
**Overall: 🟡 STABLE (WARNs persist; no new high-severity events).** Live Telegram token (AppData root) VALID via direct `getMe` (@Ogaitchhermesbot); gateway PID 25084 alive with 2 ESTABLISHED TCP connections to Telegram (149.154.166.110:443). Topic 20 confirmed as supergroup+forum target. No current-window InvalidToken, no provider rejections, no breach markers, no backup-`.env` copies, no credential caches. All token-file ACLs PASS (SYSTEM/Admin/User only). Remaining WARNs: dual-root token divergence (stale dead placeholder in `~/.hermes/.env`), 24/55 silent cron targets, 2 dead-thread jobs, multplex duplicate-credential, `.env`-reader runtime scripts, `allow_all_users`, WhatsApp adapter disabled (intent still unconfirmed), Nous Portal revocation persistent, cron receipt recovery backlog.

---

## 1. Credential Exposure

| Check | Status | Detail |
|-------|--------|--------|
| Telegram bot token (live, AppData root) | ✅ PASS | `getMe` → `{"ok":true}` (@Ogaitchhermesbot, 46-char live token, id 8277244378). Valid via direct API. |
| Stale token (`~/.hermes/.env`) | ⚠️ WARN | Holds dead placeholder (13-char, 404 on getMe). Live gateway uses AppData root. Persistent dual-root divergence debt. |
| Backup `.env` copies | ✅ PASS | **0** across `~/.hermes/backups`, `state-snapshots`, `~/hermes-backup`, `~/.openclaw`. Sustained clean. |
| Credential caches | ✅ PASS | No `bws_cache.json` / `.secret_cache` in either root. |
| `.env`-reader scripts | ⚠️ WARN | 4 runtime cron senders (`ghana_telegram_report.py`, `memory_review_telegram.py`, `h_evening_checkin_send.py`, `mum_evening_checkin.py`) + legacy dated H-health checkin scripts + 2 red-team skill scripts (godmode). Transient process-state exposure, none at rest. |
| `google_token.json` ACL (both roots) | ✅ PASS | SYSTEM / Administrators / User only (F). Present at `~/.hermes/` (11-16) and AppData root (10-18). |
| `.env` ACL (active AppData root) | ✅ PASS | SYSTEM / Administrators / User only (F). |
| `auth.json` ACL | ✅ PASS | SYSTEM / Administrators / User only (F). |
| AGENTS.md BOM / invisible chars | ✅ PASS | workspace AGENTS.md: UTF-8, no BOM. Main `~/.hermes/AGENTS.md` absent. |
| `allow_all_users` (config.yaml) | ⚠️ WARN | `allow_all_users: true` (lines 366, 876) + `GATEWAY_ALLOW_ALL_USERS: true`. Confirm intentional. |

## 2. Channel Integrity

| Channel | Status | Detail |
|---------|--------|--------|
| Gateway process | ✅ PASS | Running (PID **25084**, python 3.14.9), 2 ESTABLISHED TCP conns to Telegram. Serves 5 profiles (coach, content-buddy, harold, sat-nav, taiwah). |
| Telegram adapter | ✅ PASS | Valid token via getMe; active live connections. `gateway.log` cold (last write 10-13 — new instance logs elsewhere); exit-diag shows 0 crash signatures since 10-13 (SystemExit:78 on 10-06/10-13, resolved). |
| **WhatsApp** | ⚠️ WARN | `platforms.whatsapp.enabled: false` in config.yaml → adapter OFF despite live creds.json. Intent still unconfirmed (per prior cycle 11-18). |
| Topic 20 (Memory Review) | ✅ PASS | Supergroup + forum confirmed via `getChat`. **5 jobs** deliver to thread 20 (this job included). Token valid → delivery will succeed. |
| Cron silent delivery | ⚠️ WARN | **24/55** jobs → `origin` (16) or `local` (8); 31 telegram-targeted. Persistent, unchanged. |
| Defunct-thread jobs (telegram:123286468) | ⚠️ WARN | **2** jobs (Mom Morning + Mom Evening Exercise Reminders) target dead DM thread. Not remediated. |
| Multiplex duplicate-credential | ⚠️ WARN | default/content-buddy and default/sat-nav sharing same `TELEGRAM_BOT_TOKEN`. Persistent. |
| Cron receipt recovery | ⚠️ WARN | Backlog of deferred receipts persisted in prior cycle (483). Monitor. |

## 3. Recent Security Events

- ✅ **No `InvalidToken` / Telegram token rejection** this window — validated live via `getMe` (2026-11-20). 
- ✅ **No provider 401/403/402/429 / InvalidKey failures** in 11/19–11/20 logs.
- ✅ **No breach / unauthorized-access markers** in current logs.
- ⚠️ **Nous Portal still revoked/logged-out (PERSISTENT — not remediated).** "Nous Portal detected refresh-token reuse and revoked this session." External process called the OAuth refresh endpoint without persisting the rotated token. No operational Model impact (default runs on custom/OpenRouter). Needs `hermes auth add nous`.

---

## Trend vs 2026-11-19

| Item | 11-19 | 11-20 | Direction |
|------|-------|-------|-----------|
| Telegram token (live) | PASS | PASS | No Change |
| Gateway | PASS (PID 25084) | PASS (PID 25084) | Stable |
| WhatsApp | ⚠️ adapter OFF | ⚠️ adapter OFF (intent unconfirmed) | No Change |
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
1. **Confirm WhatsApp disable intent** — if intentional, close; if accidental, re-enable `platforms.whatsapp.enabled: true`.
2. **Restore Nous Portal** — `hermes auth add nous`; identify the external process hitting the refresh endpoint.
3. **Delete stale `~/.hermes/.env` placeholder token** → single authoritative AppData root.
4. Resolve multiplex duplicate-credential (content-buddy/sat-nav own tokens or profile_routes).
5. Fix 2 Mom exercise-reminder jobs to Nursing coord thread (424) — `123286468` is dead.
6. Re-review 24/55 silent cron targets (`origin`/`local`).
7. Confirm `allow_all_users: true` is intentional.

## Retention Note
Rolling 7-day window enforced. Kept 11-15 → 11-20 (5 audits on record). Deleted 11-12 (outside window).

---
*Generated 2026-11-20 by Hermes security-audit cron.*