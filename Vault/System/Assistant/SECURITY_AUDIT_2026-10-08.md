# Security Audit — 2026-10-08

**Host:** Windows 11 · **Hermes profile:** default · **Run type:** cron (scheduled)
**Scope:** credential exposure · channel integrity · recent security events

---

## Summary of Findings

| # | Item | Status | Severity |
|---|------|--------|----------|
| 1 | Telegram bot token validity | **WARN** (live AppData root VALID via getMe; stale `~/.hermes/.env` holds 13-char revoked placeholder, HTTP 404) | WARN |
| 2 | Backup `.env` copies | PASS (0, sustained) | — |
| 3 | `google_token.json` ACL | PASS | — |
| 4 | `.env`-reading delivery scripts | **WARN** (3 workspace `tmp_send_*` + 5 root one-offs) | LOW |
| 5 | Gateway / channel integrity | **FAIL→WARN** (stopped; last start 10-06 reloads revoked token) | WARN |
| 6 | Cron delivery targets | **FAIL** (27/57 silent: 13 local + 14 origin) | WARN |
| 7 | WhatsApp session | WARN (creds.json present at AppData but gateway down → non-functional) | LOW |
| 8 | Config `allow_all_users` | **FAIL** (true on 2 platforms, unchanged) | WARN |
| 9 | Config health | PASS (v46, no deprecated keys) | — |

---

## 1. Credential Exposure

### 1.1 Telegram bot token — **WARN (dual-root divergence, unchanged)**
- **Live cron root** `C:\Users\User\AppData\Local\hermes\.env` holds a **valid 46-char token**: direct `getMe` → `{"ok":true}` (bot ID 8277244378).
- **Stale secondary root** `~/.hermes/.env` holds a **13-char revoked placeholder** (`827724…1UJE`): `getMe` → HTTP 404. **This is the token the gateway loads**, so live gateway startup fails ("token rejected by the server").
- Both `.env` roots still exist simultaneously (AppData, 01 Oct; `~/.hermes` 1030B, 22 Aug). Not a fresh compromise — persistent credential divergence where the gateway reads the wrong (revoked) root. On-demand Bot API delivery remains functional via the valid AppData token.

### 1.2 Backup `.env` copies — **PASS (sustained)**
- `~/.hermes/backups` 0 · `~/.hermes/state-snapshots` 0 · `~/hermes-backup` 0 · `~/.openclaw` 0. No `.env` outside the two live roots. Sustained improvement (was 40–57 in early Sept).

### 1.3 `google_token.json` ACL — **PASS**
- `icacls`: `NT AUTHORITY\SYSTEM:(I)(F)`, `BUILTIN\Administrators:(I)(F)`, `User:(I)(F)` — no `Everyone` / `BUILTIN\Users`. Secure Windows default.

### 1.4 `.env`-reading delivery helper scripts — **WARN**
- **5 root one-offs** reference `.env`: `care_checkin.py`, `send_health_check.py`, `telegram_create_topic.py`, `telegram_direct_send.py`, `telegram_post_file.py`, `tmp_tg20_send.py`.
- **3 workspace** `tmp_send_*.py` parse the token directly (tmp_send_afternoon_health.py, tmp_send_evening_checkin_0809.py, tmp_send_evening_checkin_1209.py).
- These are dated one-off delivery helpers that read the token from `.env`, leaking it to process tables / shell history. No credential in plaintext in the report.

### 1.5 Extended validation
- No `bws_cache.json` / `.secret_cache` credential cache files at either root.
- `AGENTS.md`: main `~/.hermes/AGENTS.md` **absent**; workspace copy plain UTF-8, CRLF (no BOM, no zero-width/RTL) — clean.

---

## 2. Channel Integrity

### 2.1 Gateway / adapter state — **FAIL→WARN (unchanged root cause)**
- `hermes status`: **Gateway Service: ✗ stopped** (manager: manual). No gateway process running.
- `gateway.log` / `errors.log` last gateway attempt **2026-10-06 11:12:42** — Telegram connect rejected: token `827724…1UJE` rejected by the server. Last `gateway.start` PID 18048 (10-06).
- Not a crash loop (zero `asyncio.run.exception` / `ModuleNotFoundError`); the **credential-root conflict** blocks every start.
- Restore = align valid token into the loaded root, then `hermes gateway run --replace`.

