# Security Audit — 2026-10-14

**Host:** Windows 11 · **Hermes profile:** default · **Run type:** cron (scheduled)
**Scope:** credential exposure · channel integrity · recent security events

---

## Summary of Findings

| # | Item | Status | Severity |
|---|------|--------|----------|
| 1 | Telegram bot token — dual-root divergence | **WARN** (unchanged) | WARN |
| 2 | Backup `.env` copies | **PASS** (0, sustained) | — |
| 3 | `google_token.json` ACL | **PASS** | — |
| 4 | `.env`-reading delivery scripts | **IMPROVED → PASS** (was 30, now cleared) | — |
| 5 | Gateway / channel integrity | **PASS (RUNNING)** | — |
| 6 | Cron delivery targets | WARN (28/58 silent) | WARN |
| 7 | WhatsApp session | **PASS (paired + live)** | — |
| 8 | Nous Portal refresh token | WARN (invalid; non-blocking) | LOW |
| 9 | AGENTS.md BOM / config injection | PASS (main absent; workspace UTF-8, no BOM) | — |
| 10 | Gateway crash loop | PASS (0 `asyncio.run.exception`, no ModuleNotFound) | — |
| 11 | Telegram topic 20 (delivery target) | **PASS** (verified via getChat) | — |
| 12 | Browser cloud provider config | WARN (`BROWSER_USE_API_KEY` unset) | LOW |

---

## 1. Credential Exposure

### 1.1 Telegram bot token — **WARN (dual-root divergence, unchanged)**
- **Stale root** `~/.hermes/.env` still holds a revoked placeholder: direct `getMe` → **HTTP 404** (`Not Found`). Historical diverged-root artifact.
- **Live AppData root** `C:\Users\User\AppData\Local\hermes\.env` holds a **valid token**: `getMe` → `{"ok":true}`, bot **Ogaitchhermesbot** (id 8277244378). This is the token the live gateway loads.
- **Recommendation (unchanged):** remove/rotate the revoked placeholder in `~/.hermes/.env`; consolidate on the single valid AppData root.

### 1.2 Backup `.env` copies — **PASS (0, sustained)**
No `.env` in `~/.hermes/backups`, `state-snapshots`, `~/hermes-backup`, or `~/.openclaw` (maxdepth-limited). Sustained remediation across many cycles.

### 1.3 `google_token.json` ACL — **PASS**
`icacls`: only `SYSTEM:(I)(F)`, `BUILTIN\Administrators:(I)(F)`, `DESKTOP-25Q3AQC\User:(I)(F)`. No `Everyone`/`BUILTIN\Users`. Refreshed 10-13 12:18, ACL sound.

### 1.4 `.env`-reading delivery scripts — **IMPROVED → PASS** ✅
The 30 workpace scripts flagged 10-12 that read `TELEGRAM_BOT_TOKEN`/`.env` directly are **all deleted** (workspace/scripts/`ghana_telegram_report.py`, `memory_review_telegram.py`, etc. — gone). Re-scan now finds only:
- `workspace/cron_detail.py` — references `LOCALAPPDATA`/`expanduser` paths for cron inspection, **no secret read**.
- `_tg_send.py` (AppData root) — delivery helper reading the **active (valid)** AppData token; legitimate.
- Residual grep hit `~/.hermes/care_checkin.py` and root `send_*.py` — no `.env`/token reads confirmed.
**Clear improvement over 10-12 (30 → ~0).**

### 1.5 Credential cache files — **PASS**
No `bws_cache.json` / `.secret_cache` present in either root.

### 1.6 Config — **PASS (no plaintext secrets)**
No raw secrets in config; values masked. `allow_all_users: true` noted separately (see 3.3).

---

## 2. Channel Integrity

### 2.1 Gateway — **PASS (RUNNING)**
- `hermes status`: Gateway **✓ running**. PID **6308** — alive (`tasklist`: python.exe, 452 MB).
- AppData gateway.log **fresh** (last write 2026-10-14 06:48; audit at 07:02). WhatsApp flushing batches same window.
- Transient Telegram `ConnectTimeout` at 06:47-ish auto-recovered via sticky IPv4 path `149.154.166.110`; polling resumed (generation 4). No `asyncio.run.exception`, no `ModuleNotFoundError` (0 crash signatures).

