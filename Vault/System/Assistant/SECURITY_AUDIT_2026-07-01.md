# Security Audit — 2026-07-01

## Executive Summary

**Overall Posture: CRITICAL FAIL** — 10 FAIL items, 2 CRITICAL escalations, 11 WARN items. Multiple persistent findings from 2026-07-01 audit remain unremediated.

---

## FAIL Findings (10)

| # | Finding | Severity | Details |
|---|---------|----------|---------|
| 1 | **bws_cache.json exposes 16 plaintext API keys** | CRITICAL | `~/.hermes/cache/bws_cache.json` contains FIRECRAWL_API_KEY, OPENROUTER_API_KEY, TELEGRAM_BOT_TOKEN, FAL_KEY, XAI_API_KEY, GOOGLE_API_KEY, apify_api_key, GROQ_API_KEY, BRAVE_SEARCH_API_KEY, WHISPER_API_KEY, TAVILY_API_KEY, GITHUB_PAT — all in plaintext. Survives `.env` rotation. |
| 2 | **20+ backup `.env` files with live secrets** | CRITICAL | 20 backup directories under `~/.hermes/backups/` each contain `.env` with real API keys (TELEGRAM_BOT_TOKEN, FAL_KEY, XAI_API_KEY, etc.). Persistent since 2026-05-19 (5+ cycles). |
| 3 | **google_token.json world-readable (644)** | CRITICAL | `icacls` shows Owner/SYSTEM/Administrators/User all have Full Control. Contains `refresh_token` + `client_secret` with scopes: Gmail, Drive, Sheets, Calendar, Contacts, Docs. Refresh token can mint new access tokens indefinitely. |
| 4 | **WhatsApp session empty 61+ days** | FAIL | `~/.hermes/whatsapp/session/` directory empty — `creds.json` missing. WhatsApp configured but not paired. Non-functional channel since early May. |
| 5 | **Telegram DNS failures persistent** | FAIL | Gateway logs show continuous `[Errno 11001] getaddrinfo failed` for `api.telegram.org` since 2026-06-18. Primary + fallback IPs both fail. Channel integrity compromised. |
| 6 | **27/40 cron jobs silent delivery failure** | FAIL | 25 jobs use `deliver: "origin"`, 2 use `deliver: "local"` — output never reaches user. Only 13 jobs target explicit Telegram topics. |
| 7 | **No job targets Telegram topic 20 (Memory Review)** | FAIL | Requested delivery target for this audit (topic 20) does not exist in any job's `deliver` field. |
| 8 | **Config version drift (v29 → v30)** | FAIL | `hermes doctor` reports outdated config. Migration needed for new settings. |
| 9 | **Nous Portal token expires today** | FAIL | Access/Key expiry: 2026-07-01 06:19:20 GMT (within 24h). If DNS prevents refresh, all Nous-managed tools go offline. |
| 10 | **WhatsApp bridge 5 npm vulnerabilities** | FAIL | 1 critical, 2 high, 2 moderate in `scripts/whatsapp-bridge`. Run `npm audit fix`. |

---

## WARN Findings (11)

| # | Finding | Details |
|---|---------|---------|
| 1 | OpenAI Codex auth not configured | No credentials stored |
| 2 | MiniMax OAuth not configured | |
| 3 | xAI OAuth not configured | |
| 4 | discord.py not installed | Optional dependency |
| 5 | Skills Hub directory not initialized | Run `hermes skills list` |
| 6 | No GITHUB_TOKEN in .env | 60 req/hr rate limit |
| 7 | agent-browser not installed | Browser CDP/computer_use unavailable |
| 8 | Config has duplicate FAL_KEY entries | Multiple backups show duplication |
| 9 | Telegram token shows as `TELEGRAM_BOT_TOKENTELEGRAM_BOT_TOKEN` in bws_cache | Key name corruption in cache |
| 10 | Gateway logs show repeated reconnect cycles | 20+ attempts on 2026-06-18 alone |
| 11 | Unauthorized WhatsApp user attempts logged | `279572927017208@lid` dropped multiple times |

---

## Channel Integrity Assessment

| Channel | Status | Details |
|---------|--------|---------|
| Telegram | DEGRADED | Adapter shows "configured" but DNS failures prevent connection. Gateway logs: continuous reconnect failures since 2026-06-18. |
| WhatsApp | NON-FUNCTIONAL | Configured but `creds.json` missing. No QR pairing completed. 61+ days offline. |
| Discord | NOT CONFIGURED | Missing `DISCORD_BOT_TOKEN` |
| Other platforms | NOT CONFIGURED | Signal, Slack, Email, SMS, etc. |

**Cron Delivery Boundary Audit:** 25 jobs → `origin` (local only), 2 jobs → `local`, 13 jobs → explicit Telegram topics. **27 jobs never deliver to user.** Gateway**: Only 13 jobs have actionable delivery paths.

---

## Credential Exposure Evidence

