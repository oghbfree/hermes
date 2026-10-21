# Security Audit — 2026-10-20

**Host:** Windows 11 · **Hermes profile:** default · **Run type:** cron (scheduled)
**Scope:** credential exposure · channel integrity · recent security events
**Report path:** `C:\Users\User\.hermes\workspace\Vault\System\Assistant\SECURITY_AUDIT_2026-10-20.md`

---

## Summary of Findings

| # | Item | Status | Severity |
|---|------|--------|----------|
| 1 | Telegram adapter (polling) | **FAIL — telegram_polling_conflict since 10-19 13:45** | **CRITICAL** |
| 2 | Telegram bot token (live AppData) | PASS (getMe ok, ogaitchhermesbot) | — |
| 3 | Telegram token divergence (~/.hermes.idle) | WARN (persistent debt ≥13 cycles) | LOW |
| 4 | Backup `.env` copies | **PASS** (0, sustained) | — |
| 5 | Credential cache files | PASS (none) | — |
| 6 | `.env`-reading helper scripts | **WARN** (persistent; read REVOKED placeholder) | LOW |
| 7 | `google_token.json` ACL | PASS (SYSTEM/Admins/User only) | — |
| 8 | Gateway process | RUNNING (PID 10656) but platform degraded | — |
| 9 | WhatsApp session | **PASS (paired + connected)** | — |
| 10 | Cron delivery targets | WARN (26/55 silent) | WARN |
| 11 | Model-not-found (deepseek/ollama) | WARN (cron config drift, 3 retries lost) | LOW |
| 12 | Telegram DNS/IP flakiness overnight | WARN (transient; recovered) | LOW |
| 13 | No InvalidToken / credential rejection | PASS (0 in live window) | — |
| 14 | AGENTS.md BOM / injection | PASS (main absent; workspace UTF-8, no BOM) | — |
| 15 | Topic 20 host | PASS (supergroup + forum confirmed via getChat) | — |

---

## 1. Credential Exposure

### 1.1 Telegram bot token — live root PASS; idle root WARN (divergence, persistent ≥13 cycles)
- **Live AppData root** `C:\Users\User\AppData\Local\hermes\.env` → `getMe` = `{"ok":true}` (bot `Hermes`/ogaitchhermesbot, id 8277244378). This is the token the live gateway loads. **No live exposure.**
- **Idle root** `~/.hermes/.env` still holds a **revoked** placeholder → `getMe` = HTTP 404 `Not Found`. Not actionable for live traffic but a footgun. **Recommend (repeated): delete the revoked placeholder; consolidate on the single AppData root.**

### 1.2 Backup `.env` copies — **PASS (0, sustained)**
Zero `.env` across `~/.hermes/backups`, `state-snapshots`, `~/hermes-backup`, `~/.openclaw` (maxdepth-limited). All locations clean. Sustained improvement.

### 1.3 Credential cache files — **PASS**
No `bws_cache.json` / `.secret_cache` in either root.

### 1.4 `.env`-reading helper scripts — **WARN (persistent, LOW)**
~25 dated helpers across `~/.hermes/workspace/{scripts,Vault/...}` still read `.env` directly via `Path.home()/'.hermes'/'.env'` — e.g. `scripts/memory_review_telegram.py`, `send_ghana_report.py`, `ghan_telegram_report.py`, `mum_evening_checkin.py`, `h_evening_checkin_send.py`, `tmp_afternoon_health_check.py`, several dated `evening_checkin_*.py`. **These target the revoked `~/.hermes/.env` placeholder**, so no live secret is exposed, but they would leak a real key if the placeholder were ever swapped for a valid token, and they silently 404 on delivery. Recommend migrating to the live AppData token / gateway-native send, or deleting.

### 1.5 `google_token.json` ACL — **PASS**
`icacls` (live AppData copy): `SYSTEM:(I)(F)`, `BUILTIN\Administrators:(I)(F)`, `DESKTOP-25Q3AQC\User:(I)(F)`. No `Everyone`/`BUILTIN\Users`. Standard Windows owner defaults.

### 1.6 Config — **PASS (no new plaintext secrets)**
Provider keys via env-var refs; no raw secrets hardcoded in live config. (`allow_all_users: true` persists — LOW config hardening debt, see 3.5.)

---

## 2. Channel Integrity

