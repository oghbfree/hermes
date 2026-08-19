# Security Audit — 19 August 2026

**Date:** 19/08/2026
**Run by:** internal cron / Hermes Agent (default profile)
**Overall:** **FAIL → PARTIAL** (post-remediation re-check). **Credential cleanup performed 19/08 (user-authorized):** `bws_cache.json` purged, `~/.hermes/.env.bak` deleted, **13 backup `.env` copies** removed across all backup trees (hermes/backups, state-snapshots, hermes-backup, openclaw). Live `.env` + AppData root `.env` verified intact. Remaining FAILs: live `.env`-reader scripts (~33) + WhatsApp unpaired. Telegram token **VALID**, gateway **UP** (PID 12896), **NEW WARN:** dual gateway process confirmed.

**Report path:** `C:\Users\User\.hermes\workspace\Vault\System\Assistant\SECURITY_AUDIT_2026-08-19.md`

---

## Summary

- **Telegram bot token VALID** — direct `getMe` → `{"ok":true}`, `@Ogaitchhermesbot` (id 8277244378). No current `InvalidToken` in window.
- **Topic 20 (Memory Review) VERIFIED** — present in `channel_directory.json` (chat `-1003784520976`, thread 20). Delivery target valid.
- **Gateway UP (confirmed)** — PID **12896** (uv Python 3.11, `gateway run`) has **ESTABLISHED** TCP connections to Telegram `149.154.166.110:443`. **NEW:** a second gateway process also running (PID **17584**, `hermes-agent\venv` python, `gateway run`) → dual-instance risk (WARN).
- **Backup `.env` copies STABLE** — **13 total** (2 `~/.hermes/backups` + 10 `~/hermes-backup` + 1 `~/.openclaw`), flat vs 18/08.
- **Plaintext cache persists (CRITICAL)** — `bws_cache.json` (1224 B, updated 18/08 09:32) holds plaintext service keys; survives `.env` rotation.
- **Live `.env`-reader scripts persist** — ~33 total (5 `~/.hermes/*.py` + ~28 workspace `*.py`).
- **Live `.env.bak`** — plaintext backup (25 KB, dated 19/07) in live home directory (HIGH).
- **Channels affected:** WhatsApp **non-functional** (fatal `whatsapp_not_paired`, no `creds.json` — manual QR re-pair required).
- **Cron delivery:** 56 jobs; **29 silent** (14 `local` + 15 `origin`), 27 explicit `telegram:` targets (3 → topic 20).

## Findings by Area

### 1. Credential Exposure — **FAIL**

| Item | Status |
|------|--------|
| Backup `.env` copies | **FAIL (STABLE)** — 13 total (2 backups, 10 hermes-backup, 1 openclaw), flat vs 18/08 |
| Plaintext cache `bws_cache.json` | **FAIL** — present (1224 B, 18/08 09:32), plaintext service keys |
| Live `.env`-reading scripts | **FAIL** — 5 `~/.hermes/*.py` + ~28 workspace → ~33 total |
| `~/.hermes/.env.bak` (live) | **FAIL** — plaintext `.env` backup in live home dir |
| `google_token.json` ACL | **PASS** — icacls: SYSTEM/Administrators/User `(I)(F)` only; no Everyone/Users |
| `.secret_cache` | **PASS** (absent) |
| AGENTS.md BOM | **PASS** — main `~/.hermes/AGENTS.md` absent; workspace copy clean UTF-8, no BOM |
| Dual `.env` roots | **WARN** — both `~/.hermes/.env` (24.9 KB) and `AppData\Local\hermes\.env` (552 B) exist → divergence risk |

Verdict: **PARTIAL (improved)** — critical cache + `.env.bak` + 13 backup copies **resolved 19/08**; live `.env`-reader scripts remain (pending).

### 2. Channel Integrity — **FAIL** (partial)

- **Telegram (token)** — ✅ PASS: valid via `getMe`.
- **Gateway process** — ✅ PASS with caveat: PID 12896 alive, ESTABLISHED connections to Telegram. **NEW WARN:** second gateway (PID 17584, venv python) also running concurrently → potential dual-polling/duplicate delivery.
- **WhatsApp** — ❌ FAIL: fatal `whatsapp_not_paired`, no `creds.json`; manual QR re-pair required.
- **Cron delivery** — ⚠️ WARN: 56 jobs → 27 explicit `telegram:` targets (3 topic 20), **29 silent** (14 `local` + 15 `origin`).

### 3. Recent Security Events — **PASS**

- No `InvalidToken` / token revocation in current window; token currently valid.
- **Unauthorized user blocked (08-13)** — `[Telegram] Blocked unauthorized user 5146706699` — permission control functioning.
- Transient Telegram polling reconnects (08-13) — host-level network; recovered; clean connected since 08-18.
- **Nous Portal refresh token rejected** — ⚠️ WARN: auth provider offline (`This refresh token was already rejected`), not credential compromise.