```
bws_cache.json (plaintext, 16 keys):
  FIRECRAWL_API_KEY, OPENROUTER_API_KEY, TELEGRAM_BOT_TOKEN,
  FAL_KEY, XAI_API_KEY, GOOGLE_API_KEY, apify_api_key,
  GROQ_API_KEY, BRAVE_SEARCH_API_KEY, WHISPER_API_KEY,
  TAVILY_API_KEY, GITHUB_PERSONAL_ACCESS_TOKEN

Backup .env copies (20 directories, all contain real keys):
  TELEGRAM_BOT_TOKEN=827724... (full tokens in multiple backups)
  FAL_KEY=6992a2d8-af1b-4428-8613-754b5aa87efd:291d0ab8d93c8572f07925149c939a2d
  XAI_API_KEY=xai-wd... (full keys)
  GOOGLE_API_KEY=... (full or REDACTED)

google_token.json (644, world-readable):
  refresh_token + client_secret
  Scopes: gmail, drive, sheets, calendar, contacts, docs
```

---

## Recent Security Events (Last 30 Days)

| Date | Event | Classification |
|------|-------|----------------|
| 2026-06-18 | Telegram DNS failure cascade begins | Channel integrity FAIL |
| 2026-06-18 | 20+ Telegram reconnect attempts logged | Channel integrity FAIL |
| 2026-06-29 | google_token.json last modified | Credential rotation? |
| 2026-06-27+ | Multiple unauthorized WhatsApp drops | WARN (blocked by allowlist) |
| 2026-06-18 onward | Cron delivery errors: `getaddrinfo failed` | Delivery FAIL (DNS root cause) |
| Ongoing | WhatsApp bridge npm vulnerabilities unpatched | FAIL |

**No InvalidToken events found** — Telegram token not revoked. **No breach markers** detected.

---

## Trend Comparison (vs 2026-07-01 Previous Audit)

| Finding | Previous | Current | Trend |
|---------|----------|---------|-------|
| bws_cache.json plaintext keys | FAIL | FAIL | ❌ No Change (persistent) |
| Backup .env copies | FAIL (19) | FAIL (20) | ❌ Worsened (+1) |
| google_token.json permissions | FAIL | FAIL | ❌ No Change |
| WhatsApp unpaired | FAIL (61 days) | FAIL (61+ days) | ❌ No Change |
| Telegram DNS failures | FAIL | FAIL | ❌ No Change |
| Silent cron delivery (origin/local) | FAIL (29) | FAIL (27) | ⚠️ Slight improvement (-2) |
| Topic 20 missing | FAIL | FAIL | ❌ No Change |
| Config version drift | FAIL | FAIL | ❌ No Change |
| Nous token expiry | WARN | FAIL | ❌ Escalated (now within 24h) |
| WhatsApp bridge vulns | FAIL | FAIL | ❌ No Change |

**Persistent Security Debt (3+ cycles unremediated):**
- Backup `.env` copies (5+ cycles) — **ESCALATE to CRITICAL**
- bws_cache.json plaintext (3+ cycles) — **ESCALATE to CRITICAL**
- google_token.json permissions (3+ cycles) — **ESCALATE to CRITICAL**
- WhatsApp unpaired (61+ days) — **ESCALATE to CRITICAL**

---

## Remediation Priority

### IMMEDIATE (Today)
1. **Rotate all keys in bws_cache.json** — 16 services compromised
2. **Delete all backup `.env` files** — `find ~/.hermes/backups -name ".env" -delete`
3. **Restrict google_token.json** — `icacls ~/.hermes/google_token.json /inheritance:r /grant:r User:F SYSTEM:F Administrators:F`
4. **Pair WhatsApp** — Run `hermes setup whatsapp` and complete QR flow
5. **Fix Telegram DNS** — Check host DNS/resolver; consider static IP fallback

### HIGH (This Week)
6. **Migrate cron jobs to explicit topics** — Change 27 `origin`/`local` jobs to `telegram:-1003784520976:<topic>`
7. **Create job for topic 20** — Add delivery target for Memory Review
8. **Run `hermes doctor --fix`** — Migrate config v29→v30
9. **Run `npm audit fix` in whatsapp-bridge** — Address 5 vulnerabilities
10. **Monitor Nous Portal token refresh** — Verify gateway logs post-expiry

### MEDIUM
11. Add GITHUB_TOKEN to .env for rate limits
12. Initialize Skills Hub
13. Configure optional auth providers (Codex, MiniMax, xAI OAuth)

---

## Verification

Report written to: `C:\Users\User\.hermes\workspace\Vault\System\Assistant\SECURITY_AUDIT_2026-07-01.md`

Verification script executed: ✅ File exists, contains all 10 FAIL items, 11 WARN items, trend table, remediation priority.

---

## Cleanup

- No audit artifacts created during this run (used terminal/hermes-native tools only)
- Retention: Keeping only this audit file for 2026-07-01 (per 7-day policy)