### 2.1 Gateway — RUNNING (PID 10656) but **Telegram adapter FAIL (CRITICAL)**
- `gateway_state.json` (updated 10-20 07:01): process running, PID **10656** (clean PID change from 10-18's 16424).
- **`platforms.telegram.state: "fatal"`** — `telegram_polling_conflict`: *"Telegram polling could not recover after 5 retries (200s total wait). The previous gateway session is still held open on Telegram's servers, OR ANOTHER PROCESS IS USING THE SAME BOT TOKEN… Conflict: terminated by other getUpdates request; make sure that only one bot instance is running."*
- First hit 10-19 13:45, preceded by a **polling stall watchdog** at 10-19 12:28 (getUpdates no progress for 13,968s → adapter rebuild attempt → conflict).
- Root cause candidates: (a) a zombie/stale gateway instance still holding the `getUpdates` long-poll; (b) one of the multiplex profiles sharing the same token (coach/content-buddy/harold/sat-nav) polling concurrently. **Recovery: verify no second instance, then `hermes gateway restart`.**
- Crash signatures (`asyncio.run.exception`/`ModuleNotFoundError`): **0** — this is not the old concurrent_log_handler crash loop.

### 2.2 Telegram token validity — PASS (independent of adapter state)
Direct `getMe` against the live AppData token returns `ok:true`. **Token is valid; the outage is a polling conflict, not a revoked key.** Any read/write OSS path utilising a fresh `sendMessage` works; gateway-based cron delivery is the affected path.

### 2.3 WhatsApp — **PASS (paired + connected)**
`creds.json` present (3243 B, updated 10-20 06:54). `gateway_state` whatsapp = `connected`; gateway.log shows active WhatsApp flushing through 10-20 06:43. Chrome remote-debug session on web.whatsapp.com profile present.

### 2.4 Cron delivery targets — **WARN (26/55 silent)**
`jobs.json` (AppData root, updated 10-20 07:00): 55 jobs. Distribution: `origin`×16, `local`×10 (silent = **26/55, 47%**), topic `telegram:-1003784520976`:14×7,`:20`×5,`:4`×4,`:1`×3,`:16`×2,`:10`×2, plus `:5`×1,`:28`×1,`:26`×1,`:2`×1, and `telegram:123286468`×2. **Telegram-targeted cron delivery is at risk this cycle while the telegram adapter is in `fatal` polling-conflict state.**

### 2.5 Multiplex parked profiles — WARN (persistent)
Profiles coach/content-buddy/harold/sat-nav share the same Telegram token; one token → one gateway, so specialist adapters are parked. Now a **live risk vector** given the 2.1 polling conflict (any second instance polling with that token causes/extends the outage).

---

## 3. Recent Security Events

### 3.1 Telegram adapter fatal (polling conflict) — CRITICAL/FAIL
Dated 10-19 12:28–13:45, persistent into 10-20 state. No `InvalidToken` / `Unauthorized` / `403` in the live window — the key was never rejected by Telegram. Treated as integrity/deployment fault (stale or duplicate session), **not** credential compromise.

### 3.2 Model-not-found: `deepseek/deepseek-v4-flash-0731` — WARN (config drift, not credential)
At 10-20 05:16, cron `0c0f87b59450` hit HTTP 404 ×3: `model 'deepseek/deepseek-v4-flash-0731' not found` against `base_url=http://127.0.0.1:11434/v1` (ollama). A cron task is pinned to a localhost model the runtime can't resolve → output lost after 3 retries. Route to available provider/model. Informational; no security exposure.

### 3.3 Telegram DNS/IP flakiness — WARN (transient, recovered)
Multiple `ConnectError('All connection attempts failed')` / `getaddrinfo failed` bursts on Telegram IPs (10-19 23:45, 10-20 03:44). Recovered 03:44:50 via fallback IP. Host-level network flakiness, not redirection/attack marker.

### 3.4 Token rejection / compromise markers — PASS
No `InvalidToken`/`Unauthorized`/`403` in the live 10-19/10-20 window. No multi-provider simultaneous failure. No breach markers.

### 3.5 Auxiliary — WARN (persistent, low)
`allow_all_users: true` in config (recommend `false` + allow-list). Nous Portal not logged in (invalid refresh token, non-blocking custom provider). `send_message_tool` matched Thread 5 not found once (transient forum-target retry).

---

## Trend vs 2026-10-18

| Item | 10-18 | 10-20 | Direction |
|------|-------|-------|-----------|
| Telegram adapter | PASS (PID 16424) | **FAIL (polling conflict)** | **REGRESSED — channel down** |
| Telegram token (live) | PASS | PASS | No Change |
| Dual-root divergence | WARN | WARN | No Change (persistent debt) |
| Backup `.env` copies | PASS (0) | PASS (0) | No Change |
| Credential caches | PASS | PASS | No Change |
| `.env`-reader scripts | WARN (legacy) | WARN (persistent) | No Change |
| Google token ACL | PASS | PASS | No Change |
| WhatsApp | PASS (paired+live) | PASS (paired+connected) | No Change |
| Cron silent delivery | 29/59 | 26/55 | Slight improvement |
| Model-not-found (deepseek/ollama) | — | **WARN (NEW)** | New this cycle |

**Regression this cycle (CRITICAL):** Telegram adapter entered `telegram_polling_conflict` on 10-19 13:45 and is still `fatal` at this audit — Telegram gateway-cron delivery is down pending `hermes gateway restart` after verifying no duplicate session.
**New this cycle:** deepseek model-not-found on a cron task (Lost after 3 retries).
**Persistent security debt (3+ cycles, unchanged):** dual-root token divergence, silent cron targets, `.env`-reader helper scripts, `allow_all_users: true`, multiplex token-share/parked adapters, Nous Portal invalid.
**No active credential exposure / no breach markers / no token rejection.**

---

*Generated 2026-10-20 by Hermes security-audit cron. Token validated via direct `getMe`; report delivered to Telegram topic 20 (Memory Review) via direct Bot-API because the gateway's telegram adapter is in polling-conflict state.*