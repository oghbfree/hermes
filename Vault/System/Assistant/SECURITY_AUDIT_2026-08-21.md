# Security Audit — 21 August 2026

**Date:** 21/08/2026
**Run by:** internal cron / Hermes Agent (default profile)
**Overall:** **PARTIAL** — Gateway UP and polling Telegram (verified via live PID + ESTABLISHED TCP), valid working token in AppData root, credential caches clean, AGENTS.md clean. **Persisting FAIL items:** legacy `~/hermes-backup` tree still holds `.env`/`gdrive_token.json` credential copies, `~/.hermes/.env` holds a corrupt 13-char `TELEGRAM_BOT_TOKEN` (HTTP 404, diverges from valid AppData token), WhatsApp unpaired, live `.env`-reader scripts remain.

**Report path:** `C:\Users\User\.hermes\workspace\Vault\System\Assistant\SECURITY_AUDIT_2026-08-21.md`

---

## Summary

- **Gateway UP (verified)** — `hermes status` reports PID **26304**; `tasklist` confirms the process is alive (293 MB), with **13 ESTABLISHED** TCP connections including **2 to Telegram `149.154.166.110:443`**. Status accurately reflects reality this cycle. `gateway.log` is stale since 08-18 (new PID writes elsewhere), but live connections confirm active polling.
- **Telegram token VALID (AppData root)** — direct `getMe` → `{"ok":true}`, `@Ogaitchhermesbot` (id 8277244378), 46-char token. This is the token the gateway loads and the one to use for delivery.
- **⚠️ `~/.hermes/.env` holds corrupt token (PERSISTS)** — 13-char `TELEGRAM_BOT_TOKEN` → HTTP 404 `Not Found`; diverges from the valid AppData token. Same finding as 08-19 evening; **not yet remediated** (2nd consecutive audit).
- **Credential caches CLEAN** — `bws_cache.json` and `.secret_cache` both absent. `google_token.json` ACL proper (SYSTEM/Administrators/User `(I)(F)` only). AGENTS.md clean (`~/.hermes/AGENTS.md` absent; workspace copy no-BOM, no zero-width).
- **Backup `.env` copies (main trees) CLEAN** — 0 in `~/.hermes/backups`, 0 in `state-snapshots`, 0 in `~/.openclaw`.
- **Legacy tree residual FAIL** — `~/hermes-backup` still holds **7 `.env` copies** (deeply nested `system\.hermes\backups|state-snapshots\...`) + **8 `gdrive_token.json`** (Google Drive creds) + **8 `gdrive_token.json`** copies flagged. Persisting, incomplete cleanup.
- **Cron delivery** — live `jobs.json`: **55 jobs; 24 silent** (13 `local` + 11 `origin`), 31 explicit `telegram:` targets (7 → topic 20, which exists in `channel_directory.json`).
- **WhatsApp NON-FUNCTIONAL** — unpaired, no `creds.json` (fatal state in `gateway_state.json`).
- **Nous Portal refresh token rejected** — auth offline (`This refresh token was already rejected`), not a compromise indicator.

## Findings by Area

### 1. Credential Exposure — **PARTIAL** (main trees clean; legacy + divergence persist)

| Item | Status |
|------|--------|
| `bws_cache.json` / `.secret_cache` | **PASS** — both absent |
| Backup `.env` copies (main trees) | **PASS** — 0 in `~/.hermes/backups`, `state-snapshots`, `.openclaw` |
| Backup `.env` copies (legacy tree) | **FAIL** — **7 remain** in `~/hermes-backup\system\.hermes\...` (deeply nested) |
| `gdrive_token.json` (Google creds) | **FAIL** — **8 copies** in legacy `~/hermes-backup` tree |
| **`~/.hermes/.env` token integrity** | **FAIL (PERSISTS)** — 13-char truncated `TELEGRAM_BOT_TOKEN` → HTTP 404; diverges from valid AppData token |
| Live `.env`-reader scripts | **FAIL** — `~/.hermes/*.py` (care_checkin, send_health_check, telegram_create_topic, telegram_direct_send, telegram_post_file) + workspace scripts + godmode helpers |
| `google_token.json` ACL | **PASS** — icacls: SYSTEM/Administrators/User `(I)(F)` only |
| AGENTS.md BOM / zero-width | **PASS** — clean |
| Dual `.env` roots | **WARN** — both exist and hold **different** tokens (divergence real) |
| Nous Portal token | **WARN** — refresh token rejected (auth offline) |

### 2. Channel Integrity — **PARTIAL** (gateway healthy)

- **Telegram (gateway)** — ✅ PASS: PID 26304 alive, 2 ESTABLISHED to `149.154.166.110:443`.
- **Telegram (token)** — ✅ PASS via AppData root (`getMe` ok=true). ⚠️ `~/.hermes/.env` token broken (see above).
- **WhatsApp** — ❌ FAIL: `gateway_state.json` = `fatal` / `whatsapp_not_paired`, no `creds.json`.
- **Cron delivery** — ⚠️ WARN: 55 jobs → 24 silent (13 `local` + 11 `origin`), 31 telegram-targeted (7 → topic 20; topic verified present in `channel_directory.json`).