### 2.2 Telegram delivery — **PASS**
Live gateway + valid AppData token. Topic-20 target verified live via `getChat`: supergroup **Agent Hermes**, `is_forum: true` — posts with `message_thread_id` will deliver.

### 2.3 WhatsApp — **PASS (paired + live)**
`whatsapp/session/creds.json` at AppData, **3075 B, refreshed 2026-10-14 06:51** — actively flushing user/customer message batches today. Bridge live (persistent improvement; was unpaired through Sep — now stable).

### 2.4 Cron delivery targets — **WARN (28/58 silent)**
AppData `jobs.json` (58 jobs) deliver distribution:
- Telegram topic/chat-targeted: **30** (`:14`×7, `:20`×6, `:4`×4, `:26`×2, `:16`×2, `:1`×2, `:10`×2, `:8`×1, `:28`×1, `:2`×1, `telegram:123286468`×2).
- **Silent: 28/58 (48%)** — `origin`×14 + `local`×14. Persistent passive-loss pattern.
- This job (`security-policy-check`) delivers to `telegram:-1003784520976:20` ✓ verified live.

---

## 3. Recent Security Events

### 3.1 Token rejection — none in live window
`errors.log` (AppData, live root) shows **0** `InvalidToken` / HTTP 404 / Unauthorized entries. No compromise signal in the live token's log.

### 3.2 OpenRouter stream timeouts — WARN (transient, not credential)
06:48 ReadTimeout / stale 180s stream on `z-ai/glm-5.3-flash` (serving provider Relace, cf-ray JNB), plus retries. Upstream latency, not a credential/security issue. Self-recovered.

### 3.3 `allow_all_users: true` — WARN (config)
Persists in AppData config.yaml, bridged to `GATEWAY_ALLOW_ALL_USERS: true`. Grants every sender on every platform access. Persistent LOW/WARN. Recommend `false` + explicit allow-list.

### 3.4 Browser cloud provider — WARN (config integrity)
`BROWSER_USE_API_KEY` not set → browser-use cloud provider fails; falls back to local Chromium. Functionality issue, no exposure. Recommend configuring key or switching browser provider.

### 3.5 Small tooling gaps — WARN (low)
- `ddgs` package not installed → web_search falls back to keyless rescue. Low.
- Nous Portal: "not logged in — Invalid refresh token". Non-blocking (provider=custom OpenRouter), but portal-managed token-expiry monitoring degraded. WARN.

---

## Trend vs 2026-10-12

| Item | 10-12 | 10-14 | Direction |
|------|-------|-------|-----------|
| Telegram token divergence | WARN | WARN | No Change |
| Backup `.env` copies | PASS (0) | PASS (0) | No Change |
| `.env`-reader scripts | **FAIL (30)** | **PASS (~0)** | **Improved** ✅ |
| Gateway | PASS (running) | PASS (running) | No Change |
| Cron silent delivery | 28/58 | 28/58 | No Change |
| WhatsApp | PASS (online) | PASS (paired+live) | No Change |
| Nous Portal | WARN | WARN | No Change |
| AGENTS.md BOM | PASS | PASS | No Change |
| Gateway crash loop | PASS | PASS | No Change |
| Topic 20 target | PASS | PASS | No Change |

**Improvements this cycle:** Env-reader delivery-script regression fully cleared (30 → ~0) — the strongest positive since gateway recovery. **Persistent security debt (3+ cycles):** dual-root token divergence, 28/58 silent cron (`origin`/`local`), Nous Portal invalid, `allow_all_users: true`. **New findings:** browser cloud provider `BROWSER_USE_API_KEY` unset (WARN), OpenRouter transient stream timeout (WARN). No new credential exposure.

---

*Generated 2026-10-14 by Hermes security-audit cron.*