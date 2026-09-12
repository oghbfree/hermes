# Security Audit — 11 September 2026

**Date:** 11/09/2026
**Run by:** internal cron / Hermes Agent (default profile) — `security-policy-check` (id 1b7107630fe3)
**Overall:** **STABLE / RECOVERED** — Gateway **UP & active** (polling healthy today 04:31–06:15, processing Telegram + WhatsApp inbound). **Active AppData Telegram token VALID** (gateway `polling confirmed healthy`, `Connected to Telegram (polling mode)` 04:01). **Home-root `~/.hermes/.env` token REVOKED** (13-char, HTTP 404 on `getMe`) — dormant divergent root, unchanged debt. **Backup `.env` = 0**, credential caches **clean**, AGENTS.md **no BOM**, `google_token.json` ACL **PASS** (SYSTEM/Admin/User only). Nous Portal access/key exp **07:48 today (~48 min at audit)** — WARN (auto-refresh enabled). **No active credential compromise.** Major improvement vs 09/07: gateway recovered from DOWN→UP.

**Report path:** `C:\Users\User\.hermes\workspace\Vault\System\Assistant\SECURITY_AUDIT_2026-09-11.md`
**Telegram delivery target:** Topic 20 (`-1003784520976:20`, "Memory Review") — confirmed in `channel_directory.json` (thread_id 20).

---

## Summary

- **Gateway UP (RECOVERED)** — active `python` gateway process (ESTABLISHED TCP → `149.154.167.92:443`); fresh `AppData\Local\hermes\logs\gateway.log` shows Telegram polling healthy today (03:12 DNS flutter recovered; `Connected to Telegram (polling mode)` 04:01; inbound msgs processed 04:31–06:15). **PASS — channel live.** Prior 09/07 run reported gateway DOWN ~37h.
- **Active Telegram token VALID** — gateway actively POSTs/responses to `-1003784520976` today; no `InvalidToken` in fresh logs. **PASS.**
- **Home-root token REVOKED** — `~/.hermes/.env` token → HTTP 404 on `getMe`; stale `~/.hermes/logs/gateway.log` (09/09) carries the `InvalidToken ... 8277...ugM8 rejected` trace for that root. Dormant divergent root. **WARN (persistent debt).**
- **Credential exposure clean** — backup `.env` = **0** (backups/state-snapshots/hermes-backup/.openclaw); `bws_cache.json`/`.secret_cache` absent; AGENTS.md UTF-8 **no BOM**; home `google_token.json` ACL = SYSTEM / Builtin-Admins / Owner only (inherited), **no Everyone / BUILTIN\Users → PASS**.
- **Live `.env`-reader scripts persist** — ~16 workspace/temp + 6 root `~/..hermes/*.py` (`telegram_*.py`, `send_*.py`, `tmp_*.py`, `care_checkin.py`, `send_health_check.py`, `ghana_telegram_report.py`, `memory_review_telegram.py`, etc.) reference `.env`; most read the **revoked home token** → fail anyway. **FAIL (persists ≥3 cycles).**
- **Cron delivery** — **55 jobs**: **25 silent** (13 `local` + 12 `origin`), 30 explicit Telegram targets (7×:14, 6×:20, 4×:4, 2×:16/:26/:10/MDM 123286468, 1×:2/:8/:28). Topic 20 exists in channel directory. **WARN (silent jobs).** WhatsApp customer gate actively dispatching today → functional.
- **No active compromise** — gateway token valid at probe; no fresh `InvalidToken`/401/403 batch in current window (only 1 transient Nous auxiliary-vision 429 rate-limit with auto-rotation, auto-recovering; Vercel 200 OK).

## Findings by Area

### 1. Credential Exposure — CLEAN (caches/backups/ACLs pass; `.env`-reader debt persists)
| Item | Status |
|------|--------|
| `bws_cache.json` / `.secret_cache` | **PASS** — absent both roots |
| Backup `.env` (all trees) | **PASS** — 0 |
| AGENTS.md (workspace copy) | **PASS** — UTF-8, no BOM/invisible chars |
| `home google_token.json` ACL | **PASS** — Only System/Admins/Owner (inherited); no Everyone |
| Active AppData gateway token | **PASS/VALID** — polling healthy today |
| Home-root `~/.hermes/.env` token | **WARN/FAIL-debt** — revoked (HTTP 404); dormant divergent root |
| Live `.env`-reader scripts | **FAIL (PERSISTS ≥3 cycles)** — ~22 home/workspace/temp `.py` referencing `.env` |

