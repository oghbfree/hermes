# Security Audit — 2026-11-07

**Generated:** 2026-11-07 by Hermes security-audit cron
**Scope:** Credential exposure · Channel integrity · Recent security events
**Overall: 🟠 DEGRADED** — Telegram token valid and gateway polling healthy, but **WhatsApp bridge is DOWN** (exit code 1 since 2026-11-06 10:17, reconnect failing through Nov 7 07:00, attempt 18) — a regression from the Nov 6 "paired & live" state. No new credential exposure; no breach markers; no token rejection. Persistent low-severity debt unchanged (dual-root divergence, silent cron targets, defunct-thread jobs, multiplex duplicate-credential).

---

## 1. Credential Exposure

| Check | Status | Detail |
|-------|--------|--------|
| Telegram bot token (live) | ✅ PASS | AppData root `.env` token **valid** (`getMe` → `{"ok":true}`, @Ogaitchhermesbot id 8277244378). Gateway runs from AppData root → uses the good token. |
| Stale token (other root) | ⚠️ WARN | `~/.hermes/.env` (updated Nov 4) still holds a **dead placeholder** (`getMe` → HTTP 404). Live gateway unaffected. Persistent dual-root divergence debt (6+ cycles). |
| Backup `.env` copies | ✅ PASS | **0** across AppData + `~/.hermes` backups, state-snapshots, `~/hermes-backup`, `~/.openclaw`. Sustained clean. |
| Credential caches | ✅ PASS | No `bws_cache.json`, `.secret_cache`, or token cache files in either root. |
| `.env`-reader scripts | ✅ PASS | No active scripts in live workspace/`~/.hermes` reading `.env` directly (legacy helpers confirmed retired Nov 6). |
| `google_token.json` ACL | ✅ PASS | `icacls` (both roots): SYSTEM / Administrators / Owner only (F). No "Everyone" / "BUILTIN\Users". Correct Windows default. |
| AGENTS.md BOM / invisible chars | ✅ PASS | workspace AGENTS.md: UTF-8, CRLF, no BOM / invisible chars. Main `~/.hermes/AGENTS.md` absent (not a finding). |
| config.yaml secrets | ✅ PASS | No plaintext long-lived secrets; keys referenced via env. |
| Nous Portal auth | ⚠️ WARN | Portal not logged in (`Invalid refresh token`) in AppData root. Non-security, operational; consistent with prior state. |

## 2. Channel Integrity

| Channel | Status | Detail |
|---------|--------|--------|
| Gateway process | ✅ PASS | Running (PID active, status "✓ running"). Clean exit-diag (`asyncio.run.returned`, success=true, PID 28472). No crash loop. |
| Telegram adapter | ✅ PASS | **Polling healthy** — `Connected to Telegram (polling mode)` at 03:55 and 05:43 Nov 7, `getUpdates progressing`. Token valid via direct `getMe`. |
| **WhatsApp** | ❌ **FAIL (REGRESSION)** | **Bridge DOWN.** `WhatsApp bridge process exited unexpectedly (code 1)` at **2026-11-06 10:17:47**. Reconnect failing every 300s through Nov 7 07:00 (attempt 18). `creds.json` present (Nov 6 10:09) but bridge not staying up. **Regression vs Nov 6 when paired & live.** |
| Topic 20 (Memory Review) | ✅ PASS | Confirmed in `channel_directory.json` (AppData root) as `Agent Hermes / topic 20`. Also thread 424 (Nursing coord) present. |
| Cron silent delivery | ⚠️ WARN | **25/56** jobs deliver to `origin` (16) or `local` (9) — output never reaches a user. 31 topic/channel-targeted. Unchanged. |
| Defunct-thread jobs (`telegram:123286468`) | ⚠️ WARN | **2** jobs (Mom Morning + Mom Evening Exercise Reminders) still deliver to a thread not the Nursing coord thread (424). Not remediated since 10-30. |
| Multiplex duplicate credential | ⚠️ WARN→ESCALATED | Recurred Nov 7 05:46: profiles `default` and `content-buddy` both configure the same telegram credential — content-buddy's Telegram refused to start. **Persistent security debt, escalated (6th cycle).** |

## 3. Recent Security Events

- **No `InvalidToken` / telegram token rejections** in live logs this window ✅. (Only mention is historical in `bootstrap-installer.log`.)
- **No provider 401/403/InvalidKey rejections** — OpenRouter calls healthy (deepseek v4 traffic at 07:02–07:03 succeeded). ✅
- **No breach / unauthorized-access markers** ✅. (API-server "rejected invalid API key" entries are benign localhost curl probes at `127.0.0.1`, not external access.)
- **No provider quota/billing failures** (no 402/429 quota patterns) ✅.
- **Telegram transport churn (persistent, LOW):** network-error polling restart at 00:39 Nov 7, **self-healed in ~13s** (generation 2). Host-level instability, not an attack. `OpenAI APIConnectionError` in `errors.log.1` is historical/transient.
- **WhatsApp bridge exit (code 1)** at Nov 6 10:17 — the sole active channel failure this window (see §2).
- **Multiplex duplicate-credential ERROR** (Nov 7 05:46) — config-level duplicate, not a compromise.

---

## Trend vs 2026-11-06

| Item | 11-06 | 11-07 | Direction |
|------|-------|-------|-----------|
| Telegram token (live) | PASS | PASS | No Change |
| Gateway | PASS | PASS | Stable |
| **WhatsApp** | **PASS (paired, live)** | **FAIL (bridge down)** | **REGRESSION** |
| Dual-root divergence | WARN | WARN | No Change (persistent debt) |
| Backup `.env` copies | PASS (0) | PASS (0) | No Change |
| `.env`-reader scripts | PASS | PASS | No Change |
| Cron silent delivery | 25/56 | 25/56 | No Change |
| `telegram:123286468` thread loss | WARN | WARN | Not remediated (2 jobs) |
| Multiplex dup-credential | WARN (5th day) | WARN (6th day; escalated) | Persistent debt confirmed |

**Persistent security debt (3+ cycles):** dual-root token divergence, 25/56 silent cron targets, `telegram:123286468` thread loss, **multiplex duplicate-credential (escalated, 6th cycle)**.
**No new active credential exposure. No token rejection. No breach markers. New channel FAIL: WhatsApp bridge down.**

## 🔧 Remediation Priority
1. **Restore WhatsApp** — investigate bridge exit (code 1) at Nov 6 10:17; restart bridge / re-pair if session invalid. Highest priority (active channel down).
2. Resolve default/content-buddy duplicate telegram credential (now 6-day persistent debt) — give content-buddy its own token or disable its Telegram.
3. Delete the revoked `~/.hermes/.env` placeholder → single authoritative AppData root.
4. Fix the 2 Mom exercise-reminder jobs so delivery keeps the Nursing coord thread_id 424.
5. Re-review 25/56 silent cron targets (`origin`/`local`).
6. Continue monitoring Telegram host-level transport instability (self-heals in <30s) and the unfinished `hermes update`.

## Retention Note
Rolling 7-day window. Files present: 10-30, 11-01, 11-02, 11-03, 11-04, 11-06, 11-07 (7). Within budget.

---
*Generated 2026-11-07 by Hermes security-audit cron.*