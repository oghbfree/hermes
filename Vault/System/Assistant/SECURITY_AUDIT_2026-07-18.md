# Security Audit — Internal System

**Date:** 2026-07-18
**Run by:** internal cron / Hermes Agent
**Overall:** FAIL

---

## Summary

- **CRITICAL:** Telegram bot token **revoked** (HTTP 404 on `getMe`, `InvalidToken` in rotated logs) — all Telegram delivery blocked
- **CRITICAL:** Gateway **DOWN** — fails to start due to WhatsApp config error (open policy without allow-all opt-in)
- **CRITICAL:** 18 workspace scripts read `.env` directly — credentials leak to process table, shell history, logs
- **CRITICAL:** Dual Hermes roots — `~/.hermes/.env` exists but `AppData/Local/hermes/.env` missing; `hermes doctor` reports `.env` missing
- **HIGH:** 5 backup `.env` copies in `~/.hermes/backups/` contain raw API keys (OpenRouter, Telegram, Google, Firecrawl, Brave, xAI)
- **HIGH:** WhatsApp unpaired 65+ days — `creds.json` missing
- **HIGH:** 11 cron jobs use `deliver: origin` or `deliver: local` — silent delivery failures
- **HIGH:** Persistent multi-service DNS failures (Telegram, OpenRouter) — host-level network issue

---

## Findings by Area

### 1. Credential Exposure

**Files checked:**
- `~/.hermes/.env` — EXISTS (contains `OPENROUTER_API_KEY`, `TELEGRAM_BOT_TOKEN`, etc.)
- `~/.hermes/config.yaml` — EXISTS (references `${VAR}` correctly)
- `~/.hermes/auth.json` — NOT FOUND
- `~/.hermes/google_token.json` — NOT FOUND

**Detected secrets in `.env` (masked):**
- `OPENROUTER_API_KEY=sk-or-...72c1`
- `TELEGRAM_BOT_TOKEN=8277244378:***`
- `GOOGLE_API_KEY=AIza...`
- `FIRECRAWL_API_KEY=fc-...`
- `BRAVE_API_KEY=...`
- `XAI_API_KEY=...`

**File permissions (Windows ACL):**
- `~/.hermes/.env`: PASS — Owner/SYSTEM/Administrators only
- `~/.hermes/google_token.json`: **NOT FOUND** (PASS — no file to audit)

**Backup `.env` copies (FAIL — 5 copies):**
| Path | Status |
|------|--------|
| `~/.hermes/backups/backup_20260716_230410/.env` | FAIL |
| `~/.hermes/backups/backup_20260717_230330/.env` | FAIL |
| `~/.hermes/backups/latest/.env` | FAIL |
| `~/.hermes/backups/latest_failed_20260717/.env` | FAIL |
| `~/.hermes/backups/latest_failed_20260717_2/.env` | FAIL |

**Workspace scripts reading `.env` directly (FAIL — 18 files):**
```
~/send_audit.py ~/send_audit_v2.py ~/send_health_check.py
~/workspace/scripts/ghana_telegram_report.py
~/workspace/send_cron_report.py ~/workspace/send_daily_report.py
~/workspace/send_evening_checkin.py ~/workspace/send_evening_health_check.py
~/workspace/send_health_summary.py ~/workspace/send_telegram_integrated_briefing.py
~/workspace/send_telegram_report.py ~/workspace/send_telegram_temp_briefing.py
~/check_bot.py ~/check_keys.py ~/check_recent_msg.py ~/check_telegram_bot.py
~/check_telegram_topic4.py ~/check_topic_history.py
```
*Each leaks tokens to process table, shell history, and logs.*

**Dual Hermes roots (FAIL):**
- Active `.env`: `C:\Users\User\.hermes\.env`
- `hermes doctor` reports: `~/AppData/Local/hermes/.env` **missing**
- Config drift risk: credentials may diverge between roots

**Verdict: FAIL**

---

### 2. Channel Integrity

**Telegram:**
- Bot token: **REVOKED** — `GET /bot<token>/getMe` → HTTP 404 `{"ok":false,"error_code":404,"description":"Not Found"}`
- `agent.log.1` shows repeated `InvalidToken: The token was rejected by the server` / `Not Found`
- Gateway shows "Connected to Telegram (polling mode)" but token invalid — **adapter connected ≠ token valid**
- Topic 20 exists in `channel_directory.json`: `Agent Hermes / topic 20` (ID: `-1003784520976:20`)

**WhatsApp:**
- Session missing: `~/.hermes/whatsapp/session/creds.json` NOT FOUND
- Unpaired 65+ days — non-functional channel

