# Security Audit — 2026-11-09

**Generated:** 2026-11-09 by Hermes security-audit cron
**Scope:** Credential exposure · Channel integrity · Recent security events
**Overall: 🟠 DEGRADED** — Telegram fully healthy (token valid, polling healthy, topic 20 delivery confirmed). **WhatsApp bridge remains DOWN** (4th consecutive audit; WinError 5 Access-denied on every bridge start, 49 failures today alone). No new token exposure; no breach markers; no provider-key failures. Legacy `.env`-reader scripts re-appeared in the workspace tree (WARN).

---

## 1. Credential Exposure

| Check | Status | Detail |
|-------|--------|--------|
| Telegram bot token (live) | ✅ PASS | AppData root `.env` token **valid** (`getMe` → `{"ok":true}`, @Ogaitchhermesbot id 8277244378). Direct `sendMessage` to Topic 20 **succeeded** (msg 13215) — confirms token + delivery path. |
| Stale token (other root) | ⚠️ WARN | `~/.hermes/.env` holds a **dead placeholder** (`getMe` → HTTP 404). Live gateway unaffected (uses AppData root). Persistent dual-root divergence debt (8+ cycles). |
| Backup `.env` copies | ✅ PASS | **0** across `~/.hermes` backups, state-snapshots, `~/hermes-backup`, `~/.openclaw`. Sustained clean. |
| Credential caches | ✅ PASS | No `bws_cache.json`, `.secret_cache`, or token cache files in either root. |
| `.env`-reader scripts | ⚠️ WARN (NEW REGRESSION) | Nov 8 tree was clean post-deletion; **11+ scripts** now read `.env` directly across workspace (`scripts/ghana_telegram_report.py`, `memory_review_telegram.py`, `h_evening_checkin_send.py`, `mum_evening_checkin.py`; `Vault/.../MissionControl/mission_control.py`; `health/send_*.py`; plus `tmp_query_msgs.py`, `tmp_recruit_verify.py`, `tmp_recruitment_job.py`, `tmp_scan_cron.py`, `tmp_send_evening_h.py`). None contain secrets at rest (they read the token at runtime), but they leak tokens to process tables/shell history. `tmp_*.py` are test artifacts — delete. Red-teaming godmode scripts are intentional. |
| `google_token.json` ACL | ✅ PASS | `icacls` (both roots): SYSTEM / Administrators / User only (F). No "Everyone"/"BUILTIN\Users". Correct Windows default. Refresh token protected. |
| AGENTS.md BOM / invisible chars | ✅ PASS | workspace AGENTS.md: UTF-8, no BOM / invisible chars (CRLF only). Main AGENTS.md absent (not a finding). |
| config.yaml secrets | ✅ PASS | No plaintext long-lived secrets; keys referenced via env. |
| `allow_all_users: true` | ⚠️ WARN | config.yaml sets `GATEWAY_ALLOW_ALL_USERS: true` — every sender on every platform gets access. Flagged via gateway.config WARNING logs each start. Non-breach but broadens attack surface; confirm intentional. |

## 2. Channel Integrity

| Channel | Status | Detail |
|---------|--------|--------|
| Gateway process | ✅ PASS | Running (PID **34324**, python.exe, ESTABLISHED TCP to Telegram 149.154.166.110). Started 2026-11-08 19:58 `--replace`. Logs fresh (07:02). Stable. |
| Telegram adapter | ✅ PASS | **Polling healthy.** Token valid via direct `getMe`. Topic 20 delivery **verified** (`getChat` → supergroup "Agent Hermes", `is_forum: true`; sendMessage msg 13215 landed). |
| **WhatsApp** | ❌ **FAIL (PERSISTENT — 4th audit)** | **Bridge DOWN** since **2026-11-06 10:17**. Every bridge start fails: `WinError 5 Access is denied` at `bridge.js`. **49 reconnect failures today** (every 300s). `creds.json` present (Nov 6 10:09) but session not holding. Blocking Mum/Dad check-ins and 2Real poster. |
| Topic 20 (Memory Review) | ✅ PASS | Verified live this cycle (getChat + probe send). Valid delivery target. |
| Cron silent delivery | ⚠️ WARN | **25/56** jobs deliver to `origin` (16) or `local` (9) — output never reaches a user. 31 topic/channel-targeted. Unchanged. |
| Defunct-thread jobs (`telegram:123286468`) | ⚠️ WARN | **2** jobs (Mom Morning + Mom Evening Exercise Reminders) still deliver to a thread not the Nursing coord thread (424). Not remediated since 10-30. |

