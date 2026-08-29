# Security Audit — 28 August 2026

**Date:** 28/08/2026
**Run by:** internal cron / Hermes Agent (default profile)
**Overall:** **STABLE** — Gateway RUNNING (PID 19936), Telegram + WhatsApp connected, polling healthy. Telegram token VALID on the active AppData root (verified by successful getUpdates generation 5). No credential compromise events. **Persisting debt:** dual-root `.env` divergence, live `.env`-reader scripts, 25/57 cron jobs silent delivery, Nous Portal expiry imminent. **Notable improvement:** legacy backup credential files reduced 26 → 9.

**Report path:** `C:\Users\User\.hermes\workspace\Vault\System\Assistant\SECURITY_AUDIT_2026-08-28.md`
**Telegram delivery target:** Topic 20 (`telegram:-1003784520976:20`), verified supergroup forum previously via `getChat`; 7 cron jobs target topic 20.

---

## Summary

- **Channel health GREEN** — gateway PID **19936** alive (2 ESTABLISHED TCP connections to Telegram 149.154.166.110:443). `gateway_state.json` = `running`; telegram `connected` (updated 08-27 13:34), whatsapp `connected` (08-25 08:35). `gateway.log` fresh (**09:50 today**), Telegram **polling confirmed healthy: getUpdates progressing (generation 5)** at 09:50:50 — this requires a valid bot token, authoritatively confirming runtime token validity.
- **Transient network events, not credential** — repeated `getaddrinfo failed` / `All connection attempts failed` reconnect cycles across 08-25, 08-27 and 09:50 today (attempt 3/10) that all **self-recovered**. Two `NEEDS_ATTENTION` flags (08-25, 08-27, "22 attempts / 2.0 hours") were raised and cleared. Pattern is host-level DNS/network flakiness (errno 11004 getaddrinfo + IPv4 path failures), **not** InvalidToken/401 rejections.
- **No InvalidToken/Unauthorized/401 credential rejections** in current-day logs. Rotated logs (`.log.1`) contain only reconnect-attempt markers and a hardline-blocked audit curl from 08-17 — no genuine token revocation.
- **Credential caches CLEAN** — `bws_cache.json` / `.secret_cache` absent.
- **Backup trees** — main trees 0 `.env` copies (PASS). **Legacy `~/hermes-backup` IMPROVED: 9 google_token.json copies** (was 26 at 24/08 — gdrive_token & gdrive_credentials copies eliminated).
- **`google_token.json` ACL correct** — SYSTEM / Administrators / User `(I)(F)` only, no Everyone/Users group. PASS.
- **AGENTS.md** — main `~/.hermes/AGENTS.md` absent; workspace copy UTF-8 (no BOM). PASS.
- **Live `.env`-reader scripts remain (FAIL debt)** — workspace/scripts `send_ghana_report.py`, `memory_review_telegram.py`, Vault family health scripts incl. new `_token_test_2026-08-25.py`, 3 root `send_*.py`.
- **Cron delivery** — **57 jobs; 25 silent** (13 `local` + 12 `origin`), 32 explicit `telegram:` targets (7 → topic 20, present). No change vs 24/08.
- **Nous Portal** — access/key expiry **2026-08-28 10:50** (~1h from audit time) — WARN; refresh enabled.

## Findings by Area

### 1. Credential Exposure — **PARTIAL** (caches clean, backups improved; two persistent Fails)

| Item | Status |
|------|--------|
| `bws_cache.json` / `.secret_cache` | **PASS** — absent |
| Backup `.env` in main trees | **PASS** — 0 |
| `google_token.json` ACL | **PASS** — icacls SYSTEM/Administrators/User `(I)(F)` only |
| AGENTS.md BOM | **PASS** — workspace UTF-8 no BOM; main absent |
| **Runtime Telegram token (AppData root)** | **PASS/VALID** — polling health gen 5 confirms acceptance |
| Legacy Google token copies (`~/hermes-backup`) | **WARN (IMPROVED)** — 9 google_token.json (was 26; gdrive copies cleared) |
| Live `.env`-reader scripts | **FAIL (PERSISTS)** — workspace/scripts + Vault family scripts + 3 root send_*.py; new `_token_test_2026-08-25.py` reads `Path.home()/.hermes/.env` directly |
| Dual `.env` roots (credential divergence) | **WARN** — AppData holds valid runtime token; home-root `~/.hermes/.env` referenced by scripts is the truncated/corrupt copy |

### 2. Channel Integrity — **GOOD** (gateway stable)

