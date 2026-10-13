# Security Audit — 2026-10-12

**Host:** Windows 11 · **Hermes profile:** default · **Run type:** cron (scheduled)
**Scope:** credential exposure · channel integrity · recent security events

---

## Summary of Findings

| # | Item | Status | Severity |
|---|------|--------|----------|
| 1 | Telegram bot token validity | **WARN** (dual-root divergence, unchanged) | WARN |
| 2 | Backup `.env` copies | PASS (0, sustained) | — |
| 3 | `google_token.json` ACL | PASS | — |
| 4 | `.env`-reading delivery scripts | **FAIL (regression: 30 files, unchanged)** | WARN |
| 5 | Gateway / channel integrity | **PASS (RUNNING — improved)** | — |
| 6 | Cron delivery targets | WARN (28/58 silent: 14 origin + 14 local) | WARN |
| 7 | WhatsApp session | **PASS (paired + online — improved)** | — |
| 8 | Nous Portal refresh token | WARN (invalid; non-blocking — provider=custom OpenRouter) | LOW |
| 9 | AGENTS.md BOM / config injection | PASS (main absent; workspace copy UTF-8, no BOM) | — |
| 10 | Gateway crash loop | PASS (0 `asyncio.run.exception`; no ModuleNotFound) | — |
| 11 | Telegram topic 20 (delivery target) | **PASS** (verified live via getChat: supergroup + forum) | — |

---

## 1. Credential Exposure

### 1.1 Telegram bot token — **WARN (dual-root divergence, unchanged)**
- **Stale gateway root** `~/.hermes/.env` still holds a **revoked placeholder** (`827724...1UJE`): direct `getMe` → **HTTP 404** (`Not Found`). Last rejection logged 10-06 11:12 in the **stale** `~/.hermes/logs/gateway.log` (mtime 10-06). Historical events from 09-22, 10-01, 10-06 — all from the stale root token.
- **Live alternate root** `C:\Users\User\AppData\Local\hermes\.env` holds a **valid token**: `getMe` → `{"ok":true}`, bot **Ogaitchhermesbot** (id 8277244378). This is the token the live gateway loads.
- **Recommendation (unchanged):** remove/rotate the revoked placeholder in `~/.hermes/.env`; consolidate delivery on the single valid AppData root.

### 1.2 Backup `.env` copies — **PASS (0, sustained)**
No `.env` copies in `~/.hermes/backups`, `state-snapshots`, `~/hermes-backup`, or `~/.openclaw` (maxdepth-limited). Sustained remediation across 3+ cycles.

### 1.3 `google_token.json` ACL — **PASS**
`icacls`: only `NT AUTHORITY\SYSTEM:(I)(F)`, `BUILTIN\Administrators:(I)(F)`, `User:(I)(F)`. No `Everyone`/`BUILTIN\Users`. Standard owner-only protection. Refreshed 10-11 10:02, ACL sound.

### 1.4 `.env`-reading delivery scripts — **FAIL (regression, unchanged at 30)**
30 workspace `.py` files reference/read `TELEGRAM_BOT_TOKEN` directly from `~/.hermes/.env` via `Path.home()/.hermes/.env` or `os.path.expanduser("~/.hermes/.env")`. Persistent regression (was 0 on 10-09/10-10). These leak tokens to process table, shell history, and logs — and read the **stale revoked** root token, so they are non-functional for delivery anyway.
- **Active scripts** (workspace/scripts/): `ghana_telegram_report.py`, `h_evening_checkin_send.py`, `memory_review_telegram.py`, `mum_evening_checkin.py`, `send_ghana_report.py` — highest priority, in the live delivery path.
- **Home root:** `~/.hermes/care_checkin.py` also present.
- **Action:** audit for still-scheduled use, then delete; replace any needed with Hermes-native env injection.

---

## 2. Channel Integrity

