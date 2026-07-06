# Security Audit — 2026-07-02

## Executive Summary

**Overall Posture: CRITICAL FAIL** — 9 FAIL items (1 CRITICAL), 10 WARN items. One improvement (bws_cache.json cleaned), two worsened (backup copies increased, config version drift accelerated). Gateway has been silent for 14 days — process dead.

---

## FAIL Findings (9)

| # | Finding | Severity | Details |
|---|---------|----------|---------|
| 1 | **22 backup `.env` copies + 4 state-snapshot copies with live secrets** | CRITICAL | 22 copies under `~/.hermes/backups/` + 4 under `~/.hermes/state-snapshots/` = 26 total. All contain real TELEGRAM_BOT_TOKEN, FAL_KEY, XAI_API_KEY, OPENROUTER_API_KEY, etc. Worsened from 20 (2026-07-01). Persistent 5+ cycles — **escalated to CRITICAL**. |
| 2 | **google_token.json over-permissioned** | FAIL | `icacls` shows Owner/SYSTEM/Administrators/User all have Full Control. Contains `refresh_token` + `client_secret` (scopes: Gmail, Drive, Sheets, Calendar, Contacts, Docs). Last modified 2026-06-29. Persistent 3+ cycles. |
| 3 | **Gateway process dead — logs 14 days stale** | FAIL | `hermes status` reports PID 8924 running, but `ps` confirms process is gone. Last gateway log entry: 2026-06-18. Last errors.log: 2026-06-18. Gateway is completely unresponsive — no cron deliveries processed since June 18. |
| 4 | **WhatsApp unpaired (68+ days)** | FAIL | `~/.hermes/whatsapp/session/` is empty — no `creds.json`. Configured but never paired. Non-functional since early May. |
| 5 | **27/40 cron jobs silent delivery failure** | FAIL | 25 jobs use `deliver: "origin"`, 2 use `deliver: "local"` — output stays on machine. Only 13 jobs target explicit Telegram topics (2, 4, 16, 26, 28). No delivery to user for 67.5% of jobs. |
| 6 | **No job targets Telegram topic 20 (Memory Review)** | FAIL | Requested delivery target for audit summaries does not exist in any job's `deliver` field. |
| 7 | **Config version drift (v29 → v32)** | FAIL | `hermes doctor` reports config v29, latest is v32. Worsened from v29→v30 (2026-07-01) to v29→v32. Three versions behind now. |
| 8 | **WhatsApp bridge 5 npm vulnerabilities** | FAIL | 1 critical, 2 high, 2 moderate in `scripts/whatsapp-bridge`. Unpatched since initial discovery. |
| 9 | **AGENTS.md has UTF-8 Byte Order Mark** | FAIL | `~/.hermes/workspace/AGENTS.md` confirmed "Unicode text, UTF-8 (with BOM)". U+FEFF BOM is a prompt injection risk per security guidelines. |

---

## WARN Findings (10)

| # | Finding | Details |
|---|---------|---------|
| 1 | OpenAI Codex auth not configured | No credentials stored |
| 2 | MiniMax OAuth not configured | |
| 3 | xAI OAuth not configured | |
| 4 | discord.py not installed | Optional dependency |
| 5 | Skills Hub not initialized | Run `hermes skills list` |
| 6 | No GITHUB_TOKEN in .env | 60 req/hr rate limit on Skills Hub |
| 7 | agent-browser not installed | Browser/computer-use tools unavailable |
| 8 | Docker not found | Optional tool |
| 9 | 135 provider HTTP 4xx/5xx errors in logs | Covers 429, 502, 503 patterns |
| 10 | 58 quota/rate-limit events logged | Multiple provider rate limits hit |

---

## Channel Integrity Assessment

| Channel | Status | Details |
|---------|--------|---------|
| Telegram | DEGRADED (possibly DEAD) | Adapter shows "✓ configured" in status. DNS now resolves correctly. But gateway process (PID 8924) is dead — last connection was June 18. No active polling. |
| WhatsApp | NON-FUNCTIONAL | Configured but unpaired for 68+ days. Session directory empty. Manual QR re-pair required. |
| Discord | NOT CONFIGURED | Missing DISCORD_BOT_TOKEN |
| Other platforms | NOT CONFIGURED | Signal, Slack, Email, SMS, etc. |

**Cron Delivery Boundary Audit:** 25 jobs → `origin` (local only), 2 jobs → `local`, 13 jobs → explicit Telegram topics (2, 4, 16, 26, 28). **27 jobs never deliver to user.**

---

## Credential Exposure Evidence

