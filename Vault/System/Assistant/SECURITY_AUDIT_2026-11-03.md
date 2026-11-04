# Security Audit — 2026-11-03

**Generated:** 2026-11-03 07:00 by Hermes security-audit cron
**Scope:** Credential exposure · Channel integrity · Recent security events
**Overall: 🟢 HEALTHY** — Live Telegram token valid, gateway polling active, WhatsApp paired and flushing, no breach markers / no new credential exposure. Persistent low-severity debt unchanged (dual-root divergence, silent cron targets, legacy `.env`-reader scripts, Mom-reminders thread loss). NEW: multiplex duplicate-credential error on 2 consecutive restarts.

---

## 1. Credential Exposure

| Check | Status | Detail |
|-------|--------|--------|
| Telegram bot token (live) | ✅ PASS | AppData root `.env` token **valid** (`getMe` → `{"ok":true}`, @Ogaitchhermesbot id 8277244378). Gateway runs from AppData root → uses the good token. |
| Stale token (other root) | ⚠️ WARN | `~/.hermes/.env` (Aug 22) still holds a **dead placeholder** (`getMe` → HTTP 404, `827724...1UJE`). Live gateway unaffected. Persistent dual-root divergence debt (3+ cycles). |
| Backup `.env` copies | ✅ PASS | **0** via `find` across AppData + `~/.hermes` backups, state-snapshots, `~/hermes-backup`, `~/.openclaw`. Sustained clean. |
| Credential caches | ✅ PASS | `bws_cache.json`, `.secret_cache` — absent in both roots. Only `plugin_toolset_keys.json` (harmless). |
| `.env`-reader scripts | ⚠️ WARN | **5** legacy helpers persist in `~/.hermes/workspace/scripts/`: `ghana_telegram_report.py`, `h_evening_checkin_send.py`, `memory_review_telegram.py`, `mum_evening_checkin.py`, `send_ghana_report.py`. `send_ghana_report.py` reads the DEAD `~/.hermes/.env` → LOW risk. None found in the live AppData workspace. Unchanged from 11-02. |
| `google_token.json` ACL | ✅ PASS | `icacls`: SYSTEM / Administrators / Owner only (F). No "Everyone" / "BUILTIN\Users". Correct Windows default. |
| `~/.hermes/.env` ACL | ✅ PASS | SYSTEM / Administrators / Owner only (F). Clean. |
| AGENTS.md BOM / invisible chars | ✅ PASS | No BOM / invisible chars in workspace AGENTS.md. Clean. |
| config.yaml secrets | ✅ PASS | No plaintext API keys / long-lived secrets in config.yaml. |

## 2. Channel Integrity

| Channel | Status | Detail |
|---------|--------|--------|
| Gateway process | ✅ PASS | Running. Live log fresh (last write Nov 3 06:36). Established connections to Telegram IPs. Refreshed 03:48 today. |
| Gateway crash state | ✅ PASS | `gateway-exit-diag.log`: **0** `asyncio.run.exception` / `ModuleNotFoundError` entries in active window. No crash loop. |
| Telegram adapter | ✅ PASS | Polling ACTIVE (log activity Nov 3 06:36). Token valid via direct `getMe`. Transient transport flakiness: IPv4 API IP `ConnectError` at 06:36, **self-healed within ~11s** via `api.telegram.org`. Persistent low-severity, self-healing. |
| WhatsApp | ✅ PASS | Connected & live. `creds.json` present (paired). Bridge log active (241 MB, flushed Nov 3 07:01); session sync Nov 3 05:55. |
| Topic 20 (Memory Review) | ✅ PASS | Confirmed in `channel_directory.json` (`Agent Hermes / topic 20`, `-1003784520976:20`); this job delivers to `telegram:-1003784520976:20`. |
| Cron silent delivery | ⚠️ WARN | **25/56** jobs deliver to `origin` (16) or `local` (9) — output never reaches a user. 31 topic/channel-targeted. Unchanged. |
| Defunct-thread jobs (`telegram:123286468`) | ⚠️ WARN | **2** jobs — Mom Morning **and** Mom Evening Exercise Reminders — deliver to `telegram:123286468` without the Nursing coord thread (thread_id 424 lost). Not remediated since 10-30. |
| Multiplex credential conflict (NEW) | ⚠️ WARN | Duplicate-credential **ERROR** on 2 consecutive restarts (Nov 2 21:58, Nov 3 03:48): profiles `default` and `content-buddy` both configure the same telegram credential — content-buddy's Telegram instance refused to start. Other profiles (coach, harold, sat-nav) correctly skip absent credentials. |

## 3. Recent Security Events

- **No `InvalidToken` / token rejections / provider 401/403 in live logs** this window ✅.
- **No blocked-user / unauthorized-access / breach markers** ✅.
- **No provider quota/billing failures** (no 402/429). OpenRouter retries on 10-31 were transient `Connection error` retries, self-recovered — network, not credential. LOW.
- **Telegram transport churn (persistent, LOW):** IPv4 API IP `ConnectError` swap, self-healing in ~11s (06:36 today). Host-level network instability, not an attack marker.
- **Nous Portal:** invalid refresh token (LOW, persistent; custom OpenRouter provider active).

---

## Trend vs 2026-11-02

| Item | 11-02 | 11-03 | Direction |
|------|-------|-------|-----------|
| Telegram token (live) | PASS | PASS | No Change |
| Gateway | PASS | PASS | Stable |
| Dual-root divergence | WARN | WARN | No Change (persistent debt) |
| Backup `.env` copies | PASS (0) | PASS (0) | No Change |
| Credential caches | PASS | PASS | No Change |
| `.env`-reader scripts | WARN (5) | WARN (5) | No Change |
| WhatsApp | PASS | PASS | Stable |
| Cron silent delivery | 25/56 | 25/56 | No Change |
| `aebf7e736923` thread loss | WARN | WARN | **Not remediated** (2 jobs now) |
| Multiplex dup-credential | — | WARN | **NEW** (2 restarts affected) |
| ACLs (google_token, .env) | PASS | PASS | Confirmed clean |

**Persistent security debt (3+ cycles):** dual-root token divergence, 25/56 silent cron targets, legacy `.env`-reader scripts (5, stable), `telegram:123286468` thread loss. **NEW (1st):** default/content-buddy duplicate telegram credential.
**No new active credential exposure. No token rejection. No breach markers.**

## 🔧 Remediation Priority
1. Delete the revoked `~/.hermes/.env` placeholder → single authoritative AppData root.
2. Resolve default/content-buddy duplicate telegram credential (give content-buddy its own token, or disable its Telegram).
3. Retire the 5 legacy `.env`-reading helper scripts (deliver via Hermes-native path).
4. Fix the 2 Mom exercise-reminder jobs so delivery keeps Nursing coord thread_id 424.
5. Re-review 25/56 silent cron targets (`origin`/`local`).
6. Continue monitoring Telegram transport instability (self-heals in seconds).

## Retention Note
Rolling 7-day window. Oldest kept 10-28 → 11-03 (7 files). Report artifact: `C:\Users\User\.hermes\workspace\Vault\System\Assistant\SECURITY_AUDIT_2026-11-03.md`.

---
*Generated 2026-11-03 by Hermes security-audit cron.*