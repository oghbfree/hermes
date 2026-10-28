# Security Audit — 2026-10-27

**Generated:** 2026-10-27 ~07:05 by Hermes security-audit cron
**Scope:** Credential exposure · Channel integrity · Recent security events
**Overall: 🟢 HEALTHY** — No active credential exposure, no token rejection, both channels connected.

---

## 1. Credential Exposure

| Check | Status | Detail |
|-------|--------|--------|
| Telegram bot token (live) | ✅ PASS | AppData `.env` (Oct 21) token **valid** (`getMe` HTTP 200, @Ogaitchhermesbot id 8277244378). Gateway runs from AppData root → uses the good token. |
| Stale token (other root) | ⚠️ WARN | `~/.hermes/.env` (Aug 22) holds a **dead/placeholder token** (`getMe` → 404, `827724...1UJE`). Live gateway unaffected. Persistent dual-root divergence debt. |
| Backup `.env` copies | ✅ PASS | **0** via `find` across all scan trees (`~/.hermes`, `state-snapshots`, `~/hermes-backup`, `~/.openclaw`) + 1 in live AppData root. Sustained clean. |
| Credential caches | ✅ PASS | `bws_cache.json`, `.secret_cache` — absent in both roots. |
| `google_token.json` ACL | ✅ PASS | `icacls`: BUILTIN\Administrators + User only (I)(F), no Everyone/Users. Same for `.env`. |
| `.env`-reader scripts | ⚠️ WARN | ~10 legacy helper scripts across workspace read `~/.hermes/.env` directly — which holds only the **revoked** placeholder token (LOW risk), but pattern should be retired. `care_checkin.py` (root) is empty (0 bytes, obsolete). |
| AGENTS.md BOM / invisible chars | ✅ PASS | AppData `AGENTS.md` present, UTF-8 no BOM, no zero-width/RTL chars. `~/.hermes/AGENTS.md` absent (clean). |

## 2. Channel Integrity

| Channel | Status | Detail |
|---------|--------|--------|
| Gateway process | ✅ PASS | PID **15048** running (python 3.14.7), clean start 2026-10-25 04:21 (gateway-exit-diag, state_db_integrity ok). Confirmed alive in process table + ESTABLISHED conns. |
| Gateway crash state | ✅ PASS | `gateway-exit-diag` shows clean start 10-25, no crash-loop entries since. |
| Telegram adapter | ✅ PASS | Polling active/recovering. Transient `ConnectError` overnight (04:02, 04:53) each self-healing via IPv4 fallback 149.154.166.110. Valid token confirmed. |
| WhatsApp | ✅ PASS | Connected via **native gateway adapter** — active DM traffic this morning (`bridge.log` is stale from old external bridge, superseded; gateway.log shows live WhatsApp flush + customer-gate activity). Session creds present at `credentials/whatsapp/`. |
| Topic 20 (Memory Review) | ✅ PASS | Target `-1003784520976:20` confirmed; **5** cron jobs deliver to it. |
| Cron silent delivery | ⚠️ WARN | **25/56** jobs (45%) deliver to `origin` (16) or `local` (9) — output never reaches a user. 31 topic/channel-targeted. Unchanged. |
| `allow_all_users: true` | ⚠️ WARN | Grants every sender on every platform access. Persistent LOW. Recommend `false` + explicit allow-list. |

## 3. Recent Security Events

- **No `InvalidToken` / token rejections** in live gateway/agent/errors logs this window ✅. Only historical event is Oct 13 old-gateway token rejection (token 827724...1UJE) — that same token is now the explicit dead placeholder in the other root, not a live-credential incident.
- **No blocked/unauthorized-user or breach markers** in live logs ✅.
- **Telegram DNS/transport flakiness** (recurring, host-level): transient `ConnectError` overnight 04:02 & 04:53, each recovered in seconds via automatic IPv4 fallback. Classic network churn, **not an attack marker** (LOW).
- **Transient `jobs.json` Permission-denied IOError** at 03:16:50 (Errno 13). WARN — read/write race or locking on the cron schedule file; non-recurring in window. Worth one monitoring glance.
- **Nous Portal**: invalid refresh token (non-blocking; custom OpenRouter provider active). LOW (persistent).

---

## Trend vs 2026-10-26

| Item | 10-26 | 10-27 | Direction |
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
| allow_all_users | WARN | WARN | No Change |

**Improvements:** none material — system already healthy.
**Persistent security debt (3+ cycles):** dual-root token divergence (non-blocking), 25/56 silent cron targets, `.env`-reader helper scripts, `allow_all_users: true`, Telegram DNS flakiness (transient).
**New this cycle:** transient `jobs.json` permission IOError (03:16) — monitor only.
**No new active credential exposure. No token rejection. No breach markers.**

## 🔧 Remediation Priority
1. Delete the revoked `~/.hermes/.env` placeholder → single authoritative AppData root.
2. Retire remaining `.env`-reading helper scripts (they read only the dead token; `care_checkin.py` is empty/orphaned).
3. Set `allow_all_users: false` + explicit allow-list.
4. Re-review 25/56 silent cron targets (`origin`/`local`).
5. Monitor the transient `jobs.json` IOError; continue watching Telegram DNS instability (self-healing).

## Retention Note
7-day rolling window. Delete oldest files beyond 7 days (10-16, 10-17, 10-18). Keeping one file per day: 10-20, 10-22, 10-24, 10-25, 10-26 + new 10-27. Report artifact: `C:\Users\User\.hermes\workspace\Vault\System\Assistant\SECURITY_AUDIT_2026-10-27.md`.

---
*Generated 2026-10-27 by Hermes security-audit cron.*