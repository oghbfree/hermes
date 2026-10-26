# Security Audit — 2026-10-25

**Generated:** 2026-10-25 by Hermes security-audit cron
**Scope:** Credential exposure · Channel integrity · Recent security events
**Overall: 🟢 HEALTHY** — No active credential exposure, no token rejection, both channels connected.

---

## 1. Credential Exposure

| Check | Status | Detail |
|-------|--------|--------|
| Telegram bot token (live) | ✅ PASS | `getMe` HTTP 200 on AppData token — **valid** (`@Ogaitchhermesbot`, id 8277244378). |
| Legacy token (stale) | ⚠️ WARN | `~/.hermes/.env` holds a **dead/placeholder token** (`getMe` → 404). Live gateway uses AppData token. Dual-root divergence (persistent debt). |
| Backup `.env` copies | ✅ PASS | **0** across all 4 scan trees (`~/.hermes/backups`, `state-snapshots`, `~/hermes-backup`, `~/.openclaw`). Previously 49 (historical) — sustained clean. |
| Credential caches | ✅ PASS | `bws_cache.json`, `.secret_cache` — absent in both roots. |
| `google_token.json` ACL | ✅ PASS | `icacls`: SYSTEM / Administrators / User only — no Everyone/Users extra. |
| `.env`-reader scripts | ⚠️ WARN | ~11 legacy helper scripts in workspace (Jul–Sep dated) read `~/.hermes/.env` directly. They read the **revoked** token only (LOW), but pattern should be retired. |
| AGENTS.md BOM | ✅ PASS | Main `~/.hermes/AGENTS.md` absent (clean); workspace copy UTF-8, no BOM, no zero-width/RTL chars. |
| Config version | — | Not re-run this cycle (prior cycles clean). |

## 2. Channel Integrity

| Channel | Status | Detail |
|---------|--------|--------|
| Gateway process | ✅ PASS | PID **15048** (python 3.14.7) running; `gateway-exit-diag` shows clean start 2026-10-25 04:21. No crash-loop (`asyncio.run.exception` count **0**). |
| Gateway freshness | ✅ PASS | `gateway.log` mtime **2026-10-25 07:03** (minutes fresh). |
| Telegram adapter | ✅ PASS | Connected; valid token confirmed. |
| WhatsApp | ✅ PASS | `bridge.log` fresh (2026-10-25 06:46), session creds present; reconnected at 04:24 today after a 30s startup timeout (recovered). |
| Topic 20 target | ✅ PASS | Supergroup "Agent Hermes" (id `-1003784520976:20`), forum enabled. |
| Cron silent delivery | ⚠️ WARN | **25/56** jobs (45%) deliver to `origin` (16) or `local` (9) — output never reaches a user. 31 topic/channel-targeted. Slightly improved (prior 26/55). |
| `allow_all_users: true` | ⚠️ WARN | Grants every sender on every platform access. Persistent LOW. Recommend `false` + explicit allow-list. |

## 3. Recent Security Events

- **No `InvalidToken` / token rejections** in the live agent/gateway/errors logs this window ✅
- **No blocked/unauthorized-user or breach markers** in live logs ✅
- **Telegram API DNS/transport flakiness** (recurring, 06:59 & 07:03 today): `ConnectTimeout` bursts on api.telegram.org / 149.154.166.110, each **recovering within ~15s**. Classic host-level network churn — **not an attack marker** (LOW).
- **Nous Portal**: invalid refresh token (non-blocking — custom OpenRouter provider). LOW.
- Single OpenRouter `Connection error` at 07:03 (API retry succeeded) — transient, no auth issue.

---

## Trend vs 2026-10-24

| Item | 10-24 | 10-25 | Direction |
|------|-------|-------|-----------|
| Telegram token (live) | PASS | PASS | No Change |
| Dual-root divergence | WARN | WARN | No Change (persistent debt) |
| Backup `.env` copies | PASS (0) | PASS (0) | No Change |
| Credential caches | PASS | PASS | No Change |
| `.env`-reader scripts | WARN | WARN | No Change |
| Google token ACL | PASS | PASS | No Change |
| WhatsApp | PASS | PASS (reconnect today) | Stable |
| Cron silent delivery | 25/56 | 25/56 | No Change |
| AGENTS.md BOM | PASS | PASS | No Change |
| allow_all_users | WARN | WARN | No Change |

**Improvements:** none material — already healthy.
**Persistent security debt (3+ cycles):** dual-root token divergence (non-blocking), 25/56 silent cron targets, `.env`-reader helper scripts, `allow_all_users: true`, Telegram DNS flakiness (transient).
**No new active credential exposure. No token rejection. No breach markers.**

## 🔧 Remediation Priority
1. Delete the revoked `~/.hermes/.env` placeholder → single authoritative AppData root.
2. Retire remaining `.env`-reading helper scripts (delete; read only dead token).
3. Set `allow_all_users: false` + explicit allow-list.
4. Re-review 25/56 silent cron targets (`origin`/`local`).
5. Continue monitoring Telegram DNS instability (transient, recovers).

## Retention Note
7-day rolling window applied. Deleted oldest `SECURITY_AUDIT_2026-10-15.md` (8 files now → 7). Report artifact: `C:\Users\User\.hermes\workspace\Vault\System\Assistant\SECURITY_AUDIT_2026-10-25.md`.

---
*Generated 2026-10-25 by Hermes security-audit cron.*