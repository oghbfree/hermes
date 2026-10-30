# Security Audit — 2026-10-29

**Generated:** 2026-10-29 07:00 by Hermes security-audit cron
**Scope:** Credential exposure · Channel integrity · Recent security events
**Overall: 🟢 HEALTHY** — Live Telegram token valid, both channels functional, no breach markers. Persistent low-severity debt unchanged.

---

## 1. Credential Exposure

| Check | Status | Detail |
|-------|--------|--------|
| Telegram bot token (live) | ✅ PASS | AppData `.env` (Oct 21) token **valid** (`getMe` → `{"ok":true}`, @Ogaitchhermesbot id 8277244378). Gateway runs from AppData root → uses the good token. |
| Stale token (other root) | ⚠️ WARN | `~/.hermes/.env` (Aug 22) still holds a **dead/placeholder token** (`getMe` → HTTP 404, `827724...1UJE`). Live gateway unaffected. Persistent dual-root divergence debt. |
| Backup `.env` copies | ✅ PASS | **0** via `find` across all scan trees (`~/.hermes`, `state-snapshots`, `~/hermes-backup`, `~/.openclaw`). Sustained clean. |
| Credential caches | ✅ PASS | `bws_cache.json`, `.secret_cache` — absent in both roots. |
| `google_token.json` ACL | ✅ PASS | AppData root: `icacls` shows only SYSTEM + BUILTIN\Administrators + Owner (User) (I)(F). No Everyone/Users. Standard Windows ACL. |
| `.env`-reader scripts | ⚠️ WARN | 5 legacy helper scripts in workspace/scripts/ reference `.env`/dotenv (`ghana_telegram_report.py`, `h_evening_checkin_send.py`, `memory_review_telegram.py`, `mum_evening_checkin.py`, `send_ghana_report.py`). They read via the AppData `.env` **or** the dead placeholder token (LOW risk); pattern should be retired. `care_checkin.py` is 0 bytes (orphaned) at both roots. |
| AGENTS.md BOM / invisible chars | ✅ PASS | `~/.hermes/AGENTS.md` and AppData `AGENTS.md` both absent. `~/.hermes/workspace/AGENTS.md` UTF-8, no BOM. Clean. |

## 2. Channel Integrity

| Channel | Status | Detail |
|---------|--------|--------|
| Gateway process | ✅ PASS | PID **15048** alive (python 3.14.7), started 2026-10-25 04:21. AppData `gateway.log` fresh — last write today 06:38. |
| Gateway crash state | ✅ PASS | `gateway-exit-diag` last `gateway.start` 10-25 (PID 15048), one `previous_unclean_exit` (prior PID 21768) — no crash-loop entries this window. |
| Telegram adapter | ✅ PASS | Polling active. Transient DNS/transport flakiness (03:21, 06:22 dual-stack `ConnectError` on `api.telegram.org` / IPv4) — **each self-recovered in ~11s** via alternate path. Valid token confirmed via direct `getMe`. |
| WhatsApp | ✅ PASS | Connected (native gateway). Session `creds.json` present, updated today 07:00. Live. |
| Topic 20 (Memory Review) | ✅ PASS | Confirmed in `channel_directory.json` (`Agent Hermes / topic 20`, `-1003784520976:20`). |
| Cron silent delivery | ⚠️ WARN | **25/56** jobs (45%) deliver to `origin` (16) or `local` (9) — output never reaches a user. 31 topic/channel-targeted. Unchanged. |

## 3. Recent Security Events

- **No `InvalidToken` / token rejections** in live agent/errors logs this window ✅. Only historical Oct 13 event = the dead placeholder token in `~/.hermes/.env` (not a live-credential incident).
- **No blocked-user / unauthorized-access / breach markers** ✅.
- **Telegram DNS/transport flakiness** (recurring, host-level, self-healing): transient `ConnectError` at 03:21 and 06:22 today, each recovered ~11s. Network churn (LOW), not an attack marker.
- **NEW (minor):** 07:00 `ERROR hermes_cli.web_server: Failed to list cron jobs for profile sat-nav` — web-server listing error against the sat-nav profile's own cron dir (which exists and is intact). Isolated profile-level, no exposure, monitor.
- **`jobs.json` Permission-denied IOError** — not observed today (last 10-27). Not recurring.
- **Nous Portal**: invalid refresh token (non-blocking; custom OpenRouter provider active). LOW (persistent).

---

## Trend vs 2026-10-28

| Item | 10-28 | 10-29 | Direction |
|------|-------|-------|-----------|
| Telegram token (live) | PASS | PASS | No Change |
| Dual-root divergence | WARN | WARN | No Change (persistent debt) |
| Backup `.env` copies | PASS (0) | PASS (0) | No Change |
| Credential caches | PASS | PASS | No Change |
| `.env`-reader scripts | WARN (~10) | WARN (5) | **Improved** (scope narrowed/cleaned) |
| Google token ACL | PASS | PASS | No Change |
| WhatsApp | PASS | PASS | Stable |
| Cron silent delivery | 25/56 | 25/56 | No Change |
| AGENTS.md BOM | PASS | PASS | No Change |
| `jobs.json` IOError | NOT OBSERVED | NOT OBSERVED | No Change (resolved) |
| allow_all_users | WARN | WARN | No Change |
| Profile cron list err | — | WARN (NEW) | **New** (isolated, monitor) |

**Improvement:** `.env`-reader helper scripts reduced (~10 → 5 identified active).
**Persistent security debt (3+ cycles):** dual-root token divergence (non-blocking), 25/56 silent cron targets, `.env`-reader helper scripts (shrinking), `allow_all_users: true`, Telegram DNS flakiness (transient, self-healing).
**No new active credential exposure. No token rejection. No breach markers.**

## 🔧 Remediation Priority
1. Delete the revoked `~/.hermes/.env` placeholder → single authoritative AppData root.
2. Retire the 5 remaining `.env`-reading helper scripts (deliver via Hermes-native path).
3. Set `allow_all_users: false` + explicit allow-list.
4. Re-review 25/56 silent cron targets (`origin`/`local`).
5. Monitor the sat-nav profile cron-list web error (isolated; confirm not recurring).
6. Continue monitoring Telegram DNS instability (self-healing in seconds).

## Retention Note
Rolling 7-day window. Current: 10-22, 10-24, 10-25, 10-26, 10-27, 10-28, 10-29 (=7, at cap). Oldest (10-20) already dropped implicitly. Report artifact: `C:\Users\User\.hermes\workspace\Vault\System\Assistant\SECURITY_AUDIT_2026-10-29.md`.

---
*Generated 2026-10-29 by Hermes security-audit cron.*