**Gateway:**
- **DOWN** — last start 2026-07-18 04:35:35, exited cleanly at 04:35:35
- Exit reason: `Refusing to start: whatsapp has dm_policy/group_policy set to 'open' but neither GATEWAY_ALLOW_ALL_USERS nor WHATSAPP_ALLOW_ALL_USERS is enabled`
- Crash history: 7 `ModuleNotFoundError: No module named 'concurrent_log_handler'` entries since 2026-06-22 (persistent crash loop)
- PID 16720 reported by `hermes status` but gateway log shows clean exit — **status vs reality mismatch**

**Cron delivery targets:**
| Delivery Type | Count | Status |
|---------------|-------|--------|
| `deliver: origin` | 8 | SILENT FAIL — output stays local |
| `deliver: local` | 3 | SILENT FAIL — output stays local |
| `deliver: telegram:...` | 25 | BLOCKED — token revoked + DNS failures |

**Verdict: FAIL**

---

### 3. Recent Security Events

| Event | Source | Severity | Notes |
|-------|--------|----------|-------|
| Telegram token revoked (HTTP 404, InvalidToken) | `agent.log.1`, direct API call | CRITICAL | Requires immediate rotation via @BotFather |
| Gateway crash loop (concurrent_log_handler) | `gateway-exit-diag.log` | HIGH | 7 crashes since 2026-06-22 |
| Multi-service DNS failures | `gateway.log`, cron errors | HIGH | Telegram + OpenRouter affected — host-level |
| OpenRouter rate limiting (429) | `agent.log` | WARN | Worker local total request limit reached |
| Config version drift (v26→v29) | `hermes doctor` | WARN | Migration pending |

**Verdict: FAIL**

---

## FAIL Items

| ID | Severity | Description | Evidence / Source |
|----|----------|-------------|-------------------|
| 1 | CRITICAL | Telegram bot token revoked | `getMe` → HTTP 404; `agent.log.1` InvalidToken |
| 2 | CRITICAL | Gateway DOWN — WhatsApp config blocks start | `gateway.log` 2026-07-18 04:35:35 |
| 3 | CRITICAL | 18 workspace scripts read `.env` directly | `grep -r "\.env\|dotenv" ~/.hermes/workspace/*.py` |
| 4 | CRITICAL | Dual Hermes roots — `.env` missing in AppData | `hermes doctor` reports `.env` missing |
| 5 | HIGH | 5 backup `.env` copies with raw secrets | `find ~/.hermes/backups -name ".env"` |
| 6 | HIGH | WhatsApp unpaired 65+ days | `~/.hermes/whatsapp/session/creds.json` missing |
| 7 | HIGH | 11 cron jobs silent delivery (`origin`/`local`) | `~/.hermes/cron/jobs.json` |
| 8 | HIGH | Persistent DNS failures (Telegram, OpenRouter) | `gateway.log`, cron `getaddrinfo failed` |
| 9 | WARN | OpenRouter 429 rate limiting | `agent.log` |
| 10 | WARN | Config version drift (v26→v29) | `hermes doctor` |

---

## Recommended Remediations

1. **URGENT:** Rotate Telegram bot token via @BotFather; update `~/.hermes/.env`
2. **URGENT:** Fix gateway startup — set `GATEWAY_ALLOW_ALL_USERS=1` or configure WhatsApp policies
3. **HIGH:** Delete all 18 workspace scripts reading `.env` directly; use Hermes credential injection
4. **HIGH:** Consolidate to single Hermes root; remove AppData/Local/hermes or migrate `.env`
5. **HIGH:** Delete 5 backup `.env` copies; use encrypted backup strategy
6. **HIGH:** Re-pair WhatsApp (scan QR) or disable WhatsApp in gateway config
7. **MEDIUM:** Update cron jobs — change `deliver: origin`/`local` to explicit Telegram topics
8. **MEDIUM:** Fix host DNS — flush DNS, check firewall, verify upstream connectivity
9. **MEDIUM:** Install `concurrent-log-handler` in Python 3.14 venv or migrate gateway to Python 3.11
10. **LOW:** Run `hermes doctor --fix` for config migration

---

## Attachments / Evidence

- `hermes status --all` / `hermes doctor` output
- `~/.hermes/.env` (secrets masked)
- `~/.hermes/cron/jobs.json` (delivery target analysis)
- `~/.hermes/logs/gateway-exit-diag.log` (crash signatures)
- `~/.hermes/logs/gateway.log` (DNS failures, token validity mismatch)
- `~/.hermes/logs/agent.log.1` (InvalidToken history)
- `~/.hermes/channel_directory.json` (Topic 20 confirmed)
- Direct Telegram API `getMe` call → HTTP 404

**Report saved:** `C:\Users\User\.hermes\workspace\Vault\System\Assistant\SECURITY_AUDIT_2026-07-18.md`

**Telegram delivery:** FAILED — token revoked (HTTP 404). Rotation required before any Telegram delivery can succeed.