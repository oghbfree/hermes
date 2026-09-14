# Security Audit — 13 September 2026

**Date:** 13/09/2026
**Run by:** internal cron / Hermes Agent (default profile) — `security-policy-check`
**Overall:** **STABLE / RECOVERED** — Gateway **UP & active** (PID 24272 live, Telegram polling confirmed healthy 00:02, WhatsApp **connected** & paired, bridge.log active 07:01). **Active AppData Telegram token VALID** (gateway `Connected to Telegram (polling mode)` + `polling confirmed healthy: getUpdates progressing`; no `InvalidToken` in fresh live logs). **Home-root `~/.hermes/.env` token REVOKED** (dormant divergent root; old 09/09 gateway.log carries the `8277...1UJE rejected` trace). **Backup `.env` = 0**, credential caches **clean**, AGENTS.md **no BOM**, credentials dir holds only client IDs (no plaintext API keys). **Nous Portal access/key exp 07:46 today (~44 min at audit, 07:02)** — WARN (auto-refresh enabled, gateway healthy → refresh path available). **No active credential compromise.**

**Report path:** `C:\Users\User\.hermes\workspace\Vault\System\Assistant\SECURITY_AUDIT_2026-09-13.md`
**Telegram delivery target:** Topic 20 (`-1003784520976:20`, "Memory Review") — confirmed in `channel_directory.json` (thread_id 20).

---

## Summary

- **Gateway UP (RECOVERED, persists)** — active `python` process PID **24272** with **ESTABLISHED TCP → `149.154.166.110:443`**; live `AppData\Local\hermes\logs\gateway.log` fresh (07:01 today). `agent.log` shows `Connected to Telegram (polling mode)` 00:01 and `polling confirmed healthy: getUpdates progressing (generation 1)` 00:02. **PASS — channel live & stable.**
- **Active Telegram token VALID** — gateway actively polling/receiving today; **no `InvalidToken`/401/403 in the last 24 h** of live logs. **PASS.**
- **Home-root token REVOKED** — `~/.hermes/.env` is a stale divergent root (its 09/09 `gateway.log` carries `The token 827724...1UJE was rejected by the server`). Dormant. **WARN (persistent debt).**
- **Credential exposure clean** — backup `.env` = **0** in `~/.hermes/backups`, `hermes-backup`, `~/.openclaw`; no `bws_cache.json`/`.secret_cache` (cache dir holds only model/catalog caches); AGENTS.md UTF-8 **no BOM**; `credentials/` holds only Google client IDs + OAuth client (expected, no raw keys echoed).
- **Live `.env`-reader scripts persist** — ~22 home/workspace/Vault task `.py` reference `.env` (telegram_/send_/tmp_/health check-in scripts). *NEW:* `workspace/skills/red-teaming/godmode/` jailbreak/obfuscation tooling (`auto_jailbreak.py`, `godmode_race.py`, `parseltongue.py`) reads `.env`/OpenRouter tokens — held since 31/05. **FAIL (persists ≥3 cycles).**
- **Cron delivery** — **~53 jobs**: **25 silent** (13 `local` + 12 `origin`), ~28 explicit Telegram targets (7×:14, 6×:20, 4×:4, 2×:16/:26/:10/DM 123286468, 1×:2/:8/:28). **15 jobs** show a `last_delivery_error` in the recent window — dominated by `send_path_degraded` and DNS `getaddrinfo failed [Errno 11001]`/timed-out — host-level DNS flutter, **not** credential failure. **WARN (silent jobs + DNS flutters).**

## Findings by Area