- **Telegram (gateway)** — ✅ PASS: PID 19936 running, `connected`, polling healthy (getUpdates generation 5, 09:50 today), live TCP to 149.154.166.110:443.
- **Telegram (token)** — ✅ PASS on active AppData root (polling syncs = valid). Ongoing reconnect churn is DNS/network (errno 11004), not credential.
- **WhatsApp** — ✅ PASS: `creds.json` present (2950 B, mtime 08-25 12:33), state `connected`.
- **Cron delivery** — ⚠️ WARN: 57 jobs → 25 silent (13 `local` + 12 `origin`), 32 telegram-targeted (7 → topic 20).

### 3. Recent Security Events — **NO COMPROMISE** (one WARN)

- **No** new `InvalidToken` / `Unauthorized` / `Revoked` / `401` on current-day active-root logs. Rotated logs contain only reconnect markers and a 08-17 block, no genuine revocation.
- Recurrent Telegram reconnect cycles (08-25, 08-27, 09:50 today) = host-level DNS/network flakiness (getaddrinfo 11004, IPv4 path failures), all self-recovered by sticky-IPv4 fallback. Supplementary notes: the 08-25 and 08-27 `NEEDS_ATTENTION` flags were later cleared by successful reconnect (`✓ telegram reconnected 13:34`).
- Nous Portal token expiry within ~1h (10:50 today) — refresh enabled, low risk but monitor.

## FAIL Findings

| ID | Severity | Description | Evidence |
|----|----------|-------------|----------|
| 1 | high | **Live `.py` scripts read `.env` directly** (workspace/scripts send_ghana_report.py, memory_review_telegram.py; Vault/family/mum + H health scripts incl. `_token_test_2026-08-25.py`; 3 root send_*.py) — leak tokens to process table/history/logs | grep across live trees |
| 2 | high | **Credential divergence: dual `.env` roots** — AppData holds valid token; `~/.hermes/.env` (referenced by task scripts) is the truncated/corrupt copy | status + script env_path |
| 3 | medium | **25/57 cron jobs silent delivery** (13 `local` + 12 `origin`) | jobs.json delivery audit |

## WARN Findings

| ID | Description |
|----|-------------|
| 1 | Legacy `~/hermes-backup` still holds 9 `google_token.json` credential files (improved from 26, but not yet purged) |
| 2 | Nous Portal token expiry 10:50 today (~1h) — refresh enabled; verify rotation succeeds |
| 3 | Host-level Telegram DNS/network flakiness recurring (08-25, 08-27, 09:50 today) — self-recovering, but disruptive; consider host DNS review |
| 4 | `tmp_afternoon_health_check.py` (+ a few scratch health scripts) stale/unused in Vault — safe to delete |

## Trend (vs 24/08 audit)

| Item | 24/08 | This run (28/08) | Trend |
|---|---|---|---|
| Gateway | ✅ running (PID 20344) | ✅ running (PID 19936) | Stable / sustained |
| Telegram token valid (AppData) | ✅ | ✅ (polling gen 5) | Stable |
| WhatsApp | ✅ paired | ✅ paired | Stable |
| `bws_cache` | absent | absent | Good (sustained) |
| Backup `.env` (main) | 0 | 0 | Good (sustained) |
| Legacy token copies (backup) | **26** | **9** (google only) | **IMPROVED** |
| Live `.env` readers | present | present (+new `_token_test`) | No Change (debt) |
| Cron silent | 25/57 | 25/57 | No Change |
| AGENTS.md BOM / cleanup | clean | clean | Good |

**Persistent security debt (3+ cycles):** live `.env`-reader scripts; dual-root credential divergence; silent cron delivery (unchanged).

## Remediation Priority

1. **HIGH** — Rewrite/retire `.env`-reader task scripts to use Hermes-injected env or `hermes send`; delete root `send_*.py` and `_token_test_2026-08-25.py`.
2. **HIGH** — Consolidate/repair `~/.hermes/.env`: align `TELEGRAM_BOT_TOKEN` with the valid AppData token, or retire the stale root entirely.
3. **MED** — Purge remaining 9 legacy `google_token.json` copies from `~/hermes-backup`.
4. **MED** — Re-point 25 silent cron jobs to explicit topic targets (esp. 8 → topic 14, 13 `local`).
5. **LOW** — Confirm Nous Portal auto-refresh executes at ~10:50 today; monitor host DNS flakiness.

## Delivery
Summary posted to Telegram topic 20 via the live gateway (running, connected, token valid).

---

*Masked: all secrets shown as provider-prefix + truncated form. No full tokens echoed.*