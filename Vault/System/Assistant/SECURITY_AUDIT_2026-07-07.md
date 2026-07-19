# Security Audit — 2026-07-07

**Date:** `2026-07-07`
**Run by:** internal cron / Hermes Agent
**Overall:** 🟡 MODERATE FAIL — 4 FAIL items (1 CRITICAL escalation), 3 WARN

---

## Summary

| Category | Status | Details |
|----------|--------|---------|
| Credential Exposure | 🔴 CRITICAL | **49 backup .env copies** across 4 locations (UP from 29) |
| Channel Integrity | 🟢 PASS | **Gateway RECOVERED** — PID 17112 running 12.5h with 3 Telegram connections |
| Recent Security Events | 🟡 WARN | Config drift v29→v33, AGENTS.md BOM, WhatsApp 68d unpaired |

---

## 1. Credential Exposure

### 🔴 CRITICAL: 49 Backup .env Copies (PERSISTENT — 12+ cycles, WORSENED)

| Location | Count |
|----------|-------|
| `~/.hermes/backups/` | 27 (UP from 25) |
| `~/.hermes/state-snapshots/` | 4 |
| `~/.openclaw/.env` | 1 (NEW finding) |
| `~/hermes-backup/` | 17 (NEW finding — outside Hermes tree) |
| **TOTAL** | **49** |

- All contain raw API keys (OpenRouter, Telegram, Google, Firecrawl, Brave, xAI, etc.)
- **Increased from 29 (Jul 6) → 49 (Jul 7)** — +20 from newly discovered `hermes-backup/` and `~/.openclaw/` locations
- **PERSISTENT SECURITY DEBT — escalated to CRITICAL (12 cycles)**

### 🟢 PASS: Credential Cache Files
- `bws_cache.json`: Not found ✅ (9th consecutive cycle clean)
- `.secret_cache`: Not found ✅

### 🟢 PASS: google_token.json ACL
- `icacls` shows Owner: (I)(F), SYSTEM: (I)(F), Administrators: (I)(F) ✅

### 🟡 WARN: Workspace AGENTS.md UTF-8 BOM
- `~/.hermes/workspace/AGENTS.md`: **UTF-8 with BOM** ❌ (prompt injection risk)
- Main `~/.hermes/AGENTS.md`: Does not exist ✅

### 🟢 PASS: Telegram Bot Token Valid
- `getMe` returns `{"ok":true}` — bot @Ogaitchhermesbot active ✅
- No `InvalidToken` events in current logs ✅

### 🔴 FAIL: test_threads.py Directly Reads .env
- `~/.hermes/test_threads.py` (878 bytes, Jun 11) reads `TELEGRAM_BOT_TOKEN` from `.env` for topic discovery test
- Credential exposure risk — script should be deleted after use

### 🟢 PASS: Config/Jobs JSON — No BOM
- `config.yaml`, `cron/jobs.json`, `AppData/Local/hermes/config.yaml` — all clean ✅

---

## 2. Channel Integrity

### 🟢 PASS: Gateway RECOVERED (SIGNIFICANT IMPROVEMENT)
- **PID 8924 (zombie since Jun 18) GONE** — replaced by **PID 17112**
- **PID 17112**: python.exe, started **2026-07-06 18:25 UTC** (12.5 hours uptime)
- **3 ESTABLISHED connections** to Telegram (`149.154.166.110:443`)
- **Polling mode** — no webhook configured
- **Child process**: node.exe (PID 17784) — likely assistant bridge
- Token validated via `getMe` and `getWebhookInfo` — fully operational
- The old `gateway.log` (last updated Jun 18) belongs to the previous gateway instance — new gateway logs via different mechanism

### 🟢 PASS: Telegram Topic 20 Verified
- `getChat`: supergroup, `is_forum: true`
- Test message sent successfully (msg_id=8486) ✅
- Topic 20 confirmed existing and routable

### 🟡 WARN: WhatsApp Unpaired (68+ Days)
- `~/.hermes/whatsapp/session/creds.json`: **MISSING**
- WhatsApp bridge npm deps: 1 critical, 2 high, 2 moderate vulns
- 68 days without re-pair attempt

### 🟡 WARN: 27/40 Jobs Silent Delivery
- 25 jobs `deliver=origin` — output stays on machine
- 2 jobs `deliver=local` — no external delivery
- 13 jobs target Telegram topics (now deliverable again with recovered gateway)
- Affected: mum-health, dad-health, health-check, content-engine, security-policy-check, daily-briefing, etc.

### 🟢 DNS Healthy
- `api.telegram.org` resolves ✅ (149.154.166.110)
- `openrouter.ai` resolves ✅
- Prior DNS failure pattern (9077 entries) all from Jun 18 — resolved

---

## 3. Recent Security Events

### 🟢 Resolved: Gateway Crash Loop (ModuleNotFoundError)
- 7 prior crashes (Jun 22–Jul 1) with `concurrent_log_handler` ModuleNotFoundError
- **RESOLVED** — something fixed the Python 3.14 dependency or the process was recovered under Python 3.11
- PID 17112 runs under Python 3.11 (uv-managed), NOT Python 3.14

