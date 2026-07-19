# Security Audit — Internal System

**Date:** 2026-07-18 (afternoon re-run)
**Run by:** internal cron / Hermes Agent
**Overall:** FAIL

---

## Summary (vs Morning Audit)

| Finding | Morning | Afternoon | Delta |
|---------|---------|-----------|-------|
| Telegram bot token | REVOKED (HTTP 404) | **REVOKED (HTTP 404)** | ↔ No change |
| Gateway status | DOWN (WhatsApp config) | **RUNNING** (PID 6116, TCP established) | ✅ IMPROVED |
| Gateway crash loop | 7 crashes since 2026-06-22 | **7 crashes (persistent)** | ↔ No change |
| WhatsApp session | MISSING (65+ days) | **MISSING (65+ days)** | ↔ No change |
| Backup `.env` copies | 5 in `~/.hermes/backups` | **16 total** (5 + 10 + 1) | ↔ No change |
| Workspace scripts reading `.env` | 18 | **20+** | ⚠️ WORSENED |
| Cron silent delivery (`origin`/`local`) | 11 | **11** | ↔ No change |
| DNS failures (multi-service) | Persistent | **Persistent** | ↔ No change |
| `google_token.json` | NOT FOUND | **EXISTS** (created 10:06, ACL OK) | ✅ NEW |
| Dual Hermes roots | FAIL | **FAIL** | ↔ No change |

**Net change:** Gateway recovered (new PID, Python 3.11 via uv), `google_token.json` appeared. Core credential/channel failures persist.

---

## Findings by Area

### 1. Credential Exposure

**Files checked:**
- `~/.hermes/.env` — EXISTS (contains `OPENROUTER_API_KEY`, `TELEGRAM_BOT_TOKEN`, `GOOGLE_API_KEY`, `FIRECRAWL_API_KEY`, `BRAVE_API_KEY`, `XAI_API_KEY`)
- `~/.hermes/config.yaml` — EXISTS (references `${VAR}` correctly)
- `~/.hermes/auth.json` — NOT FOUND
- `~/.hermes/google_token.json` — **EXISTS** (created 2026-07-18 10:06, 1870 bytes)

**Detected secrets in `.env` (masked):**
- `OPENROUTER_API_KEY=sk-or-...72c1`
- `TELEGRAM_BOT_TOKEN=8277244378:***`
- `GOOGLE_API_KEY=AIza...`
- `FIRECRAWL_API_KEY=fc-...`
- `BRAVE_API_KEY=...`
- `XAI_API_KEY=...`

**File permissions (Windows ACL):**
- `~/.hermes/.env`: PASS — Owner/SYSTEM/Administrators only
- `~/.hermes/google_token.json`: **PASS** — `icacls` shows Owner/SYSTEM/Administrators (F) only; no Everyone/Users entries

**Backup `.env` copies (FAIL — 16 copies across 3 trees):**

| Path | Count | Status |
|------|-------|--------|
| `~/.hermes/backups/backup_*/.env` | 5 | FAIL |
| `~/hermes-backup/*/.env` | 10 | FAIL |
| `~/.openclaw/.env` | 1 | FAIL |

*Each contains raw API keys for OpenRouter, Telegram, Google, Firecrawl, Brave, xAI — persistent security debt since 2026-07-01 (12+ audit cycles).*

**Workspace scripts reading `.env` directly (FAIL — 20+ files):**
```
~/send_audit.py ~/send_audit_v2.py ~/send_health_check.py
~/workspace/check_bot.py ~/workspace/check_keys.py ~/workspace/check_recent_msg.py
~/workspace/check_telegram_bot.py ~/workspace/check_telegram_topic4.py
~/workspace/check_topic_history.py ~/workspace/morning_checkin.py
~/workspace/send_cron_report.py ~/workspace/send_daily_report.py
~/workspace/send_evening_checkin.py ~/workspace/send_evening_health_check.py
~/workspace/send_health_summary.py ~/workspace/send_telegram_integrated_briefing.py
~/workspace/send_telegram_report.py ~/workspace/send_telegram_temp_briefing.py
~/workspace/temp_telegram_send.py ~/workspace/tg_evening_checkin.py
~/workspace/tg_robert_evening_checkin.py ~/workspace/tg_send.py
~/workspace/tg_send_ghana.py ~/workspace/tmp_send_briefing.py
```
*Each leaks tokens to process table, shell history, and logs. **Major regression** — was 0 in Jul 12–13 audits, 18 this morning, 20+ now.*

**Dual Hermes roots (FAIL):**
- Active `.env`: `C:\Users\User\.hermes\.env`
- `hermes doctor` reports: `~/AppData/Local/hermes/.env` **missing**
- Config drift risk: credentials may diverge between roots

**Verdict: FAIL**

---

### 2. Channel Integrity

