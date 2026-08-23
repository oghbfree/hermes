# Security Audit — 22 August 2026

**Date:** 22/08/2026
**Run by:** internal cron / Hermes Agent (default profile)
**Overall:** **PARTIAL** — Gateway UP and polling Telegram (verified via live PID 26336 + ESTABLISHED TCP to `149.154.166.110:443`), valid working token in AppData root (`getMe` ok=true), credential caches clean, AGENTS.md/config clean. **Persisting FAIL items:** `~/.hermes/.env` holds a corrupt 13-char `TELEGRAM_BOT_TOKEN` (HTTP 404, diverges from valid AppData token), 18 Google/GDrive token copies remain in legacy `~/hermes-backup`, live `.env`-reader scripts remain, WhatsApp unpaired.

**Report path:** `C:\Users\User\.hermes\workspace\Vault\System\Assistant\SECURITY_AUDIT_2026-08-22.md`

---

## Summary

- **Gateway UP (verified)** — `hermes status` reports PID **26336**; `tasklist /FI "PID eq 26336"` confirms `python.exe` alive (238 MB), with **ESTABLISHED** TLS connections to Telegram `149.154.166.110:443`. Status accurately reflects reality this cycle.
- **Telegram token VALID (AppData root)** — direct `getMe` → `{"ok":true}`, `@Ogaitchhermesbot` (46-char token). This is the token the gateway loads and the correct one for delivery.
- **⚠️ `~/.hermes/.env` holds corrupt token (PERSISTS)** — 13-char `TELEGRAM_BOT_TOKEN` (no colon) → HTTP 404 `Not Found`; diverges from the valid AppData token. Same finding as 21/08; **not yet remediated (3rd consecutive audit)**.
- **Credential caches CLEAN** — `bws_cache.json` and `.secret_cache` both absent. `google_token.json` ACL proper (SYSTEM/Administrators/User `(I)(F)` only). AGENTS.md & config.yaml clean (no BOM, no zero-width/RTL).
- **Main-tree backups CLEAN** — 0 `.env` in `~/.hermes/backups`, `state-snapshots`, `.openclaw`. **Legacy `~/hermes-backup` `.env` copies RESOLVED** (was 7 → now 0; improvement). **GDrive/Google tokens PERSIST** (18 copies: 8 `gdrive_token.json` + 10 `google_token.json`).
- **Cron delivery** — live `jobs.json` (`AppData\Local\hermes\cron`): **56 jobs; 25 silent** (13 `local` + 12 `origin`), 31 explicit `telegram:` targets (7 → topic 20, verified present as supergroup forum via `getChat`).
- **WhatsApp NON-FUNCTIONAL** — unpaired, no `creds.json` in either session path.
- **Nous Portal refresh token rejected** — auth offline (`This refresh token was already rejected`), not a compromise indicator.

## Findings by Area

### 1. Credential Exposure — **PARTIAL** (improved; two persists)

| Item | Status |
|------|--------|
| `bws_cache.json` / `.secret_cache` | **PASS** — both absent |
| Backup `.env` copies (main trees) | **PASS** — 0 in `~/.hermes/backups`, `state-snapshots`, `.openclaw` |
| Backup `.env` copies (legacy `~/hermes-backup`) | **PASS (IMPROVED)** — was 7 on 21/08, now **0** |
| Google/GDrive token copies (legacy) | **FAIL (PERSISTS)** — **18 copies** (8 `gdrive_token.json` + 10 `google_token.json`) |
| **`~/.hermes/.env` token integrity** | **FAIL (PERSISTS, 3rd cycle)** — 13-char truncated `TELEGRAM_BOT_TOKEN` → HTTP 404; diverges from valid AppData token |
| Live `.env`-reader scripts | **FAIL (PERSISTS)** — `~/.hermes/*.py` (care_checkin, send_health_check, telegram_create_topic, telegram_direct_send, telegram_post_file) + workspace/Vault scripts |
| `google_token.json` ACL | **PASS** — icacls: SYSTEM/Administrators/User `(I)(F)` only |
| AGENTS.md BOM / zero-width / RTL | **PASS** — clean (workspace copy no-BOM; `~/.hermes/AGENTS.md` absent) |
| Dual `.env` roots | **WARN** — both exist and hold **different** tokens (divergence real) |
| Nous Portal token | **WARN** — refresh token rejected (auth offline) |

### 2. Channel Integrity — **PARTIAL** (gateway healthy)

- **Telegram (gateway)** — ✅ PASS: PID 26336 alive, 2 ESTABLISHED to `149.154.166.110:443`.
- **Telegram (token)** — ✅ PASS via AppData root (`getMe` ok=true). ⚠️ `~/.hermes/.env` token broken (see above).
- **Telegram (group)** — ✅ PASS: `getChat` → `type=supergroup`, `is_forum=true` (topic delivery valid).
- **WhatsApp** — ❌ FAIL: unpaired, no `creds.json`.
- **Cron delivery** — ⚠️ WARN: 56 jobs → 25 silent (13 `local` + 12 `origin`), 31 telegram-targeted (7 → topic 20; topic verified present).

