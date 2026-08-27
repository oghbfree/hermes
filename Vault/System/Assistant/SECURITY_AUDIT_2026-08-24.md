# Security Audit — 24 August 2026

**Date:** 24/08/2026
**Run by:** internal cron / Hermes Agent (default profile)
**Overall:** **IMPROVED** — Gateway RECOVERED (running, Telegram + WhatsApp both connected in the active AppData root). Telegram token VALID (AppData) and channel delivery healthy after a transient same-day network blip. No new security events. **Persisting FAIL/debt:** `~/.hermes/.env` token divergence (6th cycle), legacy Google/GDrive token copies in `~/hermes-backup` (26 files, worsening), live `.env`-reader task scripts, 25/57 cron jobs silent delivery.

**Report path:** `C:\Users\User\.hermes\workspace\Vault\System\Assistant\SECURITY_AUDIT_2026-08-24.md`
**Telegram delivery target:** Topic 20 (`telegram:-1003784520976:20`), verified supergroup forum via `getChat`.

---

## Summary

- **Channel health RECOVERED** — the active gateway runs from the **AppData root** (`C:\Users\User\AppData\Local\hermes\`), PID **20344** alive with ESTABLISHED TCP to Telegram (149.154.166.110:443). `gateway_state.json` = `running`; telegram `connected` (updated 2026-08-23 20:32), whatsapp `connected` (2026-08-23 11:23). Active `gateway.log` fresh (2026-08-24 05:23+). Email are delivered via this instance.
- **Telegram token VALID (AppData root)** — direct `getMe` → HTTP 200 `{"ok":true}` on the 46-char token. This is the runtime-authoritative token.
- **⚠️ Stale `~/.hermes/.env` token DOES NOT MATCH (PERSISTS, 6th cycle)** — the alternate home root holds a **13-char truncated token with no `:`** → `getMe` returns HTTP 404. Dual-root divergence remains.
- **WhatsApp now paired** — `creds.json` present in AppData session root (2950 B, mtime today 07:02); bridge process (node, PID 13440) alive. Previously reported unpaired.
- **Credential caches CLEAN** — `bws_cache.json`/`.secret_cache` absent. `google_token.json` ACL correct (SYSTEM/Administrators/User `(I)(F)` only).
- **Backup trees** — main trees clean (0 `.env` copies). **Legacy `~/hermes-backup` worsening**: **26 token-bearing files** (google_token.json x10, gdrive_token.json x8, gdrive_credentials.json x8) — up from 9 counted at 23/08.
- **Live `.env`-reader scripts remain** — workspace/scripts/*.py, Vault/family/mum/health task scripts, 3 root `send_*.py` read TELEGRAM_BOT_TOKEN from `.env` directly (FAIL debt).
- **Cron delivery** — live `jobs.json` (AppData): **57 jobs; 25 silent** (13 `local` + 12 `origin`), 32 explicit `telegram:` targets (7 → topic 20, present).
- **Nous Portal** — access/key expiry 2026-08-24 **07:46** (within 24h) — WARN. Refresh enabled; gateway healthy, so likely auto-refresh succeeds.

## Findings by Area

### 1. Credential Exposure — **PARTIAL** (caches clean; two persistent Fails)

| Item | Status |
|------|--------|
| `bws_cache.json` / `.secret_cache` | **PASS** — absent |
| Backup `.env` in main trees | **PASS** — 0 |
| `google_token.json` ACL | **PASS** — icacls SYSTEM/Administrators/User `(I)(F)` only |
| Nous Portal token | **WARN** — expiry 07:46 today (within 24h); refresh enabled, gateway stable |
| **`~/.hermes/.env` token integrity** | **FAIL (PERSISTS, 6th cycle)** — 13-char truncated, no colon → HTTP 404 |
| Legacy Google/GDrive token copies (`~/hermes-backup`) | **FAIL (WORSE)** — 26 files (google_token x10, gdrive_token x8, gdrive_credentials x8) |
| Live `.env`-reader scripts | **FAIL (PERSISTS)** — workspace/scripts/*.py + Vault health task scripts + root send_*.py |
| Credential divergence (dual `.env` roots) | **WARN** — AppData holds valid token; `~/.hermes` holds corrupt/truncated copy |

### 2. Channel Integrity — **GOOD** (gateway recovered)

- **Telegram (gateway)** — ✅ PASS: PID 20344 running, polling healthy (getUpdates progressing generation 4), live TCP to 149.154.166.110. Transient network blip 2026-08-24 02:51 (`Dual-stack ... failed`), recovered by 02:52 — host/DNS blip, not credential.
- **Telegram (token)** — ✅ PASS AppData (`getMe` 200). ⚠️ `~/.hermes/.env` token corrupt/divergent (above).
- **Telegram (group)** — ✅ PASS: `getChat` → `type=supergroup`, `is_forum=true`, title "Agent Hermes".
- **WhatsApp** — ✅ PASS (now paired): creds.json present, bridge node PID 13440 alive, state `connected`.
- **Cron delivery** — ⚠️ WARN: 57 jobs → 25 silent (13 `local` + 12 `origin`), 32 telegram-targeted (7 → topic 20 verified present).

### 3. Recent Security Events — **NO COMPROMISE** (one WARN)

- **No** new `InvalidToken` / `Unauthorized` / `Revoked` on the **active** (AppData) root current-day logs. The two historical matching flags (2026-08-13 WhatsApp, 2026-08-21 Telegram) are reconnect-attempt markers, not credential revocation on the current token, which `getMe`-validates OK.
- Telegram network blip 2026-08-24 02:51-02:52 = transient host/DNS, gateway self-recovered.
- `~/.hermes/.env` truncated token remains a genuine integrity risk, but the runtime token is valid — no evidence of external compromise.

## FAIL Findings

| ID | Severity | Description | Evidence |
|----|----------|-------------|----------|
| 1 | high | **Stale/truncated `TELEGRAM_BOT_TOKEN` in `~/.hermes/.env`** (length 13, no colon → HTTP 404) diverges from valid 46-char AppData token — **PERSISTS 6th cycle** | `getMe` on `.hermes` token = 404; AppData = 200 |
| 2 | high | **Legacy Google/GDrive credential files in `~/hermes-backup` — 26** (google_token.json x10, gdrive_token.json x8, gdrive_credentials.json x8) | `find` across legacy tree |
| 3 | high | **Live `.py` scripts read `.env` directly** (workspace/scripts + Vault/family/mum/health + 3 root send_*.py) | grep across workspace/root |
| 4 | medium | **25/57 cron jobs silent delivery** (13 `local` + 12 `origin`) | jobs.json delivery audit |

## WARN Findings

| ID | Description |
|----|-------------|
| 1 | Dual `.env` roots hold different token state (divergence persists — consolidate to AppData root) |
| 2 | Nous Portal token expiry within 24h (07:46 today); refresh enabled — watch for missing refresh |
| 3 | Historical Telegram/WhatsApp reconnect-flag entries in logs (pre-rotation; current token valid) |
| 4 | Transient host-level Telegram network blip 02:51 on 24/08 (self-recovered) |

## Trend (vs 23/08 audit)

| Item | 23/08 | This run (24/08) | Trend |
|---|---|---|---|
| Gateway | ❌ startup_failed / dead (15740) | ✅ **running** (PID 20344, Telegram+WhatsApp connected) | **IMPROVED (RECOVERED)** |
| Telegram token valid | ✅ AppData / ❌ `.hermes` corrupt | ✅ AppData / ❌ `.hermes` corrupt | No Change (debt persists, 6th cycle) |
| WhatsApp | ❌ unpaired | ✅ **paired** (creds.json, bridge alive) | **IMPROVED** |
| `bws_cache` | absent | absent | Good (sustained) |
| Backup `.env` (main) | 0 | 0 | Good (sustained) |
| Legacy token copies (backup) | 9 | **26** (10 google + 16 gdrive) | **WORSE** |
| Live `.env` readers | workspace + Vault + root | present | No Change |
| Cron silent | 25/56 | 25/57 | No Change |
| AGENTS.md BOM / cleanup | clean | clean | Good |

**Persistent security debt (3+ cycles):** `~/.hermes/.env` token divergence (6 cycles), legacy Google/GDrive credential copies (worsening), live `.env`-reader scripts, WhatsApp now resolved.

## Remediation Priority

1. **HIGH** — Consolidate/repair `~/.hermes/.env`: align `TELEGRAM_BOT_TOKEN` with the valid AppData token, or retire the stale root.
2. **HIGH** — Purge 26 legacy credential file copies from the `~/hermes-backup` tree.
3. **HIGH** — Rewrite `.env`-reader task scripts to use Hermes-injected env (or `hermes send`); delete root `send_*.py`.
4. **MED** — Re-point 25 silent cron jobs to explicit topic targets (esp. the 8 to topic `14` and 13 `local`).
5. **LOW** — Monitor Nous Portal auto-refresh; confirm token rotates at/past 07:46 today.

## Delivery
Summary posted to Telegram topic 20 via direct API using the valid AppData token (gateway healthy; direct fallback used for deterministic topic delivery).

---

*Masked: all secrets shown as provider-prefix + truncated form. No full tokens echoed.*