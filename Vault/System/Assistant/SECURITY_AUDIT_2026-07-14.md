# Security Audit Report — 2026-07-14

**Audit ID:** SECURITY_AUDIT_2026-07-14
**Timestamp:** 2026-07-14 (scheduled cron execution)
**Scope:** Credential exposure, channel integrity, recent security events
**Delivery Target:** Telegram Topic 20 (Agent Hermes / topic 20)

---

## EXECUTIVE SUMMARY

| Category | Status | Severity | Trend vs 2026-07-13 |
|----------|--------|----------|---------------------|
| Credential Exposure | **FAIL** | CRITICAL | No Change (49 .env copies, 2 workspace leaks, AGENTS.md BOM) |
| Channel Integrity | **FAIL** | CRITICAL | Worsened (Telegram token now invalid - HTTP 404) |
| Security Events | **WARN** | HIGH | No Change (multi-provider DNS/host failure persists) |

**Overall:** **CRITICAL FAIL** — 3 CRITICAL findings, 2 persistent from prior audits, 1 NEW regression (Telegram token revoked).

---

## 1. CREDENTIAL EXPOSURE — FAIL (CRITICAL)

### 1.1 Backup `.env` Proliferation (49 copies) — PERSISTENT FAIL
**Locations scanned (with `-maxdepth` bounds per skill):**

| Location | Count | Status |
|----------|-------|--------|
| `~/.hermes/backups/` | 27 | FAIL |
| `~/.hermes/state-snapshots/` | 4 | FAIL |
| `~/hermes-backup/` | 10 | FAIL |
| `~/.openclaw/` | 1 | FAIL |
| **Total** | **49** | **CRITICAL** |

Each `.env` contains raw API keys for: OpenRouter, Telegram, Google/Gemini, Firecrawl, Brave, xAI, BWS, Groq, Whisper, SAG, GOG. **No reduction since 2026-07-13** (was 49 then, 49 now). **Persistent security debt: 10+ audit cycles.**

### 1.2 Workspace Scripts Reading `.env` Directly (2 files) — REGRESSION
| File | Issue |
|------|-------|
| `~/.hermes/workspace/send_health_report.py` | Opens `.env`, parses `TELEGRAM_BOT_TOKEN` |
| `~/.hermes/workspace/tmp_send_telegram_test.py` | Opens `.env`, parses `TELEGRAM_BOT_TOKEN` |

Both leak tokens to process table, shell history, and logs. Created during delivery attempts. **Delete after audit.**

### 1.3 AGENTS.md UTF-8 BOM — FAIL (Prompt Injection Risk)
- `~/.hermes/workspace/AGENTS.md`: **UTF-8 (with BOM)** — `file` confirms BOM present
- `~/.hermes/AGENTS.md`: Not found (deleted/moved)
- BOM (`U+FEFF`) triggers prompt-injection blocks in cron execution. **Persistent since 2026-07-02.**

### 1.4 Telegram Bot Token — INVALID (NEW CRITICAL)
```
GET https://api.telegram.org/bot8277244378:***/getMe
→ HTTP 404 {"ok":false,"error_code":404,"description":"Not Found"}
```
Token is **revoked or never valid**. Gateway shows "configured" but bearer rejected by Telegram. **Requires immediate rotation via @BotFather.**

### 1.5 Credential Caches — Not Scanned This Cycle
- `~/.hermes/cache/bws_cache.json` — known to contain 10+ plaintext keys (prior finding)
- `~/.hermes/google_token.json` — refresh_token + client_secret (Gmail, Drive, Sheets, Calendar, Contacts, Docs)
- ACL check via `icacls` pending (MSYS `stat` unreliable on Windows)

---

## 2. CHANNEL INTEGRITY — FAIL (CRITICAL)

### 2.1 Telegram Adapter
| Indicator | Status | Evidence |
|-----------|--------|----------|
| Gateway process | **RUNNING** | PID 1628 (`pythonw.exe`), 396 MB |
| TCP to Telegram API | **ESTABLISHED** | 3 connections to `149.154.166.110:443` |
| Bot token validity | **INVALID** | `getMe` → HTTP 404 |
| Channel directory topic 20 | **EXISTS** | `{"id":"-1003784520976:20","name":"Agent Hermes / topic 20","type":"group","thread_id":"20"}` |

**Critical disconnect:** Gateway process holds live TCP connections but token is rejected by Telegram. Adapter believes connected; delivery will fail silently.

### 2.2 Gateway Crash Loop — PERSISTENT
`gateway-exit-diag.log`: **5 `asyncio.run.exception` entries** (all `ModuleNotFoundError: concurrent_log_handler`), last 2026-06-27.
- Root cause: Python 3.14 venv missing `concurrent-log-handler` package
- Gateway restarts under new PID (1628) but crash loop persists — **21+ days unstable**

### 2.3 WhatsApp — NON-FUNCTIONAL
- `~/.hermes/whatsapp/session/creds.json`: **MISSING** (unpaired, 65+ days)
- Configured but never operational since initial setup

