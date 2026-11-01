# Security Audit — 2026-10-30

**Generated:** 2026-10-30 14:47 by Hermes security-audit cron
**Scope:** Credential exposure · Channel integrity · Recent security events
**Overall: 🟢 HEALTHY** — Live Telegram token valid, both channels functional, no breach markers / no credential exposure. Gateway recovered from midday startup churn. Persistent low-severity debt unchanged.

---

## 1. Credential Exposure

| Check | Status | Detail |
|-------|--------|--------|
| Telegram bot token (live) | ✅ PASS | AppData `.env` (updated Oct 30 10:39) token **valid** (`getMe` → `{"ok":true}`, @Ogaitchhermesbot id 8277244378). Gateway runs from AppData root → uses the good token. |
| Stale token (other root) | ⚠️ WARN | `~/.hermes/.env` (Aug 22) still holds a **dead placeholder** (`getMe` → HTTP 404, `827724...1UJE`). Live gateway unaffected. Persistent dual-root divergence debt. |
| Backup `.env` copies | ✅ PASS | **0** via `find` across all scan trees (`~/.hermes` backups, `state-snapshots`, `~/hermes-backup`, `~/.openclaw`). Sustained clean. |
| Credential caches | ✅ PASS | `bws_cache.json`, `.secret_cache` — absent in both roots. |
| `google_token.json` ACL | ✅ PASS | Both roots `icacls`: only SYSTEM + BUILTIN\Administrators + Owner(User)(I)(F). No Everyone/Users. Standard Windows ACL. |
| `.env`-reader scripts | ⚠️ WARN | **5** legacy helpers in `workspace/scripts/` read `.env` + `TELEGRAM_BOT_TOKEN` (`ghana_telegram_report.py`, `h_evening_checkin_send.py`, `memory_review_telegram.py`, `mum_evening_checkin.py`, `send_ghana_report.py`). `send_ghana_report.py` reads the DEAD `~/.hermes/.env` → LOW risk (would fail, not exfiltrate live key). `care_checkin.py` 0 bytes (orphaned). Pattern should be retired. |
| AGENTS.md BOM / invisible chars | ✅ PASS | `~/.hermes/AGENTS.md` and AppData AGENTS.md absent; `~/.hermes/workspace/AGENTS.md` UTF-8, no BOM. Clean. |

## 2. Channel Integrity

| Channel | Status | Detail |
|---------|--------|--------|
| Gateway process | ✅ PASS (RECOVERED) | PID **16288** (python 3.14.9) started 14:43 today, ESTABLISHED TCP to Telegram (149.154.166.110:443). Old PID 15048 (memory ref) dead — superseded. |
| Gateway crash state | ⚠️ WARN (resolved) | `exit-diag` shows **startup churn 13:44–14:43**: PIDs 8992/16388/3992 exited non-zero / SystemExit code 78, resolved cleanly at 14:43 with PID 16288. **0** `asyncio.run.exception` entries → not a crash loop, a transient mid-day restart sequence now healthy. |
| Telegram adapter | ✅ PASS | Polling active, connected 14:43. Token valid via direct `getMe`. Transient 13:05 connect timeouts (30s/45s) self-recovered by 14:43. |
| WhatsApp | ✅ PASS | Connected. Session `creds.json` present under AppData root, session dir updated today ~14:11; `bridge.log` 241 MB fresh at 14:46 (live message processing). `~/.hermes/whatsapp` is empty — real session is AppData root. |
| Topic 20 (Memory Review) | ✅ PASS | Confirmed in `channel_directory.json` (`Agent Hermes / topic 20`, `-1003784520976:20`); this job delivers to `telegram:-1003784520976:20`. |
| Cron silent delivery | ⚠️ WARN | **25/56** jobs (45%) deliver to `origin` (16) or `local` (9) — output never reaches a user. 31 topic/channel-targeted. Unchanged. |

## 3. Recent Security Events

- **No `InvalidToken` / token rejections / provider 401/403/HTTP-40x** in live logs this window ✅ (only historical Oct 13 dead-placeholder event persisted in `~/.hermes/.env`).
- **No blocked-user / unauthorized-access / breach markers** ✅.
- **NEW — Telegram/WhatsApp connect timeouts (13:05):** `telegram connect timed out after 45s` + `whatsapp connect timed out after 30s`, 1/8 retry exhausted, then **self-recovered by 14:43** gateway restart. Transient network churn (LOW), not an attack marker.
- **NEW (minor) — cron delivery-target warning (14:45):** job `aebf7e736923` (thread_id 424 configured, Nursing coord) delivered to `telegram:123286468` **without** thread — target lost the thread_id. Isolated, monitor.
- **OpenRouter auxiliary PAID lane engaged (12:55):** quota-lane routing notice, not a 402/429 rejection. LOW.
- **Nous Portal:** invalid refresh token (LOW, persistent; custom OpenRouter provider active).
- **`jobs.json` IOError (10-27) and sat-nav cron-list web error (10-29):** **not observed today** — both resolved / not recurring.

---

## Trend vs 2026-10-29

| Item | 10-29 | 10-30 | Direction |
|------|-------|-------|-----------|
| Telegram token (live) | PASS | PASS | No Change |
| Dual-root divergence | WARN | WARN | No Change (persistent debt) |
| Backup `.env` copies | PASS (0) | PASS (0) | No Change |
| Credential caches | PASS | PASS | No Change |
| `.env`-reader scripts | WARN (5) | WARN (5) | No Change |
| Google token ACL | PASS | PASS | No Change |
| WhatsApp | PASS | PASS | Stable (moved to AppData root) |
| Gateway | PASS (PID 15048) | PASS (PID 16288) | **PID replaced** — healthy after churn |
| Cron silent delivery | 25/56 | 25/56 | No Change |
| Telegram connect timeout | — | 13:05 (recovered) | **New transient** (self-healed) |
| `aebf7e736923` thread loss | — | WARN | **New** (isolated, monitor) |
| sat-nav cron-list error | WARN | NOT OBSERVED | **Resolved** |

**Improvement:** sat-nav cron-list web error from 10-29 no longer fires; gateway restarted cleanly.
**Persistent security debt (3+ cycles):** dual-root token divergence, 25/56 silent cron targets, `.env`-reader helper scripts (5, stable), `allow_all_users: true`, Telegram DNS/transport flakiness (transient, self-healing).
**No new active credential exposure. No token rejection. No breach markers.**

## 🔧 Remediation Priority
1. Delete the revoked `~/.hermes/.env` placeholder → single authoritative AppData root.
2. Retire the 5 remaining `.env`-reading helper scripts (deliver via Hermes-native path).
3. Set `allow_all_users: false` + explicit allow-list.
4. Re-review 25/56 silent cron targets (`origin`/`local`).
5. Fix job `aebf7e736923` (thread_id 424) so delivery keeps the thread target.
6. Continue monitoring Telegram DNS/transport instability (self-heals in minutes).

## Retention Note
Rolling 7-day window, target 1 file/day. Current: 10-24 → 10-30. Oldest (10-22) dropped. Report artifact: `C:\Users\User\.hermes\workspace\Vault\System\Assistant\SECURITY_AUDIT_2026-10-30.md`.

---
*Generated 2026-10-30 by Hermes security-audit cron.*