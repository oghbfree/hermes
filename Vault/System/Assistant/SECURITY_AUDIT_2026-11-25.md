# Security Audit — 2026-11-25

**Generated:** 2026-11-25 09:33 by Hermes security-audit cron (*security-policy-check* job)
**Scope:** Credential exposure · Channel integrity · Recent security events
**Overall: 🟡 STABLE** — Live Telegram token (AppData root) VALID via direct `getMe` (@Ogaitchhermesbot id 8277244378). Gateway PID **17840** (replaced 25084) alive with ESTABLISHED conns. Topic 20 confirmed supergroup+forum; delivery will succeed. No current-window InvalidToken, no provider 401/403/402/429, no breach markers, **0 backup `.env` copies**, no credential caches, `google_token.json` ACL clean (SYSTEM/Admins/User only). **WhatsApp improved**: gateway reconnected (Nov 24 13:50/14:09), live `creds.json` fresh (Nov 24 20:09) — functional state resolving prior ambiguity. Persistent WARNs unchanged: dual-root token divergence, 24/55 silent cron targets, 2 dead-thread jobs, Nous Portal revocation, multiplex duplicate-credential, `allow_all_users: true`, `.env`-reader runtime senders. This cycle: Telegram ConnectError/ConnectTimeout flapping at 09:33 (auto-recovered via sticky-path re-walk); `MATRIX_HOME_ROOM` UnscopedSecretError recurring (multiplexing internal bug, non-leak).

---

## 1. Credential Exposure

| Check | Status | Detail |
|-------|--------|--------|
| Telegram bot token (live, AppData root) | ✅ PASS | `getMe` → `{"ok":true}` (@Ogaitchhermesbot, token id 8277244378). Valid via direct API. |
| Stale token (`~/.hermes/.env`) | ⚠️ WARN | Placeholder/divergent token; live gateway uses AppData root (46-char). Persistent dual-root deviation. |
| Backup `.env` copies | ✅ PASS | **0** across `~/.hermes/backups`, `state-snapshots`, `~/hermes-backup`, `~/.openclaw`. Sustained clean. |
| Credential caches | ✅ PASS | No `bws_cache.json` / `.secret_cache` in either root. |
| `.env`-reader scripts | ⚠️ WARN | Runtime workspace senders read tokens at process time: `workspace/scripts/{ghana_telegram_report, h_evening_checkin_send, memory_review_telegram, mum_evening_checkin}.py`. Plus legacy `test_sheets.py` reads `~/.openclaw/google-sheets-creds.json` (May 2026, small 295B file) — stale test artifact. |
| `google_token.json` ACL | ✅ PASS | Live root `icacls`: SYSTEM / Administrators / User (F) only. No Everyone/BUILTIN\Users. |
| AGENTS.md BOM / invisible chars | ✅ PASS | workspace AGENTS.md: UTF-8, CRLF, no BOM. Main `~/.hermes/AGENTS.md` absent. |
| `allow_all_users` (config.yaml) | ⚠️ WARN | `GATEWAY_ALLOW_ALL_USERS: true` + `allow_all_users: true` (x2 config lines). Persistent; confirm intentional. |

## 2. Channel Integrity

| Channel | Status | Detail |
|---------|--------|--------|
| Gateway process | ✅ PASS | Running (PID **17840**, replaced 25084 Nov 24 13:48), ESTABLISHED conns to Telegram + loopback. Serves coach, content-buddy, harold, sat-nav. |
| Telegram adapter | ⚠️ WARN | Token valid (getMe). **THIS cycle:** ConnectError flapping (09:33–09:34) on IPv4 paths 149.154.166.110/167.220 + dual-stack — auto-recovered at 09:34:46 via stick-path re-walk (gen 5, "#87015"). Host/network-level, not a credential event. |
| **WhatsApp** | 🟡 IMPROVED | Live root `creds.json` present+fresh (Nov 24 20:09, AppData). Gateway `reconnected successfully` (Nov 24 13:50, 14:09; Nov 17 14:13). Functional. Home-channel startup notify still fails (`127.0.0.1:3000` api_server refused) — that's the local API platform, not WhatsApp itself. |
| Topic 20 (Memory Review) | ✅ PASS | `getChat` → supergroup, forum, bot can send. **5 jobs** deliver to thread 20 (this job included). Token valid → delivery will succeed. |
| Cron silent delivery | ⚠️ WARN | **24/55** jobs → `origin` (16) or `local` (8); 31 telegram-targeted. Persistent, unchanged. |
| Defunct-thread jobs (`telegram:123286468`) | ⚠️ WARN | **2** jobs (Mom Morning + Mom Evening) target dead DM thread (user 123286468). Not remediated. |
| Multiplex duplicate-credential | ⚠️ WARN | default/content-buddy and default/sat-nav share same `TELEGRAM_BOT_TOKEN`. Persistent. |