## FAIL Findings

| ID | Severity | Description | Evidence |
|----|----------|-------------|----------|
| 1 | critical | Plaintext credential cache `bws_cache.json` (service keys) | ✅ **RESOLVED 19/08** — purged |
| 2 | high | Live `.py` scripts read `.env` directly (~33 total) | 5 `~/.hermes/*.py` + ~28 workspace (pending) |
| 3 | high | `~/.hermes/.env.bak` plaintext backup in live dir | ✅ **RESOLVED 19/08** — deleted |
| 4 | medium | WhatsApp channel non-functional (unpaired) | no `creds.json`; fatal state (pending) |
| 5 | medium | 13 backup `.env` copies remain (STABLE, not declining) | ✅ **RESOLVED 19/08** — 13/13 deleted |

## WARN Findings

| ID | Description |
|----|-------------|
| 1 | **NEW** Dual gateway processes (PID 12896 + PID 17584) → concurrent polling / duplicate-delivery risk |
| 2 | 29/56 cron jobs silent delivery (14 `local` + 15 `origin`) |
| 3 | Nous Portal refresh token rejected — auth offline |
| 4 | Dual `.env` roots (`~/.hermes/.env` + `AppData\Local\hermes\.env`) — divergence risk |
| 5 | SQLite WAL-reset corruption bug warning (3.50.4) — flagged by hermes_state; upgrade advised |

## Trend Comparison (vs 18/08 evening audit)

| Item | 18/08 | This run (19/08) | Trend |
|---|---|---|---|
| Telegram token valid | ✅ | ✅ | No Change (good) |
| Gateway online | ✅ UP (16640) | ✅ UP (12896) | No Change (good) |
| Dual gateway process | single | **dual (12896+17584)** | **NEW WARN** |
| Topic 20 present | verified | ✅ verified | No Change (good) |
| WhatsApp paired | ❌ | ❌ | No Change |
| Backup `.env` copies | 13 | **13** | No Change (stable) |
| `bws_cache.json` | present | present | No Change (critical) |
| Live `.env` readers | ~31 | ~33 | No Change |
| Cron silent delivery | 29/56 | 29/56 | No Change |
| InvalidToken in window | none | none | No Change (good) |
| Google token ACL | PASS | PASS | No Change (good) |

**Persistent security debt (3+ consecutive audits, FAIL, unremediated):** `bws_cache.json` plaintext cache, live `.env`-reader scripts, live `.env.bak`, backup `.env` copies, WhatsApp unpaired. **Escalation note:** these are long-standing (10+ cycles) — treat as persistent debt requiring scheduled remediation.

## Remediation Priority (updated 19/08 — cleanup performed)

1. ✅ **DONE** — Purge `bws_cache.json` (removed 19/08).
2. ✅ **DONE** — Delete `~/.hermes/.env.bak` (removed 19/08).
3. ✅ **DONE** — Remove 13 backup `.env` copies (0 remaining across all backup trees).
4. **PENDING** — Decommission/rewrite the ~33 `.env`-reader scripts to use Hermes-injected env.
5. **PENDING** — Resolve dual-gateway (keep one `gateway run`; confirm which PID owns ESTABLISHED conn) — requires explicit approval (AGENTS.md forbids gateway restart).
6. **PENDING** — Re-pair WhatsApp (manual QR); re-authenticate Nous Portal; upgrade embedded SQLite.
7. **PENDING** — Re-point 29 silent `origin`/`local` cron jobs to explicit topic targets.

## Attachments / Evidence

- `hermes status` → OpenRouter `sk-o...72c1`, xAI `xai-...Cfn5`, Firecrawl `fc-3...52e6` (masked); Nous Portal not logged in (rejected refresh token).
- Direct `getMe` → `ok:true`, `@Ogaitchmesbot` (id 8277244378).
- `tasklist`/wmic → gateway run PIDs **17584** (venv) + **12896** (uv), plus serve PIDs 14744 + 9384.
- `netstat` → PID 12896 ESTABLISHED to `149.154.166.110:443` (Telegram).
- `getChat`-equivalent → topic 20 present in `channel_directory.json` (both roots).
- `icacls` google_token.json → SYSTEM/Administrators/User only (PASS).
- Cron: 56 jobs → 29 silent (14 local + 15 origin); 27 telegram-targeted (3 topic 20).
- Backup `.env`: 2 (backups) + 0 (snapshots) + 10 (hermes-backup) + 1 (openclaw) = 13; plus live `.env.bak` (25 KB).
- `bws_cache.json` — 1224 B plaintext service keys, 18/08 09:32 update.
- Unauthorized user `5146706699` blocked 08-13.

---

*Masked: all secrets represented by provider-prefix + truncated form. No full tokens echoed.*
