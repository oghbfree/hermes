# Security Audit — 2026-11-08

**Generated:** 2026-11-08 by Hermes security-audit cron
**Scope:** Credential exposure · Channel integrity · Recent security events
**Overall: 🟠 DEGRADED** — Telegram token valid, gateway healthy (PID 1340, ESTABLISHED to Telegram), **but WhatsApp bridge remains DOWN** (reconnect attempt 251, failing every 300s since bridge exit 2026-11-06 10:17). **Multiplex duplicate-credential RESOLVED** (no occurrence today vs. 5th/6th-day escalation yesterday). No new credential exposure; no breach markers; no token rejection.

---

## 1. Credential Exposure

| Check | Status | Detail |
|-------|--------|--------|
| Telegram bot token (live) | ✅ PASS | AppData root `.env` token **valid** (`getMe` → `{"ok":true}`, @Ogaitchhermesbot id 8277244378). Gateway runs from AppData root → uses the good token. |
| Stale token (other root) | ⚠️ WARN | `~/.hermes/.env` (Nov 4) still holds a **dead placeholder** (`getMe` → HTTP 404). Live gateway unaffected. Persistent dual-root divergence debt (7+ cycles). |
| Backup `.env` copies | ✅ PASS | **0** across AppData + `~/.hermes` backups, state-snapshots, `~/hermes-backup`, `~/.openclaw`. Sustained clean. |
| Credential caches | ✅ PASS | No `bws_cache.json`, `.secret_cache`, or token cache files in either root. |
| `.env`-reader scripts | 🔄 REMEDIATED | Found 2 legacy direct-env readers (`AppData/Local/hermes/_tg_send.py`, `~/.hermes/workspace/scripts/send_ghana_report.py`), both unused by cron. **Deleted this cycle.** `cron_detail.py` is a false positive (reads LOCALAPPDATA env var for path only, not secrets). Live tree now clean. |
| `google_token.json` ACL | ✅ PASS | `icacls` (AppData root): SYSTEM / Administrators / Owner only (F). No "Everyone" / "BUILTIN\Users". Correct Windows default. |
| AGENTS.md BOM / invisible chars | ✅ PASS | workspace AGENTS.md (both roots): UTF-8, no BOM / invisible chars. Main AGENTS.md absent (not a finding). |
| config.yaml secrets | ✅ PASS | No plaintext long-lived secrets; keys referenced via env. |
| Nous Portal auth | ⚠️ WARN | Portal not logged in (`Invalid refresh token`) in AppData root. Non-security, operational; consistent with prior state. |

## 2. Channel Integrity

| Channel | Status | Detail |
|---------|--------|--------|
| Gateway process | ✅ PASS | Running (PID **1340**, python.exe, ESTABLISHED TCP to Telegram 149.154.166.110). Logs fresh (07:01). Stable. |
| Telegram adapter | ✅ PASS | **Polling healthy.** One polling-stall rebuild at 06:11 (generation 7), self-healed ~13s (reconnected 06:12, confirmed healthy). Token valid via direct `getMe`. |
| **WhatsApp** | ❌ **FAIL (PERSISTENT)** | **Bridge DOWN.** Exit code 1 at **2026-11-06 10:17**. Reconnect attempt **251** failing every 300s through Nov 8 06:59. `creds.json` present (Nov 6 10:09) but session not holding. **Not remediated; 3rd consecutive audit.** |
| Topic 20 (Memory Review) | ✅ PASS | `getChat` → supergroup "Agent Hermes", `is_forum: true`. Topic delivery target valid. |
| Cron silent delivery | ⚠️ WARN | **25/56** jobs deliver to `origin` (16) or `local` (9) — output never reaches a user. 31 topic/channel-targeted. Unchanged. |
| Defunct-thread jobs (`telegram:123286468`) | ⚠️ WARN | **2** jobs (Mom Morning + Mom Evening Exercise Reminders) still deliver to a thread not the Nursing coord thread (424). Not remediated since 10-30. |

## 3. Recent Security Events

- **No `InvalidToken` / telegram token rejections** in live logs this window ✅ (only historical mention in `bootstrap-installer.log` and the dead stale-root token).
- **No provider 401/403/InvalidKey / quota failures** — OpenRouter calls healthy (deepseek v4 traffic 07:01, cache hit 97%). ✅
- **No breach / unauthorized-access markers** ✅.
- **Multiplex duplicate-credential RESOLVED** — `default`/`content-buddy` same-telegram-credential error last seen 2026-11-07 05:46; **zero occurrences today**. Gateway now serving content-buddy without conflict. ✅ Improvement.
- **Telegram transport churn (LOW):** polling-stall rebuild at 06:11 Nov 8, self-healed ~13s. Host-level instability, not an attack.
- **WhatsApp bridge exit (code 1)** at Nov 6 10:17 — the sole active channel failure this window (§2).

---

## Trend vs 2026-11-07

| Item | 11-07 | 11-08 | Direction |
|------|-------|-------|-----------|
| Telegram token (live) | PASS | PASS | No Change |
| Gateway | PASS | PASS | Stable |
| **WhatsApp** | FAIL (bridge down) | FAIL (attempt 251) | No Change (persistent) |
| Dual-root divergence | WARN | WARN | No Change (persistent debt) |
| Backup `.env` copies | PASS (0) | PASS (0) | No Change |
| `.env`-reader scripts | PASS | 2 found → deleted | New finding, remediated |
| Cron silent delivery | 25/56 | 25/56 | No Change |
| `telegram:123286468` thread loss | WARN | WARN | Not remediated (2 jobs) |
| **Multiplex dup-credential** | WARN (6th day, escalated) | **✅ RESOLVED** (no occurrence) | **Resolved** |

**Persistent security debt (3+ cycles):** dual-root token divergence, 25/56 silent cron targets, `telegram:123286468` thread loss, **WhatsApp bridge down (3rd audit)**.
**New finding: 2 legacy `.env`-reader scripts → deleted. No active exposure remains. No token rejection. No breach markers.**

## 🔧 Remediation Priority
1. **Restore WhatsApp** — bridge has been down since Nov 6 10:17 (attempt 251). Investigate bridge exit (code 1) / re-pair QR session. Highest priority — active channel down 3rd day.
2. Delete revoked `~/.hermes/.env` placeholder → single authoritative AppData root (persistent debt).
3. Fix the 2 Mom exercise-reminder jobs so delivery keeps the Nursing coord thread_id 424.
4. Re-review 25/56 silent cron targets (`origin`/`local`).
5. Continue monitoring Telegram host-level transport churn (self-heals <30s).

## Retention Note
Rolling 7-day window enforced. Deleted 10-30. Files retained: 11-01 … 11-08 (7). Within budget.

---
*Generated 2026-11-08 by Hermes security-audit cron.*