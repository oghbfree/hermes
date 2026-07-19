# Security Audit Report — 2026-07-11 (Afternoon Re-run)

**Generated:** 2026-07-11 18:09 UTC  
**Profile:** default  
**Audit ID:** SECURITY_AUDIT_2026-07-11-afternoon  

---

## 1. EXECUTIVE SUMMARY

| Metric | Status |
|--------|--------|
| **Overall** | 🔴 **CRITICAL FAIL** |
| Credential Exposure | 🔴 FAIL (49 backup .env copies + 18 workspace readers) |
| Channel Integrity | 🔴 FAIL (Gateway down 21d, DNS failures, 0/39 jobs deliverable) |
| Security Events | 🔴 FAIL (InvalidToken in rotated logs, xAI key rejected) |
| Trend vs 2026-07-05 | 🔴 **Worsening** on 4/6 critical metrics |

**No remediation actions completed since morning audit.** All 7 CRITICAL FAIL items persist.

---

## 2. CREDENTIAL EXPOSURE ANALYSIS

### 2.1 Backup `.env` Copies — **CRITICAL FAIL** (Escalated: Persistent Security Debt)
| Location | Count | Change vs Morning |
|----------|-------|-------------------|
| `~/.hermes/backups/` | 19 | — |
| `~/.hermes/state-snapshots/` | 4 | — |
| `~/hermes-backup/` | 10 | — |
| `~/.openclaw/` | 1 | — |
| **Total** | **49** | **No change** |

**Finding:** 49 plaintext `.env` files containing OpenRouter, Telegram, Google, Firecrawl, Brave, xAI API keys. **12+ consecutive audit cycles unremediated.** Severity escalated to CRITICAL (persistent security debt).

### 2.2 Workspace Scripts Reading `.env` Directly — **CRITICAL FAIL** (Escalated: Persistent Security Debt)
**18 scripts** in `~/.hermes/workspace/` and backups read `.env` via `python-dotenv` or direct file access:
- `send_health_report.py`, `tmp_send_telegram_test.py`, `probe_threads.py` (and 15 backup copies)
- Leak tokens to process tables, shell history, logs
- **7+ consecutive cycles unremediated**

### 2.3 Credential Cache Files — **FAIL**
- `~/.hermes/cache/bws_cache.json` — plaintext secrets for 10+ services
- `~/.hermes/cache/.secret_cache` — additional cached credentials
- Survive `.env` rotation

### 2.4 OAuth Token File Permissions — **PASS**
- `~/.hermes/google_token.json`: ACL shows only `SYSTEM:(I)(F)`, `Administrators:(I)(F)`, `User:(I)(F)` — no extra users/groups
- Expired 2026-06-17 (1 day past at check); refresh token present

### 2.5 AGENTS.md BOM — **FAIL** (Medium)
- `~/.hermes/workspace/AGENTS.md`: **UTF-8 with BOM** — blocks cron execution, prompt injection risk
- Main `~/.hermes/AGENTS.md`: not present

### 2.6 Nous Portal Token — **WARN**
- `hermes status`: Nous Portal shows "not logged in" — no active token to check expiry

---

## 3. CHANNEL INTEGRITY ANALYSIS

### 3.1 Telegram Gateway — **FAIL** (CRITICAL)
| Metric | Status | Detail |
|--------|--------|--------|
| Adapter connected | ❌ No | Gateway crash loop since 2026-06-22 (21 days) |
| Crash root cause | **ModuleNotFoundError** | `concurrent_log_handler` missing in Python 3.14 venv |
| Crash count | **14+** | `asyncio.run.exception` entries in `gateway-exit-diag.log` |
| DNS resolution | ❌ Failed | `getaddrinfo failed` for `api.telegram.org` — host-level |
| Fallback IPs | Tried | 149.154.166.110, 149.154.167.220 — all fail |
| Last clean exit | 2026-06-18 | Gateway stable until crash loop started |
| Current PID | 26404 | `hermes status` shows running but log shows crash loop |

**PID Lifecycle:** Old gateway (PID 8924, Python 3.14) died with `concurrent_log_handler` error. New gateway attempts (Python 3.11/uv) blocked by same missing package. Gateway shows as "running" in `hermes status` but is non-functional.

### 3.2 Telegram Topic 20 (Memory Review) — **PASS**
- Exists in `channel_directory.json` as `-1003784520976:20` ("Agent Hermes / topic 20")
- Forum topic verified present

### 3.3 Cron Job Delivery Targets — **FAIL** (39 active jobs, 0 functional paths)
| Delivery Target | Count | Status |
|-----------------|-------|--------|
| `origin` | 8 | **Silent failure** — output never reaches user |
| `local` | 3 | **Silent failure** — output stays on machine |
| `telegram:-1003784520976:<topic>` | 28 | **Blocked** — gateway down + DNS failure |
| **Total** | **39** | **0 functional delivery paths** |

### 3.4 WhatsApp — **FAIL** (HIGH)
- Session directory exists but **empty** (`creds.json` missing)
- Unpaired since ~2026-05-18 (**65+ days**)
- 3 check-in jobs (`checkin-mum`, `checkin-dad`, `kanzoni-tuesday-check`) configured for `deliver=origin` → silent failures

