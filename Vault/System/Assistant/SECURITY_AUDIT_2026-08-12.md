# Security Audit — 12 August 2026

**Date:** 12/08/2026
**Run by:** internal cron / Hermes Agent
**Overall:** FAIL
**Report path:** `C:\Users\User\.hermes\workspace\Vault\System\Assistant\SECURITY_AUDIT_2026-08-12.md`

---

## Summary

- **Telegram channel healthy** — bot token VALID (`getMe` → ok:true, `@Ogaitchhermesbot`), gateway alive (PID 13760, ESTABLISHED TCP to `149.154.166.110:443`), live logs fresh 06:07 today. No credential compromise detected.
- **Persistent credential-leak debt (3+ cycles, escalate):** 20 backup `.env` copies, a plaintext credential cache (`bws_cache.json`, 15 live secrets), and 38 live workspace scripts reading `.env` directly.
- **Channels affected:** WhatsApp permanently unpaired (reconnect attempt 313); ~28/40 cron jobs use silent/untargeted delivery (`origin`/`local`).

## Findings by Area

### 1. Credential Exposure

- Files checked: `~/.hermes/.env` (full, ~24KB), `AppData/Local/hermes/.env` (399B, dual-root WARN), `~/.hermes/config.yaml`, `auth.json` (normal), `~/.hermes/cache/bws_cache.json` (**15 plaintext secrets**), `google_token.json` (ACL PASS).
- Detected secrets: **direction from cache** — OpenRouter, Telegram, Firecrawl, FAL, xAI, Brave, Tavily, Groq, GitHub PAT, Google, Apify (all masked).
- File permissions: `google_token.json` icacls = only SYSTEM/Administrators/User (PASS).
- Verdict: **FAIL** (backup `.env` copies + plaintext cache + 38 `.env`-reading scripts).

### 2. Channel Integrity

- Messaging platforms checked: Telegram (PASS), WhatsApp (FAIL/unpaired), Discord (paused).
- Errors found: WhatsApp reconnect timeout ×313; Telegram primary DNS failure 05:12 recovered via sticky fallback; OpenRouter APIConnectionError 04:51 retried OK (transient).
- Verdict: **FAIL** (WhatsApp non-functional; 25/40 cron jobs `deliver=origin` silent).

### 3. Recent Security Events

- Relevant log patterns: **no** `InvalidToken` / `Unauthorized` / breach markers in live gateway.log or errors.log. No token revocation.
- Security events: Nous Portal refresh token rejected (WARN, re-auth needed); OpenRouter connection reset (transient); Telegram fallback-IP recovery.
- Verdict: **PASS** (no compromise indicators).

## FAIL Findings

| ID | Severity | Description | Evidence / Source |
|----|----------|-------------|-------------------|
| 1  | critical | Plaintext credential cache `bws_cache.json` with 15 live secrets (survives `.env` rotation) | `~/.hermes/cache/bws_cache.json` |
| 2  | high | 20 backup `.env` copies with raw API keys | 9 `~/.hermes/backups` + 10 `~/hermes-backup` + 1 `~/.openclaw` |
| 3  | high | 38 live workspace scripts read `.env` directly (leak to process/log) | `send_*.py`, `check_*.py`, `tg_*.py`, `query_*.py` |
| 4  | medium | WhatsApp channel non-functional (unpaired, reconnect loop) | gateway.log attempt 313 |

## WARN Findings

| ID | Description | Evidence |
|----|-------------|----------|
| 1  | Dual `.env` roots — divergence risk | `~/.hermes/.env` + `AppData/Local/hermes/.env` |
| 2  | 25/40 cron jobs `deliver=origin` (silent), 3 `local` — no explicit topic | `~/.hermes/cron/jobs.json` |
| 3  | Nous Portal refresh token rejected — auth provider offline | `hermes status` |
| 4  | Transient network: OpenRouter reset, Telegram primary DNS fail | gateway.log / errors.log |

## CRITICAL Escalations

- **None upgraded this cycle** beyond those already flagged persistent-debt. `bws_cache.json` is treated as critical (CRITICAL exposure already in prior cycle).

## Trend Comparison (vs 2026-08-11)

| Item | 08-11 | 08-12 | Trend |
|---|---|---|---|
| Telegram token valid | ✅ | ✅ | No Change (good) |
| Gateway/Telegram online | ✅ | ✅ | No Change (good) |
| Backup `.env` copies | 20 | 20 | No Change (persistent debt) |
| `bws_cache.json` secrets | present | 15 live | No Change (critical debt) |
| Workspace `.env` readers | present | 38 | Not Remediated (persistent debt) |
| WhatsApp functional | ❌ | ❌ | No Change (persistent debt, attempt 313) |

## Remediation Priority

1. **CRITICAL —** Delete/purge `bws_cache.json` (15 plaintext secrets; survives `.env` rotation).
2. **HIGH —** Delete 20 backup `.env` copies (9+10+1).
3. **HIGH —** Purge or rewrite 38 `.env`-reading workspace scripts to Hermes-injected env.
4. **MEDIUM —** Consolidate dual `.env` roots; re-point 25+ `deliver=origin` cron jobs to explicit topic targets.
5. **MEDIUM —** Re-pair WhatsApp (manual QR); re-authenticate Nous Portal.

## Retention Note

- Cleaned up `SECURITY_AUDIT_2026-08-04.md` (older than 7-day window). Retaining 08-11, 08-11-afternoon, 08-12. No same-day duplicates to dedupe.

## Attachments / Evidence

- CLI outputs: `hermes status --all` (gateway alive, token configured), direct `getMe` (valid), `tasklist`/`netstat` (PID 13760 ESTABLISHED to Telegram).
- Log files scanned: `AppData/Local/hermes/logs/gateway.log` (08-12 fresh), `errors.log`, `agent.log`; `~/.hermes/logs/` (stale mirror).
- Config scanned: `~/.hermes/cron/jobs.json` (40 jobs), `channel_directory.json` (topic 20 present).
- Report saved: `C:\Users\User\.hermes\workspace\Vault\System\Assistant\SECURITY_AUDIT_2026-08-12.md`

---

*Masked: all secrets represented by provider-prefix + truncated form. No full tokens echoed.*