### 2. Channel Integrity — STABLE (gateway recovered)
- **Telegram gateway** — ✅ **PASS/RECOVERED**: active process, ESTABLISHED TCP, polling healthy, inbound processed today.
- **Active token** — ✅ PASS (gateway functioning with it; no fresh rejection).
- **WhatsApp** — ✅ functional today (customer-gate dispatches logged); channel live via gateway.
- **Cron delivery** — ⚠️ WARN: 55 jobs, 25 silent (13 local + 12 origin); 30 explicit telegram-targets; Topic 20 target valid.

### 3. Recent Security Events — NO ACTIVE THREAT
- **No token compromise**: active gateway token valid; `InvalidToken` appears only in stale `~/.hermes/logs/gateway.log` (09/09, revoked home-root token) — not in the live AppData log.
- **DNS flutter** 03:12 today (getaddrinfo failed) → self-recovered (polling restarted → healthy). Recurring host-level name resolution, not attack pattern.
- **Provider status**: no 400/401/402/403 rejections; single transient Nous auxiliary-vision 429 (rate limit, auto-rotating to alternates) → WARN/minor.

## FAIL Findings
| ID | Severity | Description | Persistent? |
|----|----------|-------------|-------------|
| 1 | **high (≥3 cycles)** | **Dual-`.env` divergence** — AppData active root valid; home-root `~/.hermes/.env` revoked (404) & referenced by many task scripts. | Yes |
| 2 | **high (≥3 cycles)** | **Live `.env`-reader scripts** (~22) read revoked home token → impure/fail; needs rewrite to AppData env or retire. | Yes |
| 3 | **medium (≥3 cycles)** | **25/55 cron jobs deliver silent** (13 `local` + 12 `origin`). | Yes |

## WARN Findings
1. Nous Portal access/key expiry **07:48 today** — within 48 min of audit; auto-refresh enabled; gateway healthy so refresh path available.
2. **25/55 silent cron delivery** (13 `local` + 12 `origin`).
3. Home-root `.env` token revoked — consolidate or retire root.
4. Transient Nous auxiliary-vision 429 rate-limit today (auto-recovered via alternates).

## Remediation Priority
1. **HIGH** — Consolidate/retire home-root `~/.hermes/.env` (revoked token) to remove dual-root divergence; align task scripts to AppData valid env.
2. **HIGH** — Rewrite/retire the ~22 `.env`-reader scripts (delivery depends on gateway now, which is healthy).
3. **MED** — Re-point 25 silent cron jobs to explicit topic targets.
4. **MED** — Confirm Nous Portal key auto-refresh at 07:48 expiry (gateway healthy, expected OK).

## Trend vs 07/09
| Item | 07/09 | This run (11/09) | Trend |
|---|---|---|---|
| Gateway | ❌ DOWN (~37h) | ✅ **UP/RECOVERED** (polling healthy today) | **Improved** |
| AppData token valid | ✅ getMe ok | ✅ active (gateway polling healthy) | Stable |
| Home token | revoked | revoked | No Change |
| Backup `.env` | 0 | 0 | Good |
| Live `.env`-readers | ~38 | ~22 (scoped scan) | Improved scan/debt |
| Cron silent | 25/55 | 25/55 | No Change |
| WhatsApp | creds present | **functional** (dispatches today) | **Improved** |

**Persistent security debt (≥3 cycles):** dual `.env` divergence, live `.env`-reader scripts, silent cron delivery. Gateway debt **cleared** (recovered).

## Delivery
Summary delivered to Telegram topic 20 ("Memory Review") via the active gateway (healthy, valid token). Home-root revoked token NOT used for delivery.

---
*Masked: all secrets printed as provider-prefix + truncated. No full tokens echoed.*