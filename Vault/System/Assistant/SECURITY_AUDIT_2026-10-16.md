# Security Audit — 2026-10-16

**Host:** Windows 11 · **Hermes profile:** default · **Run type:** cron (scheduled)
**Scope:** credential exposure · channel integrity · recent security events

---

## Summary of Findings

| # | Item | Status | Severity |
|---|------|--------|----------|
| 1 | Telegram bot token — dual-root divergence | **WARN** (persistent debt, non-blocking) | WARN |
| 2 | Backup `.env` copies | **PASS** (0, sustained) | — |
| 3 | `google_token.json` ACL | **PASS** | — |
| 4 | `.env`-reading delivery scripts | **WARN** (legacy dated files, revoked-token only) | LOW |
| 5 | Gateway / channel integrity | **PASS (RUNNING, PID 15160)** | — |
| 6 | Cron delivery targets | WARN (29/59 silent) | WARN |
| 7 | WhatsApp session | **PASS (paired + live)** | — |
| 8 | Nous Portal refresh token | WARN (invalid; non-blocking) | LOW |
| 9 | AGENTS.md BOM / config injection | PASS (main absent; workspace UTF-8, no BOM) | — |
| 10 | Gateway crash loop | PASS (no ModuleNotFound/crash signatures in live root) | — |
| 11 | Telegram topic 20 (delivery target) | **PASS** (verified via getChat) | — |

---

## 1. Credential Exposure

### 1.1 Telegram bot token — **WARN (dual-root divergence, persistent debt)**
- **Stale root** `~/.hermes/.env` holds a **revoked** token: direct `getMe` → **HTTP 404 (`Not Found`)**.
- **Live AppData root** `C:\Users\User\AppData\Local\hermes\.env` holds a **valid** token: `getMe` → `{"ok":true}` (bot Ogaitchhermesbot, id 8277244378). This is the token the live gateway loads.
- **Impact:** non-blocking — the running gateway and all Telegram delivery use the valid AppData token. The revoked `~/.hermes` token is a stale placeholder that fails any direct API call referencing that root.
- **Recommendation (repeated):** remove the revoked placeholder in `~/.hermes/.env` and consolidate on the single valid AppData root. Persistent debt ≥11 cycles.

### 1.2 Backup `.env` copies — **PASS (0, sustained)**
No `.env` in `~/.hermes/backups`, `state-snapshots`, `~/hermes-backup`, or `~/.openclaw` (maxdepth-limited). Sustained remediation across all four locations.

### 1.3 `google_token.json` ACL — **PASS**
`icacls`: only `SYSTEM:(I)(F)`, `BUILTIN\Administrators:(I)(F)`, `DESKTOP-25Q3AQC\User:(I)(F)`. No `Everyone`/`BUILTIN\Users`. File present (Oct 16). ACL sound — standard Windows defaults for the owner's own file.

### 1.4 `.env`-reading delivery scripts — **WARN (legacy dated files; LOW risk)**
Scan of `~/.hermes/workspace` finds scripts that read `TELEGRAM_BOT_TOKEN` from a `.env` file directly:
- `workspace/scripts/memory_review_telegram.py` (Jun 23), `ghana_telegram_report.py` (Jul 19), `h_evening_checkin_send.py` (Sep 10), `send_ghana_report.py`, plus dated per-day files under `Vault/family/*/health/` and loose roots (`C:/Users/User/send_*.py`, `send_topic20.py`).
- These read `Path.home() / '.hermes' / '.env'` — i.e. the **revoked** token, not the valid AppData secret. No live credential exposure (token is dead), but they keep the bad pattern alive and would leak a real secret if the placeholder were ever replaced with a valid key, or be silently overwritten into the process table.
- **Recommendation:** delete the active helpers (`memory_review_telegram.py`, `ghana_telegram_report.py`, home-dir `send_*.py`) and stop the dated `send_*`/`tmp_*` proliferation. Flag any re-creation.

### 1.5 Credential cache files — **PASS**
No `bws_cache.json` / `.secret_cache` present in either root.

### 1.6 Config — **PASS (no new plaintext secrets)**
No raw secrets beyond standard `.env`. Values masked. `GATEWAY_ALLOW_ALL_USERS: true` persists (see 3.2).

---

## 2. Channel Integrity

