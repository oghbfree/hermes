# Security Audit — 2026-10-22

**Host:** Windows 11 · **Hermes profile:** default · **Run type:** cron (scheduled)
**Scope:** credential exposure · channel integrity · recent security events
**Report path:** `C:\Users\User\.hermes\workspace\Vault\System\Assistant\SECURITY_AUDIT_2026-10-22.md`

---

## Summary of Findings

| # | Item | Status | Severity |
|---|------|--------|----------|
| 1 | Telegram adapter (polling) | **PASS — RECOVERED** (connected 10-22 10:14, PID 20060) | — |
| 2 | Telegram bot token (live AppData) | PASS (getMe ok, ogaitchhermesbot) | — |
| 3 | Telegram token divergence (~/.hermes.idle) | WARN (persistent debt ≥15 cycles) | LOW |
| 4 | Backup `.env` copies | **PASS** (0, sustained) | — |
| 5 | Credential cache files | PASS (none in either root) | — |
| 6 | `.env`-reading helper scripts | **WARN** (25, persistent; read revoked placeholder) | LOW |
| 7 | `google_token.json` ACL | PASS (SYSTEM/Admins/User only) | — |
| 8 | Gateway process | RUNNING (PID 20060), **platforms recovered** | — |
| 9 | WhatsApp session | **PASS (paired + connected)** | — |
| 10 | Cron delivery targets | WARN (26/55 silent) | WARN |
| 11 | AGENTS.md BOM / injection | PASS (main absent; workspace UTF-8, no BOM) | — |
| 12 | Telegram DNS/IP flakiness | WARN (recurring bursts today; recovers via fallback IP) | LOW |
| 13 | No InvalidToken / credential rejection | PASS (0 in live window) | — |
| 14 | Topic 20 host | PASS (supergroup + forum confirmed via getChat; send perms OK) | — |

---

## 1. Credential Exposure

### 1.1 Telegram bot token — live root VALID; idle root revoked (divergence, persistent ≥15 cycles)
- **Live AppData root** `C:\Users\User\AppData\Local\hermes\.env` → `getMe` = `{"ok":true}` (bot `Hermes`/ogaitchhermesbot, id 8277244378). This is the token the running gateway loads. **No live exposure.**
- **Idle root** `~/.hermes/.env` still holds a **revoked** placeholder → `getMe` = HTTP 404 `Not Found`. Not actionable for live traffic but a footgun. **Recommend (repeated): delete the revoked placeholder; consolidate on the single AppData root.**

### 1.2 Backup `.env` copies — **PASS (0, sustained)**
Zero `.env` across `~/.hermes/backups`, `state-snapshots`, `~/hermes-backup`, `~/.openclaw` (maxdepth-limited). All locations clean.

### 1.3 Credential cache files — **PASS**
No `bws_cache.json` / `.secret_cache` in either root (`~/.hermes` or AppData).

### 1.4 `.env`-reading helper scripts — **WARN (persistent, LOW)**
25 dated helpers across `~/.hermes/workspace/{scripts,Vault/...}` and `scripts/red-teaming/godmode/` still read `.env` directly (via `open()`, `dotenv`, `Path.home()/'.hermes'/'.env'`). These target the **revoked `~/.hermes/.env` placeholder**, so no live secret is exposed, but they would leak a real key if the placeholder were ever swapped for a valid token. Recommend migrating to the live AppData token / gateway-native send, or deleting.

### 1.5 `google_token.json` ACL — **PASS**
`icacls` (live AppData copy): `NT AUTHORITY\SYSTEM:(I)(F)`, `BUILTIN\Administrators:(I)(F)`, `DESKTOP-25Q3AQC\User:(I)(F)`. No `Everyone`/`BUILTIN\Users`. Standard Windows owner defaults.

### 1.6 Config — **PASS (no new plaintext secrets)**
Provider keys via env-var refs; no raw secrets hardcoded in live config. (`allow_all_users: true` persists — LOW config hardening debt.)

---

## 2. Channel Integrity

### 2.1 Gateway — RUNNING (PID 20060) — **Telegram adapter RECOVERED (PASS)**
- `gateway_state.json` (updated 10-22 10:15) shows process running, **PID 20060**, code v0.22.2.
- **`platforms.telegram.state: "connected"`** (updated 10-22 10:14). The 10-19/10-20 `telegram_polling_conflict` fatal is **resolved**. Log confirms healthy polling generations (up to gen 13) through today — `getUpdates progressing`.
- gateway-exit-diag shows several 10-21 restart entries (PIDs 5572/31680/27152/20060) all exiting code 75/planned `--replace` churn, but **0 `asyncio.run.exception` / concurrent_log_handler crash signatures**. This is not the old crash loop.
- Gateway exit-diagnostic log (AppData) fresh to 10-21 11:56; live `gateway-stdio.log`/`gateway.log` active to 10-22 10:15.

