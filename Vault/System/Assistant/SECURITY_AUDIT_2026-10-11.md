# Security Audit — 2026-10-11

**Host:** Windows 11 · **Hermes profile:** default · **Run type:** cron (scheduled)
**Scope:** credential exposure · channel integrity · recent security events

---

## Summary of Findings

| # | Item | Status | Severity |
|---|------|--------|----------|
| 1 | Telegram bot token validity | **WARN** (dual-root divergence, unchanged) | WARN |
| 2 | Backup `.env` copies | PASS (0, sustained) | — |
| 3 | `google_token.json` ACL | PASS | — |
| 4 | `.env`-reading delivery scripts | **FAIL (regression: 30 files)** | WARN |
| 5 | Gateway / channel integrity | **WARN** (stopped; no gateway process live) | WARN |
| 6 | Cron delivery targets | **WARN** (27/57 silent: 14 origin + 13 local) | WARN |
| 7 | WhatsApp session | WARN (paired at AppData, but gateway down → non-functional) | LOW |
| 8 | Nous Portal refresh token | WARN (invalid; non-blocking — provider=custom OpenRouter) | LOW |
| 9 | AGENTS.md BOM / config injection | PASS (main absent; workspace copy UTF-8, no BOM) | — |
| 10 | Gateway crash loop | PASS (0 `asyncio.run.exception`; no ModuleNotFound) | — |
| 11 | Telegram topic 20 (delivery target) | **PASS** (verified live via getChat: supergroup + forum) | — |

---

## 1. Credential Exposure

### 1.1 Telegram bot token — **WARN (dual-root divergence, unchanged)**
- **Stale gateway root** `~/.hermes/.env` holds a revoked placeholder: direct `getMe` → **HTTP 404** (`Not Found`). Last rejection logged 10-06 (and 10-01): "token `827724...1UJE` … invalid or revoked". This is the stale token the old gateway root loads.
- **Live alternate root** `C:\Users\User\AppData\Local\hermes\.env` holds a **valid token**: `getMe` → `{"ok":true}`, bot `Ogaitchhermesbot` (id 8277244378). On-demand Bot API delivery remains functional via this token.
- **Recommendation:** remove/rotate the revoked placeholder in `~/.hermes/.env`; align delivery to the single valid AppData root.

### 1.2 Backup `.env` copies — **PASS (0, sustained)**
No `.env` copies in `~/.hermes/backups`, `state-snapshots`, `~/hermes-backup`, or `~/.openclaw` (maxdepth-limited). Sustained remediation.

### 1.3 `google_token.json` ACL — **PASS**
`icacls`: only `BUILTIN\Administrators:(I)(F)` and `User:(I)(F)`. No `Everyone`/`BUILTIN\Users`. Standard owner-only protection. Refreshed today (10-11 10:02), ACL unchanged and sound.

### 1.4 `.env`-reading delivery scripts — **FAIL (regression)**
30 workspace `.py` files reference/read `TELEGRAM_BOT_TOKEN` directly from `~/.hermes/.env` via `Path.home()/.hermes/.env` or `os.path.expanduser("~/.hermes/.env")`. This is a **regression** — as of 10-09/10-10 this count was 0 (only legit godmode red-teaming skill helpers matched). These leak tokens to process table, shell history, and logs. Notably they read the **stale revoked** root token, so they are also non-functional for delivery.
- **Active scripts** (workspace/scripts/): `ghana_telegram_report.py`, `h_evening_checkin_send.py`, `memory_review_telegram.py`, `mum_evening_checkin.py`, `send_ghana_report.py` — **highest priority, in the live delivery path.**
- **Dated vault artifacts** (family health check-ins, `tmp_*`, `_send_*`, `_token_test_*`, 2real-agent copy): one-off delivery helpers from past gateway-down periods. Recommend deletion.
- **Action:** audit these for still-scheduled use, then delete; replace any needed with Hermes-native env injection. Do NOT delete the godmode skill helpers (legit).

---

## 2. Channel Integrity

