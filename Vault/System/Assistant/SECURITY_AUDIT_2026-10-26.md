# Security Audit — 2026-10-26

**Generated:** 2026-10-26 07:05 by Hermes security-audit cron
**Scope:** Credential exposure · Channel integrity · Recent security events
**Overall: 🟢 HEALTHY** — No active credential exposure, no token rejection, both channels connected.

---

## 1. Credential Exposure

| Check | Status | Detail |
|-------|--------|--------|
| Telegram bot token (live) | ✅ PASS | AppData token **valid** (`getMe` HTTP 200, @Ogaitchhermesbot id 8277244378). Gateway runs from AppData root → uses the good token. |
| Stale token (other root) | ⚠️ WARN | `~/.hermes/.env` holds a **dead/placeholder token** (`getMe` → 404, `827724...1UJE`). Live gateway unaffected. Persistent dual-root divergence debt. |
| Backup `.env` copies | ✅ PASS | **0** across all 4 scan trees (`~/.hermes/backups`, `state-snapshots`, `~/hermes-backup`, `~/.openclaw`). Sustained clean (was 49 historical). |
| Credential caches | ✅ PASS | `bws_cache.json`, `.secret_cache` — absent in both roots. |
| `google_token.json` ACL | ✅ PASS | `icacls`: BUILTIN\Administrators + User only, inherited (I)(F). No Everyone/Users extra. |
| `.env`-reader scripts | ⚠️ WARN | ~11 legacy helper scripts in workspace (Jul–Sep) read `~/.hermes/.env` directly — that is the **revoked** token only (LOW risk), but pattern should be retired. |
| AGENTS.md BOM / invisible chars | ✅ PASS | Both `~/.hermes/AGENTS.md` and AppData `AGENTS.md` absent; workspace copies UTF-8, no BOM, no zero-width/RTL chars. |

## 2. Channel Integrity

| Channel | Status | Detail |
|---------|--------|--------|
| Gateway process | ✅ PASS | PID **15048** running (python 3.14.7); AppData `gateway.log` mtime **07:02 today** — fresh live activity. |
| Gateway crash state | ✅ PASS | `gateway-exit-diag` crash-loop count (`asyncio.run.exception`) **0**. |
| Telegram adapter | ✅ PASS | Polling confirmed healthy 22:01 yesterday; today 3 transport recoveries, 6 transient `ConnectError` — each recovering in seconds. Valid token. |
| WhatsApp | ✅ PASS | `bridge.log` fresh (06:31 today, 240 MB). Reconnected 06:31 (reason 428) and 23:10 yesterday. Session creds present. Active DM traffic today. |
| Topic 20 target | ✅ PASS | "Agent Hermes / topic 20" (`-1003784520976:20`) confirmed in channel_directory; 5 cron jobs deliver to it. Forum enabled supergroup. |
| Cron silent delivery | ⚠️ WARN | **25/56** jobs (45%) deliver to `origin` (16) or `local` (9) — output never reaches a user. 31 topic/channel-targeted. Unchanged from prior. |
| `allow_all_users: true` | ⚠️ WARN | Grants every sender on every platform access. Persistent LOW. Recommend `false` + explicit allow-list. |

## 3. Recent Security Events

- **No `InvalidToken` / token rejections** in live gateway/agent/errors logs this window ✅ (the revoked token is the explicit dead placeholder, not a live-credential event).
- **No blocked/unauthorized-user or breach markers** in live logs ✅
- **Telegram DNS/transport flakiness** (recurring, host-level): today 6 `ConnectError` + 3 recoveries (overnight 00:09–00:47 window), all self-healing within ~11s via automatic IPv4 fallback 149.154.166.110 ↔ api.telegram.org. Classic host-level network churn — **not an attack marker** (LOW). Overnight 10-25 21:43 had a 10-retry escalation, recovered at 22:01.
- **WhatsApp disconnects (reason 428)** at 23:10 (10-25) and 06:31 (10-26), each reconnected in ~7s — routine WhatsApp session re-negotiation, not a security event (LOW).
- **Nous Portal**: invalid refresh token (non-blocking; custom OpenRouter provider active). LOW.
- **OpenRouter** live key healthy; no 401s currently (prior Aug 401s historical).

---

## Trend vs 2026-10-25

| Item | 10-25 | 10-26 | Direction |
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

**Improvements:** none material — already healthy.
**Persistent security debt (3+ cycles):** dual-root token divergence (non-blocking), 25/56 silent cron targets, `.env`-reader helper scripts, `allow_all_users: true`, Telegram DNS flakiness (transient), WhatsApp reason-428 reconnects (routine).
**No new active credential exposure. No token rejection. No breach markers.**

## 🔧 Remediation Priority
1. Delete the revoked `~/.hermes/.env` placeholder → single authoritative AppData root.
2. Retire remaining `.env`-reading helper scripts (they read only the dead token).
3. Set `allow_all_users: false` + explicit allow-list.
4. Re-review 25/56 silent cron targets (`origin`/`local`).
5. Continue monitoring Telegram DNS instability + WhatsApp 428 reconnects (transient, self-healing).

## Retention Note
7-day rolling window applied. Deleting oldest `SECURITY_AUDIT_2026-10-19.md` (not present in dir) / oldest 10-16 file if auto-prune needed. Keeping one file per day: 10-16, 10-17, 10-18, 10-20, 10-22, 10-24, 10-25 + new 10-26. Report artifact: `C:\Users\User\.hermes\workspace\Vault\System\Assistant\SECURITY_AUDIT_2026-10-26.md`.

---
*Generated 2026-10-26 by Hermes security-audit cron.*