## 3. Recent Security Events

- **No `InvalidToken` / telegram token rejections** in live logs this window ✅ — only the stale `~/.hermes/.env` placeholder (§1) and historical bootstrap mention.
- **No provider 401/403/402/429 / InvalidKey / quota failures.** OpenRouter healthy at 07:02 (deepseek traffic, cache hit 93–99%). ✅
- **No breach / unauthorized-access markers** ✅.
- **Multiplex duplicate-credential stays RESOLVED** — no `default`/`content-buddy` credential-conflict occurrences continuing from 11-08. Gateway reconciling profiles (taiwah) without conflict. ✅
- **WhatsApp bridge `WinError 5 Access denied`** — the sole active channel failure (§2). Root-cause changed from earlier timeout; now a process-spawn permission error on `bridge.js`. Requires re-pair / perm inspection, not just restart.
- **Telegram host-level transport churn (LOW):** sticky IPv4 149.154.166.110 `ConnectTimeout` at 06:55; auto re-walked to 149.154.167.220 and recovered in <14s. Self-healing host/DNS instability, not an attack.

---

## Trend vs 2026-11-08

| Item | 11-08 | 11-09 | Direction |
|------|-------|-------|-----------|
| Telegram token (live) | PASS | PASS | No Change |
| Gateway | PASS (PID 1340) | PASS (PID 34324) | Stable |
| **WhatsApp** | FAIL (attempt 251) | FAIL (49 today; WinError 5) | No Change (persistent, 4th) |
| Dual-root divergence | WARN | WARN | No Change (persistent debt) |
| Backup `.env` copies | PASS (0) | PASS (0) | No Change |
| `.env`-reader scripts | 2 deleted → clean | **~11 re-appeared** | **Regressed** |
| Cron silent delivery | 25/56 | 25/56 | No Change |
| `telegram:123286468` thread loss | WARN | WARN | Not remediated (2 jobs) |
| Multiplex dup-credential | RESOLVED | RESOLVED | No Change |

**Persistent security debt (3+ cycles):** dual-root token divergence (8+), 25/56 silent cron targets, `telegram:123286468` thread loss, **WhatsApp bridge down (4th audit)**.
**New finding:** ~11 legacy `.env`-reader scripts re-appeared (incl. 5 `tmp_*.py` test artifacts). No active token exposure, no rejection, no breach markers.

## 🔧 Remediation Priority
1. **Restore WhatsApp** — bridge down 4th day; now `WinError 5 Access denied` on `bridge.js`, not a simple restart. Inspect bridge process permissions + QR re-pair. Blocks Mum/Dad checkins + 2Real poster (highest impact).
2. **Delete stale `~/.hermes/.env` placeholder** → single authoritative AppData root (persistent debt, 8+ cycles).
3. **Delete the 5 `tmp_*.py` test artifacts** that read `.env`; audit/replace the remaining runtime env-readers with dotenv-less helpers.
4. Fix the 2 Mom exercise-reminder jobs to keep Nursing coord thread_id 424.
5. Re-review 25/56 silent cron targets (`origin`/`local`).
6. Confirm `allow_all_users: true` is intentional; if not, restrict to known senders.

## Retention Note
Rolling 7-day window enforced. Deleted 11-01. Files retained: 11-02 … 11-09 (7). Within budget.

---
*Generated 2026-11-09 by Hermes security-audit cron.*