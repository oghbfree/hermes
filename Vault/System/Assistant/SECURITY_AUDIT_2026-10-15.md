# Security Audit — 2026-10-15

**Host:** Windows 11 · **Hermes profile:** default · **Run type:** cron (scheduled)
**Scope:** credential exposure · channel integrity · recent security events

---

## Summary of Findings

| # | Item | Status | Severity |
|---|------|--------|----------|
| 1 | Telegram bot token — dual-root divergence | **WARN** (persistent debt, non-blocking) | WARN |
| 2 | Backup `.env` copies | **PASS** (0, sustained) | — |
| 3 | `google_token.json` ACL | **PASS** | — |
| 4 | `.env`-reading delivery scripts | **WARN** (legacy dated files, revoked token only) | LOW |
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
- **Impact:** non-blocking — the running gateway and all Telegram delivery use the valid AppData token. The revoked `~/.hermes` token is a stale placeholder that fails any direct API call on that root.
- **Recommendation (repeated):** remove the revoked placeholder in `~/.hermes/.env` and consolidate on the single valid AppData root. Persistent debt ≥10 cycles.

### 1.2 Backup `.env` copies — **PASS (0, sustained)**
No `.env` in `~/.hermes/backups`, `state-snapshots`, `~/hermes-backup`, or `~/.openclaw` (maxdepth-limited). Sustained remediation.

### 1.3 `google_token.json` ACL — **PASS**
`icacls`: only `SYSTEM:(I)(F)`, `BUILTIN\Administrators:(I)(F)`, `DESKTOP-25Q3AQC\User:(I)(F)`. No `Everyone`/`BUILTIN\Users`. Refreshed 10-13 12:18. ACL sound.

### 1.4 `.env`-reading delivery scripts — **WARN (legacy dated files; LOW risk)**
Scan of `~/.hermes/workspace` finds scripts that read `TELEGRAM_BOT_TOKEN` from a `.env` file directly:
- `workspace/scripts/memory_review_telegram.py` (Jun 23), `ghana_telegram_report.py` (Jul 19), `h_evening_checkin_send.py` (Sep 10), plus dated per-day files under `Vault/family/*/health/`.
- These read `Path.home() / '.hermes' / '.env'` — i.e. the **revoked** token, not the valid AppData secret. No live credential exposure, but they keep the bad pattern alive and would leak a real secret if the placeholder were ever replaced with a valid key.
- **Recommendation:** delete the active helpers (`memory_review_telegram.py`, `ghana_telegram_report.py`) and stop the dated `send_*`/`tmp_*` proliferation. Flag any re-creation.

### 1.5 Credential cache files — **PASS**
No `bws_cache.json` / `.secret_cache` present in either root.

### 1.6 Config — **PASS (no new plaintext secrets)**
No raw secrets beyond standard `.env`. Values masked. `allow_all_users: true` persists (see 3.3).

---

## 2. Channel Integrity

### 2.1 Gateway — **PASS (RUNNING)**
- `hermes status`: Gateway **✓ running**, PID **15160**. Confirmed alive via tasklist (python.exe, ~413 MB).
- **AppData** gateway.log **fresh** (last write 2026-10-15 07:42; audit ~07:41). Telegram polling healthy at 03:48, 05:35 and recovered generation 8 at 07:41 today. No `asyncio.run.exception`, no `ModuleNotFoundError` in the live root.
- Note: the `~/.hermes/logs/gateway.log` (Oct 13) shows the OLD revoked-token startup-failure — that is the stale root's history, not the live process. Do not confuse the two.

### 2.2 Telegram delivery — **PASS**
Live gateway + valid AppData token. Topic-20 target verified live via `getChat`: supergroup **Agent Hermes**, `is_forum: true` — topic posts will deliver.

### 2.3 WhatsApp — **PASS (paired + live)**
`whatsapp/session/creds.json` at AppData, **3075 B, refreshed 2026-10-15 07:40** — actively flushing batches today. Bridge stable (persistent improvement over the unpaired Sep state).

### 2.4 Cron delivery targets — **WARN (29/59 silent)**
AppData `jobs.json` (59 jobs) deliver distribution:
- Telegram topic/chat-targeted: **30** (`:14`×7, `:20`×6, `:4`×4, `:26`×2, `:16`×2, `:1`×2, `:10`×2, `:8`×1, `:28`×1, `:2`×1, `telegram:123286468`×2).
- **Silent: 29/59 (49%)** — `origin`×14 + `local`×15.
- This job (`security-policy-check`) delivers to `telegram:-1003784520976:20` ✓ verified live.

---

## 3. Recent Security Events

### 3.1 Token rejection — clean in live window
No `InvalidToken` / HTTP 404 / Unauthorized in the **AppData** errors/gateway logs. The 27 token-rejection entries found are in the stale `~/.hermes/logs` (revoked-root history up to 10-13) — not the live token. No live compromise signal.

### 3.2 `allow_all_users: true` — WARN (config)
Persists in AppData config, bridged to `GATEWAY_ALLOW_ALL_USERS: true`. Grants every sender on every platform access. Persistent LOW/WARN. Recommend `false` + explicit allow-list.

### 3.3 Nous Portal — WARN (low)
"not logged in — Invalid refresh token." Non-blocking (provider=custom OpenRouter), but portal-managed token-expiry monitoring degraded.

### 3.4 Small tooling gaps — WARN (low)
- `BROWSER_USE_API_KEY` not set → browser-use cloud provider fails; falls back to local Chromium. Functionality, no exposure.
- `ddgs` package not installed → web_search uses keyless rescue.

---

## Trend vs 2026-10-14

| Item | 10-14 | 10-15 | Direction |
|------|-------|-------|-----------|
| Telegram token divergence | WARN | WARN | No Change (persistent debt) |
| Backup `.env` copies | PASS (0) | PASS (0) | No Change |
| `.env`-reader scripts | PASS (~0) | WARN (legacy dated, revoked-only) | Slight regression (re-detected) |
| Gateway | PASS (running) | PASS (running, 15160) | No Change |
| Cron silent delivery | 28/58 | 29/59 | No Change |
| WhatsApp | PASS (paired+live) | PASS (paired+live) | No Change |
| Nous Portal | WARN | WARN | No Change |
| AGENTS.md BOM | PASS | PASS | No Change |
| Topic 20 target | PASS | PASS | No Change |
| Gateway crash loop | PASS | PASS | No Change |

**Improvements this cycle:** none material; gateway remains healthy on the valid AppData token, backup `.env` exposure stays at 0, WhatsApp live.
**Persistent security debt (3+ cycles):** dual-root token divergence (non-blocking), 29/59 silent cron (`origin`/`local`), `allow_all_users: true`, Nous Portal invalid.
**Watch items:** legacy `.env`-reader delivery scripts re-detected in workspace — dated, read only the revoked token (LOW) but should be deleted to break the pattern.
**No new active credential exposure.**

---

*Generated 2026-10-15 by Hermes security-audit cron.*