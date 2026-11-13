# Security Audit — 2026-11-12

**Generated:** 2026-11-12 by Hermes security-audit cron
**Scope:** Credential exposure · Channel integrity · Recent security events
**Overall: 🟠 DEGRADED** — Telegram fully healthy (live token valid via direct `getMe` @Ogaitchhermesbot, gateway alive PID 16696, live Telegram connection confirmed via netstat, topic 20 a valid delivery target). **WhatsApp bridge remains DOWN** (7th consecutive audit; reconnect attempt 86 today, creds.json present but session not holding). No token exposure, no breach markers, no provider-key failures this window. Credential posture unchanged and clean.

---

## 1. Credential Exposure

| Check | Status | Detail |
|-------|--------|--------|
| Telegram bot token (live, AppData root) | ✅ PASS | `getMe` → `{"ok":true}` (@Ogaitchhermesbot id 8277244378, 46-char live token). Token valid. |
| Stale token (other root) | ⚠️ WARN | `~/.hermes/.env` still holds the **13-char dead placeholder** (`827724...1UJE`), `getMe` → HTTP 404. Live gateway unaffected (uses AppData root with 46-char live token). Persistent dual-root divergence debt (11+ cycles). |
| Backup `.env` copies | ✅ PASS | **0** across `~/.hermes` backups, state-snapshots, `~/hermes-backup`, `~/.openclaw`. Sustained clean. |
| Credential caches | ✅ PASS | No `bws_cache.json`, `.secret_cache`, or token cache files in either root. |
| `.env`-reader scripts | ⚠️ WARN | Runtime cron senders read `.env` at runtime (`scripts/ghana_telegram_report.py`, `memory_review_telegram.py`, `h_evening_checkin_send.py`, `mum_evening_checkin.py`, `MissionControl/mission_control.py`, `health/send_*.py`, legacy dated mum-health check-ins). No secrets at rest; tokens enter process tables/shell history. No new `tmp_*`/test artifacts this cycle. |
| `google_token.json` ACL | ✅ PASS | SYSTEM / Administrators / User only (F). No "Everyone"/"BUILTIN\Users". Correct Windows default. |
| `.env` file ACLs (both roots) | ✅ PASS | Both `~/.hermes/.env` and `AppData\Local\hermes\.env`: SYSTEM / Administrators / User only (F). Correct. |
| AGENTS.md BOM / invisible chars | ✅ PASS | workspace AGENTS.md: UTF-8, no BOM (CRLF only). Main AGENTS.md absent. |
| config.yaml secrets | ✅ PASS | No plaintext long-lived secrets; keys referenced via env. |
| `allow_all_users` (config.yaml) | ⚠️ WARN | `GATEWAY_ALLOW_ALL_USERS: true` broadens attack surface on all platforms; confirm intentional. |

## 2. Channel Integrity

| Channel | Status | Detail |
|---------|--------|--------|
| Gateway process | ✅ PASS | Running (PID **16696**, python 3.14.9; manager=manual). Live ESTABLISHED TCP to Telegram (149.154.166.110:443 → PID 16696) confirmed via netstat. 0 `asyncio.run.exception` crash-loop entries. |
| Telegram adapter | ✅ PASS | **Polling healthy.** Live token valid via direct `getMe`. Sticky IPv4 (149.154.166.110) active. Connect cycles today via gateway.log (08:33→08:36 reconnect clean). |
| **WhatsApp** | ❌ **FAIL (PERSISTENT — 7th audit)** | **Bridge DOWN** since **2026-11-06 10:17**. Reconnect attempt **86** at 08:37 today (retry ~every 5 min). `creds.json` present (`AppData\Local\hermes\whatsapp\session\creds.json`, 3243 B, Nov 6) but session not paired/holding. Blocks Mum/Dad/2Real posters. |
| Topic 20 (Memory Review) | ✅ PASS | Valid delivery target (supergroup "Agent Hermes", forum enabled). 4 jobs target thread 20. |
| Cron silent delivery | ⚠️ WARN | **25/56** jobs deliver to `origin` (16) or `local` (9) — output never reaches a user; 31 topic-targeted. Unchanged. |
| Defunct-thread jobs (`telegram:123286468`) | ⚠️ WARN | **2** jobs (Mom Morning + Mom Evening Exercise Reminders) deliver to a non-Nursing thread. Not remediated since 10-30. |

## 3. Recent Security Events

- **No `InvalidToken` / live Telegram token rejection** this window ✅ — only the stale `~/.hermes/.env` placeholder (§1). Live token accepted by Telegram.
- **No provider 401/403/402/429 / InvalidKey / quota failures** this window ✅. One transient OpenRouter APIConnectionError at 08:31 retried and recovered (network blip, not credential).
- **No breach / unauthorized-access markers.** No `Blocked unauthorized user`, no `InvalidToken`, no unexpected paired-device events. ✅
- **Multiplex duplicate-credential stays RESOLVED** — continuing from 11-08; no `default`/`content-buddy` credential-conflict occurrences. ✅
- **WhatsApp bridge** — sole active channel failure (§2). Attempt 86, session not holding. Requires re-pair / permission inspection.
- **Live gateway logs confirmed at AppData root** — `~/.hermes/logs/gateway.log` remains a stale Oct 13 copy; live telemetry at `AppData/Local/hermes/logs/gateway.log` + `gateway-stdio.log`. RCA normal; no integrity concern.

---

## Trend vs 2026-11-11

| Item | 11-11 | 11-12 | Direction |
|------|-------|-------|-----------|
| Telegram token (live) | PASS | PASS | No Change |
| Gateway | PASS (PID 16696) | PASS (PID 16696, LIVE TCP conn) | Stable |
| **WhatsApp** | FAIL (attempt 56, timeout) | FAIL (attempt 86, timeout) | No Change (persistent, 7th) |
| Dual-root divergence | WARN | WARN | No Change (persistent debt, 11+) |
| Backup `.env` copies | PASS (0) | PASS (0) | No Change |
| `.env`-reader scripts | runtime remain | runtime remain | No Change |
| Cron silent delivery | 25/56 | 25/56 | No Change |
| `telegram:123286468` thread loss | WARN | WARN | Not remediated (2 jobs) |
| Multiplex dup-credential | RESOLVED | RESOLVED | No Change |
| `google_token.json` ACL | PASS | PASS | No Change |

**Persistent security debt (3+ cycles):** dual-root token divergence (11+), 25/56 silent cron targets, `telegram:123286468` thread loss, **WhatsApp bridge down (7th audit)**.
**No improvements or regressions this cycle** — stable; gateway confirmed live via TCP connection.

## 🔧 Remediation Priority
1. **Restore WhatsApp** — bridge down 7th day (attempt 86). Inspect bridge process + re-pair via `hermes whatsapp` / dashboard. Highest impact (Mum/Dad check-ins + 2Real poster).
2. **Delete stale `~/.hermes/.env` placeholder** → single authoritative AppData root (persistent debt, 11+ cycles).
3. Fix the 2 Mom exercise-reminder jobs to keep the Nursing coord thread (424) — `123286468` target is dead.
4. Re-review 25/56 silent cron targets (`origin`/`local`).
5. Confirm `allow_all_users: true` is intentional; restrict if not.

## Retention Note
Rolling 7-day window enforced. Retained: 11-06 … 11-12 (7). Within budget; no deletions needed this cycle.

---
*Generated 2026-11-12 by Hermes security-audit cron.*