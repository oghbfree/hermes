# Security Audit — 03 September 2026

**Date:** 03/09/2026
**Run by:** internal cron / Hermes Agent (default profile)
**Overall:** **DEGRADED** — Gateway **STOPPED/DOWN** (last Telegram disconnect 02/09 17:19, no gateway process; ~14 h downtime at audit). Root cause = **host-level DNS instability** (`getaddrinfo failed`, 2300+ hits this week; NOT a compromise). Active runtime token **VALID** (`getMe` ok:true → `Ogaitchhermesbot`), WhatsApp **paired** (creds present, fresh 01/09 11:29), caches & backup `.env` clean, no `InvalidToken`/401 this window. **Persisting debt:** ~18 live `.env`-reader scripts (home root, using revoked-token `.env`), credential divergence (home token revoked 404), 25/55 cron jobs silent delivery, legacy google_token copies (12). **NEW this cycle:** Gateway down (was running 01/09).

**Report path:** `C:\Users\User\.hermes\workspace\Vault\System\Assistant\SECURITY_AUDIT_2026-09-03.md`
**Telegram delivery target:** Topic 20 (`-1003784520976:20`,`thread_id` 20,"Agent Hermes" group, present in home channel_directory).

 Gateway down → delivery via direct Bot API (AppData token, VALID).



---

## Summary

- **Gateway DOWN** — `hermes status` = "stopped"; PID **14576** (prior running) + **16820** (home, "starting") both **dead**. Only `hermes_cli.main serve` processes run (desktop agent). Last live Telegram activity: **Disconnected 02/09 17:19:26** — all 8 connect attempts failed on `[Errno 11004] getaddrinfo failed`. Downtime ≈13.7 h at 07:02. **FAIL — channel integrity broken for gateway-mediated delivery.**
- **Host-level DNS instability (root cause)** — `getaddrinfo failed`: gateway.log **2397**, errors.log **1273** this week; Telegram reconnect flagged NEEDS_ATTENTION (2h+ continuous failure at 01/09 14:07 & 02/09 16:34); multi-service affected (Vercel MCP parked 02/09 19:25–19:45 DNS, revived 19:53). Recurrent host/network issue, not targeted attack. WARN (worsening).
- **Runtime token VALID (active))** — APPDATA `.env` token: direct `getMe` → `{"ok":true}` (`Ogaitchhermesbot`). **Home-root token REVOKED** — HTTP 404 (dormant root, known divergence). WARN.
.
credential divergence persists.