### 3. Recent Security Events — **PASS** (no new malicious events)

- No `InvalidToken` in the current window (historical revocation in older rotated logs only).
- **Unauthorized user `5146706699` blocked (08-13)** — permission control functioning; not repeated since.
- **SQLite WAL-reset corruption warning** (linked 3.50.4, vulnerable → 3.51.3+) — ⚠️ WARN; upgrade via `hermes update`.
- OpenRouter **`openrouter/owl-alpha` HTTP 404** (08-04, `security-policy-check` job) — model de-listed, config issue not security.

## FAIL Findings

| ID | Severity | Description | Evidence |
|----|----------|-------------|----------|
| 1 | high | **7 `.env` copies in legacy `~/hermes-backup` tree** | deeply nested `system\.hermes\backups\|state-snapshots\*.env` |
| 2 | high | **8 `gdrive_token.json` copies** (Google creds) in `~/hermes-backup` | legacy backup tree |
| 3 | high | **`~/.hermes/.env` has corrupt 13-char token (HTTP 404)** — PERSISTS 2nd cycle; diverges from valid AppData token | getMe 404; len=13 vs valid len=46 |
| 4 | high | Live `.py` scripts read `.env` directly | 5 `~/.hermes/*.py` + workspace scripts |
| 5 | medium | WhatsApp channel non-functional (unpaired) | no `creds.json`; state=fatal |

## WARN Findings

| ID | Description |
|----|-------------|
| 1 | 24/55 cron jobs silent delivery (13 `local` + 11 `origin`) |
| 2 | Dual `.env` roots hold **different** tokens (divergence real) |
| 3 | Nous Portal refresh token rejected — auth offline |
| 4 | SQLite 3.50.4 WAL-reset corruption bug — upgrade advised |
| 5 | Dual Hermes roots (`.hermes` + `AppData\Local\hermes`) |

## Trend (vs 19/08 evening audit)

| Item | 19/08 evening | This run (21/08) | Trend |
|---|---|---|---|
| Gateway UP | ✅ 12896 (~12896+17584) | ✅ 26304 ESTABLISHED | No Change (healthy) |
| Telegram token valid | ✅ AppData; ❌ `.hermes` corrupt | ✅ AppData; ❌ `.hermes` corrupt | **No Change (debt persists)** |
| `bws_cache.json` | absent | absent | Good (sustained) |
| Backup `.env` (main) | 0 | 0 | Good (sustained) |
| Backup `.env` (legacy) | 5 | **7** | **Worsened (+2)** |
| `gdrive_token.json` (legacy) | 8 | **8** | No Change |
| AGENTS.md BOM | clean | clean | Good |
| Live `.env` readers | ~5 root + workspace | ~5 root + workspace | No Change |
| WhatsApp | ❌ | ❌ unpaired | No Change |
| Cron silent | 24/55 | 24/55 | No Change |

**Persistent security debt (2+ consecutive cycles):** `~/.hermes/.env` token corruption (2), legacy-tree `.env` + `gdrive_token` copies (many), WhatsApp unpaired (many), live `.env`-reader scripts (many).

## Remediation Priority

1. **HIGH** — Repair/restore `~/.hermes/.env` `TELEGRAM_BOT_TOKEN` to match the valid AppData token, or delete the stale root (resolves 404 divergence).
2. **HIGH** — Delete residual `.env` (7) + `gdrive_token.json` (8) from legacy `~/hermes-backup` tree (now worsened +2).
3. **HIGH** — Decommission/rewrite `.env`-reader scripts to use Hermes-injected env.
4. **MED** — Re-pair WhatsApp (manual QR); re-authenticate Nous Portal.
5. **LOW** — Re-point 24 silent cron jobs to explicit topic targets.

## Attachments / Evidence

- `getMe` AppData root token → ok=true, `@Ogaitchhermesbot` (8277244378). `~/.hermes/.env` token (13 chars) → HTTP 404.
- `tasklist` → PID 26304 alive (293 MB). `netstat -ano` → 13 ESTABLISHED conns incl 2 to `149.154.166.110:443`.
- `os.walk` → 0 `.env` in main backup trees; **7** in `~/hermes-backup\system\.hermes\...`; **8** `gdrive_token.json`.
- `bws_cache.json` / `.secret_cache` → absent. `google_token.json` → icacls proper.
- Cron `jobs.json` → 55 jobs, 24 silent, 31 telegram-targeted (7 → topic 20; topic present in `channel_directory.json`).

---
*Masked: all secrets represented by provider-prefix + truncated form. No full tokens echoed.*