## 3. Recent Security Events

- ✅ **No `InvalidToken` / Telegram token rejection this window** — live token validated via `getMe` (2026-11-25). 0 matches in current `agent.log`; rotated logs clean.
- ✅ **No provider 401/403/402/429 / InvalidKey failures** in 11/24–11/25 live logs.
- ✅ **No new unauthorized-access / breach markers** this window.
- ⚠️ **Nous Portal still revoked (PERSISTENT — not remediated).** `hermes status --full` → "not logged in …Nous Portal detected refresh-token reuse and revoked this session." Requires `hermes auth add nous`.
- ℹ️ **Telegram ConnectError/ConnectTimeout flapping** (09:33–09:34 today) — network-layer, auto-recovered; monitor (2nd consecutive cycle).
- ℹ️ **`MATRIX_HOME_ROOM` UnscopedSecretError** recurring (1042 total count in errors.log; 2026-11-25 09:36 hit). Multiplexing internal profile-scoping bug (Workstream A), documented non-leak. Recommend `hermes gateway restart`.

---

## Trend vs 2026-11-23

| Item | 11-23 | 11-25 | Direction |
|------|-------|-------|-----------|
| Telegram token (live) | PASS | PASS | No Change |
| Gateway | PASS (PID 25084) | PASS (PID 17840) | Stable (PID rotated) |
| WhatsApp | ambiguous (conflicting) | IMPROVED (reconnected, creds fresh) | **Improved** |
| Nous Portal | revoked | revoked | **Unremediated** |
| Multiplex dup-credential | WARN | WARN | No Change |
| Dual-root token divergence | WARN | WARN | No Change (persistent) |
| Backup `.env` copies | PASS (0) | PASS (0) | No Change |
| `.env`-reader scripts | runtime remain (4) | runtime remain (4) + legacy test_sheets | No Change |
| Cron silent delivery | 24/55 | 24/55 | No Change (persistent) |
| `telegram:123286468` thread loss | WARN (2) | WARN (2) | Not remediated |
| Telegram flapping | WARN (ConnectTimeout) | WARN (ConnectError/Timeout) | **Recurring** |
| Token-file ACLs | PASS | PASS | No Change |

**Persistent security debt (3+ cycles):** dual-root token divergence, 24/55 silent cron targets, `telegram:123286468` thread loss, Nous Portal revocation, multiplex duplicate-credential, `allow_all_users: true`. **New/recurring:** Telegram ConnectError flapping (2nd cycle).

## 🔧 Remediation Priority
1. **Restore Nous Portal** — `hermes auth add nous`; keepalive failing daily; all Nous-managed tools offline.
2. **Resolve multiplex duplicate-credential** (content-buddy/sat-nav own tokens) + restart gateway to clear `MATRIX_HOME_ROOM` UnscopedSecretError backlog.
3. **Delete stale `~/.hermes/.env` placeholder token** → single authoritative AppData root.
4. **Fix 2 Mom exercise-reminder jobs** to a valid thread — `123286468` is dead.
5. Re-review 24/55 silent cron targets; audit `5128ceaa` batch-poster + `c3db50` checkin-mum (kill WA-spam).
6. Remove legacy `test_sheets.py` / drop stale `~/.openclaw/google-sheets-creds.json`.
7. **Monitor Telegram ConnectError flapping** — 2nd consecutive cycle; verify not an emerging host-network problem.
8. Confirm `allow_all_users: true` is intentional.

## Retention Note
Rolling 7-day window. Deleted `SECURITY_AUDIT_2026-11-16.md` to keep 7 on record.

---
*Generated 2026-11-25 by Hermes security-audit cron.*
