# Security Audit — 2026-11-23

**Generated:** 2026-11-23 07:03 by Hermes security-audit cron (*security-policy-check* job)
**Scope:** Credential exposure · Channel integrity · Recent security events
**Overall: 🟡 STABLE** — Live Telegram token (AppData root) VALID via direct `getMe` (@Ogaitchhermesbot id 8277244378). Gateway PID 25084 alive (many ESTABLISHED conns). Topic 20 confirmed supergroup+forum; delivery will succeed. No current-window InvalidToken, no provider rejections, no breach markers, no backup-`.env` copies, no credential caches, `google_token.json` ACL clean (SYSTEM/Admins/User only). Persistent WARNs unchanged: dual-root token divergence, 24/55 silent cron targets, 2 dead-thread jobs, Nous Portal revocation, WhatsApp adapter ambiguity, `allow_all_users: true`, `.env`-reader runtime senders, multiplex duplicate-credential. New: intermittent Telegram ConnectTimeout flapping (network-level, auto-recovers) — classified channel-integrity WARN.

---

## 1. Credential Exposure

| Check | Status | Detail |
|-------|--------|--------|
| Telegram bot token (live, AppData root) | ✅ PASS | `getMe` → `{"ok":true}` (@Ogaitchhermesbot, live token id 8277244378). Valid via direct API. |
| Stale token (`~/.hermes/.env`) | ⚠️ WARN | 13-char dead placeholder; live gateway uses AppData root (46-char). Persistent dual-root divergence. |
| Backup `.env` copies | ✅ PASS | **0** across `~/.hermes/backups`, `state-snapshots`, `~/hermes-backup`, `~/.openclaw`. Sustained clean. |
| Credential caches | ✅ PASS | No `bws_cache.json` / `.secret_cache` in either root. |
| `.env`-reader scripts | ⚠️ WARN | **4** runtime workspace senders read tokens at process time (transient, none at rest): `workspace/scripts/{ghana_telegram_report, h_evening_checkin_send, memory_review_telegram, mum_evening_checkin}.py`. No independent leak scripts at rest. |
| `google_token.json` ACL | ✅ PASS | AppData root `icacls`: SYSTEM / Administrators / User (F) only. No Everyone/BUILTIN\Users. |
| AGENTS.md BOM / invisible chars | ✅ PASS | workspace AGENTS.md: UTF-8, CRLF, no BOM. Main `~/.hermes/AGENTS.md` absent. |
| `allow_all_users` (config.yaml) | ⚠️ WARN | Confirmed persistent; confirm intentional (not re-checked line-level this cycle). |

## 2. Channel Integrity

| Channel | Status | Detail |
|---------|--------|--------|
| Gateway process | ✅ PASS | Running (PID **25084**), many ESTABLISHED conns (loopback + Telegram). Serves coach, content-buddy, harold, sat-nav, taiwah. |
| Telegram adapter | ⚠️ WARN | Token valid (getMe). **NEW this cycle:** repeated ConnectTimeout flapping on IPv4 paths (149.154.166.110/167.220) at 06:50, 06:55, 06:58 — auto-recovers via sticky-path re-walk (generation 9, "#87015"). Host/network-level, not a credential event. |
| **WhatsApp** | ⚠️ WARN | Live root `creds.json` present (Nov 21, AppData). Conflicting state: AppData `gateway_state.json` → `connected` (Nov 17), stale `~/.hermes/gateway_state.json` → `fatal/whatsapp_not_paired` (Oct 13). Intent still unconfirmed per 11-18 cycle. |
| Topic 20 (Memory Review) | ✅ PASS | `getChat` → `type: supergroup`, `is_forum: true`, bot can send. **5 jobs** deliver to thread 20 (this job included). Token valid → delivery will succeed. |
| Cron silent delivery | ⚠️ WARN | **24/55** jobs → `origin` (16) or `local` (8); 31 telegram-targeted. Persistent, unchanged. |
| Defunct-thread jobs (`telegram:123286468`) | ⚠️ WARN | **2** jobs (Mom Morning + Mom Evening) target dead DM thread (user 123286468). Not remediated. |
| Multiplex duplicate-credential | ⚠️ WARN | default/content-buddy and default/sat-nav share same `TELEGRAM_BOT_TOKEN`. Persistent. |

## 3. Recent Security Events

- ✅ **No `InvalidToken` / Telegram token rejection this window** — live token validated via `getMe` (2026-11-23). No InvalidToken in current or rotated logs.
- ✅ **No provider 401/403/402/429 / InvalidKey failures** in 11/22–11/23 live logs.
- ✅ **No new unauthorized-access / breach markers** this window.
- ⚠️ **Nous Portal still revoked (PERSISTENT — not remediated).** 2026-11-23 06:00 keepalive: "No access token found for Nous Portal login." Requires `hermes auth add nous`.
- ℹ️ **Telegram ConnectTimeout flapping** (06:50–06:59 today) — network-layer, auto-recovered; monitor.
- ℹ️ **Cron receipt recovery deferred** warnings (11-22 19:53, 21:31) — operational scheduler backlog, not a security event.

---

## Trend vs 2026-11-22

| Item | 11-22 | 11-23 | Direction |
|------|-------|-------|-----------|
| Telegram token (live) | PASS | PASS | No Change |
| Gateway | PASS (PID 25084) | PASS (PID 25084) | Stable |
| WhatsApp | adapter OFF | ambiguous (conflicting state files) | No Change |
| Nous Portal | revoked | revoked | **Unremediated** |
| Multiplex dup-credential | WARN | WARN | No Change |
| Dual-root token divergence | WARN | WARN | No Change (persistent) |
| Backup `.env` copies | PASS (0) | PASS (0) | No Change |
| `.env`-reader scripts | runtime remain | runtime remain (4) | No Change |
| Cron silent delivery | 24/55 | 24/55 | No Change (persistent) |
| `telegram:123286468` thread loss | WARN (2) | WARN (2) | Not remediated |
| Telegram ConnectTimeout flapping | — | WARN | **NEW** |
| Token-file ACLs | PASS | PASS | No Change |

**Persistent security debt (3+ cycles):** dual-root token divergence, 24/55 silent cron targets, `telegram:123286468` thread loss. **Unremediated event:** Nous Portal revocation.

## 🔧 Remediation Priority
1. **Confirm WhatsApp enable intent** — resolve conflicting state files; re-enable `platforms.whatsapp.enabled: true` if accidental (Mum/Dad check-in routing depends on it).
2. **Restore Nous Portal** — `hermes auth add nous`; keepalive is failing daily.
3. **Delete stale `~/.hermes/.env` placeholder token** → single authoritative AppData root.
4. **Resolve multiplex duplicate-credential** (content-buddy/sat-nav own tokens).
5. **Fix 2 Mom exercise-reminder jobs** to a valid thread — `123286468` is dead.
6. Re-review 24/55 silent cron targets; audit `5128ceaa` batch-poster + `c3db50` checkin-mum.
7. **Monitor Telegram ConnectTimeout flapping** — verify not an emerging host-network problem.
8. Confirm `allow_all_users: true` is intentional.

## Retention Note
Rolling 7-day window. Counted 11-15 → 11-23; deleting 11-15 to keep 7 on record.

---
*Generated 2026-11-23 by Hermes security-audit cron.*