### 2.1 Gateway — **WARN (stopped)**
- `hermes status`: Gateway **✗ stopped** (manager: manual process).
- **No live gateway process:** the only `hermes...serve` python is the HTTP API (PID 14000); the two ESTABLISHED connections to Telegram (PID 10404) belong to the **desktop Telegram.exe**, not the gateway. `gateway.log` last entry **10-10 17:07** (warmup), no 10-11 entries; no `asyncio.run.exception` / crash signature. Gateway is idle/stopped, not crash-looping.

### 2.2 Telegram delivery — **PASS (via direct Bot API)**
The AppData root token is valid, so cron output reaches users via direct Bot API (Pattern A), independent of the stopped gateway. This cycle's summary will be delivered to topic 20.

### 2.3 WhatsApp — **WARN (paired but offline)**
`whatsapp/session/creds.json` present at **AppData** (3074 B, 10-10 10:20) = **paired**; config "✓ configured". Gateway is down, so the WhatsApp bridge is **non-functional until gateway restarts**.

### 2.4 Cron delivery targets — **WARN (27/57 silent)**
`jobs.json` (57 jobs) deliver distribution (via AppData root):
- Telegram topic/chat-targeted: **30** (`:14`×7, `:20`×6, `:4`×4, `:26`×2, `:16`×2, `:1`×2, `:10`×2, `:8`×1, `:28`×1, `:2`×1, plus `telegram:123286468`×2).
- Silent: **27/57 (47%)** — `origin`×14 + `local`×13. Persistent passive-loss pattern.
- This job (`security-policy-check`) delivers to `telegram:-1003784520976:20` ✓ target verified live.

---

## 3. Recent Security Events

### 3.1 Token rejection (10-01 / 10-06) — dual-root divergence, unchanged
`agent.log`/`errors.log`: Telegram gateway startup rejected token `827724...1UJE` (10-01 13:37, 10-06 11:12). Bot id matches the **valid** AppData bot — the rejected attempts used the **stale `~/.hermes` placeholder**, while the live AppData token stayed valid. No NEW `InvalidToken` in this audit window beyond those two dates.

### 3.2 Nous Portal — **WARN (invalid refresh token)**
`hermes status`: Portal "not logged in — Invalid refresh token". Non-blocking (provider=custom OpenRouter), but portal-managed token-expiry monitoring degraded.

### 3.3 `allow_all_users: true` — WARN (config)
Repeatedly logged today: `config.yaml allow_all_users: true grants every sender on every platform access`. Known LOW previously; persists. Recommend setting to `false` with an explicit allow-list.

### 3.4 Config health — PASS
No plaintext secrets in config; no BOM in AGENTS.md (main absent; workspace copy UTF-8 CRLF). Minor operational notes: `web_search` backend `ddgs` missing (uses one-shot keyless rescue); `2Real — Daily Operations Check` cron fails on missing skill `2real-enterprises-agent`.

---

## Trend vs 2026-10-10

| Item | 10-10 | 10-11 | Direction |
|------|-------|-------|-----------|
| Telegram token divergence | WARN | WARN | No Change |
| Backup `.env` copies | PASS (0) | PASS (0) | No Change |
| `.env`-reader scripts | PASS (0) | **FAIL (30)** | **Worsened** |
| Gateway | WARN (stopped) | WARN (stopped, no live proc) | No Change |
| Cron silent delivery | 27/57 | 27/57 | No Change |
| WhatsApp | WARN (offline, creds paired) | WARN (offline, creds paired) | No Change |
| Nous Portal | WARN | WARN | No Change |
| AGENTS.md BOM | PASS | PASS | No Change |
| Gateway crash loop | PASS | PASS | No Change |
| Topic 20 target | PASS | PASS | No Change |

**Persistent security debt (3+ cycles):** dual-root token divergence, gateway stopped, 27/57 silent cron, Nous Portal invalid.
**New regression this cycle:** 30 `.env`-reading delivery scripts (was 0). **No new CRITICALs.**

---

*Generated 2026-10-11 by Hermes security-audit cron.*