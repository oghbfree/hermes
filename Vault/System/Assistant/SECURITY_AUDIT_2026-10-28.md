# Security Audit — 2026-10-28

**Generated:** 2026-10-28 ~07:05 by Hermes security-audit cron
**Scope:** Credential exposure · Channel integrity · Recent security events
**Overall: 🟢 HEALTHY** — No active credential exposure, no token rejection, both channels functional.

---

## 1. Credential Exposure

| Check | Status | Detail |
|-------|--------|--------|
| Telegram bot token (live) | ✅ PASS | AppData `.env` (Oct 21) token **valid** (`getMe` HTTP 200, @Ogaitchhermesbot id 8277244378). Gateway runs from AppData root → uses the good token. |
| Stale token (other root) | ⚠️ WARN | `~/.hermes/.env` (Aug 22) holds a **dead/placeholder token** (`getMe` → 404, `827724...1UJE`). Live gateway unaffected. Persistent dual-root divergence debt. |
| Backup `.env` copies | ✅ PASS | **0** via `find` across all scan trees (`~/.hermes`, `state-snapshots`, `~/hermes-backup`, `~/.openclaw`). Sustained clean. |
| Credential caches | ✅ PASS | `bws_cache.json`, `.secret_cache` — absent in both roots. |
| `google_token.json` ACL | ✅ PASS | Both roots: `icacls` shows only SYSTEM + BUILTIN\Administrators + Owner (I)(F). No Everyone/Users. Standard Windows ACL. |
| `.env`-reader scripts | ⚠️ WARN | ~10 legacy helper scripts across `workspace/scripts/` reference `.env`/dotenv. They read only the **revoked** placeholder token (LOW risk); pattern should be retired. `care_checkin.py` (root) is 0 bytes (obsolete). |
| AGENTS.md BOM / invisible chars | ✅ PASS | `~/.hermes/AGENTS.md` and AppData `AGENTS.md` both absent. `~/.hermes/workspace/AGENTS.md` UTF-8, no BOM. Clean. |

## 2. Channel Integrity

| Channel | Status | Detail |
|---------|--------|--------|
| Gateway process | ✅ PASS | PID **15048** alive (tasklist + ps -W, 485,904 K, python 3.14.7), started 2026-10-25 04:21. AppData `gateway.log` fresh — last write today 06:34. |
| Gateway crash state | ✅ PASS | `gateway-exit-diag` shows clean start 10-25, one `previous_unclean_exit` (prior PID 21768) — no crash-loop entries since. |
| Telegram adapter | ✅ PASS | Polling active/recovering. Transient `ConnectError` today 06:34 on 149.154.167.220 → recovered in **11s** via IPv4 fallback 149.154.166.110. Valid token confirmed via direct `getMe`. |
| WhatsApp | ✅ PASS | Connected via **native gateway adapter**. Live DM traffic today (flush events 10-28 00:31). Session creds present at `whatsapp/session/creds.json` (updated today 06:57). |
| Topic 20 (Memory Review) | ✅ PASS | Confirmed in `channel_directory.json` (Agent Hermes / topic 20). This job delivers to `telegram:-1003784520976:20`. |
| Cron silent delivery | ⚠️ WARN | **25/56** jobs (45%) deliver to `origin` (16) or `local` (9) — output never reaches a user. 31 topic/channel-targeted. Unchanged. |
| `allow_all_users: true` | ⚠️ WARN | Grants every sender on every platform access. Persistent LOW. Recommend `false` + explicit allow-list. This warning re-emits every ~6 min in agent.log today. |

## 3. Recent Security Events

- **No `InvalidToken` / token rejections** in live gateway/agent logs this window ✅. Only historical Oct 13 event is the dead placeholder token in `~/.hermes/.env` — not a live-credential incident.
- **No blocked/unauthorized-user breach markers** ✅. Only WhatsApp "blocked number / no auto-reply" skip events (10-24, 93575056490) — normal owner-requested blocking, not a security event.
- **Telegram DNS/transport flakiness** (recurring, host-level): transient `ConnectError` today 06:34, recovered in 11s via automatic IPv4 fallback. Network churn, not an attack marker (LOW).
- **`jobs.json` Permission-denied IOError**: last occurrence 2026-10-27 03:16 (desktop.log). **Not observed today** — non-recurring/improved. Rotated logs (agent.log.1, errors.log.1) hold older occurrences.
- **Nous Portal**: invalid refresh token (non-blocking; custom OpenRouter provider active). LOW (persistent).

---

## Trend vs 2026-10-27

| Item | 10-27 | 10-28 | Direction |
|------|-------|-------|-----------|
| Telegram token (live) | PASS | PASS | No Change |
| Dual-root divergence | WARN | WARN | No Change (persistent debt) |
| Backup `.env` copies | PASS (0) | PASS (0) | No Change |
| Credential caches | PASS | PASS | No Change |
| `.env`-reader scripts | WARN | WARN | No Change |
| Google token ACL | PASS | PASS | No Change |
| WhatsApp | PASS | PASS | Stable |
| Cron silent delivery | 25/56 | 25/56 | No Change |
| AGENTS.md BOM | PASS | PASS | No Change |
| `jobs.json` IOError | WARN (03:16) | NOT OBSERVED | **Improved** |
| allow_all_users | WARN | WARN | No Change |

**Improvement:** `jobs.json` permission IOError absent today (last 10-27 03:16).
**Persistent security debt (3+ cycles):** dual-root token divergence (non-blocking), 25/56 silent cron targets, `.env`-reader helper scripts, `allow_all_users: true`, Telegram DNS flakiness (transient).
**No new active credential exposure. No token rejection. No breach markers.**

## 🔧 Remediation Priority
1. Delete the revoked `~/.hermes/.env` placeholder → single authoritative AppData root.
2. Retire remaining `.env`-reading helper scripts (they read only the dead token; `care_checkin.py` is empty/orphaned).
3. Set `allow_all_users: false` + explicit allow-list.
4. Re-review 25/56 silent cron targets (`origin`/`local`).
5. Continue monitoring Telegram DNS instability (self-healing in seconds).

## Retention Note
Rolling 7-day window. Keep newest per day. Current dir: 10-20, 10-22, 10-24, 10-25, 10-26, 10-27, 10-28 (+new). Drop oldest when window exceeds 7. Report artifact: `C:\Users\User\.hermes\workspace\Vault\System\Assistant\SECURITY_AUDIT_2026-10-28.md`.

---
*Generated 2026-10-28 by Hermes security-audit cron.*