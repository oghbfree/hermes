# Security Audit — 2026-11-02

**Generated:** 2026-11-02 09:06 by Hermes security-audit cron
**Scope:** Credential exposure · Channel integrity · Recent security events
**Overall: 🟢 HEALTHY** — Live Telegram token valid, gateway polling ACTIVE today, WhatsApp paired and flushing, no breach markers / no new credential exposure. Persistent low-severity debt unchanged (dual-root divergence, silent cron targets, legacy `.env`-reader scripts, Mom-reminders thread loss).

---

## 1. Credential Exposure

| Check | Status | Detail |
|-------|--------|--------|
| Telegram bot token (live) | ✅ PASS | AppData root `.env` token **valid** (`getMe` → `{"ok":true}`, @Ogaitchhermesbot id 8277244378). Gateway runs from AppData root → uses the good token. |
| Stale token (other root) | ⚠️ WARN | `~/.hermes/.env` (Aug 22) still holds a **dead placeholder** (`getMe` → HTTP 404, `827724...1UJE`). Live gateway unaffected. Persistent dual-root divergence debt (3+ cycles). |
| Backup `.env` copies | ✅ PASS | **0** via `find` across all scan trees (AppData + `~/.hermes` backups, state-snapshots, `~/hermes-backup`, `~/.openclaw`). Sustained clean. |
| Credential caches | ✅ PASS | `bws_cache.json`, `.secret_cache` — absent in both roots. |
| `.env`-reader scripts | ⚠️ WARN | **5** legacy helpers persist in `~/.hermes/workspace/scripts/`: `ghana_telegram_report.py`, `h_evening_checkin_send.py`, `memory_review_telegram.py`, `mum_evening_checkin.py`, `send_ghana_report.py`. `send_ghana_report.py` reads the DEAD `~/.hermes/.env` → LOW risk. Skill helper scripts excluded (legit). Unchanged from 11-01. |
| `google_token.json` ACL | ✅ PASS | `icacls`: SYSTEM / Administrators / Owner only (F). No "Everyone" or "BUILTIN\Users". Correct Windows default. |
| `~/.hermes/.env` ACL | ✅ PASS | SYSTEM / Administrators / Owner only (F). Clean. |
| AGENTS.md BOM / invisible chars | ✅ PASS | No BOM / invisible chars in workspace AGENTS.md. Clean. |

## 2. Channel Integrity

| Channel | Status | Detail |
|---------|--------|--------|
| Gateway process | ✅ PASS | Live PID **1800** (python 3.14.9) running. `tasklist` confirms process alive. |
| Telegram adapter | ✅ PASS | **Polling ACTIVE Nov 2 09:06** — `getUpdates progressing (generation 1)`, `set_my_commands` OK (60 cmds). Token valid via direct `getMe`. No token rejection this window. |
| WhatsApp | ✅ PASS | Connected & live. `creds.json` present; message batches flushing Nov 2 09:06–09:08 across DMs. Bridge active. |
| WhatsApp home-notification | ⚠️ WARN | `Home-channel startup notification failed for whatsapp:-1003784520976:` — startup ping to home channel did not deliver. Isolated; bot still active on user DMs. LOW. |
| Topic 20 (Memory Review) | ✅ PASS | This job delivers to `telegram:-1003784520976:20`; targets confirmed reachable via `getChat` (supergroup + forum). |
| Cron silent delivery | ⚠️ WARN | **25/56** jobs deliver to `origin` (16) or `local` (9) — output never reaches a user. 31 topic/channel-targeted. Essentially unchanged. |
| Defunct thread job `aebf7e736923` | ⚠️ WARN | Mom Morning Exercise Reminders still delivering with thread_id **lost** — logged Nov 2 09:07: `deliver=telegram:123286468`, `thread_id: None` (was 424). **Not remediated.** |

## 3. Recent Security Events

- **No `InvalidToken` / token rejections / provider 401/403 in live logs** this window ✅.
- **No blocked-user / unauthorized-access / breach markers** ✅ (last blocked-user event: Aug 13).
- **No provider quota/billing failures** (no 402/429).
- **`config.yaml allow_all_users: true`** → every sender on every platform granted access (bridged to `GATEWAY_ALLOW_ALL_USERS`; an explicit env var would win). ⚠️ LOW if intentionally open-lab; revisit if this is not desired.
- **Nous Portal:** invalid refresh token (LOW, persistent; custom OpenRouter provider active).
- **Non-security operational noise** (ignored): skill-not-found `2real-enterprises-agent`, one WebSocket teardown warning, tool sandbox blocks on recursive-delete of interpreter (expected).

---

## Trend vs 2026-11-01

| Item | 11-01 | 11-02 | Direction |
|------|-------|-------|-----------|
| Telegram token (live) | PASS | PASS | No Change |
| Gateway polling | PASS | PASS (ACTIVE today) | Stable |
| Dual-root divergence | WARN | WARN | No Change (persistent debt) |
| Backup `.env` copies | PASS (0) | PASS (0) | No Change |
| Credential caches | PASS | PASS | No Change |
| `.env`-reader scripts | WARN (5) | WARN (5) | No Change |
| WhatsApp | PASS | PASS | Stable |
| Cron silent delivery | 25/57 | 25/56 | No Change |
| `aebf7e736923` thread loss | WARN | WARN | **Not remediated** |
| ACLs (google_token, .env) | — | PASS | Confirmed clean |

**Improvement:** none materially changed; stable and healthy.
**Persistent security debt (3+ cycles):** dual-root token divergence, 25/56 silent cron targets, legacy `.env`-reader scripts (5, stable), `aebf7e736923` thread loss.
**No new active credential exposure. No token rejection. No breach markers.**

## 🔧 Remediation Priority
1. Delete the revoked `~/.hermes/.env` placeholder → single authoritative AppData root.
2. Retire the 5 legacy `.env`-reading helper scripts (deliver via Hermes-native path).
3. Fix job `aebf7e736923` (Mom Morning Reminders) so delivery keeps thread_id 424.
4. Re-review 25/56 silent cron targets (`origin`/`local`).
5. Confirm `allow_all_users: true` is intentional (or pin `GATEWAY_ALLOW_ALL_USERS`).

## Retention Note
Rolling 7-day window. Oldest (10-26) dropped; 10-27 → 11-02 retained (7 files). Report artifact: `C:\Users\User\.hermes\workspace\Vault\System\Assistant\SECURITY_AUDIT_2026-11-02.md`.

---
*Generated 2026-11-02 by Hermes security-audit cron.*
