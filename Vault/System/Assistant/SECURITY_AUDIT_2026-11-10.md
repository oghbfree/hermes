# Security Audit — 2026-11-10

**Generated:** 2026-11-10 by Hermes security-audit cron
**Scope:** Credential exposure · Channel integrity · Recent security events
**Overall: 🟠 DEGRADED** — Telegram fully healthy (live token valid, gateway stable PID 34324, polling healthy, topic 20 confirmed live). **WhatsApp bridge remains DOWN** (5th consecutive audit; `WinError 5 Access denied` on `bridge.js`, attempt 279 today). No token exposure, no breach markers, no provider-key failures. Legacy `.env`-reader scripts re-appeared again in the workspace tree (WARN) — test artifacts deleted this cycle.

---

## 1. Credential Exposure

| Check | Status | Detail |
|-------|--------|--------|
| Telegram bot token (live, AppData root) | ✅ PASS | `getMe` → `{"ok":true}` (@Ogaitchhermesbot id 8277244378). Token valid. |
| Stale token (other root) | ⚠️ WARN | `~/.hermes/.env` still holds a **dead placeholder** (`getMe` → HTTP 404). Live gateway unaffected (uses AppData root). Persistent dual-root divergence debt (9+ cycles). |
| Backup `.env` copies | ✅ PASS | **0** across `~/.hermes` backups, state-snapshots, `~/hermes-backup`, `~/.openclaw`. Sustained clean. |
| Credential caches | ✅ PASS | No `bws_cache.json`, `.secret_cache`, or token cache files in either root. |
| `.env`-reader scripts | ⚠️ WARN (RE-APPEARED) | 7 test artifacts deleted this cycle (`tmp_query_msgs.py`, `tmp_recruit_verify.py`, `tmp_recruitment_job.py`, `tmp_scan_cron.py`, `tmp_send_evening_h.py`, `query_msgs2.py`, `query_telegram_msgs.py`). Runtime scripts remain (intentional cron senders: `scripts/ghana_telegram_report.py`, `memory_review_telegram.py`, `h_evening_checkin_send.py`, `mum_evening_checkin.py`, `Vault/.../MissionControl/mission_control.py`, `health/send_*.py`, 2real-agent suite). None contain secrets at rest — they read via env at runtime, but leak tokens to process tables/shell history. |
| `google_token.json` ACL | ✅ PASS | Both roots: SYSTEM / Administrators / User only (F). No "Everyone"/"BUILTIN\Users". Correct Windows default. Export/refresh token protected. |
| AGENTS.md BOM / invisible chars | ✅ PASS | workspace AGENTS.md: UTF-8, no BOM (CRLF only). Main AGENTS.md absent (not a finding). |
| config.yaml secrets | ✅ PASS | No plaintext long-lived secrets; keys referenced via env. |
| `allow_all_users: true` | ⚠️ WARN | `GATEWAY_ALLOW_ALL_USERS: true` in config.yaml + gateway.config WARNING each start — broadens attack surface on all platforms; confirm intentional. |

## 2. Channel Integrity

| Channel | Status | Detail |
|---------|--------|--------|
| Gateway process | ✅ PASS | Running (PID **34324**, python.exe). Started 2026-11-08 `--replace`. Stable; consistency across both status representations. |
| Telegram adapter | ✅ PASS | **Polling healthy.** Live token valid via direct `getMe`. Topic 20 verified (`getChat` → supergroup "Agent Hermes", `is_forum: true`). |
| **WhatsApp** | ❌ **FAIL (PERSISTENT — 5th audit)** | **Bridge DOWN** since **2026-11-06 10:17**. Every bridge start fails: `WinError 5 Access is denied` at `bridge.js`. **Attempt 279** at 06:57 today (retry every 300s). `creds.json` present (AppData root) but session not holding. Blocking Mum/Dad/everyone's check-ins and 2Real poster. |
| Topic 20 (Memory Review) | ✅ PASS | Verified live this cycle (getChat supergroup + forum). Valid delivery target. |
| Cron silent delivery | ⚠️ WARN | **25/56** jobs deliver to `origin` (16) or `local` (9) — output never reaches a user. 31 topic-targeted. Unchanged. |
| Defunct-thread jobs (`telegram:123286468`) | ⚠️ WARN | **2** jobs (Mom Morning + Mom Evening Exercise Reminders) deliver to a thread not the Nursing coord thread (424). Not remediated since 10-30. |

