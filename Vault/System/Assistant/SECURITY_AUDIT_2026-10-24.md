# Security Audit — 2026-10-24

**Host:** Windows 11 · **Hermes profile:** default · **Run type:** cron (scheduled)
**Scope:** credential exposure · channel integrity · recent security events
**Report path:** `C:\Users\User\.hermes\workspace\Vault\System\Assistant\SECURITY_AUDIT_2026-10-24.md`

---

## Summary of Findings

| # | Item | Status | Severity |
|---|------|--------|----------|
| 1 | Telegram bot token (live AppData) | **PASS** (getMe ok; Ogaitchhermesbot, topics enabled) | — |
| 2 | Dual-root token divergence (~/.hermes.idle) | **WARN** (persistent debt ≥15 cycles) | LOW |
| 3 | Backup `.env` copies | **PASS** (0, sustained) | — |
| 4 | Credential cache files | PASS (none in either root) | — |
| 5 | `google_token.json` ACL | PASS (SYSTEM/Admins/User only) | — |
| 6 | `.env`-reading helper scripts | **WARN** (54 refs in workspace; persistent) | LOW |
| 7 | Gateway process | RUNNING (PID 17516), telegram + whatsapp connected | — |
| 8 | WhatsApp session | **PASS** (paired; creds fresh today) | — |
| 9 | Cron delivery targets | **WARN** (25/56 silent, 44.6%) | WARN |
| 10 | AGENTS.md BOM / injection | PASS (main absent; workspace UTF-8, no BOM) | — |
| 11 | Telegram DNS/IP flakiness | WARN (recurring bursts; recovers via fallback IP) | LOW |
| 12 | No InvalidToken / credential rejection | **PASS** (0 in live window) | — |
| 13 | Topic 20 host | PASS (supergroup + forum confirmed via getChat) | — |

---

## 1. Credential Exposure

### 1.1 Telegram bot token — live root VALID; idle root revoked (divergence persistent ≥15 cycles)
- **Live AppData root** `C:\Users\User\AppData\Local\hermes\.env` → `getMe` = `{"ok":true}` (bot `Hermes`/Ogaitchhermesbot, id 8277244378, `has_topics_enabled:true`). This is the token the running gateway (PID 17516) loads. **No live exposure.**
- **Idle root** `~/.hermes/.env` still holds a **revoked placeholder** (13-char) → not tested against Telegram. Not actionable for live traffic but a footgun. **Recommend (repeated): delete the revoked placeholder; consolidate on the single AppData root.**

### 1.2 Backup `.env` copies — **PASS (0, sustained)**
Zero `.env` across `~/.hermes/backups`, `state-snapshots`, `~/hermes-backup`, `~/.openclaw` (maxdepth-limited). All locations clean.

### 1.3 Credential cache files — **PASS**
No `bws_cache.json` / `.secret_cache` in `~/.hermes/cache/` or AppData cache.

### 1.4 `google_token.json` ACL — **PASS**
`icacls` (live AppData copy): `NT AUTHORITY\SYSTEM:(I)(F)`, `BUILTIN\Administrators:(I)(F)`, `DESKTOP-25Q3AQC\User:(I)(F)`. No `Everyone`/`BUILTIN\Users`. Standard Windows owner defaults.

### 1.5 `.env`-referencing helper scripts — **WARN (persistent, LOW)**
~54 workspace `.py` files reference the `.env` path/dotenv (broad grep, includes benign). Helpers target the **revoked `~/.hermes/.env` placeholder**, so no live secret is exposed, but they would leak a real key if the placeholder were swapped. `send_evening_health_check.py` is 0-byte (inert). Recommend migrating to live token / gateway-native send, or deleting.

### 1.6 Config — **PASS (no new plaintext secrets)**
Provider keys via env-var refs; no raw secrets hardcoded in live config. (`allow_all_users: true` persists — LOW config hardening debt, flagged in gateway logs 10-24 07:00.)

---

## 2. Channel Integrity

### 2.1 Gateway — RUNNING (PID 17516) — **both platforms connected**
- `gateway_state.json`: process running, **PID 17516**, `platforms.telegram.state: connected` (updated 10-24 06:37), `platforms.whatsapp.state: connected` (updated 10-23 08:46). No errors retrying.
- Live `gateway.log` fresh to 10-24 06:59. Healthy polling generations through today **(gen 8, 10-24 06:37)**.
- gateway-exit-diag: 0 `asyncio.run.exception` / `concurrent_log_handler` crash signatures. Last start 10-23 08:44 (PID 17516, python 3.14.7). This is not the old crash loop.

### 2.2 WhatsApp — **PASS (paired + connected)**
`creds.json` present (3243 B, updated 10-24 06:56) at AppData root. `gateway_state` whatsapp = `connected`. **Note improvement:** channels fully functional (gateway log shows active WhatsApp DM flushing today).

### 2.3 Cron delivery targets — **WARN (25/56 silent, 44.6%)**
`jobs.json` (AppData root): **56 jobs**. Distribution: `origin`×16, `local`×9 (silent = **25/56, 44.6%**), topic-`telegram:-1003784520976:` → `:14`×7, `:20`×5, `:4`×4, `:1`×4, `:10`×3, `:16`×2, plus `:26`,`:28`,`:2`,`:5`×1 each, and `telegram:123286468`×2. With both adapters connected, topic-targeted cron delivery flows again. Silent count slightly improved (26→25).

### 2.4 Multiplex parked profiles — WARN (persistent)
Profiles coach/content-buddy/harold/sat-nav share the same Telegram token; one token → one gateway. `multiplex_standalone_reason` flags adapters as parked. No duplicate-polling conflict observed this cycle; shared token remains the risk vector.

