# Security Audit — 2026-09-25

**Host:** Windows 11 · **Hermes profile:** default · **Run type:** cron (scheduled)
**Scope:** credential exposure · channel integrity · recent security events

---

## Summary of Findings

| # | Item | Status | Severity |
|---|------|--------|----------|
| 1 | Telegram bot token validity | **FAIL** | **CRITICAL** |
| 2 | Backup `.env` copies | PASS (0) | — |
| 3 | Workspace `.env`-reading scripts | **FAIL** (35) | WARN |
| 4 | `google_token.json` ACL | PASS | — |
| 5 | Gateway status / channel integrity | **FAIL** (down: telegram token rejected, whatsapp unpaired) | CRITICAL |
| 6 | Cron delivery targets | **FAIL** (26/56 non-topic; 30 topic-targeted blocked) | WARN |
| 7 | WhatsApp session | **FAIL** (unpaired) | WARN |
| 8 | Config syntax drift | WARN (shell_init_files, external_dirs quoted) | LOW |
| 9 | Provider auth events | PASS (no current multi-provider failure) | — |
| 10 | CRITICAL escalation | Telegram token revocation detected across 5+ consecutive audits | **CRITICAL** |

---

## 1. Credential Exposure

### 1.1 Telegram bot token — **FAIL / CRITICAL**
- Direct `getMe` validation: `{"ok":false,"error_code":404,"description":"Not Found"}` → **token is revoked/invalid**.
- Pattern in `gateway.log` and `agent.log` since 2026-08-22, recurring 08-22, 08-31, 09-05, 09-09, 09-15, 09-22:
  `Telegram bot token rejected: The token 827724...1UJE was rejected by the server.`
- Severity escalated (5+ consecutive cycles): **persistent credential compromise / revocation**. Requires rotation via @BotFather.
- **Blocking effect:** no Telegram delivery possible this cycle (all patterns gated on token validity).

### 1.2 Backup `.env` copies — **PASS**
- `~/.hermes/backups`: 0 · `~/.hermes/state-snapshots`: 0 · `~/hermes-backup`: 0 · `~/.openclaw`: 0.
- Full remediation of the long-standing backup `.env` finding.

### 1.3 Workspace `.env`-reading scripts — **FAIL / WARN**
- 35 scripts in `~/.hermes/workspace` (incl. `Vault/...`) match env-reading/open/dotenv/token patterns. Many are dated one-off delivery helpers (`tmp_*_send_*.py`, `morning_check_2026-*.py`, `evening_checkin_*.py`).
- `~/.hermes/*.py` root scripts present: `care_checkin.py`, `send_health_check.py`, `telegram_create_topic.py`, `telegram_direct_send.py`, `telegram_post_file.py`, `tmp_tg20_send.py` — these read `.env` directly.
- These leak tokens to process tables / shell history. Recommend deleting one-off helpers and centralizing the token read.

### 1.4 `google_token.json` ACL — **PASS**
- `icacls`: SYSTEM, Administrators, User all `(I)(F)` — no `Everyone`/`BUILTIN\Users`. Standard secure Windows default.

### 1.5 Config keys / auth providers — **WARN**
- Nous Portal: `Invalid refresh token` (not logged in). No Codex/xAI OAuth. Not blocking current run (provider = custom endpoint).
- Keys present: OpenRouter `sk-o...`, xAI `xai-...`, Firecrawl `fc-3...`. All masked.

---

## 2. Channel Integrity

### 2.1 Gateway — **FAIL / CRITICAL**
- Last `gateway.start`: 2026-09-22 13:52, PID 14988 (Python 3.14.3), exited code 78:
  - telegram: token rejected (revoked)
  - whatsapp: enabled but not paired
- **Not a crash-loop** (zero `asyncio.run.exception`/`ModuleNotFoundError` this window) — gateway exits cleanly due to non-retryable token conflict.
- `gateway.log` cold since 2026-09-22 13:52.

### 2.2 WhatsApp — **FAIL / WARN**
- `~/.hermes/whatsapp/session/creds.json` **missing** → configured but not paired. Persistent finding.

### 2.3 Cron delivery targets (jobs.json: 56 jobs) — **WARN**
- `telegram-topic`: 30 (BLOCKED — token revoked)
- `local`: 13
- `origin`: 13
- **26/56** jobs deliver to `local`/`origin` (never reach a user); **30** topic-targeted jobs cannot deliver while token is revoked.
- Current `security-policy-check` job targets `telegram:-1003784520976:20`.

### 2.4 DNS/provider health
- No simultaneous multi-provider network failure observed this cycle. Status connectivity baseline normal.

---

## 3. Recent Security Events

- **Telegram token revocation** — confirmed via direct API (HTTP 404). Recurring rejected-token events through 2026-09-22. **Treat as potential credential compromise; rotate immediately.**
- **2026-08-04 OpenRouter 401** (`Missing Authentication header`) — transient/older, single occurrence, not current.
- No unauthorized-access markers, no `InvalidToken` batch in rotated logs beyond gateway token rejection above.
- No `402`/`429` provider quota events in this window.

---

## 4. Trend / Same-day comparison

Previous audit: 2026-09-24. No same-day re-run.

| Finding | 09-24 | Trend |
|---------|-------|-------|
| Telegram token revoked | FAIL | **No Change (CRITICAL, 5+ cycles)** |
| Backup `.env` copies | PASS (0) | Improved (sustained remediation) |
| Workspace `.env` readers | FAIL | Not Remediated |
| WhatsApp unpaired | FAIL | No Change |
| Gateway down | FAIL | No Change |
| Config syntax drift | — | New WARN this cycle |

---

## 5. Recommendations

1. **Rotate Telegram token via @BotFather** and update `~/.hermes/.env` (highest priority; restores all Telegram delivery).
2. Delete one-off `tmp_*send*.py` / dated checkin scripts once no longer needed; consolidate token read into a single helper.
3. Re-pair WhatsApp session when next interactive window allows.
4. Fix config syntax: `hermes config set terminal.shell_init_files '[]'` and `skills.external_dirs '[...]'`.
5. Re-run audit after token rotation to confirm delivery restored.

---

*Report generated by Hermes security-audit skill (cron).*