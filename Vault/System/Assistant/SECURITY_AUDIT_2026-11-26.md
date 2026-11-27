# Security Audit — 2026-11-26

**Generated:** 2026-11-26 08:44 by Hermes security-audit cron (*security-policy-check* job)
**Scope:** Credential exposure · Channel integrity · Recent security events
**Overall: 🟡 STABLE** — Live Telegram token (AppData root, 46-char `...1UJE`) VALID via direct `getMe` (@Ogaitchhermesbot id 8277244378). Gateway PID **17840** alive; active today 08:42 (Telegram polling recovery gen 9 via fallback IP 149.154.166.110). Topic 20 confirmed supergroup+forum → this job's delivery will succeed. WhatsApp creds fresh (Nov 24 20:09). **0 backup `.env` copies**, no credential caches, both `google_token.json` ACLs clean (SYSTEM/Admins/User only). All `InvalidToken` events are **historical** (Oct 1/6/13, pre-recovery) — none in current window. No provider 401/403/402/429 this window. Persistent WARNs unchanged: dual-root token divergence, 24/55 silent cron targets (16 origin + 8 local), 2 dead-thread jobs (123286468), Nous Portal revocation, multiplex duplicate-credential, `allow_all_users: true`, `.env`-reader runtime senders. Recurring non-leak: `MATRIX_HOME_ROOM` UnscopedSecretError (last 08:43 today).

---

## 1. Credential Exposure

| Check | Status | Detail |
|-------|--------|--------|
| Telegram bot token (live, AppData root) | ✅ PASS | `getMe` → `{"ok":true}` (@Ogaitchhermesbot, token id 8277244378). Valid via direct API. |
| Stale token (`~/.hermes/.env`) | ⚠️ WARN | 13-char placeholder/divergent token (returns HTTP 404 on getMe). Live gateway uses AppData root (46-char). Persistent dual-root deviation. |
| Backup `.env` copies | ✅ PASS | **0** across `~/.hermes/backups`, `state-snapshots`, `~/hermes-backup`, `~/.openclaw`. Sustained clean. |
| Credential caches | ✅ PASS | No `bws_cache.json` / `.secret_cache` in either root. |
| `.env`-reader scripts | ⚠️ WARN | Runtime workspace senders read tokens at process time: `workspace/scripts/{ghana_telegram_report, h_evening_checkin_send, memory_review_telegram, mum_evening_checkin}.py` + `~/.hermes/care_checkin.py`. Plus legacy test artifacts `workspace/{test_creds, test_sheets}.py`, dated checkin scripts under Vault. |
| `google_token.json` ACL | ✅ PASS | Both roots `icacls`: SYSTEM / Administrators / User (F) only. No Everyone/BUILTIN\Users. |
| AGENTS.md BOM / invisible chars | ✅ PASS | workspace AGENTS.md: UTF-8, CRLF, no BOM. Main `~/.hermes/AGENTS.md` absent. |
| `allow_all_users` (config.yaml) | ⚠️ WARN | `GATEWAY_ALLOW_ALL_USERS: true` (line 2) + `allow_all_users: true` (lines 366, 876). Persistent; confirm intentional. |

## 2. Channel Integrity

| Channel | Status | Detail |
|---------|--------|--------|
| Gateway process | ✅ PASS | Running (PID **17840**), alive via tasklist. Serves coach, content-buddy, harold, sat-nav. |
| Telegram adapter | ✅ PASS | Token valid (getMe). **THIS cycle:** active at 08:42 — "polling recovered: getUpdates progressing (generation 9)" after ConnectError via api.telegram.org; auto-recovered via sticky path 149.154.166.110. Network-level, transient, self-healed. |
| **WhatsApp** | ✅ PASS-ISH | Live root `creds.json` present + fresh (Nov 24 20:09, AppData). Functional. (Note: stale `~/.hermes/logs/gateway.log` is Oct 13 — refers to `~/.hermes` path pairing, not live AppData session.) |
| Topic 20 (Memory Review) | ✅ PASS | `getChat` → supergroup, is_forum=True. This job (`security-policy-check`) delivers to `telegram:-1003784520976:20`. Token valid → delivery succeeds. |
| Cron silent delivery | ⚠️ WARN | **24/55** jobs → `origin` (16) or `local` (8); 31 telegram-targeted (incl. 5 to thread 20). Persistent, unchanged. |
| Defunct-thread jobs (`telegram:123286468`) | ⚠️ WARN | **2** jobs (Mom Morning + Mom Evening) target dead DM thread (user 123286468). Not remediated. |
| Multiplex duplicate-credential | ⚠️ WARN | default/content-buddy and default/sat-nav share same `TELEGRAM_BOT_TOKEN`. Persistent. |