### 🟢 No Breach Markers
- No unauthorized access patterns detected
- No token revocation events (current token valid)
- No traffic redirection evidence
- No `InvalidToken` events in current logs

### 🟡 WARN: Config Version Drift
- v29 → v33 (worsened from v29→v32 on Jul 6)
- Run `hermes doctor --fix` to migrate

### 🟡 WARN: hermes status Reports 47 Jobs, jobs.json Has 40
- 7 job discrepancy persists — likely ephemeral/in-memory jobs
- Not security-critical but signals state drift

### 🟡 WARN: Config Staleness
- No cron logs being produced (cron logs dir absent)
- agenet.log, errors.log, gateway.log last updated Jun 18 (old instance)

---

## 4. Trend vs Prior Audit (2026-07-06)

| Finding | Jul 6 | Jul 7 | Change |
|---------|-------|-------|--------|
| Backup .env copies | 🔴 29 (CRITICAL) | 🔴 **49** (CRITICAL) | 🔴 **Worsening (+20) — expanded scope** |
| Gateway status | 🔴 Dead 17.6d (zombie) | 🟢 **RECOVERED** (PID 17112, 12.5h) | ✅ **Major improvement** |
| Gateway crash attempts | 7 (last Jul 1) | **Resolved** | ✅ **Fixed** |
| WhatsApp unpaired | 66+ days | **68+ days** | 🔴 Worsening |
| AGENTS.md BOM (workspace) | 🔴 FAIL | 🟡 WARN | No change |
| Config drift | v29→v32 (WARN) | v29→**v33** (WARN) | 🔴 Worsening |
| bws_cache.json | ✅ Clean | ✅ Clean | No change |
| DNS health | ✅ Resolves | ✅ Resolves | No change |
| 27/40 silent jobs | 🔴 FAIL | 🟡 WARN | Improved (gateway now available) |
| Telegram token | ✅ Valid | ✅ Valid | No change |
| Topic 20 | N/A | ✅ Verified exists | ✅ Verified |
| test_threads.py credential leak | ✅ None flagged | 🔴 FAIL | **Regressed** |
| OpenClaw + hermes-backup .envs | 🔴 Not checked | 🔴 18 copies found | 🔴 **New discovery** |

### Persistent Security Debt (12+ cycles unremediated)
- **Backup `.env` copies** — 49 copies, 12+ cycles, CRITICAL — **scope expanded**
- **WhatsApp unpaired** — 68+ days
- **AGENTS.md workspace BOM** — 6+ cycles
- **Config drift** — worsened v29→v33

### Escalating Items
- **Backup .env copies**: Now 49 total after discovering `hermes-backup/` and `~/.openclaw/` locations. Scope expanded significantly.
- **test_threads.py**: New credential-leaking artifact discovered.

### De-escalating Items
- **Gateway**: From 🔴 FAIL to 🟢 PASS — fully recovered and operational
- **Cron delivery**: Now potentially functional (gateway available to route messages)

---

## 5. Recommendations

### IMMEDIATE
1. **🔴 CRITICAL — Delete ALL backup .env copies (49!):**
   ```bash
   find ~/.hermes/backups -name ".env" -delete
   find ~/.hermes/state-snapshots -name ".env" -delete
   find ~/hermes-backup -name ".env" -delete
   rm -f ~/.openclaw/.env
   ```

2. **🔴 HIGH — Delete credential-leaking scripts:**
   ```bash
   rm -f ~/.hermes/test_threads.py
   ```

3. **🔴 HIGH — Strip AGENTS.md BOM:**
   ```bash
   sed -i '1s/^\xEF\xBB\xBF//' ~/.hermes/workspace/AGENTS.md
   ```

4. **🟡 HIGH — Update config:**
   ```bash
   hermes doctor --fix
   ```

### MEDIUM
5. **Fix cron delivery targets**: Migrate 27 `origin`/`local` jobs to Telegram topics now that gateway is available
6. **Re-pair WhatsApp**: 68+ days unpaired — needs QR code pairing
7. **Delete old OpenClaw .env**: Ensure secrets are migrated to Hermes `.env` first

---

## 6. Retention Cleanup

- **7-day window:** Keep files Jun 30 – Jul 7
- **Files to retain:**
  - SECURITY_AUDIT_2026-07-01.md
  - SECURITY_AUDIT_2026-07-02.md
  - SECURITY_AUDIT_2026-07-03.md
  - SECURITY_AUDIT_2026-07-04.md
  - SECURITY_AUDIT_2026-07-05.md
  - SECURITY_AUDIT_2026-07-06.md
  - SECURITY_AUDIT_2026-07-07.md (this report)

- **Files to delete (out of 7-day window):**
  - SECURITY_AUDIT_2026-06-29.md (older than 7 days)

- **Deleted this session:**
  - SECURITY_AUDIT_2026-06-29.md (7-day window — removed)