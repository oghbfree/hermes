# Security Audit — 23 August 2026

**Date:** 23/08/2026
**Run by:** internal cron / Hermes Agent (default profile)
**Overall:** **PARTIAL** — Telegram token VALID in the active AppData root (direct `getMe` → ok=true), no new credential-cache or backup-.env regressions (0 copies in all main + legacy trees), config/AGENTS.md clean. **Persisting FAIL/debt:** corrupt stale `~/.hermes/.env` token divergence (5th cycle), legacy Google/GDrive token copies (9 found, down from 18), live `.env`-reader scripts remain, WhatsApp unpaired, gateway down (startup failed, no live PID).

**Report path:** `C:\Users\User\.hermes\workspace\Vault\System\Assistant\SECURITY_AUDIT_2026-08-23.md`
**Telegram delivery target:** Topic 20 (`telegram:-1003784520976:20`), verified supergroup forum.

---

## Summary

- **Telegram token VALID (AppData root)** — direct `getMe` → `{"ok":true}` (46-char token). This is the runtime-authoritative token and is healthy for delivery.
- **⚠️ Stale `~/.hermes/.env` token DOES NOT MATCH (PERSISTS, 5th cycle)** — the alternate root `.env` holds a version ending in `...B91UJE` across BOTH files this cycle? No — the hermes-home `.env` token is length 13 (truncated/corrupt), vs 46-char valid AppData token. HTTP 404 on the short one. Divergence between dual roots is real and remains unremediated.
- **Gateway DOWN this cycle** — `gateway_state.json` reports `startup_failed` (exit_reason: `telegram: token rejected`; `whatsapp: not paired`), last update 2026-08-22 12:16. PID 15740 in state is **NOT running** (ps confirmed). A newer AppData token validates OK, so gateway failure may predate a token rotation, but the process is currently dead.
- **Credential caches CLEAN** — `bws_cache.json` / `.secret_cache` absent. `google_token.json` ACL correct (SYSTEM/Administrators/User `(I)(F)` only).
- **Backup trees CLEAN** — 0 `.env` copies in main trees; legacy `~/hermes-backup` has **9** Google/GDrive token copies (down from 18 — improvement).
- **Live `.env`-reader scripts remain** — workspace + Vault task scripts read `TELEGRAM_BOT_TOKEN` directly from `.env` (FAIL, debt).
- **WhatsApp** — unpaired in `~/.hermes/whatsapp/session/` (no `creds.json`). AppData session has creds.json (2950 B, updated today) — see note below.
- **Cron delivery** — live `jobs.json`: **56 jobs; 25 silent** (13 `local` + 12 `origin`), 31 explicit `telegram:` targets (7 → topic 20, present).

## Findings by Area

### 1. Credential Exposure — **PARTIAL** (improved on legacy tokens; two persists)

