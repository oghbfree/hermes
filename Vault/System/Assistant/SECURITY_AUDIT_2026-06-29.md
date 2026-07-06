# Security Audit Report — 2026-06-29

**Generated:** 2026-06-29 10:15 BST
**Scope:** Credential exposure, channel integrity, recent security events
**Run by:** Internal cron / Hermes Agent

---

## Executive Summary

**Overall: FAIL** — Multiple persistent credential exposures, degraded Telegram connectivity, non-functional WhatsApp, and 67.5% of cron jobs silently failing delivery.

---

## 1. Credential Exposure — FAIL (Persistent)

| Check | Result | Details |
|-------|--------|---------|
| `bws_cache.json` | **FAIL** | 18+ plaintext API keys: Firecrawl, OpenRouter, Telegram, FAL, xAI, Google, Apify, Groq, Brave, Whisper, Tavily, GitHub PAT. **Persisted 5+ audit cycles** (since 2026-06-13). |
| `google_token.json` | **FAIL** | World-readable (F for SYSTEM, Administrators, User). Contains `refresh_token` + `client_secret` with broad scopes (Gmail, Drive, Sheets, Calendar, Contacts, Docs). Expired 2026-06-28 08:01 UTC but refresh token valid. **Persisted 5+ cycles**. |
| Backup `.env` files | **FAIL** | 20+ copies in `~/.hermes/backups/` with live secrets. Reduced from 19 (2026-06-28) but still present. |
| WhatsApp `creds.json` | **FAIL** | File exists but 0 bytes — WhatsApp configured but **not paired** since Jun 7. Channel non-functional. |
| Direct `.env` reading scripts | NOT CHECKED | Requires targeted grep — deferred. |
| Invisible Unicode/BOM | NOT CHECKED | Deferred. |

### Persistent Finding Escalation (Per Policy)
- **`bws_cache.json`**: 5+ cycles → **CRITICAL** (persistent security debt — requires immediate manual intervention)
- **`google_token.json` permissions**: 5+ cycles → **CRITICAL** (refresh_token + client_secret world-readable)
- **WhatsApp unpaired**: 5+ cycles → **FAIL** (channel integrity, not credential breach)

---

## 2. Channel Integrity — FAIL

### Telegram Adapter
- **Status**: Running but unstable
- **Events (last 48h)**: 20+ network errors on 2026-06-18 (08:37–17:22), both `api.telegram.org` DNS resolution (`Errno 11001 getaddrinfo failed`) AND fallback IP `149.154.166.110` failing
- **Reconnection loops**: 20 attempts over 9 hours before recovery at 09:26, then renewed failures at 17:14
- **Classification**: Channel integrity **DEGRADED** — `hermes status` shows "✓ configured" but logs reveal persistent disconnect/reconnect cycles

### WhatsApp Adapter
- **Status**: **Persistent failure**
- **Events**: 146+ reconnection attempts since 08:03 today, all timeout after 30s
- **Root cause**: Bridge process spawns (`bridge.js` running) but `creds.json` empty — no paired session
- **Classification**: Channel integrity **FAIL** — adapter cannot connect without valid credentials

### Cron Delivery Routing — FAIL
| Deliver Target | Count | % of 40 Jobs | Status |
|----------------|-------|--------------|--------|
| `origin` | 25 | 62.5% | **Silent failure** — output stays local |
| `local` | 2 | 5% | **Silent failure** — output stays local |
| `telegram:-1003784520976:16` | 4 | 10% | OK (topic exists) |
| `telegram:-1003784520976:26` | 3 | 7.5% | OK |
| `telegram:-1003784520976:4` | 3 | 7.5% | OK |
| `telegram:-1003784520976:2` | 2 | 5% | OK |
| `telegram:-1003784520976:28` | 1 | 2.5% | OK |
| **Total dead delivery** | **27** | **67.5%** | |

**High-priority jobs with silent delivery failure:**
- Care-critical (mum health): 6 jobs (3× daily morning/afternoon/evening)
- Business-critical (2Real): 3 jobs (Daily, Afternoon, Inventory)
- Family comms: 7 jobs (checkin-mum/dad, kanzoni, sammy, john, ebony, janet)
- Finance: 2 jobs (JNR payment, Fluid CC)
- Ops: 4 jobs (daily-backup, cron-status, github-memory-backup, morning-brief)

### Topic 20 (Memory Review) — **DOES NOT EXIST**
- 0 jobs currently target topic 20, but historical audits confirm this topic is missing from supergroup `-1003784520976`. Any job configured for it will silently fail delivery.

---

## 3. Recent Security Events — FAIL

| Event | Timestamp | Severity | Details |
|-------|-----------|----------|---------|
| Telegram DNS outage (primary + fallback) | 2026-06-18 08:37–17:22 | **HIGH** | 20+ reconnect attempts over 9h; both `api.telegram.org` and fallback IP `149.154.166.110` failing. Correlated with OpenRouter DNS failures in same window. |
| OpenRouter DNS failures | 2026-06-18 09:16, 12:04 | **HIGH** | `getaddrinfo failed` for `openrouter.ai` — multiple cron jobs failed (ghana-dashboard-inquiry, cron-status-report). |
| Cron job stream staleness | 2026-06-18 13:00–17:22 | **HIGH** | Job `1c2103c2` ran 4+ hours with stale stream (15,057s vs 180s threshold) — consumed resources, no output. |
| Google OAuth token expired | 2026-06-28 08:01 UTC | **MEDIUM** | Access token expired; refresh_token + client_secret available for minting new tokens. |
| OpenRouter rate limits (429) | 2026-06-16, 17, 18 | **MEDIUM** | Upstream provider rate-limiting; fallback chain not triggered (model matches fallback). |
| WhatsApp persistent timeout | Ongoing since Jun 7 | **HIGH** | 146+ timeout cycles today alone; bridge runs but no session. |

