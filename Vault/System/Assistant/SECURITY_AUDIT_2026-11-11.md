# Security Audit — 2026-11-11

**Generated:** 2026-11-11 by Hermes security-audit cron
**Scope:** Credential exposure · Channel integrity · Recent security events
**Overall: 🟠 DEGRADED** — Telegram fully healthy (live token valid via direct `getMe`, gateway restarted clean today PID 16696, topic 20 verified). **WhatsApp bridge remains DOWN** (6th consecutive audit; shifted from `WinError 5` to connect timeouts, creds.json present but session not holding). No token exposure, no breach markers, no provider-key failures this window. Credential posture unchanged and clean.

---

## 1. Credential Exposure

| Check | Status | Detail |
|-------|--------|--------|
| Telegram bot token (live, AppData root) | ✅ PASS | `getMe` → `{"ok":true}` (@Ogaitchhermesbot id 8277244378). Token valid. |
| Stale token (other root) | ⚠️ WARN | `~/.hermes/.env` still holds a **13-char dead placeholder** (`827724...` masked). Live gateway unaffected (uses AppData root with 46-char live token). Persistent dual-root divergence debt (10+ cycles). |
| Backup `.env` copies | ✅ PASS | **0** across `~/.hermes` backups, state-snapshots, `~/hermes-backup`, `~/.openclaw`. Sustained clean. |
| Credential caches | ✅ PASS | No `bws_cache.json`, `.secret_cache`, or token cache files in either root. |
| `.env`-reader scripts | ⚠️ WARN | 1 runtime sender set remains (intentional cron senders: `scripts/ghana_telegram_report.py`, `memory_review_telegram.py`, `h_evening_checkin_send.py`, `mum_evening_checkin.py`, `Vault/.../MissionControl/mission_control.py`, `health/send_*.py`). No secrets at rest — read via env at runtime, but leak tokens to process table/shell history. No new test artifacts this cycle. |
| `google_token.json` ACL | ✅ PASS | Both roots: SYSTEM / Administrators / User only (F). No "Everyone"/"BUILTIN\Users". Correct Windows default. |
| AGENTS.md BOM / invisible chars | ✅ PASS | workspace AGENTS.md: UTF-8, no BOM (CRLF only). Main AGENTS.md absent (not a finding). |
| config.yaml secrets | ✅ PASS | No plaintext long-lived secrets; keys referenced via env. |
| `allow_all_users` (config.yaml) | ⚠️ WARN | `GATEWAY_ALLOW_ALL_USERS: true` broadens attack surface on all platforms; confirm intentional. |

## 2. Channel Integrity

| Channel | Status | Detail |
|---------|--------|--------|
| Gateway process | ✅ PASS | Running (PID **16696**, python 3.14.9). Clean restart today 12:07; prior PID 5436 had an **unclean exit** flagged `gateway.previous_unclean_exit` (heartbeat stopped 05:28). No crash loop (0 `asyncio.run.exception` entries). |
| Telegram adapter | ✅ PASS | **Polling healthy.** Live token valid via direct `getMe`. Sticky IPv4 (149.154.166.110) actively recovering during hostname ConnectTimeouts — resilient. Topic 20 verified (`getChat` → supergroup "Agent Hermes", `is_forum: true`). |
| **WhatsApp** | ❌ **FAIL (PERSISTENT — 6th audit)** | **Bridge DOWN.** Symptom shift: 11-10 was `WinError 5 Access denied` on `bridge.js` (attempt 279); as of 11-11 it is **repeated `connect timed out after 30s`** (retries every 60–300s). `creds.json` present (AppData root, 3243 B) but "not paired" / session not holding. Blocks Mum/Dad/2Real poster. |
| Topic 20 (Memory Review) | ✅ PASS | Verified live this cycle (supergroup + forum). Valid delivery target. |
| Cron silent delivery | ⚠️ WARN | **25/56** jobs deliver to `origin` (16) or `local` (9) — output never reaches a user. 31 topic-targeted. Unchanged. |
| Defunct-thread jobs (`telegram:123286468`) | ⚠️ WARN | **2** jobs (Mom Morning + Mom Evening Exercise Reminders) deliver to a non-Nursing thread. Not remediated since 10-30. |

## 3. Recent Security Events

- **No `InvalidToken` / live Telegram token rejection** this window ✅ — only the stale `~/.hermes/.env` placeholder (§1) and historical rotated-log entries. Live token accepted.
- **No provider 401/403/402/429 / InvalidKey / quota failures** in raw scan (run logs show only routine OpenRouter/DeepSeek API traffic to CoreWeave/Wafer). ✅
- **No breach / unauthorized-access markers** — no `Blocked unauthorized user`, no `Friended-by`, no `InvalidToken` events. ✅
- **Multiplex duplicate-credential stays RESOLVED** — continuing from 11-08; no `default`/`content-buddy` credential-conflict occurrences. ✅
- **WhatsApp bridge** — sole active channel failure (§2). Same session not holding; symptom now timeout rather than WinError 5. Requires re-pair / permission inspection.
- **Gateway unclean exit (PID 5436 → 16696)** — prior gateway died quietly (last heartbeat 05:28); clean replacement at 12:07 today. No breach indicator; routine process turnover triggers recovery.
- **Live gateway logs confirmed at AppData root** — `~/.hermes/logs/gateway.log` remains a stale Oct 13 copy; live telemetry at `AppData/Local/hermes/logs/gateway.log` + `gateway-stdio.log`. RCA normal; no integrity concern.

---

## Trend vs 2026-11-10

| Item | 11-10 | 11-11 | Direction |
|------|-------|-------|-----------|
| Telegram token (live) | PASS | PASS | No Change |
| Gateway | PASS (PID 34324) | PASS (PID 16696, clean restart) | Stable (PID turnover) |
| **WhatsApp** | FAIL (attempt 279; WinError 5) | FAIL (timeout loop) | No Change (persistent, 6th) — symptom shift |
| Dual-root divergence | WARN | WARN | No Change (persistent debt, 10+) |
| Backup `.env` copies | PASS (0) | PASS (0) | No Change |
| `.env`-reader scripts | 7 test deleted; runtime remain | runtime remain only | No Change |
| Cron silent delivery | 25/56 | 25/56 | No Change |
| `telegram:123286468` thread loss | WARN | WARN | Not remediated (2 jobs) |
| Multiplex dup-credential | RESOLVED | RESOLVED | No Change |
| `google_token.json` ACL | PASS | PASS | No Change |

**Persistent security debt (3+ cycles):** dual-root token divergence (10+), 25/56 silent cron targets, `telegram:123286468` thread loss, **WhatsApp bridge down (6th audit)**.
**No improvements or regressions this cycle** — stable aside from gateway PID turnover.

## 🔧 Remediation Priority
1. **Restore WhatsApp** — bridge down 6th day; symptom shifted WinError 5 → connect timeout. Inspect bridge process + re-pair via `hermes whatsapp` / dashboard. Highest impact (Mum/Dad check-ins + 2Real poster).
2. **Delete stale `~/.hermes/.env` placeholder** → single authoritative AppData root (persistent debt, 10+ cycles).
3. Fix the 2 Mom exercise-reminder jobs to keep the Nursing coord thread (424) — `123286468` target is dead.
4. Re-review 25/56 silent cron targets (`origin`/`local`).
5. Confirm `allow_all_users: true` is intentional; restrict if not.

## Retention Note
Rolling 7-day window enforced. Files retained: 11-04 … 11-10 (7) before this write; adding 11-11, deleting 11-04. Within budget.

---
*Generated 2026-11-11 by Hermes security-audit cron.*