# Security Audit — 2026-10-04

**Host:** Windows 11 · **Hermes profile:** default · **Run type:** cron (scheduled)
**Scope:** credential exposure · channel integrity · recent security events

---

## Summary of Findings

| # | Item | Status | Severity |
|---|------|--------|----------|
| 1 | Telegram bot token validity | **WARN** (live AppData root VALID; stale `~/.hermes/.env` holds revoked placeholder) | WARN |
| 2 | Backup `.env` copies | PASS (0) | — |
| 3 | Workspace `.env`-reading scripts | **FAIL** (33 refs + 6 root one-offs, unchanged) | WARN |
| 4 | `google_token.json` ACL | PASS | — |
| 5 | Gateway / channel integrity | **FAIL** (stopped; reads stale revoked token, code 78) | WARN |
| 6 | Cron delivery targets | **FAIL** (27/57 silent) | WARN |
| 7 | WhatsApp session | **FAIL** (not paired) | WARN |
| 8 | Config `allow_all_users` | **FAIL** (true on 2 platforms) | WARN |
| 9 | Provider auth events | WARN (Nous Portal invalid refresh token) | LOW |

---

## 1. Credential Exposure

### 1.1 Telegram bot token — **WARN (dual-root divergence, unchanged)**
- **Live cron root** `C:\Users\User\AppData\Local\hermes\.env` holds a **valid 46-char token**: direct `getMe` → `{"ok":true}` (bot `Ogaitchhermesbot`, ID 8277244378).
- **Stale secondary root** `~/.hermes/.env` holds a **13-char revoked placeholder** (`827724..…1UJE`): `getMe` → HTTP 404. **This is the token the gateway loads**, so live gateway startup fails with "token rejected by the server."
- Both `.env` roots exist simultaneously (AppData 552B, 01 Oct; `~/.hermes` 1030B, 22 Aug). The divergence means whichever root the gateway path reads determines connectivity. The live token is valid — on-demand Bot API delivery remains possible — but the gateway process is pinned to a stale, revoked credential copy.
- Not a new compromise — a persistent credential divergence (read of the wrong root).

### 1.2 Backup `.env` copies — **PASS**
- `~/.hermes/backups`: 0 · `~/.hermes/state-snapshots`: 0 · `~/hermes-backup`: 0 · `~/.openclaw`: 0.
- Sustained full remediation. No `.env` outside the two live roots.

### 1.3 Workspace `.env`-reading scripts — **FAIL / WARN (unchanged, persistent debt)**
- **33** `.py` files under `~/.hermes/workspace` reference `TELEGRAM_BOT_TOKEN`; plus 6 root one-offs (`care_checkin.py`, `send_health_check.py`, `telegram_create_topic.py`, `telegram_direct_send.py`, `telegram_post_file.py`, `tmp_tg20_send.py`).
- Same count as 10-03 (33). These dated one-off delivery helpers parse the token directly from `.env`, leaking tokens to process tables / shell history.

### 1.4 `google_token.json` ACL — **PASS**
- `icacls`: `NT AUTHORITY\SYSTEM:(I)(F)`, `BUILTIN\Administrators:(I)(F)`, `User:(I)(F)` — no `Everyone` / `BUILTIN\Users`. Secure Windows default.

### 1.5 Extended validation
- No `bws_cache.json` / `.secret_cache` credential cache files at either root.
- OpenRouter `sk-o…`, xAI `xai-…`, Firecrawl `fc-3…` keys present and masked in status.
- `AGENTS.md`: main `~/.hermes/AGENTS.md` **absent**; workspace copy is plain UTF-8 (no BOM, no zero-width/RTL) — clean.

---

## 2. Channel Integrity

### 2.1 Gateway / adapter state — **FAIL / WARN**
- `hermes status`: **gateway stopped** (Manager: manual process). `gateway.log` last event: clean `exit_clean` on **2026-10-01 13:37**, cause — **non-retryable startup conflict**: telegram token rejected (stale placeholder) + whatsapp not paired. `gateway-exit-diag.log` confirms code-78 `SystemExit` exits (09-15, 09-22, 10-01), last start 10-01 PID 13436.
- Not a crash-loop (zero `asyncio.run.exception` / `ModuleNotFoundError` this window). Adapters are down purely because the gateway reads the stale revoked token.
- Restore = align the live token into the loaded root, then `hermes gateway run`.

### 2.2 WhatsApp — **FAIL / WARN**
- `creds.json` **missing/unpaired** at both `platforms/whatsapp/session/` and `whatsapp/session/`. Persistent finding.

### 2.3 Cron delivery targets (`jobs.json`: 57 jobs, AppData root) — **FAIL / WARN**
- `telegram:<chat>`: 30 (topic-targeted, incl. 6 → topic 20) · `local`: 13 · `origin`: 14 → **27/57 jobs (47%) deliver to `local`/`origin` and may never reach a user.** Unchanged from prior cycle.
- `security-policy-check` job targets `telegram:-1003784520976:20`. Quota targets: topic 20 (6), 14 (7), 4 (4), 26 (2), 16 (2), 1 (2), 10 (2) etc.

### 2.4 DNS / network health
- No simultaneous multi-provider outage this cycle. Baseline normal.

---

## 3. Recent Security Events

- **Telegram token: live root valid (getMe ok); stale `~/.hermes/.env` holds revoked placeholder** → repeated gateway startup rejects of the stale token (09-15, 09-22, 10-01 pattern). No fresh compromise — a divergence where the gateway loads the wrong root.
- **Config warning:** `allow_all_users: true` on 2 platforms (config.yaml lines 596, 699) — every sender granted access. WARN pending intent confirmation.
- **Nous Portal:** `Invalid refresh token`, not logged in — non-blocking (provider = custom OpenRouter endpoint).
- No unauthorized-access or breach markers, no unauthorized `402`/`429` provider quota events this window. No `InvalidToken`/`Unauthorized` in rotated logs (agent.log.1 / errors.log.1 clean).

---

## 4. Trend Comparison

Previous audit: **2026-10-03**. No same-day re-run.

| Finding | 10-03 | Trend (10-04) |
|---------|-------|---------------|
| Telegram token | WARN (dual-root divergence) | No Change (valid live, stale placeholder) |
| Backup `.env` copies | PASS (0) | Sustained PASS |
| Workspace `.env` readers | FAIL (33) | No Change (33) |
| WhatsApp session | FAIL (unpaired) | No Change (unpaired) |
| Gateway down | FAIL (stopped, stale token) | No Change (stopped, code 78) |
| Cron silent delivery | FAIL (27/57) | No Change (27/57) |

**Persistent security debt** (3+ consecutive cycles, unchanged): dual-root token divergence, workspace env-reader scripts (33), gateway down, WhatsApp unpaired, cron silent delivery 27/57, `allow_all_users: true`.

---

## 5. Recommendations

1. **Align the Telegram token to one authoritative root (highest priority).** Copy the valid 46-char token from `AppData\Local\hermes\.env` into `~/.hermes/.env` and delete the stale 13-char revoked placeholder. Restores live gateway + all topic delivery.
2. Re-run the gateway (`hermes gateway run --replace`) after token alignment to restore live adapters (telegram + whatsapp).
3. Consolidate the 33 workspace + 6 root `.env`-reading delivery scripts into one shared sender helper and delete dated one-offs.
4. Re-pair WhatsApp session at next interactive window.
5. Revisit `allow_all_users: true` → restrict to a known-user allowlist if not intentional.
6. Re-authenticate Nous Portal on next refresh failure (provider already on custom OpenRouter endpoint).

---

*Report generated by Hermes security-audit skill (cron).*