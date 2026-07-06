# Security Audit — 2026-07-03 (12:06 UTC)

## Summary

| Category | Status | Details |
|----------|--------|---------|
| Credential Exposure | 🔴 CRITICAL | 26 backup .env copies with live secrets |
| Channel Integrity | 🔴 FAIL | Gateway dead (15 days), WhatsApp unpaired (62+ days), 25/40 jobs silent-delivery |
| Recent Security Events | 🟡 WARN | Historical InvalidToken (resolved), xAI key rejection (resolved), host-level DNS failures |
| Config Drift | 🟡 WARN | yaml v23, doctor v29, latest v32 (-3 versions) |

---

## 1. Credential Exposure

### 🔴 CRITICAL: 26 Backup .env Copies (PERSISTENT — 8+ cycles)
- **22 copies** in `~/.hermes/backups/` (including `latest`, `latest_old`, `latest_old_*`)
- **4 copies** in `~/.hermes/state-snapshots/`
- Count unchanged at 26 for 8 consecutive audit cycles
- All contain raw API keys (OpenRouter, Telegram, Google, Firecrawl, etc.)
- **PERSISTENT SECURITY DEBT — escalated to CRITICAL** (3+ consecutive audits without remediation)
- `-maxdepth 3` find completed in <1s (skill-tested pattern)

### 🟢 PASS: Credential Cache Files
- `bws_cache.json`: Not found ✅ (resolved since ~Jun 26)
- `.secret_cache`: Not found ✅ (resolved since ~Jun 26)
- 5th consecutive clean cycle

### 🟢 PASS: google_token.json ACL
- `icacls` shows only Owner: (I)(F), SYSTEM: (I)(F), Administrators: (I)(F)
- No "Everyone" or "BUILTIN\Users" — standard Windows default, PASS

### 🔴 FAIL: Workspace AGENTS.md UTF-8 BOM
- `~/.hermes/workspace/AGENTS.md`: **UTF-8 with BOM** ❌
- Main `~/.hermes/AGENTS.md`: Absent (resolved) ✅
- BOM in workspace copy can trigger prompt injection blocks for workspace context

### 🟡 WARN: Scripts Directly Reading .env
- 5 workspace scripts read `.env` directly: `check_bot.py`, `check_keys.py`, `check_telegram_bot.py`, `check_telegram_topic4.py`, `morning_checkin.py`
- 1 test script: `test_threads.py`
- These extract TELEGRAM_BOT_TOKEN at runtime, risking leakage to process tables and logs

### 🟢 PASS: Telegram Bot Token Valid
- `getMe` returned `ok:true` — Bot ID 8277244378 (@Ogaitchhermesbot) is live
- Historical InvalidToken (Jun 8) fully resolved — current token accepted by Telegram

---

## 2. Channel Integrity

### 🔴 FAIL: Gateway Dead — 15 Days Stale
- Last log entry: **2026-06-18 17:22:29**
- PID 8924: **NOT RUNNING**
- Final state: DNS failures to `api.telegram.org` (primary + fallback IP 149.154.166.110)
- OpenRouter API also failed in same window (`[Errno 11001] getaddrinfo failed`) — host-level DNS issue, not targeted attack
- **15 consecutive days of gateway failure** — longest documented outage

### 🔴 FAIL: 27/40 Jobs Silent Delivery (25 origin + 2 local)
- 25 jobs deliver to `origin` — output stays local, never reaches user
- 2 jobs deliver to `local` — silent as well
- Only 13/40 jobs target Telegram topics (partial delivery channel)
- All 13 topic-targeted jobs affected by gateway failure (no delivery)

### 🔴 FAIL: WhatsApp Unpaired (62+ Days)
- `~/.hermes/whatsapp/session/` is **empty** — no `creds.json` found
- No existing WhatsApp session — requires manual QR re-pair via phone
- Persistent finding across 8+ cycles

### 🟢 PASS: .env ACL
- Only Owner/SYSTEM/Administrators have Full Control

### 🟡 WARN: Telegram Bot Token ACL
- Same as .env — only authorized users, PASS

---

## 3. Recent Security Events

