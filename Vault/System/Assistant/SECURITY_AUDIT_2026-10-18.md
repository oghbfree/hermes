# Security Audit — 2026-10-18

**Host:** Windows 11 · **Hermes profile:** default · **Run type:** cron (scheduled)
**Scope:** credential exposure · channel integrity · recent security events

---

## Summary of Findings

| # | Item | Status | Severity |
|---|------|--------|----------|
| 1 | Telegram bot token — dual-root divergence | **WARN** (persistent debt) | WARN |
| 2 | Backup `.env` copies | **PASS** (0, sustained) | — |
| 3 | `google_token.json` ACL | **PASS** | — |
| 4 | `.env`-reading delivery scripts | **WARN** (legacy dated, revoked-token only) | LOW |
| 5 | Gateway / channel integrity | **PASS (RUNNING, PID 16424)** | — |
| 6 | Cron delivery targets | WARN (29/59 silent) | WARN |
| 7 | WhatsApp session | **PASS (paired + live)** — transient send hiccups noted | LOW |
| 8 | OpenRouter credits — **RESOLVED** | **PASS (no 402 today; 10-17 batch only)** | — |
| 9 | Telegram DNS flakiness | WARN (transient; recovered) | LOW |
| 10 | Nous Portal / auxiliary auth | WARN (invalid/degraded, non-blocking) | LOW |
| 11 | AGENTS.md BOM / config injection | PASS (main absent; workspace UTF-8, no BOM) | — |
| 12 | Gateway crash loop | PASS (0 crash signatures) | — |
| 13 | Telegram topic 20 (delivery target) | **PASS** (verified via getChat) | — |
| 14 | Multiplex — profiles sharing token | **WARN** (specialist adapters parked) | MEDIUM |

---

## 1. Credential Exposure

### 1.1 Telegram bot token — **WARN (dual-root divergence, persistent debt ≥12 cycles)**
- **Live AppData root** `C:\Users\User\AppData\Local\hermes\.env` holds a **valid** token: `getMe` → `{"ok":true}` (bot Ogaitchhermesbot, id 8277244378). This is what the live gateway loads.
- **Stale root** `~/.hermes/.env` still holds a **revoked** token: `getMe` → HTTP 404 `Not Found`.
- Non-blocking (all live delivery uses the valid AppData token), but the revoked placeholder remains a footgun. **Recommendation (repeated): delete the revoked placeholder; consolidate on the single AppData root.**

### 1.2 Backup `.env` copies — **PASS (0, sustained)**
Zero `.env` across `~/.hermes/backups`, `state-snapshots`, `~/hermes-backup`, `~/.openclaw` (maxdepth-limited). All locations clean.

### 1.3 `google_token.json` ACL — **PASS**
`icacls`: `SYSTEM:(I)(F)`, `BUILTIN\Administrators:(I)(F)`, `DESKTOP-25Q3AQC\User:(I)(F)`. No `Everyone`/`BUILTIN\Users`. Standard Windows owner defaults.

### 1.4 `.env`-reading delivery scripts — **WARN (legacy, LOW risk)**
~30 dated `send_*`/`tmp_*` helpers across `~/.hermes/workspace` plus 3 loose root files (`~/send_ghana_dashboard.py`, `~/send_report.py`, `~/send_telegram_report.py`). These read `Path.home()/.hermes/.env` — i.e. the **revoked** token. No live credential exposure (placeholder revoked), but the bad pattern persists and would leak a real secret if the placeholder were swapped for a valid key. **Recommend deleting active helpers + home-dir `send_*.py`.**

### 1.5 Credential cache files — **PASS**
No `bws_cache.json` / `.secret_cache` in either root.

### 1.6 Config — **PASS (no new plaintext secrets)**
Provider keys via env var refs (`${OPENROUTER_API_KEY}`); no raw secrets hardcoded. `allow_all_users: true` persists (config.yaml lines 596, 699; see 3.4).

---

## 2. Channel Integrity

### 2.1 Gateway — **PASS (RUNNING, PID 16424)**
- `hermes status` + `gateway_state.json`: running, PID **16424**. `tasklist` confirms PID 16424 alive (python.exe, 454 MB). **PID changed since 10-17 (was 2788) → clean restart observed.**
- `gateway.log` fresh to **09:06** (last write just before audit). Telegram + WhatsApp both `connected` in state file, updated 09:05–09:06.
- Crash signatures (`asyncio.run.exception` / `ModuleNotFoundError`) in live root: **0**.

### 2.2 Telegram delivery — **PASS**
Live gateway + valid AppData token. Topic-20 host verified via `getChat`: **supergroup, `is_forum: true`** — thread posts deliver. Manual `getMe` confirms token bearer: ok.