**Telegram:**
- Bot token: **REVOKED** — `GET /bot8277244378:***/getMe` → HTTP 404 `{"ok":false,"error_code":404,"description":"Not Found"}`
- `agent.log.1` shows repeated `InvalidToken: The token was rejected by the server` / `Not Found`
- Gateway shows "Connected to Telegram (polling mode)" but token invalid — **adapter connected ≠ token valid**
- Topic 20 exists in `channel_directory.json`: `Agent Hermes / topic 20` (ID: `-1003784520976:20`) — **PASS**

**WhatsApp:**
- Session missing: `~/.hermes/whatsapp/session/creds.json` NOT FOUND
- Unpaired 65+ days — non-functional channel

**Gateway:**
- **RUNNING** — PID 6116 (Python 3.11 via uv), ESTABLISHED TCP to `149.154.166.110:443` (Telegram)
- Previous starts (04:35, 10:00, 11:43) exited cleanly due to WhatsApp config: `Refusing to start: whatsapp has dm_policy/group_policy set to 'open' but neither GATEWAY_ALLOW_ALL_USERS nor WHATSAPP_ALLOW_ALL_USERS is enabled`
- Crash history: 7 `ModuleNotFoundError: No module named 'concurrent_log_handler'` entries since 2026-06-22 (Python 3.14 venv) — **persistent crash loop**
- PID mismatch: `hermes status` reported PID 6116; `gateway-exit-diag.log` last `gateway.start` was PID 8220 (10:43) — **status vs reality mismatch resolved** (new process replaced old)

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
| Gateway crash loop (`concurrent_log_handler`) | `gateway-exit-diag.log` | HIGH | 7 crashes since 2026-06-22 |
| Multi-service DNS failures | `gateway.log`, cron errors | HIGH | Telegram + OpenRouter affected — host-level |
| OpenRouter rate limiting (429) | `agent.log` | WARN | Worker local total request limit reached |
| Config version drift (v26→v29) | `hermes doctor` | WARN | Migration pending |
| `google_token.json` created | `ls -la` | INFO | Appeared 2026-07-18 10:06; ACL verified OK |

**Verdict: FAIL**

---

## FAIL Items (Prioritized)

| ID | Severity | Description | Evidence / Source |
|----|----------|-------------|-------------------|
| 1 | CRITICAL | Telegram bot token revoked | `getMe` → HTTP 404; `agent.log.1` InvalidToken |
| 2 | CRITICAL | 20+ workspace scripts read `.env` directly | `grep -r "\.env\|dotenv" ~/.hermes/workspace/*.py` |
| 3 | CRITICAL | Dual Hermes roots — `.env` missing in AppData | `hermes doctor` reports `.env` missing |
| 4 | HIGH | 16 backup `.env` copies with raw secrets | `find` across 3 backup trees |
| 5 | HIGH | WhatsApp unpaired 65+ days | `~/.hermes/whatsapp/session/creds.json` missing |
| 6 | HIGH | 11 cron jobs silent delivery (`origin`/`local`) | `~/.hermes/cron/jobs.json` |
| 7 | HIGH | Persistent DNS failures (Telegram, OpenRouter) | `gateway.log`, cron `getaddrinfo failed` |
| 8 | HIGH | Gateway crash loop (`concurrent_log_handler`) | 7 entries in `gateway-exit-diag.log` |
| 9 | WARN | OpenRouter 429 rate limiting | `agent.log` |
| 10 | WARN | Config version drift (v26→v29) | `hermes doctor` |

---

## Recommended Remediations

1. **URGENT:** Rotate Telegram bot token via @BotFather; update `~/.hermes/.env`
2. **URGENT:** Delete all 20+ workspace scripts reading `.env` directly; use Hermes credential injection
3. **HIGH:** Fix gateway crash loop — `pip install concurrent-log-handler` in Python 3.14 venv OR migrate gateway to Python 3.11 (current working PID)
4. **HIGH:** Consolidate to single Hermes root; remove AppData/Local/hermes or migrate `.env`
5. **HIGH:** Delete 16 backup `.env` copies; implement encrypted backup strategy
6. **HIGH:** Re-pair WhatsApp (scan QR) or disable WhatsApp in gateway config
7. **MEDIUM:** Update cron jobs — change `deliver: origin`/`local` to explicit Telegram topics
8. **MEDIUM:** Fix host DNS — flush DNS, check firewall, verify upstream connectivity
9. **MEDIUM:** Run `hermes doctor --fix` for config migration
10. **LOW:** Monitor `google_token.json` rotation; verify scopes on next refresh

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

**Report saved:** `C:\Users\User\.hermes\workspace\Vault\System\Assistant\SECURITY_AUDIT_2026-07-18-afternoon.md`

**Telegram delivery:** FAILED — token revoked (HTTP 404). Rotation required before any Telegram delivery can succeed.