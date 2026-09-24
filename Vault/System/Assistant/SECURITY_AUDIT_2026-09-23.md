# Security Audit — 23 September 2026

**Date:** 23/09/2026 (DMY dd/mm/yy)
**Run by:** internal cron / Hermes Agent (default profile) — security-policy-check
**Overall:** **CRITICAL / DEGRADED** — Telegram gateway **DOWN**: live bot token **rejected by the server** (started 22/09 13:52, no successful reconnect since), PID dead, logs 17h+ stale. **Credential exposure otherwise clean** (backup `.env` = 0, no caches, ACLs PASS) but **45 workspace `.py` `env`-reader touchpoints** flag a rising leak surface. Carried: dual-`.env` divergence, Nous Portal auth invalid, 26 silent cron deliveries, WhatsApp unpaired.

**Report path:** `C:\Users\User\.hermes\workspace\Vault\System\Assistant\SECURITY_AUDIT_2026-09-23.md`
**Delivery target:** Topic 20 (`-1003784520976:20`, "Memory Review") — **target exists in channel_directory** (topic id 20) but token revoked → delivery likely FAILS until rotation.

---

## Summary — MAJOR REGRESSION vs 22/09
- **Telegram gateway — DOWN (CRITICAL).** No running gateway python process. `gateway.log` last entry **22/09 13:52:19**: *"Telegram bot token rejected: The token `827724...1UJE` was rejected by the server. The token is invalid or was revoked."* → gateway exited cleanly, never reconnected. Log mtime 22/09 13:52 (≈17.5h stale vs now 07:03 23/09). PID 8396 in status **dead** (`ps` empty). **`getMe` on home-root token → HTTP 404 (revoked).**
- **This is a regression:** yesterday's 06:18 audit reported the live token **VALID** (@Ogaitchhermesbot, msg_id 11402 probe OK). The token was accepted earlier, then **rejected 22/09 13:52** → treated as **potential credential compromise / token revoked or rotated** — requires rotation via @BotFather.
- **Credential exposure — CLEAN (PASS):** backup `.env` = **0** across backups/state-snapshots/hermes-backup/.openclaw. No `bws_cache.json` / `.secret_cache`. Workspace AGENTS.md UTF-8 no BOM (CRLF), main `~/.hermes/AGENTS.md` absent. `google_token.json` ACL PASS (SYSTEM/Admins/User only — 22/09 08:01 refreshed, 1870 B).
- **Rising leak surface (WARN/FAIL):** **39–45** `.py` files under `workspace/` + `~/.hermes/` matched `.env`/token patterns. This is a **major increase** from the 3 known stale one-offs tracked 22/09 → **persistent security debt, escalating**.
- **Nous Portal — carried FAIL**, `invalid_grant` / "Invalid refresh token" (terminal; requires interactive re-auth, cannot from cron).

## Findings by Area

### 1. Credential Exposure — Mostly CLEAN, one rising surface
| Item | Status |
|------|--------|
| `bws_cache.json` / `.secret_cache` | **PASS** — absent |
| Backup `.env` (all roots) | **PASS** — 0 |
| AGENTS.md (workspace) | **PASS** — UTF-8, no BOM (CRLF only; main `~/.hermes/AGENTS.md` absent) |
| `google_token.json` ACL | **PASS** — SYSTEM:(I)(F) / Administrators:(I)(F) / User:(I)(F) only |
| Stale home-root `~/.hermes/.env` token | **FAIL (carried)** — 13-char stub, `getMe` HTTP 404 (revoked) |
| Live AppData-root token | **CRITICAL FAIL (NEW 22/09 13:52)** — **rejected by the server**; all Telegram delivery broken until rotated |
| Workspace `.env`-reader `.py` one-offs | **FAIL (ESCALATING)** — 39–45 files match `.env`/token patterns (was 3 stale ones on 22/09); majority are delivery/checkin utilities in `workspace/scripts/`, `workspace/Vault/family/mum/health/`, `Vault/family/H/health/` that read `TELEGRAM_BOT_TOKEN` from `.env` directly |

### 2. Channel Integrity — Telegram DOWN, WhatsApp unpaired
- **Telegram gateway — DOWN (CRITICAL).** No python gateway process running; last good connect 18/08 09:32 (polling); last rejection + exit 22/09 13:52. Log stale 17.5h.
- **Live token — now INVALID/REVOKED** (rejected by server 22/09 13:52; home-root copy getMe 404). All variants of delivery fail until rotate.
- **Topic 20** — exists in `channel_directory.json` (Agent Hermes / topic 20) but NOT deliverable while token revoked.
- **Cron delivery** — **56 jobs**: **30 target Telegram** (6→topic 20), **13 `local`** + **13 `origin`** silent (26 silent, carried debt). Jobs targeting `local`/`origin` never reach a user.
- **WhatsApp** — **unpaired** (no `creds.json`). (22/09 audit believed disabled-by-config; **23/09 gateway log shows WhatsApp "enabled but not paired"** at startup → reclassified as unpaired, must verify config.)
- Network/DNS **healthy** (api.telegram.org reachable, HTTP 302) → failures are **token/credential**, not infrastructure.