### 2.3 WhatsApp — **PASS (paired + live, minor send hiccups)**
`creds.json` present (3075 B, updated 09:06 today). Gateway shows one initial connect timeout at 09:05, **recovered 09:06** (attempt 2 success). Two send failures logged at 09:07 (`Home-channel startup notification failed`, `[Whatsapp] Fallback send also failed`) — transient during the post-reconnect window, bridge otherwise stable and flushing DMs. Flagged LOW.

### 2.4 Cron delivery targets — **WARN (29/59 silent)**
`jobs.json` (59 jobs). Distribution: `telegram:-1003784520976` topic targets 30 (`:14`×7,`:20`×6,`:4`×4,`:26`×2,`:16`×2,`:1`×2,`:10`×2,`:8`×1,`:28`×1,`:2`×1) + `telegram:123286468`×2. **Silent: 29 (49%)** — `local`×15 + `origin`×14. This job (security-policy-check 07:00) delivers to `telegram:-1003784520976:20` ✓ verified for the audit posting.

### 2.5 Multiplex parked profiles — **WARN (persistent)**
Profiles **coach, content-buddy, harold, sat-nav** each carry the same `TELEGRAM_BOT_TOKEN` as default; bearer probe all return HTTP 200 (same valid token). One token serves one gateway → specialist adapters are **parked** (cannot answer directly on Telegram). Not credential exposure, but a channel-availability gap for the delegated team. `taiwah` profile present with no token line.

---

## 3. Recent Security Events

### 3.1 OpenRouter credits — **RESOLVED (no 402 today)**
- **Yesterday (10-17 03:25 batch):** 20 × HTTP 402 (`requires more credits` / `in_flight_budget`), model `z-ai/glm-5.3-flash` — some early cron output lost.
- **Today (10-18):** **0 × 402** in `errors.log`. The one earlier grep hit was a tool-echo, not a real 402. **Upstream credit exhaustion cleared** (credits added or spend normalized). No 401/403 — the key itself is valid throughout. **Improvement vs 10-17.**

### 3.2 Telegram DNS/IP flakiness — **WARN (transient, recovered)**
MWA adapter connected 09:05 with a logs gap around startup; the 09:07 WhatsApp send failures correlate. No host-wide multi-service DNS outage observed this window.

### 3.3 Token rejection — **PASS (clean in live window)**
`InvalidToken` / `Unauthorized` / HTTP 404 today in live AppData errors/agent logs: **0**. No live compromise signal; the only 404 is the stale `~/.hermes` placeholder token (1.1). (`agent.log` shows 64 lifetime 404/Unauthorized matches — historical, none dated today.)

### 3.4 `allow_all_users: true` — **WARN (config, persistent)**
Grants every sender on every platform access. Persistent LOW/WARN. Recommend `false` + explicit allow-list.

### 3.5 Auxiliary integration warnings — **WARN (low)**
- `web_search` backend `ddgs` package missing (keyless fallback; main search unaffected).
- `whatsapp-customer-gate` plugin: `'GatewayRunner' object has no attribute 'send_message'` (2× today) — plugin integration gap (relates to 2.3 send hiccups), not data exposure.
- Nous Portal / auxiliary client: historical invalid-refresh-token state; non-blocking (custom/OpenRouter provider).

---

## Trend vs 2026-10-17

| Item | 10-17 | 10-18 | Direction |
|------|-------|-------|-----------|
| Telegram token divergence | WARN | WARN | No Change (persistent debt) |
| Backup `.env` copies | PASS (0) | PASS (0) | No Change |
| `.env`-reader scripts | WARN (legacy) | WARN (legacy, revoked-only) | No Change |
| Gateway | PASS (PID 2788) | PASS (PID 16424) | Clean restart, healthy |
| Cron silent delivery | 29/59 | 29/59 | No Change |
| WhatsApp | PASS (paired+live) | PASS (paired+live, minor hiccups) | Slight — send hiccups noted |
| **OpenRouter credits** | **FAIL (402 ×20)** | **RESOLVED (0 today)** | **IMPROVED — cleared** |
| Multiplex parked profiles | WARN | WARN | No Change |
| Nous Portal | WARN | WARN | No Change |
| AGENTS.md BOM | PASS | PASS | No Change |
| Topic 20 target | PASS | PASS | No Change |
| Gateway crash loop | PASS | PASS | No Change |

**Improvements this cycle:** OpenRouter credit exhaustion from 10-17 fully cleared (0× 402 today); gateway confirmed healthy on clean new PID (16424) with Telegram + WhatsApp live.
**New this cycle:** minor WhatsApp send hiccups (post-reconnect, transient).
**Persistent security debt (3+ cycles):** dual-root token divergence, 29/59 silent cron, `allow_all_users: true`, multiplex token-share / parked adapters, legacy `.env`-reader scripts, Nous Portal invalid.
**No active credential exposure / no breach markers.**

---

*Generated 2026-10-18 by Hermes security-audit cron.*