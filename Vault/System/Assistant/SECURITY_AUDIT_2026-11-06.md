# Security Audit — 2026-11-06

**Generated:** 2026-11-06 by Hermes security-audit cron
**Scope:** Credential exposure · Channel integrity · Recent security events
**Overall: 🟢 HEALTHY** — Live Telegram token valid, gateway polling active, WhatsApp paired and live, no breach markers, no new credential exposure. Credential hygiene IMPROVED (legacy `.env`-reader helper scripts retired; backup `.env` copies remain 0). Persistent low-severity debt unchanged (dual-root divergence, silent cron targets, defunct-thread jobs, multiplex duplicate-credential — now escalated to persistent security debt).

---

## 1. Credential Exposure

| Check | Status | Detail |
|-------|--------|--------|
| Telegram bot token (live) | ✅ PASS | AppData root `.env` token **valid** (`getMe` → `{"ok":true}`, @Ogaitchhermesbot id 8277244378). Gateway runs from AppData root → uses the good token. |
| Stale token (other root) | ⚠️ WARN | `~/.hermes/.env` (updated Nov 4 14:37) still holds a **dead placeholder** (`getMe` → HTTP 404). Live gateway unaffected. Persistent dual-root divergence debt (5+ cycles). No new live active secrets at risk. |
| Backup `.env` copies | ✅ PASS | **0** via `find` across AppData + `~/.hermes` backups, state-snapshots, `~/hermes-backup`, `~/.openclaw`. Sustained clean. |
| Credential caches | ✅ PASS | `bws_cache.json`, `.secret_cache` — absent in both roots. |
| `.env`-reader scripts | ✅ PASS (IMPROVED) | Previously-flagged legacy helpers (`ghana_telegram_report.py`, `memory_review_telegram.py`, `h_evening_checkin_send.py`, `mum_evening_checkin.py`, `send_ghana_report.py`, `send_evening_health_check.py`, etc.) **no longer present** in live workspace/scripts or `~/.hermes`. Only third-party matches in `uv cache/` (libs). Retired. |
| `google_token.json` ACL | ✅ PASS | `icacls` (both roots): SYSTEM / Administrators / Owner only (F). No "Everyone" / "BUILTIN\Users". Correct Windows default. |
| AGENTS.md BOM / invisible chars | ✅ PASS | workspace AGENTS.md: UTF-8, CRLF, no BOM / invisible chars. Clean. |
| config.yaml secrets | ✅ PASS | No plaintext API keys / long-lived secrets in config.yaml (all `api_key:` fields referenced via env). |
| Nous Portal auth | ⚠️ WARN | Portal not logged in (`Invalid refresh token`) in AppData root. Non-security operational; consistent with prior state. |

## 2. Channel Integrity

| Channel | Status | Detail |
|---------|--------|--------|
| Gateway process | ✅ PASS | Running since Nov 5 04:58 (PID 29824, Python 3.14.9, replaced prior PID 15952 cleanly). Active Telegram + WhatsApp processing through Nov 6 09:38. |
| Gateway crash state | ✅ PASS | No `ModuleNotFoundError` in this window. Only historical (Oct 13 and earlier) `SystemExit: 78` entries in exit-diag. No crash loop. |
| Telegram adapter | ✅ PASS | Polling **active** (recovered generation 6 at Nov 6 09:37:01). Token valid via direct `getMe`. Persistent low-severity transport churn — see §3. |
| WhatsApp | ✅ PASS (IMPROVED) | **Paired & live** at AppData (`creds.json` updated Nov 6 09:36; app-state-sync keys present). Bridge flushing text batches and running customer-gate. Previous `~/.hermes` unpaired path is legacy — live root is paired. |
| Topic 20 (Memory Review) | ✅ PASS | Confirmed in `channel_directory.json` (`Agent Hermes / topic 20`, `-1003784520976:20`). Also thread 424 (Nursing coord) present. |
| Cron silent delivery | ⚠️ WARN | **25/56** jobs deliver to `origin` (16) or `local` (9) — output never reaches a user. 31 topic/channel-targeted. Unchanged. |
| Defunct-thread jobs (`telegram:123286468`) | ⚠️ WARN | **2** jobs (Mom Morning + Mom Evening Exercise Reminders) still deliver to `telegram:123286468` thread — not the Nursing coord thread (424). Not remediated since 10-30. |
| Multiplex duplicate credential | ⚠️ WARN→ESCALATED | Recurred again (Nov 1 11:25, Nov 2 21:58, Nov 3 03:48, Nov 4 01:20, Nov 5 04:59): profiles `default` and `content-buddy` both configure the same telegram credential — content-buddy's Telegram instance refused to start. **5th consecutive day → persistent security debt**, escalated. |

