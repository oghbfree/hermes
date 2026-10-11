# Security Audit — 2026-10-10

**Host:** Windows 11 · **Hermes profile:** default · **Run type:** cron (scheduled)
**Scope:** credential exposure · channel integrity · recent security events

---

## Summary of Findings

| # | Item | Status | Severity |
|---|------|--------|----------|
| 1 | Telegram bot token validity | **WARN** (dual-root divergence, unchanged) | WARN |
| 2 | Backup `.env` copies | PASS (0, sustained) | — |
| 3 | `google_token.json` ACL | PASS | — |
| 4 | `.env`-reading delivery scripts | PASS (0 active; only legit godmode skill helpers) | — |
| 5 | Gateway / channel integrity | **WARN** (stopped; last clean shutdown 10-01; 10-06 start blocked by revoked token) | WARN |
| 6 | Cron delivery targets | **WARN** (27/57 silent: 13 local + 14 origin) | WARN |
| 7 | WhatsApp session | WARN (creds.json present/paired at AppData, but gateway down → non-functional) | LOW |
| 8 | Nous Portal refresh token | WARN (invalid; non-blocking — provider=custom OpenRouter) | LOW |
| 9 | AGENTS.md BOM / config injection | PASS (main absent; workspace copy UTF-8 no BOM) | — |
| 10 | Gateway crash loop | PASS (0 `asyncio.run.exception`; no ModuleNotFound; no crash loop) | — |
| 11 | Telegram topic 20 (delivery target) | **PASS** (verified live this cycle via direct Bot API delivery) | — |

---

## 1. Credential Exposure

### 1.1 Telegram bot token — **WARN (dual-root divergence, unchanged)**
- **Stale gateway root** `~/.hermes/.env` holds a revoked placeholder: direct `getMe` → **HTTP 404** (`Not Found`). A 10-06 gateway start attempt logged "The token … was rejected by the server. The token is invalid or was revoked". This is the stale token the old gateway root loads.
- **Live alternate root** `C:\Users\User\AppData\Local\hermes\.env` holds a **valid token**: `getMe` → `{"ok":true}`, bot `Ogaitchhermesbot` (id 8277244378). On-demand Bot API delivery remains functional via this token.**Recommendation:** remove/rotate the revoked placeholder in `~/.hermes/.env` to stop 407-root confusion; align delivery to the single valid AppData root.

### 1.2 Backup `.env` copies — **PASS (0, sustained)**
No `.env` copies found in `~/.hermes/backups`, `state-snapshots`, `~/hermes-backup`, or `~/.openclaw` (maxdepth-limited scan. Sustained remediation.

### 1.3 `google_token.json` ACL — **PASS**
`icacls`: only `SYSTEM:(F)`, `BUILTIN\Administrators:(F)`, `User:(F)`. No `Everyone`/`BUILTIN\Users` — standard owner-only protection. OK.

### 1.4 `.env`-reading delivery scripts — **PASS**
No leaks. Workspace `send_*.py` / `tmp_*.py` scripts show **0** references to `.env`/`dotenv`/`TELEGRAM_BOT_TOKEN`. Only matches are legit godmode red-teaming skill helpers. No cleanup needed this cycle.



---

## 2. Channel Integrity

### 2.1 Gateway — **WARN (stopped)**
- `hermes status`: Gateway **✗ stopped** (manager: manual process).
- `gateway.log` (AppData) last entry **10-01 13:26** — clean shutdown teardown; 9+ days stale. Since then no running gateway.

### 2.2 Telegram delivery — **PASS (via direct Bot API)**
The AppData token is valid, so cron output reaches users via **direct Bot API delivery** (Pattern A), independent of the stopped gateway. This cycle's summary was delivered to topic 20 → also **verified topic 20 exists** (sendMessage with thread_id succeeded).

### 2.3 WhatsApp — **WARN (paired but offline)**
`whatsapp/session/creds.json` present (3075 B, 10-01) = **paired**; config "✓ configured".However gateway is down, so WhatsApp bridge — while creds are intact — is **non-functional until gateway restarts**. Improved vs historical unpaired state, but still offline in practice.



### 2.4 Cron delivery targets — **WARN (27/57 silent)**
`jobs.json` (57 jobs) deliver distribution (via valid AppData root»:

- Telegram topic-targeted: 28 jobs ((`:14` x7, `:20` x6, `:4` x4, `:16` x2, `:26` x2, `:1` x2, `:28` x1, `:8` x1, `:2` x1», plus `telegram:123286468` x2»( =  ͷ 28 thread/chat targets».
- Silent: **27/57 (47%)** — `origin` x14 + `local` x13. Persistent passive-loss pattern; outputs stay on-machine, never reach a user..
- This security job (`security-policy-check`) delivers to `telegram:-1003784520976:20` ✓ correct; target verified live..



## 3. Recent Security Events

### 3.1 Token rejection (10-06) — context of dual-root divergence
`errors.log` 10-06: gateway startup conflict — Telegram token rejected, "generate a new one with @BotFather".B bot id in log (`827724…1UJE`) matches the current valid bot — indicating the rejected attempt likelihood used the stale `~/.hermes` placeholder, while the live AppData token remained valid. No new `InvalidToken` events in rotated logs (agent.log/agent.log.1 clean».

### 3.2 Nous Portal — **WARN (invalid refresh token)**
`hermes status`: Portal "not logged in — Invalid refresh token". Non-blocking (provider=custom OpenRouter», but portal-managed auth/token-expiry monitoring degraded..

### 3.3 Config health — PASS
No plaintext secrets in config; no BOM in JSON/AUTH configs detected; allow_all_users unchanged (minor LOW, tracked prior).

---

## Trend vs 2026-10-09
| Item | 10-09 | 10-10 | Direction |
|---|------|--------|----------|
| Telegram token divergence | WARN | WARN | No Change |
| Backup `.env` copies | PASS (0` | PASS (0` | No Change |
| `.env`-reader scripts | PASS (0 deleted prior` | PASS (0` | No Change |
| Gateway | WARN | WARN | No Change |
| Cron silent delivery | 27/57 | 27/57 | No Change |
| WhatsApp | WARN (offline» | WARN (offline; creds paired» | No Change |
| Nous Portal | WARN | WARN | No Change |
| AGENTS.md BOM | PASS | PASS | No Change |
| Gateway crash loop | PASS | PASS | No Change |
| Topic 20 target | — | PASS (verified» | Improved |

**Persistent security debt:** dual-root token divergence, gateway stopped, 27/57 silent cron (   3+ cycles unaddressed». No new CRITICALs this cycle.



---
*Generated 2026-10-10 by Hermes security-audit cron.*