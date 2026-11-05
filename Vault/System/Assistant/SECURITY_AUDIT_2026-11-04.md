# Security Audit — 2026-11-04

**Generated:** 2026-11-04 07:00 by Hermes security-audit cron
**Scope:** Credential exposure · Channel integrity · Recent security events
**Overall: 🟢 HEALTHY** — Live Telegram token valid, gateway polling active, WhatsApp live and flushing, no breach markers / no new credential exposure. Persistent low-severity debt unchanged (dual-root divergence, silent cron targets, legacy `.env`-reader scripts, Mom-reminders thread loss). Multiplex duplicate-credential error **recurs a 3rd day** (escalating to persistent security debt).

---

## 1. Credential Exposure

| Check | Status | Detail |
|-------|--------|--------|
| Telegram bot token (live) | ✅ PASS | AppData root `.env` token **valid** (`getMe` → `{"ok":true}`, @Ogaitchhermesbot id 8277244378). Gateway runs from AppData root → uses the good token. |
| Stale token (other root) | ⚠️ WARN | `~/.hermes/.env` (Aug 22) still holds a **dead placeholder** (`getMe` → HTTP 404, `827724...1UJE`). Live gateway unaffected. Persistent dual-root divergence debt (4+ cycles). |
| Backup `.env` copies | ✅ PASS | **0** via `find` across AppData + `~/.hermes` backups, state-snapshots, `~/hermes-backup`, `~/.openclaw`. Sustained clean. |
| Credential caches | ✅ PASS | `bws_cache.json`, `.secret_cache` — absent in both roots. |
| `.env`-reader scripts | ⚠️ WARN | **5+ legacy helpers** read `TELEGRAM_BOT_TOKEN` directly from the dead `~/.hermes/.env` (LOW risk): `workspace/scripts/{ghana_telegram_report.py, h_evening_checkin_send.py, memory_review_telegram.py, mum_evening_checkin.py, send_ghana_report.py}` plus `2real-agent/ghana_telegram_report.py`, `MissionControl/mission_control.py`, `workspace/send_evening_health_check.py`. Unchanged from 11-03. |
| `google_token.json` ACL | ✅ PASS | `icacls`: SYSTEM / Administrators / Owner only (F). No "Everyone" / "BUILTIN\Users". Correct Windows default. |
| AGENTS.md BOM / invisible chars | ✅ PASS | No BOM / invisible chars in workspace AGENTS.md. Clean. |
| config.yaml secrets | ✅ PASS | No plaintext API keys / long-lived secrets in config.yaml (all `api_key:` fields empty — referenced via env). |

## 2. Channel Integrity

| Channel | Status | Detail |
|---------|--------|--------|
| Gateway process | ✅ PASS | Running. PID 15952. Live log fresh (last write Nov 4 07:03). Established connections to Telegram IPs (149.154.166.110:443). |
| Gateway crash state | ✅ PASS | No `asyncio.run.exception` / `ModuleNotFoundError` in active window. No crash loop. |
| Telegram adapter | ✅ PASS | Polling ACTIVE (log Nov 4 06:53:33 "polling confirmed healthy"). Token valid via direct `getMe`. Transient connect churn at 06:53 self-healed within ~30s. Persistent low-severity transport instability. |
| WhatsApp | ✅ PASS | Connected & live. Bridge flushing text batches (Nov 4 06:55, 07:03). |
| Topic 20 (Memory Review) | ✅ PASS | Confirmed in `channel_directory.json` (`Agent Hermes / topic 20`, `-1003784520976:20`). |
| Cron silent delivery | ⚠️ WARN | **25/56** jobs deliver to `origin` (16) or `local` (9) — output never reaches a user. 31 topic/channel-targeted. Unchanged. |
| Defunct-thread jobs (`telegram:123286468`) | ⚠️ WARN | **2** jobs — Mom Morning **and** Mom Evening Exercise Reminders — deliver to `telegram:123286468` without the Nursing coord thread (thread_id 424 lost). Not remediated since 10-30. |
| Multiplex duplicate credential | ⚠️ WARN→ESCALATE | Recurred **3rd consecutive day** (Nov 2 21:58, Nov 3 03:48, Nov 4 01:20): profiles `default` and `content-buddy` both configure the same telegram credential — content-buddy's Telegram instance refused to start. Now **persistent security debt** (3+ cycles). |

## 3. Recent Security Events

- **No `InvalidToken` / token rejections / provider 401/403 in live logs** this window ✅. (The only InvalidToken matches in live root are test-file mentions in `bootstrap-installer.log` — not real events.)
- **No blocked-user / unauthorized-access / breach markers** ✅.
- **No provider quota/billing failures** (no 402/429) ✅.
- **Telegram transport churn (persistent, LOW):** Dual-stack + IPv4 API IP `ConnectError` "All connection attempts failed" at 06:53, self-healed within ~30s (polling healthy by 06:53:33). Host-level network instability, not an attack marker.
- **Multiplex duplicate-credential ERROR** (Nov 4 01:20) — same event as §2; config-level, not a compromise.

---

## Trend vs 2026-11-03

| Item | 11-03 | 11-04 | Direction |
|------|-------|-------|-----------|
| Telegram token (live) | PASS | PASS | No Change |
| Gateway | PASS | PASS | Stable |
| Dual-root divergence | WARN | WARN | No Change (persistent debt) |
| Backup `.env` copies | PASS (0) | PASS (0) | No Change |
| Credential caches | PASS | PASS | No Change |
| `.env`-reader scripts | WARN (5) | WARN (5+) | No Change |
| WhatsApp | PASS | PASS | Stable |
| Cron silent delivery | 25/56 | 25/56 | No Change |
| `telegram:123286468` thread loss | WARN | WARN | **Not remediated** (2 jobs) |
| Multiplex dup-credential | WARN | WARN | **Recurred 3rd day → ESCALATED** |

**Persistent security debt (3+ cycles):** dual-root token divergence, 25/56 silent cron targets, legacy `.env`-reader scripts, `telegram:123286468` thread loss, **multiplex duplicate-credential (now escalated)**.
**No new active credential exposure. No token rejection. No breach markers.**

## 🔧 Remediation Priority
1. Delete the revoked `~/.hermes/.env` placeholder → single authoritative AppData root.
2. Resolve default/content-buddy duplicate telegram credential (give content-buddy its own token, or disable its Telegram) — now persistent debt.
3. Retire the 5+ legacy `.env`-reading helper scripts (deliver via Hermes-native path).
4. Fix the 2 Mom exercise-reminder jobs so delivery keeps Nursing coord thread_id 424.
5. Re-review 25/56 silent cron targets (`origin`/`local`).
6. Continue monitoring Telegram transport instability (self-heals in ~30s).

## Retention Note
Rolling 7-day window. Delete `SECURITY_AUDIT_2026-10-27.md` (oldest, beyond window) after this write to hold at 7 files.

---
*Generated 2026-11-04 by Hermes security-audit cron.*