### 3. Recent Security Events — **PASS** (no new malicious events)

- No `InvalidToken` in the current window (historical revocations in older rotated logs only).
- No repeated unauthorized-access events in current window.
- **Gateway crash signature** — `ImportError: cannot import name 'get_context_length_from_provider_error' from 'agent.model_metadata'` + 7 `asyncio.run.exception` entries in `gateway-exit-diag.log`; gateway last clean log date 08-18 (report a WARN, correlated with 08-18 gateway.start overwritten). Live ESTABLISHED connections confirm current instance supersedes the crashed one.
- **SQLite WAL-reset corruption warning** (linked 3.50.4, vulnerable → 3.51.3+) — ⚠️ WARN; upgrade via `hermes update`.
- OpenRouter `openrouter/owl-alpha` HTTP 404 + 401 from 08-04 — stale config issue, not current security concern.

## FAIL Findings

| ID | Severity | Description | Evidence |
|----|----------|-------------|----------|
| 1 | high | **18 Google/GDrive token copies in legacy `~/hermes-backup`** (8 `gdrive_token.json` + 10 `google_token.json`) | `find` across legacy backup tree |
| 2 | high | **`~/.hermes/.env` has corrupt 13-char token (HTTP 404)** — PERSISTS 3rd cycle; diverges from valid AppData token | getMe 404; len=13 vs valid len=46 |
| 3 | high | Live `.py` scripts read `.env` directly | 5 `~/.hermes/*.py` + workspace + Vault scripts |
| 4 | medium | WhatsApp channel non-functional (unpaired) | no `creds.json`; state fatal |

## WARN Findings

| ID | Description |
|----|-------------|
| 1 | 25/56 cron jobs silent delivery (13 `local` + 12 `origin`) |
| 2 | Dual `.env` roots hold **different** tokens (divergence real) |
| 3 | Nous Portal refresh token rejected — auth offline |
| 4 | SQLite 3.50.4 WAL-reset corruption bug — upgrade advised |
| 5 | Gateway `ImportError` crash signature + 7 asyncio crash entries (08-14/08-18) |

## Trend (vs 21/08 audit)

| Item | 21/08 | This run (22/08) | Trend |
|---|---|---|---|
| Gateway UP | ✅ 26304 | ✅ 26336 ESTABLISHED to Telegram | No Change (healthy) |
| Telegram token valid | ✅ AppData; ❌ `.hermes` corrupt | ✅ AppData; ❌ `.hermes` corrupt | **No Change (debt persists)** |
| `bws_cache.json` | absent | absent | Good (sustained) |
| Backup `.env` (main) | 0 | 0 | Good (sustained) |
| Backup `.env` (legacy) | 7 | **0** | **IMPROVED (+7 gone)** |
| Google tokens (legacy) | 8 gdrive + google | **18 total (8 gdrive + 10 google)** | **Worsened/uncertain count** |
| AGENTS.md BOM | clean | clean | Good |
| Live `.env` readers | ~5 root + workspace | ~5 root + workspace | No Change |
| WhatsApp | ❌ | ❌ unpaired | No Change |
| Cron silent | 24/55 | 25/56 | Roughly No Change |

**Persistent security debt (3+ cycles):** `~/.hermes/.env` token corruption (3rd cycle), legacy Google/GDrive token copies (many), WhatsApp unpaired (many), live `.env`-reader scripts (many).

## Remediation Priority

1. **HIGH** — Repair `~/.hermes/.env` `TELEGRAM_BOT_TOKEN` to match the valid AppData token, or remove the stale root `.env` divergence.
2. **HIGH** — Delete residual Google/GDrive token copies (18) from legacy `~/hermes-backup` tree.
3. **HIGH** — Decommission/rewrite `.env`-reader scripts to use Hermes-injected env.
4. **MED** — Re-pair WhatsApp (manual QR); re-authenticate Nous Portal.
5. **LOW** — Re-point 25 silent cron jobs to explicit topic targets.

## Attachments / Evidence

- `getMe` AppData root token → ok=true, `@Ogaitchhermesbot`. `~/.hermes/.env` token (13 chars) → HTTP 404.
- `tasklist` → PID 26336 alive (238 MB). `netstat -ano` → 2 ESTABLISHED to `149.154.166.110:443`.
- `find` → 0 `.env` in main trees + legacy; **18** Google/GDrive token copies in legacy.
- `getChat` → supergroup + is_forum=true. `bws_cache.json`/`.secret_cache` → absent. `google_token.json` → icacls proper.
- Cron `jobs.json` → 56 jobs, 25 silent, 31 telegram-targeted (7 → topic 20).

---
*Masked: all secrets represented by provider-prefix + truncated form. No full tokens echoed.*