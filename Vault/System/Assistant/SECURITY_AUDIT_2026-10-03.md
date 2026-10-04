# Security Audit — 2026-10-03

**Host:** Windows 11 · **Hermes profile:** default · **Run type:** cron (scheduled)
**Scope:** credential exposure · channel integrity · recent security events

---

## Summary of Findings

| # | Item | Status | Severity |
|---|------|--------|----------|
| 1 | Telegram bot token validity | **WARN** (live AppData root VALID; stale `~/.hermes/.env` copy holds revoked placeholder — divergence) | WARN |
| 2 | Backup `.env` copies | PASS (0) | — |
| 3 | Workspace `.env`-reading scripts | **FAIL** (33 script refs, worsening) | WARN |
| 4 | `google_token.json` ACL | PASS | — |
| 5 | Gateway / channel integrity | **FAIL** (stopped; loads stale revoked token) | WARN |
| 6 | Cron delivery targets | **FAIL** (27/57 local/origin) | WARN |
| 7 | WhatsApp session | **FAIL** (not paired) | WARN |
| 8 | Config `allow_all_users` | **FAIL** (true on 2 platforms) | WARN |
| 9 | Provider auth events | WARN (Nous Portal invalid refresh token) | LOW |

---

## 1. Credential Exposure

### 1.1 Telegram bot token — **WARN (dual-root divergence)**
- **Live cron root** `C:\Users\User\AppData\Local\hermes\.env` holds a **valid 46-char token**: direct `getMe` → `{"ok":true}` (bot `Ogaitchhermesbot`, ID 8277244378).
- **Stale secondary root** `~/.hermes/.env` holds a **13-char revoked placeholder** (`827724..…1UJE`): `getMe` → HTTP 404. **This is the token the gateway loads**, so live gateway startup fails with "token rejected by the server."
- **Key nuance (regression vs 10-02):** 10-02 audit read the token from the AppData root (valid). The divergence between the two `.env` files means whichever root the gateway/status path reads determines connectivity. The live token is valid — on-demand Bot API delivery remains possible — but the gateway process is pinned to a stale, revoked credential copy.
- **Resolution of CRITICAL finding:** Prior audits (09-22 → 09-25) flagged total revocation as CRITICAL. A valid token now exists at the live root; the blocked state is a **credential divergence** (stale placeholder at `~/.hermes/.env`), not total loss.

### 1.2 Backup `.env` copies — **PASS**
- `~/.hermes/backups`: 0 · `~/.hermes/state-snapshots`: 0 · `~/hermes-backup`: 0 · `~/.openclaw`: 0.
- Sustained full remediation. No duplicate `.env` outside the two live roots.

### 1.3 Workspace `.env`-reading scripts — **FAIL / WARN (worsening)**
- **33** `.py` files under `~/.hermes/workspace` reference `TELEGRAM_BOT_TOKEN`; plus root one-offs (`care_checkin.py`, `send_health_check.py`, `telegram_create_topic.py`, `telegram_direct_send.py`, `telegram_post_file.py`, `tmp_tg20_send.py`).
- Regressed from 16 (10-02) → 33 today. Many are dated one-off delivery helpers (`tmp_*send_*.py`, `evening_checkin_2026-*.py`) parsing the token directly from `.env`. These leak tokens to process tables / shell history.
- Note: several token-referencing files are the audit's own support scripts / legitimate dtype references; the actionable set is the dated one-off senders.

### 1.4 `google_token.json` ACL — **PASS**
- `icacls`: `NT AUTHORITY\SYSTEM:(I)(F)`, `BUILTIN\Administrators:(I)(F)`, `User:(I)(F)` — no `Everyone` / `BUILTIN\Users`. Secure Windows default.

### 1.5 Extended validation
- No `bws_cache.json` / `.secret_cache` credential cache files at either root.
- OpenRouter `sk-o…`, xAI `xai-…`, Firecrawl `fc-3…` keys present and masked. `AGENTS.md`: main `~/.hermes/AGENTS.md` **absent**; workspace copy is plain UTF-8 (no BOM, no zero-width/RTL chars) — clean.

---

## 2. Channel Integrity