## 3. Recent Security Events

- **No `InvalidToken` / token rejections / provider 401/403 in live logs** this window ✅. (Only InvalidToken matches in agent.log.1 are test-file mentions from the prior audit run — not real events.)
- **No blocked-user / unauthorized-access / breach markers** ✅. (All `pre_gateway_dispatch skip` entries are owner-typed / no-catalog-match / blocked-number routing — normal WhatsApp gating, not access events.)
- **No provider quota/billing failures** (no 402/429 quota patterns) ✅.
- **Telegram transport churn (persistent, LOW):** recurring `httpx.ConnectError` / `getaddrinfo failed` / "All connection attempts failed" — Nov 5 18:18 sticky-path failure, Nov 6 09:20–09:36 polling reconnect failures. All **self-healed** within ~30s (recovered generation 6 at 09:37:01, `getUpdates progressing`). Host-level network instability, not an attack marker.
- **Multiplex duplicate-credential ERROR** (Nov 5 04:59) — same event as §2; config-level duplicate, not a compromise.
- **`hermes status` source-update warning:** "an update is still running" (`.update_exit_code` from Oct 30) — the AppData root update never completed cleanly; gateway runs fine on previous dependencies. Operational WARN, not a security event.

---

## Trend vs 2026-11-04

| Item | 11-04 | 11-06 | Direction |
|------|-------|-------|-----------|
| Telegram token (live) | PASS | PASS | No Change |
| Gateway | PASS | PASS | Stable |
| Dual-root divergence | WARN | WARN | No Change (persistent debt) |
| Backup `.env` copies | PASS (0) | PASS (0) | No Change |
| Credential caches | PASS | PASS | No Change |
| `.env`-reader scripts | WARN (5+) | **PASS (retired)** | **IMPROVED** |
| WhatsApp | PASS | PASS (paired, live) | Stable / Improved |
| Cron silent delivery | 25/56 | 25/56 | No Change |
| `telegram:123286468` thread loss | WARN | WARN | Not remediated (2 jobs) |
| Multiplex dup-credential | WARN (escalated) | WARN (5th day) | **Persistent debt confirmed** |

**Persistent security debt (3+ cycles):** dual-root token divergence, 25/56 silent cron targets, `telegram:123286468` thread loss, **multiplex duplicate-credential (escalated)**.
**No new active credential exposure. No token rejection. No breach markers. Credential hygiene improving (`.env`-readers retired).**

## 🔧 Remediation Priority
1. Delete the revoked `~/.hermes/.env` placeholder → single authoritative AppData root.
2. Resolve default/content-buddy duplicate telegram credential (give content-buddy its own token, or disable its Telegram) — now 5-day persistent debt.
3. Fix the 2 Mom exercise-reminder jobs so delivery keeps the Nursing coord thread_id 424.
4. Re-review 25/56 silent cron targets (`origin`/`local`).
5. Complete the pending `hermes update` to clear the source-update warning.
6. Continue monitoring Telegram transport instability (self-heals in ~30s).

## Retention Note
Rolling 7-day window. Deleted `SECURITY_AUDIT_2026-10-29.md` (oldest, beyond window) to hold at 7 files.

---
*Generated 2026-11-06 by Hermes security-audit cron.*