- **WhatsApp PAIRED** — APPDATA session dir: `creds.json` (2950 B, 01/09 11:29), baileys state fresh through 01/09. PASS (against prior "connected".
- **Credential caches CLEAN** — `bws_cache.json` / `.secret_cache` absent (both roots). PASS (sustained.
.
absent
.
**Backup `.env`** — **0** across `~/.hermes/backups`, `~/.hermes/state-snapshots`, `~/hermes-backup`, `~/.openclaw`. PASS (sustained).
- **Legacy google_token copies** — **12** (10 `hermes-backup` + 2 `~/.hermes/backups`;(+1 vs 11. WARN.
-. **`google_token.json` ACL (home)** — SYSTEM / Administrators / User `(I)(F)` only,, no Everyone/Users. Active(AppData) google_token absent. PASS..
- **AGENTS.md** — main `~/.hermes/AGENTS.md` + AppData variants absent; workspace copy UTF-8, CRLF, **no BOM**, no invisible chars. PASS.
- **Live `.env`-reader scripts (FAIL debt)** — **~18 live files** in HOME root tree: `workspace/scripts/send_ghana_report.py`,`memory_review_telegram.py`,`ghana_telegram_report.py`; `Vault/family/mum/health/*checkin*.py` (7)+`tmp_afternoon_send.py` +`_token_test_2026-08-25.py`; root `send_health_check.py`,`telegram_direct_send.py`,`telegram_create_topic.py`,`telegram_post_file.py`,`scripts/test_paths.py`. All read `~/.hermes/.env` — whose token is **REVOKED (404)** → these direct-send scripts would fail today.
  AppData workspace scan: **0** env-readers (active root clean..
- **Cron delivery** — **55 jobs (APPDATA source-of-truth); 25 silent(13 `local` + 12 `origin`), 30 explicit telegram targets. Home `~/.hermes/cron/jobs.json` absent (jobs registered under AppData root.. WARN..
- **Nous Portal** — access/key expiry **2026-09-03 07:47:32** (~45 min from audit time 07:02.) — WARN;, refresh enabled.

## Findings by Area

### 1. Credential Exposure — PARTIAL (caches/backups clean; FAIL debt persists)
| Item | Status |
|------|--------|
| `bws_cache.json` / `.secret_cache` | **PASS** — absent both roots |
| Backup `.env` (all trees) | **PASS** — 0 |
| `google_token.json` ACL (home) | **PASS** — SYSTEM/Administrators/User `(I)(F)` only; active-root file absent |
| AGENTS.md BOM / invisible chars | **PASS** — UTF-8, no BOM |
| Active runtime token (AppData) | **PASS/VALID** — getMe ok `Ogaitchhermesbot` |
| Home-root `~/.hermes/.env` token | **WARN** — revoked (HTTP 404); dormant divergent root |
| Legacy google_token copies | **WARN** — 12 (10 hermes-backup + 2 internal),+1 |
| Live `.env`-reader scripts | **FAIL (PERSISTS,≥3 cycles)** — ~18 (home root, referencing revoked-token `.env`; AppData clean |

### 2. Channel Integrity — DEGRADED (gateway down)
- **Gateway** — ❌ **FAIL**: stopped; PID firsters dead; last disconnect 02/09 17:19 (DNS). ~14 h down.
- **Telegram (token, active)** — ✅ PASS: getMe ok; Topic 20 present (home cdir;). AppData `channel_directory.json` does not enumerate topic 20 — catalog drift, (prior known.)
- **WhatsApp** — ✅ PASS: paired (creds.json,state fresh 01/09).
- **Cron delivery** — ⚠️ WARN: 55 jobs → 25 silent(13 `local` + 12 `origin`), 30 telegram-targeted. Gateway down blocks gateway-mediated telegram delivery this window.

### 3. Recent Security Events — NO COMPROMISE (channel outage + DNS)
- **No** new `InvalidToken` / `Unauthorized` / 401 in active logs this window; `gateway.log.1` InvalidToken count **0**. Token clean..
- **Vercel MCP 401** (01/09) — **resolved/not re-observed**; replaced by DNS-driven Vercel park (02/09 19:25–19:45, revived 19:53). Improved.

- **Host-level DNS failure recurrence** — `getaddrinfo failed` 2300+; gateway-down root cause; not a compromise. WARN (worsening.
.
**No credential compromise detected.**
- Access control(enforcement added 08-13 allowlist) — no new unauthorized-user events this window. Good.


## FAIL Findings
| ID | Severity | Description | Persistent? |
|----|----------|-------------|-------------|
| 1 | **high (NEW)** | **Gateway DOWN/stopped** — PID 14576/16820 dead,last Telegram disconnect 02/09 17:19 via `getaddrinfo failed`; no gateway process; gateway-mediated delivery blocked | No (up 01/09) |
| 2 | high (PERSISTS,≥3 cycles) | **~18 live `.py` scripts read `.env` directly** (home-root workspace/Vault/root), referencing a REVOKED token — leak + broken delivery | Yes |
| 3 | high (PERSISTS,≥3 cycles) | **Credential divergence: dual `.env` roots** — AppData valid;home-root REVOKED (404) but referenced by task scripts | Yes |
| 4 | medium (PERSISTS,≥3 cycles) | **25/55 cron jobs silent delivery** (13 `local` + 12 `origin`) | Yes |

## WARN Findings
| ID | Description |
|----|-------------|
| 1 | **Host-level DNS instability (`getaddrinfo failed`)** — gateway.log 2397 / errors.log 1273; recurring multi-service outages; root cause of gateway down |
| 2 | Nous Portal access/key expiry **07:47:32 today** (~45 min at audit) — confirm auto-refresh (gateway down may affect refresh path) |
| 3 | 12 legacy `google_token.json` (10 hermes-backup + 2 internal),+1 — not purged |
| 4 | Home-root `.env` token revoked — dormant root should be consolidated or retired |
| 5 | AppData `channel_directory.json` does not enumerate topic 20 (home cdir does) — catalog drift |
| 6 | `gateway_state.json` stale — reports "running" pid 14576 (dead) — status-vs-reality mismatch |

## CRITICAL Escalations
None escalated this cycle (gateway down is NEW, up 01/09; the 3 persistent debt items remain high/medium,monitored ≥3 cycles as persistent security debt.)

## Trend Comparison (vs 01/09 audit)
| Item |  ‌‌01/09 | This run (03/09) | Trend |
|---|---|---|---|
| Gateway | ✅ running (PID 14576) | ❌ **STOPPED/DOWN** (~14h) | **Degraded (NEW)** |
| Telegram token valid (active) | ✅ getMe ok | ✅ getMe ok `Ogaitchhermesbot` | Stable |
| Home-root token | revoked (404) | revoked (404) | No Change |
| WhatsApp | ✅ connected/reconnected | ✅ paired (creds 01/09) | Stable |
| `bws_cache` / caches | clean | clean | Good (sustained) |
| Backup `.env` | 0 | 0 | Good (sustained) |
| Legacy google_token copies | 9+2 | 10+2 | Slight worsening(+1 |
| Live `.env` readers | ~17 | ~18 | No Change (debt) |
| Vercel MCP auth | **401 (new)** | absent (DNS park instead) | Improved/Resolved |
| DNS `getaddrinfo failed` | present | 2300+ (worsening) | Worsening (root-cause of gateway down) |
| Cron silent | 25/55 | 25/55 | No Change |

**Persistent security debt (≥3 cycles):** live `.env`-reader scripts; credential divergence (dual roots); silent cron delivery.

## Remediation Priority
1. **HIGH (URGENT)** — Restart gateway (`hermes gateway run --replace`,Python 3.11 path); resolve host DNS instability (flapping getaddrinfo — check resolver/DNS servers/`hosts`; consider Telegram IP pinning 149.154.166/167.. Restores all Telegram delivery.
2. **HIGH** — Rewrite/retire `.env`-reader scripts (home root); these read a REVOKED token and our failing anyway. Delete dated one-offs (`_token_test_2026-08-25.py`,`tmp_afternoon_send.py`,`test_paths.py`)..
3. **HIGH** — Align home-root `~/.hermes/.env` `TELEGRAM_BOT_TOKEN` with valid AppData token, or retire stale root (token revoked..
4. **MED** — Purge legacy `google_token.json` (12 copies.. 
5. **MED** — Re-point 25 silent cron jobs to explicit topic targets; reconcile AppData channel_directory his home cdir.
; confirm Nous Portal refresh at 07:47.


## Delivery
Gateway down → summary posted to Telegram topic 20 via **direct Bot API** (Pattern A, AppData token VALID;verified `getMe` ok;Topic 20 present in home cdir).

## Retention Note
Report retained in `Vault/System/Assistant/` per job directive; rolling 7-day window: 7 files(on rolling basis.. No cleanup required this cycle(7 files,, all distinct dates..

---
*Masked: all secrets shown as provider-prefix + truncated form. No full tokens echoed.*