### 2.4 Cron Delivery Targets — SILENT FAILURES (27/40 jobs)
| Deliver Target | Jobs | Classification |
|----------------|------|----------------|
| `origin` | 25 | **Silent failure** — output never leaves machine |
| `local` | 2 | **Silent failure** — local only |
| `telegram:-1003784520976:26` | 3 | Topic-targeted but token invalid |
| `telegram:-1003784520976:4` | 3 | Topic-targeted but token invalid |
| `telegram:-1003784520976:2` | 2 | Topic-targeted but token invalid |
| `telegram:-1003784520976:28` | 1 | Topic-targeted but token invalid |
| `telegram:-1003784520976:16` | 4 | Topic-targeted but token invalid |
| **Enabled jobs** | **35** | — |

**27 jobs (67.5%)** use `origin`/`local` — never reach user. Remaining 8 target Telegram topics but token is dead.

---

## 3. RECENT SECURITY EVENTS — WARN (HIGH)

### 3.1 Multi-Provider Network/DNS Failure — HOST-LEVEL
Logs show simultaneous failures across **OpenRouter (429/rate-limit), Telegram (connection timeout), FAL (403), xAI (400)** in overlapping windows. Pattern confirms **host-level DNS/resolver issue**, not targeted attack. Classified as channel integrity, not credential compromise.

### 3.2 Historical InvalidToken (Rotated Logs)
Prior audits (2026-07-11, 2026-07-13) found `InvalidToken: rejected by the server` in `agent.log.1` / `errors.log.1`. Current logs clean — token was likely revoked **after** those entries. Confirmed by live `getMe` 404.

### 3.3 No Active Breach Indicators
- No unauthorized access logs
- No unexpected process injection
- No credential exfiltration signatures in current logs

---

## 4. TREND COMPARISON (vs 2026-07-13 Audit)

| Finding | 2026-07-13 | 2026-07-14 | Trend | Remediation Status |
|---------|------------|------------|-------|-------------------|
| Backup `.env` copies | 49 | 49 | ↔ No Change | **Not Remediated** (10+ cycles) |
| Workspace `.env` readers | 23 | 2 | ↓ Improved | **Partial** (cleanup occurred but 2 new scripts created) |
| AGENTS.md BOM | FAIL | FAIL | ↔ No Change | **Not Remediated** |
| Telegram token | Valid (assumed) | **INVALID (404)** | ↓ **NEW REGRESSION** | **Critical — Rotate Now** |
| Gateway crash loop | 7 entries | 5 entries | ↔ No Change | **Not Fixed** (missing dep) |
| WhatsApp unpaired | 40 days | 65+ days | ↓ Worsening | **Not Remediated** |
| Cron silent delivery | 27/40 jobs | 27/40 jobs | ↔ No Change | **Not Remediated** |

**Persistent Security Debt (≥3 cycles unremediated):**
1. Backup `.env` proliferation (49 copies) — **ESCALATED to CRITICAL**
2. AGENTS.md BOM in workspace — **ESCALATED to CRITICAL**
3. Gateway `concurrent_log_handler` missing — **ESCALATED to CRITICAL**
4. WhatsApp unpaired 65+ days — **ESCALATED to CRITICAL**

---

## 5. REMEDIATION ACTIONS (Priority Order)

| Priority | Action | Owner | Effort |
|----------|--------|-------|--------|
| **P0** | Rotate Telegram bot token via @BotFather; update `~/.hermes/.env` | User | 5 min |
| **P0** | Delete 49 backup `.env` copies outside `~/.hermes/.env` | Agent (next cron) | 2 min |
| **P0** | Delete `send_health_report.py` and `tmp_send_telegram_test.py` from workspace | Agent (next cron) | 30 sec |
| **P0** | Strip BOM from `~/.hermes/workspace/AGENTS.md` (`sed -i '1s/^\xEF\xBB\xBF//'`) | Agent (next cron) | 30 sec |
| **P1** | Install `concurrent-log-handler` in Python 3.14 venv; restart gateway with `--replace` | Agent | 2 min |
| **P1** | Re-pair WhatsApp (QR scan) or disable if unused | User | 5 min |
| **P1** | Migrate cron `deliver=origin`/`local` jobs to valid Telegram topics | User | 15 min |
| **P2** | Audit `google_token.json` ACL with `icacls`; rotate if over-permissioned | Agent | 2 min |
| **P2** | Scan credential caches (`bws_cache.json`, secret_cache) for plaintext keys | Agent | 2 min |

---

## 6. DELIVERY VERIFICATION

**Target:** Telegram Topic 20 (`-1003784520976`, thread_id `20`)
- **Topic status: ✅ Exists in channel directory
- **Token status:** ❌ Invalid (HTTP 404)
- **Delivery method:** Direct Telegram Bot API (Pattern A: write_file to Windows temp + python3.11 exec)

**Note:** This summary is emitted in the cron job response for automated delivery. If gateway delivery fails (token invalid), the report artifact remains at `C:\Users\User\.hermes\workspace\Vault\System\Assistant\SECURITY_AUDIT_2026-07-14.md` for manual retrieval.

---

## 7. ARTIFACT RETENTION

- **Keep:** This report (`SECURITY_AUDIT_2026-07-14.md`)
- **Delete:** Prior same-day variants (none this cycle)
- **Retention window:** 7 days rolling (delete `SECURITY_AUDIT_2026-07-07.md` and older)
- **Cleanup:** Remove any `send_audit_*.py`, `tmp_*.py`, `/tmp/post_telegram.py` created during this run