### 2.2 WhatsApp — **WARN**
- `C:\...\AppData\Local\hermes\whatsapp\session\creds.json` present (4864B), but gateway is down → session non-functional. `~/.hermes` root creds.json missing.

### 2.3 Cron delivery targets (`jobs.json`: 57 jobs, AppData root) — **FAIL / WARN (unchanged)**
- `telegram:<chat>` targeted: 30 (incl. 6 → topic 20, 7 → topic 14). `local`: 13 · `origin`: 14 → **27/57 jobs (47%) deliver to `local`/`origin` and may never reach a user.** Unchanged from 10-05.
- `security-policy-check` job targets `telegram:-1003784520976:20`. **Topic 20 independently confirmed to EXIST** in `channel_directory.json` (`-1003784520976:20`, "Agent Hermes / topic 20"). Topic-addressed delivery will succeed once the gateway holds a valid token.

### 2.4 DNS / network health
- No simultaneous multi-provider outage. Baseline normal.

---

## 3. Recent Security Events

- **Telegram token divergence persists** — live root valid (getMe ok), stale root revoked placeholder driving repeated gateway startup failures (09-15, 09-22, 10-01, 10-06). No fresh compromise; a persistent config-root conflict.
- **`allow_all_users: true`** on 2 platforms (AppData config.yaml lines 598, 701) — every sender granted access. Unchanged; WARN pending intent confirmation.
- **Duplicate credential across profiles** (reported 10-05: content-buddy/harold/sat-nav share default's TELEGRAM_BOT_TOKEN) — not re-flagged by this cycle's profilation check; carry-forward open.
- **Nous Portal:** `Invalid refresh token`, not logged in — non-blocking (provider = custom OpenRouter endpoint).
- **SQLite WAL-reset warning:** linked SQLite 3.50.4 vulnerable to the WAL-reset corruption bug (37× this session); recommend `hermes update` to ≥3.51.3. LOW.
- No unauthorized-access / breach markers, no unauthorized quota events. Rotated logs clean of Telegram InvalidToken.

---

## 4. Trend Comparison

Previous audit: **2026-10-05**. No same-day re-run.

| Finding | 10-05 | Trend (10-08) |
|---------|-------|---------------|
| Telegram token | WARN (dual-root divergence) | No Change (valid live, stale placeholder) |
| Backup `.env` copies | PASS (0) | Sustained PASS |
| Workspace `.env` readers | FAIL (35 refs) | Improved (3 `tmp_send_*` + 5 root; broad-count methodology narrower this cycle) |
| Google token ACL | PASS | Sustained PASS |
| Gateway down | FAIL (stopped, stale token) | No Change (stopped, 10-06 rejected) |
| Cron silent delivery | FAIL (27/57) | No Change (27/57) |
| WhatsApp session | partial pair | No Change (down w/ gateway) |
| `allow_all_users: true` | FAIL (2 platforms) | No Change |
| Duplicate-profile credential | NEW (3 profiles) | Carry-forward (inconclusive this cycle) |

**Persistent security debt** (3+ consecutive cycles, unchanged): dual-root token divergence, gateway down, cron silent delivery 27/57, `allow_all_users: true`.

---

## 5. Recommendations

1. **Align the Telegram token to one authoritative root (highest priority).** Copy the valid token from `AppData\Local\hermes\.env` into `~/.hermes/.env` (and all profiles) and delete the stale revoked placeholder. Restores live gateway + all topic delivery.
2. Re-run the gateway (`hermes gateway run --replace`) after token alignment.
3. Consolidate/delete the 5 root + 3 workspace one-off `.env`-reading delivery scripts into one shared sender helper.
4. Revisit `allow_all_users: true` → restrict to a known-user allowlist if not intentional.
5. Resolve the duplicate-profile Telegram credential via `profile_routes` / `hermes gateway migrate --multiplex`.
6. Run `hermes update` to remediate the SQLite WAL-reset vulnerability warning.

---

*Report generated by Hermes security-audit skill (cron).*
