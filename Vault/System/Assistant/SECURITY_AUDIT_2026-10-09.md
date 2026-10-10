# Security Audit — 2026-10-09

**Host:** Windows 11 · **Hermes profile:** default · **Run type:** cron (scheduled)
**Scope:** credential exposure · channel integrity · recent security events

---

## Summary of Findings

| # | Item | Status | Severity |
|---|------|--------|----------|
| 1 | Telegram bot token validity | **WARN** (dual-root divergence, unchanged) | WARN |
| 2 | Backup `.env` copies | PASS (0, sustained) | — |
| 3 | `google_token.json` ACL | PASS | — |
| 4 | `.env`-reading delivery scripts | **IMPROVED→PASS** (8 deleted this cycle; 0 active) | — |
| 5 | Gateway / channel integrity | **FAIL→WARN** (stopped; last start 10-06 loads revoked token) | WARN |
| 6 | Cron delivery targets | **FAIL** (27/57 silent: 13 local + 14 origin) | WARN |
| 7 | WhatsApp session | WARN (creds present at AppData but gateway down → non-functional) | LOW |
| 8 | Config `allow_all_users` | WARN (true on 2 platforms, unchanged) | LOW |
| 9 | Config health | PASS (v46, no plaintext secrets) | — |
| 10 | Gateway crash loop | **IMPROVED→PASS** (0 asyncio/ModuleNotFound); no crash loop signal | — |
| 11 | Nous Portal refresh token | WARN (invalid; non-blocking, provider = custom OpenRouter) | LOW |

---

## 1. Credential Exposure

### 1.1 Telegram bot token — **WARN (dual-root divergence, unchanged)**
- **Stale gateway root** `~/.hermes/.env` holds a **13-char revoked placeholder** (`827724…1UJE`): direct `getMe` → **HTTP 404**. **This is the token the gateway loads**, so every gateway start fails ("token rejected by the server").
- **Live alternate root** `C:\Users\User\AppData\Local\hermes\.env` holds a **valid 46-char token**: `getMe` → `{"ok":true}`, bot `Ogaitchhermesbot`. On-demand Bot API delivery remains functional via this token.

### 1.2 Backup `.env` copies — **PASS (sustained)**
- `~/.hermes/backups` 0 · `~/.hermes/state-snapshots` 0 · `~/hermes-backup` 0 · `~/.openclaw` 0.No `.env` outside the two live roots. Sustained improvement (was 40–57 in early Sept).

### 1.3 `google_token.json` ACL — **PASS**
- `icacls`: `SYSTEM:(I)(F)`, `BUILTIN\Administrators:(I)(F)`, `User:(I)(F)` — no `Everyone` / `BUILTIN\Users`. Secure Windows default.


### 1.4 `.env`-reading delivery scripts — **IMPROVED→PASS (cleaned this cycle)**
- Deleted **8** one-off token-reading helpers this cycle:
  - Root: `send_health_check.py`, `telegram_create_topic.py`, `telegram_direct_send.py`, `telegram_post_file.py`, `tmp_tg20_send.py` (+ `tmp_tg20_summary.txt`)
  - Workspace: `tmp_send_afternoon_health.py`, `tmp_send_evening_checkin_0809.py`, `tmp_send_evening_checkin_1209.py`
- Verified: **0 active `.env`-readers remain** in `~/.hermes/` or `~/.hermes/workspace/`. `tmp_send_evening_h.py` reads a cache file (not `.env`); `care_checkin.py` is an empty 0-byte placeholder — neither leaks. Regression resolved vs 10-08 (8 present).


### 1.5 Extended validation
- No `bws_cache.json` / `.secret_cache` credential caches at either rootstate.

- `AGENTS.md`: main `~/.hermes/AGENTS.md` **absent**; workspace copy plain UTF-8, CRLF (no BOM, no zero-width/RTL) — clean.

---

## 2. Channel Integrity