### 2.1 Gateway — **PASS (RUNNING — improved from yesterday)**
- `hermes status`: Gateway **✓ running**, manager manual process, PID **9352** — confirmed **alive** via `tasklist`.
- **AppData gateway.log** fresh: last entry **2026-10-12 06:51**, gated via the valid AppData token.
- No `asyncio.run.exception` / no `ModuleNotFoundError` crash signature (0 entries). The earlier startup-rejection entries in `~/.hermes/logs/gateway.log` (mtime 10-06) belong to the **stale root** and are historical, not current.
- **Key improvement over 10-11:** gateway was stopped yesterday; today it is running and processing messages.

### 2.2 Telegram delivery — **PASS**
Live gateway + valid AppData token → cron output reaches users. Topic 20 target verified live via `getChat` (supergroup `Agent Hermes`, `is_forum: true`).

### 2.3 WhatsApp — **PASS (paired + online — improved)**
`whatsapp/session/creds.json` present at **AppData** (3074 B, refreshed **2026-10-12 06:57**). AppData gateway.log shows WhatsApp actively flushing message batches (06:22, 06:26, 06:51 today) with customer-gate dispatch. Bridge is **live** — improvement from yesterday's offline state.

### 2.4 Cron delivery targets — **WARN (28/58 silent)**
AppData `jobs.json` (58 jobs) deliver distribution:
- Telegram topic/chat-targeted: **30** (`:14`×7, `:20`×6, `:4`×4, `:26`×2, `:16`×2, `:1`×2, `:10`×2, `:8`×1, `:28`×1, `:2`×1, plus `telegram:123286468`×2).
- Silent: **28/58 (48%)** — `origin`×14 + `local`×14. Persistent passive-loss pattern.
- This job (`security-policy-check`) delivers to `telegram:-1003784520976:20` ✓ target verified live.

---

## 3. Recent Security Events

### 3.1 Token rejection — dual-root divergence, unchanged
`errors.log` (stale root) logs token `827724...1UJE` rejections dated **09-22, 10-01, 10-06** — all from the stale `~/.hermes` placeholder. No `InvalidToken` / rejection entries in the **AppData** `errors.log` (clean). Live AppData token valid today. Not a compromise — a config-divergence artifact.

### 3.2 Nous Portal — **WARN (invalid refresh token)**
`hermes status`: Portal "not logged in — Invalid refresh token". Non-blocking (provider=custom OpenRouter), but portal-managed token-expiry monitoring degraded.

### 3.3 `allow_all_users: true` — WARN (config)
`GATEWAY_ALLOW_ALL_USERS: true` persists in AppData config.yaml. Grants every sender on every platform access. Persistent LOW/WARN. Recommend `false` with an explicit allow-list.

### 3.4 Config health — PASS
No plaintext secrets in config; no BOM in AGENTS.md (main absent; workspace copy UTF-8 CRLF). OpenRouter `sk-o...72c1`, xAI `xai-...Cfn5`, Firecrawl `fc-3...52e6` present-but-masked.

---

## Trend vs 2026-10-11

| Item | 10-11 | 10-12 | Direction |
|------|-------|-------|-----------|
| Telegram token divergence | WARN | WARN | No Change |
| Backup `.env` copies | PASS (0) | PASS (0) | No Change |
| `.env`-reader scripts | FAIL (30) | FAIL (30) | No Change |
| Gateway | WARN (stopped) | **PASS (running)** | **Improved** |
| Cron silent delivery | 27/57 | 28/58 | No Change |
| WhatsApp | WARN (offline) | **PASS (online)** | **Improved** |
| Nous Portal | WARN | WARN | No Change |
| AGENTS.md BOM | PASS | PASS | No Change |
| Gateway crash loop | PASS | PASS | No Change |
| Topic 20 target | PASS | PASS | No Change |

**Improvements this cycle:** Gateway restored (running + processing), WhatsApp live. **Persistent security debt (3+ cycles):** dual-root token divergence, 28/58 silent cron, Nous Portal invalid, `allow_all_users: true`. **New regression:** none this cycle.

---

*Generated 2026-10-12 by Hermes security-audit cron.*