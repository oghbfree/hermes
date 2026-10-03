# Security Audit — 2026-10-02

**Host:** Windows 11 · **Hermes profile:** default · **Run type:** cron (scheduled)
**Scope:** credential exposure · channel integrity · recent security events

---

## Summary of Findings

| # | Item | Status | Severity |
|---|------|--------|----------|
| 1 | Telegram bot token validity | **PASS** (valid — getMe ok) | — |
| 2 | Backup `.env` copies | PASS (0) | — |
| 3 | Workspace `.env`-reading scripts | **FAIL** (16 flagged) | WARN |
| 4 | `google_token.json` ACL | PASS | — |
| 5 | Gateway / channel integrity | **FAIL** (disconnected since 2026-10-01 13:26) | WARN |
| 6 | Cron delivery targets | **FAIL** (27/57 local/origin) | WARN |
| 7 | WhatsApp session | **WARN** (creds present, adapter disconnected) | WARN |
| 8 | Config `allow_all_users` | **FAIL** (true on 2 platforms) | WARN |
| 9 | Provider auth events | WARN (Nous Portal invalid refresh token) | LOW |

---

## 1. Credential Exposure

### 1.1 Telegram bot token — **PASS** (IMPROVED)
- Direct `getMe` validation (2026-10-02): `{"ok":true}` → **token valid** (46 chars, bot `Ogaitchhermesbot` / ID 8277244378).
- **Resolution of a CRITICAL finding** that persisted across 5+ audits (last confirmed revoked on 2026-09-22/09-25). Token now reads live and is accepted by Telegram.
- Primary token source verified at `C:\Users\User\AppData\Local\hermes\.env` (the live cron root). `~/.hermes/.env` is a stale secondary copy.

### 1.2 Backup `.env` copies — **PASS**
- `~/.hermes/backups`: 0 · `~/.hermes/state-snapshots`: 0 · `~/hermes-backup`: 0 · `~/.openclaw`: 0.
- Sustained full remediation. No duplicate `.env` anywhere outside the two live roots.

### 1.3 Workspace `.env`-reading scripts — **FAIL / WARN**
- 16 `.py` scripts across `~/.hermes/` and `~/.hermes/workspace/` reference secret token names or read `.env` directly: `send_health_check.py`, `telegram_create_topic.py`, `telegram_direct_send.py`, `telegram_post_file.py`, `tmp_tg20_send.py`, `workspace/scripts/ghana_telegram_report.py`, `h_evening_checkin_send.py`, `memory_review_telegram.py`, `mum_evening_checkin.py`, `send_ghana_report.py`, plus `workspace/tmp_send_*.py` one-offs.
- Reduced from 35 (09-25). Most are one-off delivery helpers that parse `TELEGRAM_BOT_TOKEN=` from `.env`. These leak tokens to process tables / shell history. Recommend deletion or consolidating token read into a single shared helper.
- No `test_*.py` credential probes found this cycle.

### 1.4 `google_token.json` ACL — **PASS**
- `icacls`: `NT AUTHORITY\SYSTEM:(I)(F)`, `BUILTIN\Administrators:(I)(F)`, `User:(I)(F)`. No `Everyone` / `BUILTIN\Users`. Standard secure Windows default. (Path: `C:\Users\User\.hermes\google_token.json`.)

### 1.5 Extended vendor validation
- Validated via `getMe` (authoritative): token accepted. No `bws_cache.json` / `.secret_cache` credential cache files present at either Hermes root.
- OpenRouter `sk-o...`, xAI `xai-...`, Firecrawl `fc-3...` keys present and masked.

---

## 2. Channel Integrity

### 2.1 Gateway / adapter state — **FAIL / WARN**
- `hermes status`: **gateway stopped**; `gateway_state.json` → both `telegram` and `whatsapp` state `disconnected` since **2026-10-01 13:26:25**.
- `gateway.log` last event: clean shutdown 2026-10-01 13:26 (SNT "Gateway stopped", `exit_clean`). Not a crash-loop this window (zero `asyncio.run.exception` / `ModuleNotFoundError` in recent logs).
- **Key nuance:** adapters are disconnected, but the **token itself is valid** — on-demand delivery (direct Bot API) remains possible even with the gateway process down.

### 2.2 WhatsApp — **WARN**
- `C:\Users\User\AppData\Local\hermes\whatsapp\session\creds.json` **present** (3,075 bytes, updated 2026-10-01 13:21) — session data exists, but the adapter is currently `disconnected`. Not paired-active at audit time.

### 2.3 Cron delivery targets (`jobs.json`: 57 jobs) — **FAIL / WARN**
- `telegram-topic`: 30 (topic-targeted, incl. 6 → topic 20, 7 → topic 14, 4 → topic 4)
- `local`: 13 · `origin`: 14 → **27/57 jobs (47%) deliver to `local`/`origin` and may never reach a user.**
- Current `security-policy-check` job targets `telegram:-1003784520976:20`. Delivery of this summary is independent of the gateway (direct API, token valid).

### 2.4 DNS / network health
- No simultaneous multi-provider network outage this cycle. Connectivity baseline normal.

---

## 3. Recent Security Events

- **Telegram token previously revoked → now VALID (resolution).** No `InvalidToken` / `401` / `403` / `404` token-rejection events in `agent.log`, `errors.log`, or `gateway.log` this window.
- **Config warning:** `allow_all_users: true` set on 2 platforms (config.yaml lines 596, 699) — every sender on those platforms is granted access. Flagged as WARN pending intent confirmation.
- **Nous Portal:** `Invalid refresh token` (not logged in) — not blocking (provider = custom OpenRouter endpoint).
- Repeated benign `tui_gateway.server` RPC warnings (`session-scoped RPC rejected ... detached/reaped runtime`) — operational noise, not a breach.
- No unauthorized-access markers, no provider quota (`402`/`429`) events this window.

---

## 4. Trend Comparison

Previous audit: **2026-09-25**. No same-day re-run.

| Finding | 09-25 | Trend (10-02) |
|---------|-------|---------------|
| Telegram token revoked | FAIL (CRITICAL) | **RESOLVED** — token valid |
| Backup `.env` copies | PASS (0) | Sustained PASS |
| Workspace `.env` readers | FAIL (35) | **Improved** (35 → 16) |
| WhatsApp session | FAIL (unpaired) | Improved (creds present; adapter disconnected) |
| Gateway down | FAIL (token rejected) | **Improved** (adapters down but token valid; no crash) |
| Config drift | WARN | New WARN (allow_all_users) |

---

## 5. Recommendations

1. **Rotate/confirm token provenance:** token is valid — ensure the live root (`AppData\Local\hermes\.env`) remains the authoritative token and the stale `~/.hermes/.env` copy does not drift.
2. Delete or consolidate the 16 one-off `.env`-reading delivery scripts into a single shared sender helper.
3. Re-run the gateway (`hermes gateway run`) to restore live Telegram/WhatsApp adapter connectivity — delivery currently depends on on-demand direct API.
4. Re-pair WhatsApp session at next interactive window if persistent inbound/outbound WhatsApp is needed.
5. Revisit `allow_all_users: true` → restrict platform to a known-user allowlist if the broad grant is not intentional.
6. Re-authenticate Nous Portal (keep it on refresh failure) to avoid future credential-drift cascade.

---

*Report generated by Hermes security-audit skill (cron).*