## 3. Recent Security Events

- **No `InvalidToken` / live Telegram token rejection** this window ✅ — only the stale `~/.hermes/.env` placeholder (§1) and historical rotated-log entries (Aug 2026). Live token accepted.
- **No provider 401/403/402/429 / InvalidKey / quota failures** in the audit window ✅.
- **No breach / unauthorized-access markers.** No `Blocked unauthorized user` events today (only one historical Aug 13 block). ✅
- **Multiplex duplicate-credential stays RESOLVED** — continuing from 11-08; no `default`/`content-buddy` credential-conflict occurrences. ✅
- **WhatsApp bridge `WinError 5 Access denied`** — sole active channel failure (§2). Same root cause from 11-09: process-spawn permission error on `bridge.js`. Persistently fails on every 300s retry. Requires re-pair / permission inspection.
- **Live gateway logs rotated to AppData root** — `~/.hermes/logs/gateway.log` is now a stale Oct 13 copy; live logs are at `AppData/Local/hermes/logs/gateway.log` + `gateway-stdio.log`. RCA normal; no integrity concern.

---

## Trend vs 2026-11-09

| Item | 11-09 | 11-10 | Direction |
|------|-------|-------|-----------|
| Telegram token (live) | PASS | PASS | No Change |
| Gateway | PASS (PID 34324) | PASS (PID 34324) | Stable |
| **WhatsApp** | FAIL (attempt 49) | FAIL (attempt 279; WinError 5) | No Change (persistent, 5th) |
| Dual-root divergence | WARN | WARN | No Change (persistent debt) |
| Backup `.env` copies | PASS (0) | PASS (0) | No Change |
| `.env`-reader scripts | ~11 re-appeared | 7 deleted; runtime remain | **Improved** (test artifacts removed) |
| Cron silent delivery | 25/56 | 25/56 | No Change |
| `telegram:123286468` thread loss | WARN | WARN | Not remediated (2 jobs) |
| Multiplex dup-credential | RESOLVED | RESOLVED | No Change |
| `google_token.json` ACL | PASS | PASS | No Change |

**Persistent security debt (3+ cycles):** dual-root token divergence (9+), 25/56 silent cron targets, `telegram:123286468` thread loss, **WhatsApp bridge down (5th audit, attempt 279)**.
**Improvement this cycle:** 7 leaked test artifact scripts deleted (`.env`-reader test-tooling cleaned back out of the tree).

## 🔧 Remediation Priority
1. **Restore WhatsApp** — bridge down 5th day; `WinError 5 Access denied` on `bridge.js` at attempt 279. Inspect bridge process permissions + QR re-pair. Blocks Mum/Dad check-ins + 2Real poster (highest impact).
2. **Delete stale `~/.hermes/.env` placeholder** → single authoritative AppData root (persistent debt, 9+ cycles).
3. **Prevent `.env`-reader script churn** — runtime senders are intentional, but recurring test-artifact regeneration (`tmp_*`/`query_*`) must stop; review whether they should read a shared helper instead.
4. Fix the 2 Mom exercise-reminder jobs to keep Nursing coord thread_id 424.
5. Re-review 25/56 silent cron targets (`origin`/`local`).
6. Confirm `allow_all_users: true` is intentional; if not, restrict to known senders.

## Retention Note
Rolling 7-day window enforced. Deleted 11-03. Files retained: 11-04 … 11-10 (7). Within budget.

---
*Generated 2026-11-10 by Hermes security-audit cron.*
