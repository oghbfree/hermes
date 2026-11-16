# Security Audit — 2026-11-15

**Generated:** 2026-11-15 07:00 by Hermes security-audit cron (*security-policy-check* job)
**Scope:** Credential exposure · Channel integrity · Recent security events
**Overall: 🟢 HEALTHY** — Telegram fully healthy (live 46-char token VALID via direct `getMe` @Ogaitchhermesbot; gateway PID 2272 with ESTABLISHED TCP to Telegram; polling confirmed via getUpdates at 05:00). **WhatsApp bridge RECOVERED** (creds.json live-refreshed today 07:01; WhatsApp agent messages in gateway.log 05:39) — resolves the 7-audit persistent FAIL. No backup-`.env` copies (0), no token exposure, no credential caches, no breach markers, no provider-key failures this window. Remaining items are longstanding WARNs (dual-root token divergence, 25/56 silent cron targets, 2 dead-thread jobs).

---

## 1. Credential Exposure

| Check | Status | Detail |
|-------|--------|--------|
| Telegram bot token (live, AppData root) | ✅ PASS | `getMe` → `{"ok":true}` (@Ogaitchhermesbot, 46-char live token). Token valid via direct API. |
| Stale token (`~/.hermes/.env`) | ⚠️ WARN | Still holds the **13-char dead placeholder**; `getMe` → HTTP 404. Live gateway uses AppData root. Persistent dual-root divergence debt (12+ cycles). |
| Backup `.env` copies | ✅ PASS | **0** across `~/.hermes` + AppData backups, state-snapshots, `~/hermes-backup`, `~/.openclaw`. Sustained clean. |
| Credential caches | ✅ PASS | No `bws_cache.json`, `.secret_cache`, or token-cache files in either root. |
| `.env`-reader scripts | ⚠️ WARN | No new leaks in `workspace/*.py` (scan clean). Runtime cron senders (`scripts/ghana_telegram_report.py`, `memory_review_telegram.py`, `MissionControl/`, `health/send_*.py`) still read `.env` at runtime — tokens transiently enter process/shell state, none at rest. |
| `google_token.json` ACL (both roots) | ✅ PASS | SYSTEM / Administrators / User only (F). No Everyone/Users. Correct Windows default. |
| `.env` ACLs (both roots) | ✅ PASS | SYSTEM / Administrators / User only (F). |
| AGENTS.md BOM / invisible chars | ✅ PASS | workspace AGENTS.md: UTF-8, no BOM (CRLF). Main `~/.hermes/AGENTS.md` absent. |
| `allow_all_users` (config.yaml) | ⚠️ WARN | `GATEWAY_ALLOW_ALL_USERS: true` broadens attack surface; confirm intentional. |

## 2. Channel Integrity

| Channel | Status | Detail |
|---------|--------|--------|
| Gateway process | ✅ PASS | Running (PID **2272**, python.exe, ~862 MB). Live ESTABLISHED TCP to Telegram (149.154.166.110:443) via netstat. gateway.log fresh (last write 06:19). 0 crash-loop entries. |
| Telegram adapter | ✅ PASS | Polling healthy. Live token valid; `getUpdates progressing` confirmed 05:00. Sticky IPv4 path active. Transient network flakiness 10–14 Nov (getaddrinfo/timeouts/dual-stack re-walks) recovered to sticky IPv4 — host-level network, not channel outage. |
| **WhatsApp** | ✅ **PASS (RECOVERED)** | **Bridge UP.** creds.json live-refreshed **2026-11-15 07:01**; gateway flushing WhatsApp agent messages today (05:39), no pairing errors. Closes the FAIL first logged 11-06 (7 audits). |
| Topic 20 (Memory Review) | ✅ PASS | Valid supergroup target; 5 jobs deliver to thread 20 (this job included). |
| Cron silent delivery | ⚠️ WARN | **25/56** jobs deliver to `origin` (16) or `local` (9) — output never reaches a user; 31 topic-targeted. Unchanged. |
| Defunct-thread jobs (`telegram:123286468`) | ⚠️ WARN | **2** jobs (Mom Morning + Mom Evening Exercise Reminders) still target a dead thread. Not remediated. |

## 3. Recent Security Events

- ✅ **No `InvalidToken` / Telegram token rejection** this window. Live token accepted by Telegram. Only the stale `~/.hermes/.env` placeholder (§1) is dead.
- ✅ **No provider 401/403/402/429 / InvalidKey failures.** One transient OpenRouter `Connection error` (04:54) retried and recovered — network blip, not credential.
- ✅ **No breach / unauthorized-access markers** (no "Blocked unauthorized user", no unexpected paired devices).
- ✅ **Multiplex duplicate-credential stays RESOLVED** — no `default`/`content-buddy` conflict occurrences.
- ⚠️ Host-level network flakiness 10–14 Nov (Telegram dual-stack/IPv4 failures, OpenRouter connection errors) — consistent with DNS/networking, not a targeted event.
- **WhatsApp resolution** — bridge recovered (re-pair held, blocks lifted 14-Nov 02:56); sole active channel failure cleared.

---

## Trend vs 2026-11-12

| Item | 11-12 | 11-15 | Direction |
|------|-------|-------|-----------|
| Telegram token (live) | PASS | PASS | No Change |
| Gateway | PASS (PID 16696) | PASS (PID 2272, live TCP) | Stable |
| **WhatsApp** | FAIL (attempt 86) | **PASS (RECOVERED)** | **IMPROVED** |
| Dual-root token divergence | WARN | WARN | No Change (persistent, 12+) |
| Backup `.env` copies | PASS (0) | PASS (0) | No Change |
| `.env`-reader scripts | runtime remain | runtime remain (workspace clean) | No Change |
| Cron silent delivery | 25/56 | 25/56 | No Change |
| `telegram:123286468` thread loss | WARN (2) | WARN (2) | Not remediated |
| Multiplex dup-credential | RESOLVED | RESOLVED | No Change |
| `google_token.json` ACL | PASS | PASS | No Change |

**Persistent security debt (3+ cycles):** dual-root token divergence (12+), 25/56 silent cron targets, `telegram:123286468` thread loss. **WhatsApp removed from debt.** One clear improvement this cycle (WhatsApp).

## 🔧 Remediation Priority
1. **Delete stale `~/.hermes/.env` placeholder** → single authoritative AppData root (persistent debt, 12+ cycles).
2. Fix the 2 Mom exercise-reminder jobs to the Nursing coord thread (424) — `123286468` target is dead.
3. Re-review 25/56 silent cron targets (`origin`/`local`).
4. Confirm `allow_all_users: true` is intentional; restrict if not.

## Retention Note
Rolling 7-day window enforced. Removed 11-06 (oldest); retained: 11-07 … 11-12 + 11-15 (7). No audits were produced 11-13/11-14 (jobs failed offline) — this run also closes that gap.

---
*Generated 2026-11-15 by Hermes security-audit cron.*