| Item | Status |
|------|--------|
| `bws_cache.json` / `.secret_cache` | **PASS** — both absent |
| Backup `.env` in main trees | **PASS** — 0 in `~/.hermes/backups`, `state-snapshots`, `.openclaw` |
| Backup `.env` (legacy `~/hermes-backup`) | **PASS** — 0 |
| Google/GDrive token copies (legacy) | **FAIL (IMPROVED)** — **9** copies (down from 18) |
| **`~/.hermes/.env` token integrity** | **FAIL (PERSISTS, 5th cycle)** — 13-char truncated `TELEGRAM_BOT_TOKEN`, diverges from valid 46-char AppData token |
| Live `.env`-reader scripts | **FAIL (PERSISTS)** — workspace/scripts/*.py + Vault/family health task scripts |
| `google_token.json` ACL | **PASS** — icacls: SYSTEM/Administrators/User `(I)(F)` only |
| Credential divergence (dual roots) | **WARN** — hermes-home `.env` and AppData `.env` both present with different token state |
| Nous Portal token | **WARN** — last auth error `invalid_grant`/`managed_access_token_refresh_failure` (offline refresh), not compromise |

### 2. Channel Integrity — **PARTIAL** (gateway down; token valid)

- **Telegram (gateway)** — ❌ FAIL: state `startup_failed`, PID 15740 not running; gateway log last write 2026-08-22 12:16 (cold).
- **Telegram (token)** — ✅ PASS via active AppData root (`getMe` ok=true). ⚠️ `~/.hermes/.env` token corrupt/divergent (above).
- **Telegram (group)** — ✅ PASS: `getChat` → `type=supergroup`, `is_forum=true`, title "Agent Hermes" (topic delivery valid).
- **WhatsApp** — ❌ FAIL: `~/.hermes/whatsapp/session/creds.json` **absent** (unpaired). Note: `AppData/Local/hermes/whatsapp/session/creds.json` exists (2950 B, mtime today) — channel may be partially paired in the active root, but gateway not running to confirm; state file still says unpaired. Treat as NOT functional.
- **Cron delivery** — ⚠️ WARN: 56 jobs → 25 silent (13 `local` + 12 `origin`), 31 telegram-targeted (7 → topic 20; topic verified present).

### 3. Recent Security Events — **PASS** (no new malicious events)

- No `InvalidToken` in current-day logs (`grep` clean in errors/gateway logs).
- Credential divergence between dual `.env` roots is a real integrity concern, but the **active** token validates — no evidence of external compromise.
- **SQLite 3.50.4 WAL-reset corruption bug** (fixed in 3.51.x) — ⚠️ WARN, upgrade via update.
- Gateway `startup_failed` with `telegram: token rejected` (from 2026-08-22 12:16 state) is consistent with the short stale token being loaded by the last run — old instance dead, not an ongoing intrusion.

## FAIL Findings

| ID | Severity | Description | Evidence |
|----|----------|-------------|----------|
| 1 | high | **Stale/truncated `TELEGRAM_BOT_TOKEN` in `~/.hermes/.env`** (length 13, no colon → HTTP 404) diverges from the valid 46-char AppData token — **PERSISTS 5th cycle** | `getMe` on `.hermes` token = 404; AppData token = ok |
| 2 | high | **Google/GDrive token copies in legacy `~/hermes-backup`** — 9 files (`google_token.json` x9; gdrive x0) remain | `find` across legacy backup tree |
| 3 | high | **Live `.py` scripts read `.env` directly** (workspace/scripts + Vault/family/mum/health task scripts) | grep across workspace |
| 4 | medium | WhatsApp channel non-functional (unpaired root; AppData creds present but gateway down) | creds presence split; state fatal |

## WARN Findings

| ID | Description |
|----|-------------|
| 1 | 25/56 cron jobs silent delivery (13 `local` + 12 `origin`) |
| 2 | Dual `.env` roots hold different token state (divergence real, needs consolidation) |
| 3 | Nous Portal refresh token errors (auth offline — `invalid_grant`) |
| 4 | SQLite 3.50.4 WAL-reset corruption bug — upgrade advised |
| 5 | Gateway currently down (`startup_failed`); delivery relies on direct API fallback |

## Trend (vs 22/08 audit)

| Item | 22/08 | This run (23/08) | Trend |
|---|---|---|---|
| Gateway UP | ✅ 26336 ESTABLISHED | ❌ dead (PID 15740 not running) | **WORSE — down** |
| Telegram token valid | ✅ AppData / ❌ `.hermes` corrupt | ✅ AppData / ❌ `.hermes` corrupt | No Change (debt persists) |
| `bws_cache.json` | absent | absent | Good (sustained) |
| Backup `.env` (main) | 0 | 0 | Good (sustained) |
| Backup `.env` (legacy) | 0 | 0 | Good (sustained) |
| Google tokens (legacy) | 18 | **9** | **IMPROVED** (9 removed) |
| AGENTS.md BOM | clean | clean | Good |
| Live `.env` readers | ~5 root + workspace | ~5 root + workspace | No Change |
| WhatsApp | ❌ unpaired | ❌ unpaired | No Change |
| Cron silent | 25/56 | 25/56 | No Change |

**Persistent security debt (3+ cycles):** `~/.hermes/.env` token divergence (5 cycles), legacy Google/GDrive token copies, WhatsApp unpaired, live `.env`-reader scripts.

## Remediation Priority

1. **HIGH** — Consolidate/repair `~/.hermes/.env`: align `TELEGRAM_BOT_TOKEN` with the valid AppData token or remove the stale root entirely.
2. **HIGH** — Delete remaining 9 Google token copies from legacy `~/hermes-backup` tree.
3. **HIGH** — Rewrite `.env`-reader scripts to use Hermes-injected env (or `hermes send`).
4. **MED** — Re-pair / re-verify WhatsApp pairing; restart gateway to validate loaded token.
5. **LOW** — Re-point 25 silent cron jobs to explicit topic targets.

## Delivery
Summary posted to Telegram topic 20 via direct API using the valid AppData token (gateway down → direct fallback used).

---

*Masked: all secrets shown as provider-prefix + truncated form. No full tokens echoed.*