### 2.2 Telegram token validity — **PASS (independent of adapter state)**
Direct `getMe` against the live AppData token returns `ok:true`. **Token valid; recovery confirms the 10-20 outage was a stale/duplicate polling session, not a revoked key.**

### 2.3 WhatsApp — **PASS (paired + connected)**
`creds.json` present (3243 B, updated 10-21 19:26) at AppData root. `gateway_state` whatsapp = `connected` (updated 10-21 11:56).

### 2.4 Cron delivery targets — **WARN (26/55 silent)**
`jobs.json` (AppData root): 55 jobs. Distribution: `origin`×16, `local`×10 (silent = **26/55, 47%**), topic-`telegram:-1003784520976:` → `:14`×7, `:20`×5, `:4`×4, `:1`×3, `:16`×2, `:10`×2, plus `:26`×1, `:28`×1, `:2`×1, `:5`×1, and `telegram:123286468`×2. With the telegram adapter now connected, topic-targeted cron delivery should flow again (subject to per-job success).

### 2.5 Multiplex parked profiles — WARN (persistent)
Profiles coach/content-buddy/harold/sat-nav share the same Telegram token; one token → one gateway. `multiplex_standalone_reason` in gateway_state flags all four as parked. No duplicate-polling conflict observed this cycle (recovery is stable), but the shared token remains the risk vector that caused the 10-19 conflict.

---

## 3. Recent Security Events

### 3.1 Telegram adapter recovery (polling conflict resolved) — RESOLVED
The 10-19 13:45 `telegram_polling_conflict` fatal (adapter `fatal` on 10-20) has cleared. Polling confirmed healthy across multiple generations on 10-21 and 10-22 (latest 10-22 10:14). No `InvalidToken` / `Unauthorized` / `403` in the live window — the key was never rejected by Telegram. Treated as integrity/deployment fault (stale or duplicate session), now remediated by gateway restarts.

### 3.2 Telegram DNS/IP flakiness — WARN (transient, recurring, recovered)
Multiple `ConnectError('All connection attempts failed')` / IP-fail bursts today: 10-22 07:55 (attempts 1–4) and 10-22 10:13 (attempt 5). Each recovered seconds-to-a-minute later via the sticky IPv4 fallback `149.154.166.110`. Irrecoverable-only-at-10-13 prior cycles. Host-level network/DNS flakiness, not redirection/attack marker (no multiple mismatched hosts, no certificate anomalies).

### 3.3 Token rejection / compromise markers — PASS
No `InvalidToken` / `Unauthorized` / `403` / `404`-on-token in the **live** 10-21/10-22 window (the earlier `gateway.log:558` count was from the stale `~/.hermes` death log for the revoked placeholder, not live traffic). No multi-provider simultaneous failure. No breach markers.

### 3.4 Auxiliary — WARN (persistent, low)
`allow_all_users: true` in config (recommend `false` + allow-list). Nous Portal not logged in (invalid refresh token, non-blocking custom provider). Multiplex token-share / parked specialist adapters (see 2.5).

---

## Trend vs 2026-10-20

| Item | 10-20 | 10-22 | Direction |
|------|-------|-------|-----------|
| Telegram adapter | **FAIL (polling conflict)** | **PASS (connected)** | **IMPROVED — channel back up** |
| Telegram token (live) | PASS | PASS | No Change |
| Dual-root divergence | WARN | WARN | No Change (persistent debt) |
| Backup `.env` copies | PASS (0) | PASS (0) | No Change |
| Credential caches | PASS | PASS | No Change |
| `.env`-reader scripts | WARN (25) | WARN (25) | No Change |
| Google token ACL | PASS | PASS | No Change |
| WhatsApp | PASS (paired+connected) | PASS (paired+connected) | No Change |
| Cron silent delivery | 26/55 | 26/55 | No Change |
| Model-not-found (deepseek/ollama) | WARN (NEW) | Not observed in window | Improved/not repeated |
| AGENTS.md | PASS (no BOM) | PASS (no BOM) | No Change |

**Improvement this cycle (key finding):** Telegram adapter **recovered** from the 10-19/10-20 `telegram_polling_conflict` fatal. Gateway PID 20060 now shows `platforms.telegram.state: connected` with healthy polling (gen 13, 10-22 10:14). Gateway-based Telegram cron delivery should be functional again.
**Persistent security debt (3+ cycles, unchanged):** dual-root token divergence, silent cron targets (26/55), `.env`-reader helper scripts (25), `allow_all_users: true`, multiplex token-share/parked adapters, Nous Portal invalid.
**No active credential exposure / no breach markers / no token rejection in the live window.**

---

*Generated 2026-10-22 by Hermes security-audit cron. Token validated via direct `getMe`. Telegram channel integrity confirmed via live gateway_state + polling logs; topic 20 delivery target verified via `getChat` (supergroup + forum).*