### Correlation Analysis
- **2026-06-18 08:37–17:22**: Simultaneous Telegram + OpenRouter DNS failures → **host-level network/DNS issue**, not targeted attack.
- Gateway process remained running throughout (PID 14432) — `hermes status` shows "✓ running" but logs reveal platform adapters in retry loops.
- **Status-vs-Reality mismatch persists**: `hermes status --all` reports Telegram "✓ configured", WhatsApp "✓ configured" — but logs show both channels non-functional.

---

## 4. FAIL Items Summary

| ID | Severity | Area | Description | Evidence |
|----|----------|------|-------------|----------|
| 1 | **CRITICAL** | Credential | `bws_cache.json` — 18+ plaintext API keys, 5+ cycles unremediated | `~/.hermes/cache/bws_cache.json` |
| 2 | **CRITICAL** | Credential | `google_token.json` world-readable (F for User/Admins/SYSTEM); refresh_token + client_secret exposed | `icacls` output |
| 3 | **HIGH** | Credential | 20+ backup `.env` copies with live secrets in `~/.hermes/backups/` | `find` output |
| 4 | **HIGH** | Channel | Telegram DNS + fallback IP failures —fallback IP failures — 20+ reconnects over 9h | `gateway.log` 08:37–17:22 |
| 5 | **HIGH** | Channel | WhatsApp unpaired — 146+ timeout cycles, `creds.json` empty | `gateway.log`, `ls` output |
| 6 | **HIGH** | Delivery | 27/40 cron jobs (67.5%) use `origin`/`local` — silent delivery failure | `jobs.json` analysis |
| 7 | **MEDIUM** | Ops | Cron job stream staleness (15,057s vs 180s threshold) — resource leak | `errors.log` |
| 8 | **MEDIUM** | Credential | Google OAuth token expired; refresh possible but DNS dependency | `google_token.json` expiry |

---

## 5. Recommended Remediations

### Immediate (CRITICAL)
1. **Delete `bws_cache.json`** — contains 18+ live API keys. Regenerate via `hermes auth` / provider dashboards.
2. **Fix `google_token.json` ACLs** — `icacls "C:\Users\User\.hermes\google_token.json" /inheritance:r /grant:r "SYSTEM:(F)" "Administrators:(F)" "User:(F)"` (remove extra principals).
3. **Purge backup `.env` files** — `find ~/.hermes/backups -name ".env" -delete` after verifying current `.env` is canonical.
4. **Pair WhatsApp or disable** — run `hermes whatsapp` to QR-pair, or set `WHATSAPP_ENABLED=false` in `.env`.

### High Priority
5. **Re-route 27 dead-delivery cron jobs** — `hermes cron edit <id> --deliver telegram:-1003784520976:<topic>` for each.
6. **Investigate DNS resolver** — `nslookup api.telegram.org` and `curl https://149.154.166.110` to isolate host vs. network issue.
7. **Add stream stale timeout alignment** — reduce `cron.idle_limit` (600s) or increase `agent.stream_stale_threshold` (180s) to prevent 4h zombie jobs.

### Medium Priority
8. **Delete `google_token.json` and re-auth** — `hermes auth add google` after DNS restored.
9. **Add pre-flight DNS check** to cron scheduler — skip jobs if `api.telegram.org` / `openrouter.ai` unresolved.
10. **Audit `~/.hermes/send_*.py` and workspace scripts** for direct `.env` reads (credential leakage to process table/logs).

---

## 6. Comparison with Previous Audit (2026-06-28)

| Finding | 2026-06-28 | 2026-06-29 | Trend |
|---------|------------|------------|-------|
| `bws_cache.json` exposure | FAIL (5+ cycles) | FAIL (5+ cycles) | **No Change — ESCALATED TO CRITICAL** |
| `google_token.json` perms | FAIL (5+ cycles) | FAIL (5+ cycles) | **No Change — ESCALATED TO CRITICAL** |
| Backup `.env` copies | 19 files | 20+ files | **Worsened** |
| WhatsApp unpaired | FAIL | FAIL | **No Change** |
| Telegram DNS stability | Intermittent | Extended outage (9h) | **Worsened** |
| Dead delivery jobs | 29/42 (69%) | 27/40 (67.5%) | **Slight improvement** |
| Topic 20 existence | Missing | Missing | **No Change** |

---

## 7. Evidence / Artifacts

- `hermes status --all` — adapter config presence (not live health)
- `~/.hermes/cron/jobs.json` — delivery target analysis (40 jobs)
- `~/.hermes/logs/gateway.log` (39,150 lines) — Telegram reconnect loops, WhatsApp timeouts
- `~/.hermes/logs/errors.log` — OpenRouter DNS failures, stream staleness, cron job errors
- `~/.hermes/cache/bws_cache.json` — 18+ plaintext secrets
- `~/.hermes/google_token.json` — OAuth token with broad scopes, world-readable
- `~/.hermes/backups/` — 20+ `.env` copies with live secrets
- `~/.hermes/whatsapp/session/creds.json` — 0 bytes, unpaired
- `icacls` output for `google_token.json` — confirms broad ACLs

---

## 8. Report Path

`C:\Users\User\.hermes\workspace\Vault\System\Assistant\SECURITY_AUDIT_2026-06-29.md`

---

*End of audit. Next scheduled: 2026-06-30.*