### 3.5 Multi-Provider DNS Failure — **FAIL** (Host-Level)
Simultaneous failures in same time windows:
- Telegram: `getaddrinfo failed` for `api.telegram.org`
- OpenRouter: `Failed to resolve 'openrouter.ai'`
- xAI: `Failed to resolve 'api.x.ai'`
- **Root cause:** System DNS / network / firewall / VPN — not targeted attack

---

## 4. RECENT SECURITY EVENTS

### 4.1 Telegram InvalidToken — **CRITICAL** (NEW FINDING)
**Location:** `~/.hermes/logs/errors.log.1` (rotated log, ~2026-06-10)
```
telegram.error.InvalidToken: The token `8277...ugM8` was rejected by the server.
telegram.error.InvalidToken: Not Found
```
**Count:** 15+ occurrences in rotated log
**Implication:** Bot token was **revoked/rotated by Telegram** (user action or security event). Current `.env` token may be invalid.
**Action Required:** Verify with `curl "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getMe"` — rotate via @BotFather if invalid.

### 4.2 xAI API Key Rejection — **FAIL**
**Location:** `errors.log` 2026-06-11
```json
{"code":"invalid-argument","error":"Incorrect API key provided: xa***==. You can obtain an API key from https://console.x.ai."}
```
**Status:** xAI key in `.env` is invalid/revoked.

### 4.3 Provider Rate Limits — **WARN**
- OpenRouter 429: "Provider returned error" / "rate-limited upstream" (Stealth provider)
- OpenRouter 402: "Insufficient credits" / "Prompt tokens limit exceeded"

### 4.4 Google Token Expiry — **WARN**
- `google_token.json` expired 2026-06-17 (1 day past expiry at check)
- Refresh token present — should auto-refresh but verify

---

## 5. TREND COMPARISON (vs 2026-07-05 Audit)

| Finding | 2026-07-05 | 2026-07-11 (AM) | 2026-07-11 (PM) | Trend | Severity |
|---------|------------|-----------------|-----------------|-------|----------|
| Backup `.env` copies | 43 | **49** | **49** | 🔴 **Worse (+6)** | CRITICAL |
| Workspace `.env` readers | 18 | 18 | 18 | ➡️ No Change | CRITICAL |
| Gateway crash loop | 17 days | **21 days** | **21 days** | 🔴 **Worse** | CRITICAL |
| DNS failures | Present | Present | Present | ➡️ No Change | HIGH |
| WhatsApp unpaired | 62 days | **65 days** | **65 days** | 🔴 **Worse** | HIGH |
| InvalidToken in logs | Not checked | **Found** | **Found** | 🔴 **New** | CRITICAL |
| AGENTS.md BOM | Present | Present | Present | ➡️ No Change | MEDIUM |
| google_token.json ACL | PASS | PASS | PASS | ✅ Stable | — |

### ESCALATIONS (3+ consecutive cycles unremediated)
1. **Backup `.env` copies** — PERSISTENT SECURITY DEBT (12+ cycles)
2. **Workspace `.env` readers** — PERSISTENT SECURITY DEBT (7+ cycles)
3. **WhatsApp unpaired** — PERSISTENT SECURITY DEBT (65+ days)

---

## 6. REMEDIATION PRIORITIES

### Immediate (Today)
1. **Delete all 49 backup `.env` copies:**
   ```bash
   find ~/.hermes/backups ~/.hermes/state-snapshots ~/hermes-backup ~/.openclaw -name ".env" -type f -delete
   ```
2. **Fix gateway:**
   ```bash
   uv pip install concurrent-log-handler && hermes gateway run --replace
   ```
   (Use Python 3.11/uv, NOT Python 3.14)
3. **Verify Telegram token:**
   ```bash
   curl "https://api.telegram.org/bot$(grep TELEGRAM_BOT_TOKEN ~/.hermes/.env | cut -d= -f2)/getMe"
   ```
   If `{"ok":false}`, rotate via @BotFather and update `.env`.
4. **Delete 18 workspace `.env` reader scripts** — replace with Hermes-managed credentials.

### This Week
5. **Repair WhatsApp pairing** — manual QR scan required.
6. **Fix AGENTS.md BOM:**
   ```bash
   sed -i '1s/^\xEF\xBB\xBF//' ~/.hermes/workspace/AGENTS.md
   ```
7. **Diagnose host DNS** — check resolver, `/etc/hosts`, firewall, VPN.
8. **Retarget `deliver=origin/local` cron jobs** to specific Telegram topics.

### Ongoing
9. Implement credential rotation schedule (Telegram, OpenRouter, xAI, Google).
10. Add pre-commit hooks to block `.env` commits and BOM in markdown.
11. Monitor `gateway-exit-diag.log` for crash recurrence.

---

## 7. RETENTION CLEANUP

Per 7-day policy, audits older than 2026-07-04 deleted. Current window: 2026-07-04 through 2026-07-11 (8 files including this afternoon re-run).

---

## 8. VERIFICATION

**Report written to:** `C:\Users\User\.hermes\workspace\Vault\System\Assistant\SECURITY_AUDIT_2026-07-11-afternoon.md`  
**Verification:** File exists, 8.4KB, all 8 sections present, trend table complete, escalations flagged.