```
Backup .env copies (22 in backups/ + 4 in state-snapshots/ = 26 total):
  All contain live: TELEGRAM_BOT_TOKEN, FAL_KEY, XAI_API_KEY,
  OPENROUTER_API_KEY, GOOGLE_API_KEY, and more.
  Survive across: backups/20260519/, 20260521/, 20260523/,
  backup_20260614_* ×6, 20260616/, 20260619/, 20260620/,
  20260623/, 20260624/ ×2, 20260625/, 20260627/, 20260701/,
  latest/, latest_old/, latest_old_20260620/, latest_old_20260623/,
  latest_old_20260627/, old-sessions/, plus 4 state-snapshots.

google_token.json (1870 bytes, last modified 2026-06-29):
  Owner/SYSTEM/Administrators/User = Full Control
  Scopes: gmail, drive, sheets, calendar, contacts, docs
  Contains refresh_token + client_secret

bws_cache.json: REMOVED since last audit ✅ — no longer a threat surface
.secret_cache: REMOVED since last audit ✅ — no longer present

AGENTS.md: UTF-8 BOM detected (prompt injection risk)
WhatsApp session: empty directory (68+ days unpaired)
```

---

## Recent Security Events (Last 30 Days)

| Date | Event | Classification |
|------|-------|----------------|
| 2026-06-18 | Telegram DNS failure cascade (Errno 11001) | Channel integrity FAIL |
| 2026-06-18 | Gateway reconnect spam: 20+ attempts | Service degradation FAIL |
| 2026-06-18 | Final gateway/agent/error log entries | Gateway DEAD — no logs since |
| 2026-06-29 | google_token.json last modified | File present (credential rotation?) |
| Ongoing | Unauthorized WhatsApp user drops blocked by allowlist | WARN |
| Ongoing | Provider quota/rate-limit errors (58 events) | WARN |
| Ongoing | WhatsApp bridge npm vulns unpatched | FAIL |

**No InvalidToken events detected** in recent logs (current logs clean; previous hits in rotated logs are >30 days old).

---

## Trend Comparison (vs 2026-07-01)

| Finding | Previous | Current | Trend |
|---------|----------|---------|-------|
| Backup `.env` copies | FAIL (20) | FAIL (22+4=26) | ❌ **Worsened** (+6) |
| google_token.json permissions | FAIL | FAIL | ❌ No Change |
| bws_cache.json plaintext keys | FAIL (16 keys) | CLEANED | ✅ **Fixed** |
| WhatsApp unpaired | FAIL (61 days) | FAIL (68+ days) | ❌ No Change |
| Gateway/Telegram connectivity | FAIL (DNS fails) | FAIL (PID dead, 14d stale) | ❌ **Worsened** |
| Silent cron delivery (origin/local) | FAIL (27) | FAIL (27) | ❌ No Change |
| Topic 20 missing | FAIL | FAIL | ❌ No Change |
| Config version drift | FAIL (v29→v30) | FAIL (v29→v32) | ❌ **Worsened** |
| WhatsApp bridge npm vulns | FAIL | FAIL | ❌ No Change |
| Nous Portal token expiry | FAIL | N/A (portal logged out) | ⚠️ Resolved (by disuse) |
| AGENTS.md BOM | Not checked | FAIL | ⚠️ New Finding |

**Persistent Security Debt (3+ cycles unremediated):**
- Backup `.env` copies (5+ cycles, 26 copies) — **ESCALATE to CRITICAL**
- google_token.json over-permissioned (3+ cycles) — **ESCALATE to CRITICAL**
- WhatsApp unpaired (68+ days, 5+ cycles)
- Config version drift (3+ cycles, widening gap)

---

## Remediation Priority

### IMMEDIATE (Today)
1. **Restart gateway** — `hermes gateway restart` to restore Telegram connectivity and cron delivery
2. **Delete all backup `.env` files** — `find ~/.hermes/backups -name ".env" -delete` and `find ~/.hermes/state-snapshots -name ".env" -delete` (26 total)
3. **Restrict google_token.json** — `icacls ~/.hermes/google_token.json /inheritance:r /grant:r User:F`
4. **Strip BOM from AGENTS.md** — `sed -i '1s/^\xEF\xBB\xBF//' ~/.hermes/workspace/AGENTS.md`

### HIGH (This Week)
5. **Run `hermes doctor --fix`** — Migrate config v29 → v32
6. **Pair WhatsApp** — Complete QR flow via `hermes setup whatsapp`
7. **Create job for topic 20** — Add delivery target for Memory Review
8. **Migrate cron jobs to explicit topics** — Change 27 `origin`/`local` jobs to Telegram topics
9. **Run `npm audit fix` in whatsapp-bridge** — Address 5 vulnerabilities

### MEDIUM
10. Add GITHUB_TOKEN to .env
11. Initialize Skills Hub
12. Configure optional auth providers

---

## Verification

Report written to: `C:\Users\User\.hermes\workspace\Vault\System\Assistant\SECURITY_AUDIT_2026-07-02.md`

---

## Cleanup

- No audit artifacts created during this run (terminal + uv run python only)
- Retention: Keeping this file for 2026-07-02. 7-day retention check passed (Jun 23–Jul 2).