### 2.1 Gateway — **PASS (RUNNING)**
- **Live AppData root** `hermes status`: Gateway **✓ running**, PID **15160**. Confirmed via live `gateway_state.json` (updated 2026-10-16 10:37) and gateway.log fresh to 10:38 (110 writes in the past minute) — the gateway is actively processing.
- Telegram adapter **connected** (updated 2026-10-16 10:35). WhatsApp adapter **connected**, actively flushing text batches as late as 10:38 today (WhatsApp DM traffic live).
- No `asyncio.run.exception`, no `ModuleNotFoundError` in the live AppData root (crash-loop signatures = 0).
- **Note:** the `~/.hermes` gateway_state/startup failure (revoked token, dead PID 16356, log cold since Oct 13) is the **stale legacy root's** history — do not confuse it with the live AppData process. This was the correct resolution of the dual-root state.

### 2.2 Telegram delivery — **PASS**
Live gateway + valid AppData token. Topic-20 target verified live via `getChat`: supergroup **Agent Hermes**, `is_forum: true`, `can_send_messages: true` — topic posts will deliver.

### 2.3 WhatsApp — **PASS (paired + live)**
WhatsApp adapter connected; gateway.log 10:35–10:38 today shows continuous DM batch flushing (owner chats + postpaid customer routing). Bridge stable.

### 2.4 Cron delivery targets — **WARN (29/59 silent)**
AppData `jobs.json` (59 jobs, all with explicit `deliver`) distribution:
- Telegram topic/chat-targeted: **30** (`:14`×7, `:20`×6, `:4`×4, `:26`×2, `:16`×2, `:1`×2, `:10`×2, `:8`×1, `:28`×1, `:2`×1, `telegram:123286468`×2).
- **Silent: 29/59 (49%)** — `origin`×14 + `local`×15.
- This job delivers to `telegram:-1003784520976:20` ✓ verified (topic 20 is in topic list and getChat confirms forum supergroup).

---

## 3. Recent Security Events

### 3.1 Token rejection — clean in live window
No `InvalidToken` / HTTP 404 / `Unauthorized` in the **live AppData** gateway/errors logs today (grep count: 0). The 27 token-rejection entries found earlier are in the stale `~/.hermes/logs` (revoked-root history up to Oct 13), not the live token. No live compromise signal.

### 3.2 `GATEWAY_ALLOW_ALL_USERS: true` — WARN (config)
Persists in AppData config. Grants every sender on every platform access. Persistent LOW/WARN. Recommend `false` + explicit allow-list.

### 3.3 Nous Portal — WARN (low)
"not logged in — Invalid refresh token." Non-blocking (provider=custom/OpenRouter), but portal-managed token-expiry monitoring degraded.

### 3.4 Transient OpenRouter connection retries — WARN (low)
Today's errors.log shows **95** `Connection error` retries across cron conversations (`provider=openrouter`, model `deepseek-*`), with successful retry on attempt 2/3 within seconds. Network/upstream flakiness, not credential rejection (no 401/402/429 hard failures). No data exposure.

---

## Trend vs 2026-10-15

| Item | 10-15 | 10-16 | Direction |
|------|-------|-------|-----------|
| Telegram token divergence | WARN | WARN | No Change (persistent debt) |
| Backup `.env` copies | PASS (0) | PASS (0) | No Change |
| `.env`-reader scripts | WARN (legacy) | WARN (legacy, revoked-only) | No Change |
| Gateway | PASS (running, 15160) | PASS (running, 15160) | No Change (healthy) |
| Cron silent delivery | 29/59 | 29/59 | No Change |
| WhatsApp | PASS (paired+live) | PASS (paired+live) | No Change |
| Nous Portal | WARN | WARN | No Change |
| AGENTS.md BOM | PASS | PASS | No Change |
| Topic 20 target | PASS | PASS | No Change |
| Gateway crash loop | PASS | PASS | No Change |

**Improvements this cycle:** none material; gateway remains healthy on the valid AppData token (Telegram + WhatsApp both connected and live today), backup `.env` exposure stays at 0.
**Persistent security debt (3+ cycles):** dual-root token divergence (non-blocking), 29/59 silent cron (`origin`/`local`), `GATEWAY_ALLOW_ALL_USERS: true`, Nous Portal invalid.
**Watch items:** legacy `.env`-reader delivery scripts remain in workspace + home dir — dated, currently read only the revoked token (LOW) but should be deleted to break the pattern.
**No new active credential exposure.**

---

*Generated 2026-10-16 by Hermes security-audit cron.*