---

## 3. Recent Security Events

### 3.1 Token rejection / compromise markers — **PASS**
No `InvalidToken` / `Unauthorized` / `403` / `404`-on-token in the **live** 10-23/10-24 window. The 2 "Unauthorized"-text hits in `errors.log` (10-22/10-23) were benign (OpenRouter retry + Telegram DNS-discovery log text), not token rejection. No multi-provider simultaneous failure, no cert/SSL anomalies (3 log hits were false positives on the word "send"). No breach markers.

### 3.2 Telegram DNS/IP flakiness — **WARN (transient, recurring, recovered)**
`ConnectError('All connection attempts failed')` bursts recur (e.g. 10-24 06:36, attempts 1–2; cumulative grep count 11563 in gateway.log) — each recovers seconds-to-a-minute later via the sticky IPv4 fallback `149.154.166.110` (last recovered 10-24 06:37, generation 8). Host-level network/DNS flakiness, **not** redirection/attack marker.

### 3.3 Gateway health — **PASS**
No crash loop (0 exceptional exit signatures). Latest start clean, both platforms connected, no `concurrent_log_handler` ModuleNotFoundError.

### 3.4 Auxiliary — WARN (persistent, low)
`allow_all_users: true` (recommend `false` + allow-list). Dual-root token divergence (see 1.1). Multiplex token-share / parked adapters (see 2.4).

---

## FAIL Findings
- **None this cycle.** No credential exposure, no token rejection, no breach markers in the live window. All FAIL items from prior cycles have resolved (backup .env copies, credential caches, telegram_polling_conflict).

## WARN Findings
- Dual-root token divergence (~/.hermes idle placeholder, persistent ≥15 cycles) — LOW
- `.env`-referencing helper scripts (~54 workspace refs, persistent) — LOW
- Silent cron delivery targets (25/56, 44.6%) — WARN
- Telegram DNS instability (recurring `All connection attempts failed` bursts; recovers via 149.154.166.110) — LOW
- Multiplex parked profiles (shared Telegram token) — LOW
- `allow_all_users: true` config hardening — LOW
- Nous Portal: not safely logged in (invalid refresh token, non-blocking custom provider) — LOW

## CRITICAL Escalations
- **None.** No persistent FAIL item reached 3+ consecutive cycles requiring escalation. WhatsApp (paired + connected) no longer an unpaired-days finding; a past TOP finding thread (backup .env copies) remains at zero.

## Trend Comparison (vs 2026-10-22)

| Item | 10-22 | 10-24 | Direction |
|------|-------|-------|-----------|
| Telegram adapter | PASS (connected) | PASS (connected) | No Change (stable) |
| Telegram token (live) | PASS | PASS | No Change |
| Dual-root divergence | WARN | WARN | No Change (persistent debt) |
| Backup `.env` copies | PASS (0) | PASS (0) | No Change |
| Credential caches | PASS | PASS | No Change |
| `.env`-reader scripts | WARN (25) | WARN (54 refs) | No Change (persistent) |
| Google token ACL | PASS | PASS | No Change |
| WhatsApp | PASS (paired+connected) | PASS (paired+connected) | No Change |
| Cron silent delivery | 26/55 | 25/56 | Slightly improved |
| AGENTS.md | PASS (no BOM) | PASS (no BOM) | No Change |

**Persistent security debt (3+ cycles, unchanged):** dual-root token divergence (~/.hermes idle), `.env`-referencing helper scripts, silent cron targets (25/56), `allow_all_users: true`, multiplex token-share/parked adapters, Telegram DNS flakiness.
**No active credential exposure / no token rejection / no breach markers in the live window. Channels healthy (Telegram + WhatsApp connected).**

## Key Findings (machine-checked)
- `bws_cache.json`: absent in both roots — PASS
- backup .env copies: 0 (sustained) — PASS
- `google_token.json` ACL: SYSTEM/Admins/User only — PASS
- WhatsApp unpaired 0 days (paired + connected) — PASS
- 25/56 Cron Jobs silent (origin/local) — WARN
- Topic 20 Missing: false (present — supergroup "Agent Hermes", forum enabled)
- Integrated Daily Synthesis: not in this audit scope (delivery-review item)
- Config Version Drift: not re-run this cycle (prior cycles reported clean)
- Nous Portal Token: invalid refresh (non-blocking custom provider) — LOW
- DNS Instability: Telegram API ConnectError bursts, recurring, recovered — LOW
- Health Log Gaps: none detected in live health/log window

## Remediation Priority
1. Delete the revoked `~/.hermes/.env` placeholder → single authoritative AppData root.
2. Move `.env`-reading helper scripts to gateway-native send / live token; delete inert `send_evening_health_check.py` (0-byte).
3. Set `allow_all_users: false` + allow-list; re-login Nous Portal.
4. Re-review the 25/56 silent cron targets (origin/local) for intended delivery.
5. Continue monitoring Telegram DNS instability (transient, recovers; not an attack marker).

## Retention Note
Retention applied per policy: 7-day rolling window in the report dir. Deleted `SECURITY_AUDIT_2026-10-14.md` (oldest) after writing 10-24; 7 files retained (10-15 → 10-24). Report artifact: `C:\Users\User\.hermes\workspace\Vault\System\Assistant\SECURITY_AUDIT_2026-10-24.md`.

---

*Generated 2026-10-24 by Hermes security-audit cron. Token validated via direct `getMe`. Gateway health via live gateway_state + polling logs; topic 20 delivery target verified via `getChat` (supergroup "Agent Hermes", forum enabled).*