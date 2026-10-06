# Security Audit — 2026-10-05

**Host:** Windows 11 · **Hermes profile:** default · **Run type:** cron (scheduled)
**Scope:** credential exposure · channel integrity · recent security events

---

## Summary of Findings

| # | Item | Status | Severity |
|---|------|--------|----------|
| 1 | Telegram bot token validity | **WARN** (live AppData root VALID via getMe; stale `~/.hermes/.env` holds 13-char revoked placeholder, HTTP 404) | WARN |
| 2 | Backup `.env` copies | PASS (0) | — |
| 3 | Workspace `.env`-reading scripts | **FAIL** (35 refs, +2 vs 10-04) | WARN |
| 4 | `google_token.json` ACL | PASS | — |
| 5 | Gateway / channel integrity | **FAIL** (no process running; last log 10-01, startup_failed code 78) | WARN |
| 6 | Cron delivery targets | **FAIL** (27/57 silent: 13 local + 14 origin) | WARN |
| 7 | WhatsApp session | **FAIL→WARN improvement** (creds.json present 3075B but `registered: False` — partial pair only) | WARN |
| 8 | Config `allow_all_users` | **FAIL** (true on 2 platforms) | WARN |
| 9 | Duplicate platform credential across profiles | **FAIL** (NEW — content-buddy/harold/sat-nav share default's TELEGRAM_BOT_TOKEN) | WARN |
| 10 | Provider auth events | WARN (Nous Portal invalid refresh token; recurring mcp.vercel.com 401 this cycle) | LOW |

---

## 1. Credential Exposure

### 1.1 Telegram bot token — **WARN (dual-root divergence, unchanged)**
- **Live cron root** `C:\Users\User\AppData\Local\hermes\.env` holds a **valid 46-char token**: direct `getMe` → `{"ok":true}` (bot `Hermes` / `@Ogaitchhermesbot`, ID 8277244378).
- **Stale secondary root** `~/.hermes/.env` holds a **13-char revoked placeholder** (`827724…1UJE`): `getMe` → HTTP 404. **This is the token the gateway loads**, so live gateway startup fails ("token rejected by the server").
- Both `.env` roots still exist simultaneously (AppData 552B, 01 Oct; `~/.hermes` 1030B, 22 Aug). Not a fresh compromise — persistent credential divergence where the gateway reads the wrong (revoked) root. On-demand Bot API delivery remains fully functional via the valid AppData token (probe to topic 20 succeeded, msg_id 11719).

### 1.2 Backup `.env` copies — **PASS (sustained)**
- `~/.hermes/backups` 0 · `~/.hermes/state-snapshots` 0 · `~/hermes-backup` 0 · `~/.openclaw` 0. No `.env` outside the two live roots.

### 1.3 Workspace `.env`-reading scripts — **FAIL / WARN (worsened)**
- **35** `.py` files under `~/.hermes/workspace` reference `TELEGRAM_BOT_TOKEN` / `open(…env)` / `dotenv` (was 33 on 10-04, +2). Plus 6 root one-offs: `care_checkin.py`, `send_health_check.py`, `telegram_create_topic.py`, `telegram_direct_send.py`, `telegram_post_file.py`, `tmp_tg20_send.py` — all dated delivery helpers that parse the token directly from `.env`, leaking tokens to process tables / shell history.

### 1.4 `google_token.json` ACL — **PASS**
- `icacls`: `NT AUTHORITY\SYSTEM:(I)(F)`, `BUILTIN\Administrators:(I)(F)`, `User:(I)(F)` — no `Everyone` / `BUILTIN\Users`. Secure Windows default.

### 1.5 Extended validation
- No `bws_cache.json` / `.secret_cache` credential cache files at either root.
- `AGENTS.md`: main `~/.hermes/AGENTS.md` **absent**; workspace copy plain UTF-8 (no BOM, no zero-width/RTL) — clean.

---

## 2. Channel Integrity

### 2.1 Gateway / adapter state — **FAIL / WARN (untouched)**
- `hermes status` plus process check: **no gateway process running** (only browser_harness and Hermes app PIDs). `gateway.log` last event 2026-10-01 13:26. `gateway-exit-diag.log` shows repeated code-78 `SystemExit` (09-15, 09-22, **10-01**, last PID 13436) — cause: **telegram token rejected (stale placeholder) + whatsapp not paired**. Zero `asyncio.run.exception` / `ModuleNotFoundError` → not a crash loop, a credential-root conflict.
- Restore = align the valid token into the loaded root, then `hermes gateway run --replace`.

### 2.2 WhatsApp — **FAIL→WARN (improvement)**
- `C:\...\AppData\Local\hermes\whatsapp\session\creds.json` now **present (3075B)** with `me id 233204252252:71@s.whatsapp.net`, but **`registered: False`** — a partial pairing only; session non-functional while gateway is down. App-state-sync keys dated 01 Oct.

### 2.3 Cron delivery targets (`jobs.json`: 57 jobs, AppData root) — **FAIL / WARN (unchanged)**
- `telegram:<chat>` targeted: 30 (incl. 6 → topic 20). `local`: 13 · `origin`: 14 → **27/57 jobs (47%) deliver to `local`/`origin` and may never reach a user.** Unchanged from 10-04.
- `security-policy-check` job targets `telegram:-1003784520976:20`. **Topic 20 independently verified to EXIST this cycle** (Bot API sendMessage probe → msg_id 11719), so topic-addressed delivery will succeed once the gateway gets a valid token.

### 2.4 DNS / network health
- No simultaneous multi-provider outage. Baseline normal.

---

## 3. Recent Security Events

- **Telegram token divergence persists** — live root valid (getMe ok), stale root revoked placeholder driving repeated gateway startup failures (09-15, 09-22, 10-01). No fresh compromise.
- **Duplicate platform credential across profiles (NEW):** `hermes doctor` flags default↔content-buddy, default↔harold, default↔sat-nav all holding the **same** `TELEGRAM_BOT_TOKEN`. One token can serve only one gateway → the higher-priority profile claims it, the others' adapters park. Prefer `profile_routes` in default's config, or issue per-profile bot tokens. `taiwah` profile correctly has none.
- **`allow_all_users: true`** on 2 platforms (config.yaml lines 596, 699) — every sender granted access. WARN pending intent confirmation.
- **Nous Portal:** `Invalid refresh token`, not logged in — non-blocking (provider = custom OpenRouter endpoint).
- **mcp.vercel.com 401 Unauthorized** repeated throughout this cycle (06:38→07:05) — Vercel MCP server rejecting an unconfigured/expired token. Non-gateway, non-Telegram; WARN (unconfigured MCP integration).
- No unauthorized-access / breach markers, no unauthorized quota events. Rotated logs (agent.log.1 / errors.log.1) clean of InvalidToken/Unauthorized for Telegram.

---

## 4. Trend Comparison

Previous audit: **2026-10-04**. No same-day re-run.

| Finding | 10-04 | Trend (10-05) |
|---------|-------|---------------|
| Telegram token | WARN (dual-root divergence) | No Change (valid live, stale placeholder) |
| Backup `.env` copies | PASS (0) | Sustained PASS |
| Workspace `.env` readers | FAIL (33) | **Worsened (35)** |
| WhatsApp session | FAIL (unpaired/missing) | **Improved (creds present, partial pair)** |
| Gateway down | FAIL (stopped, stale token) | No Change (stopped, code 78) |
| Cron silent delivery | FAIL (27/57) | No Change (27/57) |
| `allow_all_users: true` | FAIL (2 platforms) | No Change |
| Duplicate-profile credential | — | **NEW (3 profiles)** |

**Persistent security debt** (3+ consecutive cycles, unchanged): dual-root token divergence, workspace env-reader scripts (now 35), gateway down, cron silent delivery 27/57, `allow_all_users: true`. **New this cycle:** duplicate Telegram credential across 3 profiles.

---

## 5. Recommendations

1. **Align the Telegram token to one authoritative root (highest priority).** Copy the valid 46-char token from `AppData\Local\hermes\.env` into `~/.hermes/.env` (and all profiles) and delete the stale 13-char revoked placeholder. Restores live gateway + all topic delivery.
2. Re-run the gateway (`hermes gateway run --replace`) after token alignment.
3. **Resolve the duplicate-profile credential** via `profile_routes` in default's config (or per-profile bot tokens) — run `hermes gateway migrate --multiplex`.
4. Consolidate the 35 workspace + 6 root `.env`-reading delivery scripts into one shared sender helper; delete dated one-offs.
5. Complete WhatsApp pairing (creds present but `registered: False`) at next interactive window.
6. Revisit `allow_all_users: true` → restrict to a known-user allowlist if not intentional.
7. Configure/rotate the Vercel MCP token to clear the recurring 401s.

---

*Report generated by Hermes security-audit skill (cron).*