### 3. Recent Security Events
- **token rejected / InvalidToken / Unauthorized: 769 grep hits** across logs (cumulative, dominated by the 15/09 + 22/09 rejection clusters). **Live restart 22/09 13:52 rejected** → token NOT accepted.
- **No `invalid_grant` recurrence today** for Nous (0 hits in agent.log this window), but 22/09 audit confirmed prior term-error — carried as unresolved auth state.
- **No BOM / invisible-char (U+200B / U+202E) injection** in AGENTS.md. No webhook/rogue-login markers found.

## FAIL Findings
| ID | Severity | Description | Persistent? |
|----|----------|-------------|-------------|
| 1 | **CRITICAL (NEW this cycle)** | **Telegram token rejected by server (revoked/invalid)** — gateway exited 22/09 13:52, all delivery down. Rotate via @BotFather. | New |
| 2 | **high (≥4 cycles, carried)** | **Dual-`.env` divergence** — stale home-root `.env` revoked; live AppData root also now rejected. Retire stale root. | Yes |
| 3 | **high (carried)** | **Nous Portal auth invalid** — `invalid_grant`; auxiliary client offline; cannot re-auth from cron. | Yes |
| 4 | **medium (ESCALATING)** | **~40 workspace `.env`-reader scripts** — leak surface up from 3 to ~40. Cleanup needed. | Yes (worsening) |
| 5 | **medium (carried)** | **Silent cron delivery** — 26/56 (`local`/`origin`); reminders/checkins never reach user. | Yes |
| 6 | **medium (carried)** | **WhatsApp unpaired** — no `creds.json`. | Yes |

## CRITICAL Escalations
- **Telegram token revoked → all Telegram delivery (incl. this topic-20 post) blocked.** Highest-priority security action: rotate `TELEGRAM_BOT_TOKEN` via @BotFather and update live `.env`; verify via `getMe`.

## WARN Findings
1. Telegram token rejection = **potential credential compromise**, not just outage.
2. Workspace `.env`-reader scripts proliferated (39–45) — token touchpoint bloat.
3. Nous Portal auth invalid (operational).
4. 26 silent cron deliveries (local/origin).
5. WhatsApp unpaired.

## Remediation Priority
1. **CRITICAL** — Rotate Telegram token via @BotFather; update **live** `/c/Users/User/AppData/Local/hermes/.env`; verify `getMe` → `{"ok":true}`; restart gateway.
2. **HIGH** — Retire stale home-root `~/.hermes/.env` (single authoritative root).
3. **HIGH** — Re-auth Nous Portal interactively (`hermes model` / `hermes auth add nous`).
4. **MED** — Delete ~40 `.env`-reading one-offs under `workspace/scripts`, `Vault/family/mum/health`, `Vault/family/H/health`; keep only canonical senders that source from gateway env.
5. **MED** — Re-point 26 silent jobs to explicit topic targets.
6. **LOW** — Re-pair WhatsApp (QR) when interactive available.

## Retention Note
7-day window (16–23/09): kept 17,18,20,21,22/09 + today **23/09** (5 files). Removed `SECURITY_AUDIT_2026-09-15.md` (8 days old). One file per day.

## Trend Comparison (vs 22/09)
| Item | 22/09 (prior) | 23/09 (this run) | Trend |
|---|---|---|---|
| Gateway | UP (PID 15220, connected) | **DOWN** (token rejected, PID dead, 17.5h stale) | **REGRESSION — CRITICAL** |
| Telegram token (live) | VALID | **REJECTED/revoked** | **REGRESSION — CRITICAL** |
| Backup `.env` | 0 | 0 | Good |
| Caches | clean | clean | Good |
| AGENTS.md | no BOM (main absent) | no BOM (main absent) | Good |
| google_token ACL | PASS | PASS | Good |
| Workspace `.env`-readers | 3 stale | **39–45** | **ESCALATING** |
| Dual-`.env` divergence | present | present (both roots now bad) | No change (worse) |
| Nous Portal | auth invalid | auth invalid | No change |
| WhatsApp | disabled-by-config | **unpaired** (per gateway log) | Reclassified |
| Topic 20 | probe-confirmed (msg 11402) | exists but not deliverable (token revoked) | Degraded |