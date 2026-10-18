# Security Audit — 2026-10-17

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
| 5 | Gateway / channel integrity | **PASS (RUNNING, PID 2788)** | — |
| 6 | Cron delivery targets | WARN (29/59 silent) | WARN |
| 7 | WhatsApp session | **PASS (paired + live)** | — |
| 8 | OpenRouter credits — **NEW FAIL** | **FAIL (402 exhausted, some cron output failed)** | HIGH |
| 9 | Telegram DNS flakiness | WARN (transient; recovered 07:08) | LOW |
| 10 | Nous Portal / auxiliary auth | WARN (invalid/degraded, non-blocking) | LOW |
| 11 | AGENTS.md BOM / config injection | PASS (main absent; workspace UTF-8, no BOM) | — |
| 12 | Gateway crash loop | PASS (0 crash signatures) | — |
| 13 | Telegram topic 20 (delivery target) | **PASS** (verified via getChat) | — |
| 14 | Multiplex — profiles sharing token | **WARN (NEW)** (specialist adapters parked) | MEDIUM |

---

## 1. Credential Exposure

### 1.1 Telegram bot token — **WARN (dual-root divergence, persistent debt ≥11 cycles)**
- **Live AppData root** `C:\Users\User\AppData\Local\hermes\.env` holds a **valid** token: `getMe` → `{"ok":true}` (bot Ogaitchhermesbot, id 8277244378). This is what the live gateway loads.
- **Stale root** `~/.hermes/.env` still holds a **revoked** token: `getMe` → HTTP 404 `Not Found`.
- Non-blocking (all live delivery uses the valid AppData token), but the revoked placeholder remains a footgun — any direct API call or legacy script referencing `~/.hermes` fails. **Recommendation (repeated): delete the revoked placeholder; consolidate on the single AppData root.**

### 1.2 Backup `.env` copies — **PASS (0, sustained)**
Zero `.env` across `~/.hermes/backups`, `state-snapshots`, `~/hermes-backup`, `~/.openclaw` (maxdepth-limited). Sustained remediation, all four locations clean.

### 1.3 `google_token.json` ACL — **PASS**
`icacls`: `SYSTEM:(I)(F)`, `BUILTIN\Administrators:(I)(F)`, `DESKTOP-25Q3AQC\User:(I)(F)`. No `Everyone`/`BUILTIN\Users`. Standard Windows owner defaults. File present (Oct 16).

### 1.4 `.env`-reading delivery scripts — **WARN (legacy, LOW risk)**
~30 dated `send_*`/`tmp_*` Python helpers across `~/.hermes/workspace` (+ `Vault/family/*/health/`, `Vault/business/…`) and 4 loose root files (`~/send_ghana_dashboard.py`, `~/send_report.py`, `~/send_telegram_report.py`, `~/.hermes/care_checkin.py`). These read `Path.home()/.hermes/.env` — i.e. the **revoked** token. No live credential exposure, but they keep the bad pattern alive and would leak a real secret if the placeholder were ever replaced with a valid key. **Recommend deleting the active helpers + home-dir `send_*.py`.**

### 1.5 Credential cache files — **PASS**
No `bws_cache.json` / `.secret_cache` in either root.

### 1.6 Config — **PASS (no new plaintext secrets)**
No raw secrets beyond standard `.env`. `GATEWAY_ALLOW_ALL_USERS: true` persists (see 3.4).

---

## 2. Channel Integrity

### 2.1 Gateway — **PASS (RUNNING, PID 2788)**
- `hermes status` + `gateway_state.json`: running, PID **2788**. `tasklist` confirms PID 2788 alive (python.exe, 423 MB). **PID changed since 10-16 (was 15160) → clean restart observed.**
- `gateway.log` fresh to **07:09** (last write minutes before audit). Telegram + WhatsApp both `connected` in state file, updated 07:08.
- Crash signatures (`asyncio.run.exception` / `ModuleNotFoundError`) in live root: **0**.

### 2.2 Telegram delivery — **PASS**
Live gateway + valid AppData token. Topic-20 host verified via `getChat`: **supergroup, `is_forum: true`** — thread posts deliver. Manual `getMe` to confirm token bearer: ok.

### 2.3 WhatsApp — **PASS (paired + live)**
`creds.json` present (3075 B). gateway.log 07:08–07:09 shows continuous DM batch flushing (owner + customer routing). Bridge stable.

### 2.4 Cron delivery targets — **WARN (29/59 silent)**
`jobs.json` (59 jobs). Distribution: `telegram:-1003784520976` topic targets 30 (`:14`×7,`:20`×6,`:4`×4,`:26`×2,`:16`×2,`:1`×2,`:10`×2,`:8`×1,`:28`×1,`:2`×1) + `telegram:123286468`×2. **Silent: 29 (49%)** — `local`×15 + `origin`×14. This job delivers to `telegram:-1003784520976:20` ✓ verified.

