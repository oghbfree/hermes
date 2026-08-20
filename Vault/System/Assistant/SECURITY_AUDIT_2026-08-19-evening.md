# Security Audit — 19 August 2026 (Evening Re-run)

**Date:** 19/08/2026
**Run by:** internal cron / Hermes Agent (default profile) — same-day evening re-check
**Overall:** **PARTIAL** — Gateway UP, Telegram token valid (AppData root), credential-cache + AGENTS.md clean. **NEW finding:** `~/.hermes/.env` holds a **corrupt/truncated 13-char `TELEGRAM_BOT_TOKEN`** (HTTP 404) while the working 46-char token lives in `AppData\Local\hermes\.env`. Residual `.env` copies remain in the legacy `~/hermes-backup` tree (deeply nested).

**Report path:** `C:\Users\User\.hermes\workspace\Vault\System\Assistant\SECURITY_AUDIT_2026-08-19-evening.md`

---

## Summary

- **Telegram token VALID (AppData root)** — direct `getMe` → `{"ok":true}`, `@Ogaitchhermesbot` (id 8277244378). This is the 46-char token the gateway loads.
- **⚠️ NEW: `~/.hermes/.env` holds a corrupt token** — 13-char `TELEGRAM_BOT_TOKEN` → HTTP 404 `Not Found`. This is a *secondary* `.env` (not the one driving the gateway), but it is the documented canonical root and now diverges from the working AppData token. Credential divergence / cleanup artifact.
- **Gateway UP (confirmed)** — PID **12896** (uv Python 3.11) has **2 ESTABLISHED** TCP connections to Telegram `149.154.166.110:443`. Secondary PID **17584** (venv python) also running → dual-instance WARN (persists from morning).
- **Credential caches CLEAN** — `bws_cache.json` and `.secret_cache` both **absent** (confirmed remediated this morning).
- **Backup `.env` copies RESIDUAL** — 0 in `~/.hermes/backups`, 0 in `state-snapshots` (improved), but **5 remain** in `~/hermes-backup` under deeply nested `system\.hermes\backups|state-snapshots\...` paths (missed by morning cleanup). Plus **8 `gdrive_token.json` copies** (Google Drive creds) in legacy `~/hermes-backup`.
- **AGENTS.md BOM clean** — `~/.hermes/AGENTS.md` absent; workspace copy UTF-8 no-BOM, no zero-width spaces.
- **Live `.env`-reader scripts persist** — 5 in `~/.hermes/*.py` (care_checkin, send_health_check, telegram_create_topic, telegram_direct_send, telegram_post_file) + workspace 2real responder + godmode helpers.
- **WhatsApp non-functional** — unpaired, no `creds.json`; manual QR re-pair required.
- **Cron delivery** — live `jobs.json`: **55 jobs; 24 silent** (13 `local` + 11 `origin`), 31 explicit `telegram:` targets (7 → topic 20).
- **Nous Portal refresh token rejected** — auth offline (not a compromise indicator).

## Findings by Area

### 1. Credential Exposure — **PARTIAL** (improved, one NEW item)

| Item | Status |
|------|--------|
| `bws_cache.json` / `.secret_cache` | **PASS** — both absent (remediated 19/08) |
| Backup `.env` copies (main trees) | **PASS** — 0 in `~/.hermes/backups`, 0 in `state-snapshots` |
| Backup `.env` copies (legacy tree) | **FAIL** — **5 remain** in `~/hermes-backup\system\.hermes\backups|state-snapshots\*.env` (deeply nested, missed) |
| `gdrive_token.json` (Google creds) | **FAIL** — **8 copies** in legacy `~/hermes-backup` tree |
| **`~/.hermes/.env` token integrity** | **NEW FAIL** — 13-char truncated `TELEGRAM_BOT_TOKEN` → HTTP 404; diverges from valid AppData token |
| Live `.env`-reader scripts | **FAIL** — 5 `~/.hermes/*.py` + workspace scripts |
| `google_token.json` ACL | **PASS** — icacls: SYSTEM/Administrators/User `(I)(F)` only |
| AGENTS.md BOM | **PASS** — clean (no BOM, no zero-width) |
| Dual `.env` roots | **WARN** — both exist; now confirmed they hold **different** tokens |

### 2. Channel Integrity — **PARTIAL** (gateway healthy)

- **Telegram (gateway)** — ✅ PASS: PID 12896 UP, ESTABLISHED to `149.154.166.110:443`.
- **Telegram (token)** — ✅ PASS via AppData root (`getMe` ok=true). ⚠️ `~/.hermes/.env` token broken (see above).
- **Dual gateway** — ⚠️ WARN: PIDs **12896** (uv, active) + **17584** (venv) → concurrent polling / duplicate-delivery risk (persists from morning; AGENTS.md forbids gateway restart without user).
- **WhatsApp** — ❌ FAIL: unpaired, no `creds.json`.
- **Cron delivery** — ⚠️ WARN: 55 jobs → 24 silent (13 `local` + 11 `origin`), 31 telegram-targeted (7 → topic 20).