### 🟢 Historical InvalidToken — Resolved
- Multiple `InvalidToken` rejections on **2026-06-08** — bot token `8277...ugM8` was rejected
- By 2026-06-10, gateway was connecting successfully again
- Current token (as confirmed by `getMe`) is fully valid
- Resolution likely: token rotation at Telegram, then updated in `.env`

### 🟢 Historical xAI Key Rejection — Resolved (Jun 11)
- `xAI image gen failed (400): Incorrect API key provided` on 2026-06-11
- Single-provider issue, not a credential leak. Probably key rotation/expiry.

### 🟡 WARN: Host-Level DNS Failures (Jun 18)
- Multi-service failure: BOTH `api.telegram.org` AND `openrouter.ai` failed with `getaddrinfo failed` (Errno 11001)
- Telegram fallback IPs (149.154.166.110) also failed
- Pattern confirms host-level DNS/network issue, not targeted attack
- Gateway has not recovered since these failures

### 🟡 WARN: Config Version Drift
- yaml: `_config_version: 23`
- doctor: schema v29 (was v23 previously — improved!)
- latest schema: v32
- 3 versions behind — partial improvement from earlier audit cycles

### 🟡 WARN: WhatsApp Bridge npm Vulnerabilities
- 1 critical, 2 high, 2 moderate vulnerabilities reported by `hermes doctor`
- Affects WhatsApp bridge only — not exploitable while WhatsApp is unpaired

---

## 4. Trend vs Prior Audit (2026-07-03 Afternoon @ 11:48)

| Finding | Afternoon (11:48) | This Audit (12:06) | Change |
|---------|-------------------|--------------------|--------|
| Gateway alive | PASS ✅ (recovered) | 🔴 FAIL (dead 15d) | **Regressed** — died again in ~80 min |
| backup .env (26) | 🔴 CRITICAL | 🔴 CRITICAL | No change |
| WhatsApp unpaired | 🔴 FAIL | 🔴 FAIL | No change (62+ days) |
| Workspace AGENTS.md BOM | 🔴 FAIL | 🔴 FAIL | No change |
| Config drift (v23→v29→v32) | 🟡 WARN | 🟡 WARN | No change |
| bws_cache.json | ✅ Gone | ✅ Gone | No change (clean) |
| Telegram token validity | N/A | ✅ Valid | New check — good |
| 2 local-delivery jobs | 🔴 FAIL | 🔴 FAIL | No change |
| 27/40 silent jobs | 🔴 FAIL | 🔴 FAIL | No change |

### Notable: Gateway Recovery Was Brief
- The 11:48 afternoon audit reported gateway alive (PID 8924, logs updating)
- 80 minutes later at 12:06: gateway dead again, logs still at June 18
- Either the recovery was temporary, or the audit was inaccurate
- **Lesson:** Single-point-in-time verification is insufficient for gateway state

---

## 5. Recommendations

1. **Backup cleanup (CRITICAL):** Delete all backup `.env` copies. Hermes credentials are in `~/.hermes/.env`; backups should not duplicate secrets. 26 copies is extreme.
2. **Restart gateway:** Gateway process is dead. Hermes cron jobs cannot deliver messages until gateway is running. Try `hermes gateway start` or manual restart.
3. **Strip AGENTS.md BOM:** `sed -i '1s/^\xEF\xBB\xBF//' ~/.hermes/workspace/AGENTS.md`
4. **Re-pair WhatsApp:** Session empty, needs QR code re-pairing via phone. WhatsApp bridge has been non-functional for 62+ days.
5. **Fix local-delivery jobs:** `mum-health-morning` and `mum-health-evening` deliver to `local` — update to a Telegram topic.
6. **Consider DNS stability:** Investigate host DNS resolver. Multi-service `getaddrinfo` failures caused the gateway crash. Temporary workaround: static DNS entries for `api.telegram.org`.

---

## 6. Retention Cleanup

- **Deleted:** None (no files older than 7 days)
- **Replaced:** `SECURITY_AUDIT_2026-07-03.md` (morning audit) → this report
- **Kept:** 8 files in workspace (Jun 26 to Jul 3 range)
- **Deduplication:** `SECURITY_AUDIT_2026-07-03-afternoon.md` should be deleted (same day, superseded)