### 2.5 Multiplex parked profiles — **WARN (NEW)**
`gateway_state.json` reports profiles **coach, content-buddy, harold, sat-nav** each hold the same `TELEGRAM_BOT_TOKEN` as default → one token serves one gateway; the specialist profiles' Telegram adapters are **parked**. This is a channel-integrity limitation for the delegated team (they cannot answer directly on Telegram). Not credential exposure, but a capacity/availability gap to resolve via separate tokens or profile_routes.

---

## 3. Recent Security Events

### 3.1 OpenRouter credits / in-flight budget exhausted — **FAIL (NEW, HIGH)**
**20 × HTTP 402** events in `errors.log` today (03:25 batch), provider=openrouter, model `z-ai/glm-5.3-flash`, `limit_source: openrouter_credits` / `openrouter_in_flight_budget`:
> "This request requires more credits, or fewer max_tokens… adjust the key's monthly limit"
- **Impact:** `Streaming failed before delivery` in cron `5128ceaa2c09` — at least the early-morning cron batch lost LLM output. Downstream reports from those jobs likely empty/failed.
- **Nature:** upstream credit exhaustion, **not** credential compromise (key valid, no 401/403). Operational availability failure.
- **Action required:** add credits at openrouter.ai/settings/credits and/or lower `max_tokens`; verify next cron batch.

### 3.2 Telegram DNS/IP flakiness — **WARN (transient, recovered)**
Multiple `api.telegram.org` / IPv4-literal failures today (getaddrinfo failed, ConnectTimeout, All connection attempts failed). Gateway **recovered 07:08** via sticky IPv4 `149.154.166.110` ("Telegram API transport recovered", polling resumed, gen 4). Transient host-network flakiness, self-healed; no data exposure.

### 3.3 Token rejection — **PASS (clean in live window)**
`InvalidToken` / `HTTP 404` / `Unauthorized` in live AppData logs today: **0**. No live compromise signal; the only 404 is the stale `~/.hermes` placeholder token (1.1).

### 3.4 `GATEWAY_ALLOW_ALL_USERS: true` — **WARN (config, persistent)**
Grants every sender on every platform access. Persistent LOW/WARN. Recommend `false` + explicit allow-list.

### 3.5 Nous Portal / auxiliary auth — **WARN (low)**
`hermes status`: "not logged in — Invalid refresh token." Auxiliary Nous client unavailable. Non-blocking (provider=custom/OpenRouter) but portal token monitoring degraded. Also `web_search` `ddgs` package missing (one-shot keyless rescue) and `whatsapp-customer-gate` plugin logs `'GatewayRunner' object has no attribute 'send_message'` (2×, WARN — plugin integration, not data exposure).

---

## Trend vs 2026-10-16

| Item | 10-16 | 10-17 | Direction |
|------|-------|-------|-----------|
| Telegram token divergence | WARN | WARN | No Change (persistent debt) |
| Backup `.env` copies | PASS (0) | PASS (0) | No Change |
| `.env`-reader scripts | WARN (legacy) | WARN (legacy, revoked-only) | No Change |
| Gateway | PASS (PID 15160) | PASS (PID 2788) | Clean restart, healthy |
| Cron silent delivery | 29/59 | 29/59 | No Change |
| WhatsApp | PASS (paired+live) | PASS (paired+live) | No Change |
| **OpenRouter credits** | — (clean) | **FAIL (402 ×20)** | **NEW — regression** |
| Multiplex parked profiles | — | **WARN (NEW)** | **NEW** |
| Nous Portal | WARN | WARN | No Change |
| AGENTS.md BOM | PASS | PASS | No Change |
| Topic 20 target | PASS | PASS | No Change |
| Gateway crash loop | PASS | PASS | No Change |

**Improvements this cycle:** gateway confirmed healthy on a clean new PID (2788) with Telegram + WhatsApp both live; backup `.env` exposure holds at 0.
**New this cycle:** OpenRouter credit exhaustion (20× 402, lost cron output — HIGH, action required); multiplex token-share parks specialist-profile adapters (MEDIUM).
**Persistent security debt (3+ cycles):** dual-root token divergence, 29/59 silent cron, `GATEWAY_ALLOW_ALL_USERS: true`, Nous Portal invalid, legacy `.env`-reader scripts.
**No active credential exposure / no breach markers.**

---

*Generated 2026-10-17 by Hermes security-audit cron.*