### 2.1 Gateway / adapter state — **FAIL→WARN (unchanged root cause)**
- `hermes status`: **Gateway Service: ✗ stopped** (manager: manual.) No gateway process running.
- Last gateway attempt **2026-10-06 11:12:42** — Telegram connect rejected: `827724…1UJE` rejected by the server (gateway log spanning 09-09 →  .10-06).. Last `gateway.start` PID  .18048 (10-06..
- **Not a crash loop** — zero `asyncio.run.exception` / `ModuleNotFoundError` this cycle (the earlier `concurrent_log_handler` crash is resolved.) The **credential-root conflict** blocks every start.
- Restore = align the valid 46-char token into `~/.hermes/.env` (authoritative root), then `hermes gateway run --replace`.

### 2.2 WhatsApp — **WARN**
- `C:\...\AppData\Local\hermes\platforms\whatsapp\session\creds.json` present (4864B, Jul  .19) but gateway is down → session non-functional. `~/.hermes` root creds missing.. Once gateway restarts with aligned root, re-evaluate IR session validity.



###  ..3 Cron delivery targets (`jobs.json`:  .57 jobs, AppData root) — **FAIL / WARN (unchanged)**
- `telegram:<chat>` targeted:  .30 (incl. 6 → topic 20, 7 → topic  .14). `local`:  .13 · `origin`:  .14 → **27/57 jobs (47%) deliver to `local`/`origin`** and may never reach a user. Unchanged from 10-08.
- **Topic 20 independently confirmed to EXIST** in `channel_directory.json` (`-1003784520976:20`, "Agent Hermes / topic 20"). Topic-addressed delivery succeeds once the gateway holds the valid token (or via direct API with the valid AppData token.


###  ..4 DNS / network health
- No simultaneous multi-provider outage. Baseline normal.


---

##  ..3. Recent Security Events

- **Telegram token divergence persists** — live AppData root valid (getMe ok,); stale gateway root revoked placeholder driving repeated gateway startup failures ( 09-15,  .09-22,  .10-01,  .10-06). No fresh compromise;a persistent config-root conflict.

- **No new breach markers** this cycle: no Unauthorized/InvalidToken rejections on the valid token, no new quota events, no malicious file writes found.



- **Nous Portal:** `Invalid refresh token`, not logged in — non-blocking (provider = custom OpenRouter endpoint.
.

- **`allow_all_users: true`** on 2 platforms (AppData config.yaml lines 598,,  .701) — every sender granted access. Unchanged; WARN pending intent confirmation.



- No SQLite / config BOM issues this cycle. Config version v46, all `api_key:` fields empty (secrets resolved via `${VAR}` from `.env`) — no plaintext secrets in config.yaml.

---

##  ..4. Trend Comparison

Previous audit: **2026-10-08**. No same-day re-run.



| Finding | 10-08 | Trend (10-09) |
|---------|-------|---------------|
| Telegram token | WARN (dual-root divergence) | No Change (valid AppData, revoked gateway root) |
| Backup `.env` copies | PASS (0) | Sustained PASS |
| `.env`-reading delivery scripts | FAIL (8) | **Improved→PASS (0; 8 deleted this cycle)** |
| Google token ACL | PASS | Sustained PASS |
| Gateway down | FAIL (stopped, 10-06 rejected) | No Change (stopped, blocked by token) |
| Gateway crash loop | PASS | Sustained PASS (0 crash signals) |
| Cron silent delivery | FAIL (27/57) | No Change (27/57) |
| WhatsApp session | WARN (down w/ gateway) | No Change |
| `allow_all_users: true` | WARN (2 platforms) | No Change |
| Config health | PASS (v46) | Sustained PASS (no plaintext secrets) |

**Persistent security debt** (3+ consecutive cycles, unchanged): dual-root token divergence, gateway down, cron silent delivery 27/57, `allow_all_users: true`, WhatsApp non-functional.


---

## 5. Recommendations

1. **Align the Telegram token to one authoritative root (highest priority).** Copy the valid 46-char token from `AppData\Local\hermes\.env` into `~/.hermes\.env` (and all profiles) and delete the stale revoked placeholder. Restores live gateway + all topic delivery.
2. **Re-run the gateway** (`hermes gateway run --replace`) after token alignment. Verify `Connected to Telegram (polling mode)` in `gateway.log` and a running PID with ESTABLISHED TCP to Telegram.
3. **Consolidate the dual `.env` roots** (`~/.hermes` and `AppData\Local\hermes`) to a single authoritative location to prevent future credential divergence. Re-pair the WhatsApp IR session (`creds.json` dated Jul 19 may be stale) once the gateway restarts.
4. Revisit `allow_all_users: true` (2 platforms) — restrict to a known-user allowlist if not intentional.
5. Re-route the  .27/57 `local`/`origin` cron targets via topic-routing as part of config consolidation.

---

*Report generated by Hermes security-audit skill (cron.* Data: creds scan, gateway logs, jobs.json, channel_directory.json, direct getMe token validation.*