## 3. Recent Security Events

- ✅ **No current-window `InvalidToken` / it token rejection** — live token validated via `getMe` (2026-11-26). All `rejected by the server` entries are historical (Oct 1, Oct 6, Oct 13), before the Nov recovery.
- ✅ **No provider 401/403/402/429 / InvalidKey failures** in 11/24–11/26 live logs (only stale Aug/Oct entries).
- ✅ **No new unauthorized-access / breach markers** this window.
- ⚠️ **Nous Portal still revoked (PERSISTENT — not remediated).** Refresh-token reuse detected; requires `hermes auth add nous`. All Nous-managed tools offline.
- ℹ️ **Telegram ConnectError + auto-recovery this cycle** (08:42) — network-layer, self-healed via sticky IP (rolling pattern; 3rd+ consecutive cycle of morning flapping).
- ℹ️ **`MATRIX_HOME_ROOM` UnscopedSecretError** recurred 08:43 today. Multiplexing internal profile-scoping bug (Workstream A), documented non-leak. Recommend `hermes gateway restart`.

---

## Trend vs 2026-11-25

| Item | 11-25 | 11-26 | Direction |
|------|-------|-------|-----------|
| Telegram token (live) | PASS | PASS | No Change |
| Gateway | PASS (PID 17840) | PASS (PID 17840) | No Change |
| WhatsApp | IMPROVED (reconnected) | PASS (creds fresh) | Stable |
| Nous Portal | revoked | revoked | **Unremediated** |
| Multiplex dup-credential | WARN | WARN | No Change |
| Dual-root token divergence | WARN | WARN | No Change (persistent) |
| Backup `.env` copies | PASS (0) | PASS (0) | No Change |
| `.env`-reader scripts | runtime (4) + legacy | runtime (4) + care_checkin + legacy | Mild change |
| Cron silent delivery | 24/55 | 24/55 | No Change (persistent) |
| `telegram:123286468` thread loss | WARN (2) | WARN (2) | Not remediated |
| Telegram flapping | WARN | PASS (auto-recovered) | Recurring, self-healed |
| Token-file ACLs | PASS | PASS | No Change |

**Persistent security debt (3+ cycles):** dual-root token divergence, 24/55 silent cron targets, `telegram:123286468` thread loss, Nous Portal revocation, multiplex duplicate-credential, `allow_all_users: true`. **New/recurring:** Telegram morning ConnectError flapping (self-heals; monitoring).

## 🔧 Remediation Priority
1. **Restore Nous Portal** — `hermes auth add nous`; keepalive failing daily; all Nous-managed tools offline.
2. **Resolve multiplex duplicate-credential** (content-buddy/sat-nav own tokens) + `hermes gateway restart` to clear `MATRIX_HOME_ROOM` UnscopedSecretError backlog.
3. **Delete stale `~/.hermes/.env` 13-char placeholder token** → single authoritative AppData root.
4. **Fix 2 Mom exercise-reminder jobs** targeting dead thread `123286468`.
5. Re-review 24/55 silent cron targets; audit `5128ceaa` batch-poster + `c3db50` checkin-mum.
6. Remove legacy `test_creds.py` / `test_sheets.py`; consolidate dated Vault checkin scripts.
7. Confirm `allow_all_users: true` intentional (3 config sites).
8. **Monitor Telegram morning flapping** — recurring; currently self-heals via sticky IP.

## Retention Note
Rolling 7-day window. Deleted `SECURITY_AUDIT_2026-11-17.md` to keep 7 on record.

---
*Generated 2026-11-26 by Hermes security-audit cron.*