### 1. Credential Exposure — CLEAN caches/backups/ACLs; `.env`-reader debt persists
| Item | Status |
|------|--------|
| `bws_cache.json` / `.secret_cache` | **PASS** — absent; cache dir clean |
| Backup `.env` (backups/hermes-backup/.openclaw) | **PASS** — 0 |
| AGENTS.md (workspace copy) | **PASS** — UTF-8, no BOM/invisible chars |
| `credentials/` (google/oauth/telegram) | **PASS** — client IDs only; no raw API keys echoed |
| WhatsApp session `creds.json` | **PASS** — present at live `AppData\Local\hermes\whatsapp\session\` (paired); absent in stale `~/.hermes` |
| Active AppData gateway token | **PASS/VALID** — polling healthy, no rejection in 24 h |
| Home-root `~/.hermes/.env` token | **WARN/FAIL-debt** — revoked (dormant divergent root) |
| Live `.env`-reader scripts | **FAIL (PERSISTS ≥3 cycles)** — ~22 + godmode tooling |

### 2. Channel Integrity — STABLE (gateway recovered; persists)
- **Telegram gateway** — ✅ **PASS/RECOVERED**: PID 24272 live, ESTABLISHED TCP → Telegram, polling confirmed healthy 00:02, inbound processing.
- **Active token** — ✅ PASS (no fresh rejection; gateway functioning with it).
- **WhatsApp** — ✅ **connected & paired** (live `creds.json`; bridge.log active 07:01); functional.
- **Cron delivery** — ⚠️ WARN: 25/53 silent (`13 local` + `12 origin`); 15 recent delivery errors are DNS/degraded-path (host-level), not credential.

### 3. Recent Security Events — NO ACTIVE THREAT
- **No token compromise**: `InvalidToken`/`rejected by the server` appears **only** in stale home-root `~/.hermes/logs/gateway.log` (09/09, revoked home token) — not in live AppData logs.
- **DNS flutter**: `Errno 11001 getaddrinfo failed` + `send_path_degraded` + timed-out across several jobs — recurring host-level name resolution, not attack pattern; gateway self-recovers.
- **Red-teaming/godmode tooling present** (`auto_jailbreak.py`, `godmode_race.py`, `parseltongue.py`, since 31/05) — obfuscation/jailbreak scripts that read `.env`/OpenRouter tokens. Flag: monitor & remove if not actively used for sanctioned red-team work.

## FAIL Findings
| ID | Severity | Description | Persistent? |
|----|----------|-------------|-------------|
| 1 | **high (≥3 cycles)** | **Dual-`.env` divergence** — AppData active root valid; home-root `~/.hermes/.env` revoked & referenced by task scripts. | Yes |
| 2 | **high (≥3 cycles)** | **Live `.env`-reader scripts** (~22) + godmode jailbreak tooling read tokens from `.env`. | Yes |
| 3 | **medium (≥3 cycles)** | **25/53 cron jobs deliver silent** (13 `local` + 12 `origin`). | Yes |

## WARN Findings
1. Nous Portal access/key expiry **07:46 today** — ~44 min at audit; auto-refresh enabled; gateway healthy → expected OK.
2. **25/53 silent cron delivery** (13 `local` + 12 `origin`).
3. Home-root `.env` token revoked — consolidate or retire the divergent root.
4. **DNS flutters** (`getaddrinfo failed` / `send_path_degraded`) affected 15 jobs recently — recurring host-level, self-recovers.
5. **godmode/red-teaming jailbreak scripts** present (May 31) reading `.env`/OpenRouter keys — review necessity.

## Remediation Priority
1. **HIGH** — Consolidate/retire home-root `~/.hermes/.env` (revoked token) to remove dual-root divergence; align task scripts to AppData valid env.
2. **HIGH** — Rewrite/retire ~22 `.env`-reader scripts; remove or gate godmode/red-teaming jailbreak tooling if not actively used.
3. **MED** — Re-point 25 silent cron jobs to explicit topic targets (topic 20 valid & reachable).
4. **MED** — Confirm Nous Portal key auto-refresh at 07:46 expiry.

## Trend vs 11/09
| Item | 11/09 | This run (13/09) | Trend |
|---|---|---|---|
| Gateway | ✅ UP/RECOVERED | ✅ **UP, stable** (PID 24272, polling confirmed) | **Stable** |
| AppData token valid | ✅ active | ✅ active (no rejection 24 h) | Stable |
| Home token | revoked | revoked | No Change |
| Backup `.env` | 0 | 0 | Good |
| Live `.env`-readers | ~22 | ~22 + godmode tooling new | **Worse (new exposure)** |
| Cron silent | 25/55 | 25/~53 | No Change |
| WhatsApp | functional | **connected & paired** (live bridge 07:01) | **Improved** |

**Persistent security debt (≥3 cycles):** dual `.env` divergence, live `.env`-reader scripts, silent cron delivery. Gateway debt **cleared** (recovered, sustaining).

## Delivery
Summary delivered to Telegram topic 20 ("Memory Review"). Active AppData token used (gateway healthy). Home-root revoked token NOT used.

---
*Masked: all secrets printed as provider-prefix + truncated. No full tokens echoed.*