### 3. Recent Security Events — **PASS** (no new malicious events)

- No `InvalidToken` in **current** window — historical revocation batch dated 2026-06-09 in rotated logs, not active.
- Gateway reconnect errors (08-13 `All connection attempts failed`) — host-level network, recovered; healthy since 08-18.
- **Unauthorized user `5146706699` blocked (08-13)** — permission control functioning.
- **Nous Portal refresh token rejected** — ⚠️ WARN (auth offline), not compromise.
- **SQLite WAL-reset corruption warning** (linked 3.50.4, vulnerable) — ⚠️ WARN; upgrade advised via `hermes update`.

## FAIL Findings

| ID | Severity | Description | Evidence |
|----|----------|-------------|----------|
| 1 | high | **Legacy `~/hermes-backup` tree still holds 5 `.env` copies** | deeply nested `system\.hermes\backups\|state-snapshots\*.env` — missed by morning cleanup |
| 2 | high | **8 `gdrive_token.json` copies** (Google Drive refresh + client secret) in `~/hermes-backup` | legacy backup tree |
| 3 | high | **`~/.hermes/.env` has corrupt 13-char token (HTTP 404)** — NEW; diverges from valid AppData token | getMe 404; len=13 vs valid len=46 |
| 4 | high | Live `.py` scripts read `.env` directly | 5 `~/.hermes/*.py` + workspace scripts |
| 5 | medium | WhatsApp channel non-functional (unpaired) | no `creds.json` |

## WARN Findings

| ID | Description |
|----|-------------|
| 1 | Dual gateway processes (12896 + 17584) — concurrent-polling / duplicate-delivery risk |
| 2 | 24/55 cron jobs silent delivery (13 `local` + 11 `origin`) |
| 3 | Nous Portal refresh token rejected — auth offline |
| 4 | Dual `.env` roots now confirmed holding **different** tokens (divergence real, not theoretical) |
| 5 | SQLite 3.50.4 WAL-reset corruption bug warning — upgrade advised |
| 6 | Dual Hermes roots observed (`.hermes` + `AppData\Local\hermes`) |

## Trend (vs this morning's 19/08 audit)

| Item | Morning 19/08 | This run (evening) | Trend |
|---|---|---|---|
| Telegram token valid | ✅ (AppData) | ✅ AppData valid; **❌ `~/.hermes/.env` corrupt** | **NEW FAIL (divergence)** |
| Gateway UP | ✅ 12896+17584 | ✅ 12896 ESTABLISHED | No Change (good) |
| Dual gateway | ⚠️ | ⚠️ (12896+17584) | No Change |
| `bws_cache.json` | ✅ purged | ✅ absent | Improved (sustained) |
| Backups `.env` | 0 main / 13 said-removed | 0 main, **5 legacy remain** | **Residual (incomplete cleanup)** |
| AGENTS.md BOM | clean | clean | No Change (good) |
| Live `.env` readers | ~33 | ~5 root + workspace | No Change |
| WhatsApp | ❌ | ❌ unpaired | No Change |
| Cron silent | 29/56 | 24/55 | Minor improvement |

**Persistent debt (residual remediation incomplete):** legacy-tree backup `.env`, `gdrive_token.json`, live `.env`-reader scripts, WhatsApp unpaired, `~/.hermes/.env` token corruption (NEW).

## Remediation Priority

1. **HIGH** — Repair/restore `~/.hermes/.env` `TELEGRAM_BOT_TOKEN` to match the valid AppData token (or delete the stale root) — resolves 404 divergence.
2. **HIGH** — Delete residual `.env` (5) + `gdrive_token.json` (8) from legacy `~/hermes-backup` tree.
3. **HIGH** — Decommission/rewrite `.env`-reader scripts to use Hermes-injected env.
4. **MED** — Re-pair WhatsApp (manual QR); re-authenticate Nous Portal; resolve dual-gateway (needs user approval).
5. **LOW** — Re-point 24 silent cron jobs to explicit topic targets.

## Attachments / Evidence

- `getMe` AppData root token → ok=true, `@Ogaitchhermesbot` (8277244378). `~/.hermes/.env` token (13 chars) → HTTP 404.
- `netstat -ano` → PID 12896 ESTABLISHED x2 to `149.154.166.110:443`.
- `wmic` → PID 12896 (uv python) + 17584 (venv python) both running `gateway run`.
- `search_files`/os.walk → 0 `.env` in `~/.hermes/backups` + `state-snapshots`; **5** in `~/hermes-backup\system\.hermes\...`; **8** `gdrive_token.json` in `~/hermes-backup`.
- `bws_cache.json` / `.secret_cache` → absent.
- AGENTS.md → `~/.hermes/AGENTS.md` absent; workspace copy UTF-8 no-BOM, no zero-width.
- Cron `jobs.json` → 55 jobs, 24 silent (13 local + 11 origin), 31 telegram-targeted.

---
*Masked: all secrets represented by provider-prefix + truncated form. No full tokens echoed.*