### 2.1 Gateway / adapter state — **FAIL / WARN**
- `hermes status`: **gateway stopped** (Manager: manual process). `gateway.log` last event: clean `exit_clean` on **2026-10-01 13:37**, cause — **non-retryable startup conflict**: telegram token rejected (stale placeholder) + whatsapp not paired.
- Not a crash-loop (zero `asyncio.run.exception` / `ModuleNotFoundError` this window). `gateway-exit-diag.log` last entries are clean `code 78` token-conflict exits (2026-09-15, 09-22, 10-01).
- Adaptors are down purely because the gateway reads the stale revoked token. Restoring gateway = align the live token to the loaded root and re-run `hermes gateway run`.

### 2.2 WhatsApp — **FAIL / WARN**
- `creds.json` **missing/misconfigured** at both `platforms/whatsapp/session/` and `whatsapp/session/` — enabled but not paired. Persistent finding.

### 2.3 Cron delivery targets (`jobs.json`: 57 jobs) — **FAIL / WARN**
- `telegram-topic`: 30 (topic-targeted, incl. → topic 20) · `local`: 13 · `origin`: 14 → **27/57 jobs (47%) deliver to `local`/`origin` and may never reach a user.** Matches prior cycle.
- Current `security-policy-check` job targets `telegram:-1003784520976:20`. Delivery of this summary uses the **live valid** token via direct Bot API.

### 2.4 DNS / network health
- No simultaneous multi-provider outage this cycle. Connectivity baseline normal.

---

## 3. Recent Security Events

- **Telegram token: live root valid (getMe ok); stale `~/.hermes/.env` holds revoked placeholder** → gateway startup repeatedly rejects the stale token (08-22, 08-31, 09-05, 09-09, 09-15, 09-22, 10-01 pattern). Not a fresh compromise — a divergence the gateway path is reading the wrong root.
- **Config warning:** `allow_all_users: true` on 2 platforms (config.yaml) — every sender granted access. WARN pending intent confirmation.
- **Nous Portal:** `Invalid refresh token` (not logged in) — non-blocking (provider = custom OpenRouter endpoint).
- Repeated benign `tui_gateway.server` RPC / `agent.auxiliary_client` PAID-lane / `model_metadata` context-length warnings — operational noise, not a breach.
- **SQLite** WAL-reset warning on `state.db` (3.50.4 < 3.51.3) — upgrade recommended, not a security breach.
- No unauthorized-access markers, no unauthorized `402`/`429` provider quota events this window.

---

## 4. Trend Comparison

Previous audit: **2026-10-02**. No same-day re-run.

| Finding | 10-02 | Trend (10-03) |
|---------|-------|---------------|
| Telegram token | PASS (valid, live root) | **WARN** — token valid at live AppData root, but stale `~/.hermes/.env` holds revoked placeholder (new divergence) |
| Backup `.env` copies | PASS (0) | Sustained PASS |
| Workspace `.env` readers | FAIL (16) | **Worse** (16 → 33) |
| WhatsApp session | WARN (creds present) | **Worse** (creds missing / unpaired) |
| Gateway down | FAIL (adapters down, token valid) | FAIL (stopped, reads stale revoked token) |
| Cron silent delivery | FAIL (27/57) | No Change (27/57) |

---

## 5. Recommendations

1. **Align the Telegram token to one authoritative root (highest priority).** The live 46-char valid token exists at `AppData\Local\hermes\.env`; replace the revoked 13-char placeholder in `~/.hermes/.env` (or ensure the gateway loads the AppData root). This restores live gateway + topic delivery.
2. Re-run the gateway (`hermes gateway run`) after token alignment to restore live adapters (telegram + whatsapp).
3. Delete or consolidate the 33 dated one-off `.env`-reading delivery scripts into a single shared sender helper.
4. Re-pair WhatsApp session at next interactive window.
5. Revisit `allow_all_users: true` → restrict to a known-user allowlist if not intentional.
6. Upgrade SQLite embedded runtime (`hermes update`) to clear the WAL-reset warning; re-authenticate Nous Portal on refresh failure.

---

*Report generated by Hermes security-audit skill (cron).*