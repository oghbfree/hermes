# Security Audit — 14 September 2026 (re-run 08:39 GMT)

**Date:** 14/09/2026 (DMY dd/mm/yy)
**Run by:** internal cron / Hermes Agent (default profile) — `security-policy-check` (same-day re-run; supersedes 07:10 run)
**Overall:** **STABLE / RECOVERED** — Gateway **UP & active** (PID 13848, both Telegram AND WhatsApp adapters `connected` as of 08:26 today); live `gateway.log` fresh (08:27) showing real Telegram command registration (`set_my_commands OK`, 60 cmds) → **active AppData token accepted by Telegram**. **No `InvalidToken`/rejection in fresh live logs.** **Backup `.env` = 0**, credential caches **clean**, `google_token.json` + `auth.json` ACL **secure** (SYSTEM/Administrators/User only). AGENTS.md **no BOM**. Home-root `~/.hermes/.env` still a **13-char stale divergent root** (dormant). **Nous Portal access/key exp 09:21 today (~23 min at 08:58)** — WARN (auto-refresh enabled, gateway healthy). **Vercel MCP 401 Unauthorized** (4× 13/09) persists — isolated connector auth, not a Telegram credential failure. **No active credential compromise.**

**Report path:** `C:\Users\User\.hermes\workspace\Vault\System\Assistant\SECURITY_AUDIT_2026-09-14.md`
**Telegram delivery target:** Topic 20 (`-1003784520976:20`, "Memory Review") — 6 cron jobs target it; reachable in prior audits.

---

## Summary

- **Gateway UP (RECOVERED, sustains)** — active process PID **13848**; `gateway_state.json` shows telegram `connected` + whatsapp `connected` (updated 08:26 today); `gateway.log` fresh 08:27 with `set_my_commands OK` for all scopes (60 commands). Clean restart 08:26 (PID 27652→13848, normal scheduler replacement, `state_db_integrity: ok`). **PASS — channel live & stable.**
- **Active Telegram token VALID** — gateway successfully ran `set_my_commands` (bot-authorized op) at 08:27 and no `InvalidToken`/401/403 in the last 24 h of live logs. (Direct `getMe` grep was blocked by the cron secret-read approval gate; gateway auth success is authoritative proof the 46-char AppData token is accepted.) **PASS.**
- **WhatsApp connected & paired** — live `creds.json` at `AppData\Local\hermes\whatsapp\session\creds.json` (2951 B, dated today 08:36); adapter `connected`. **PASS.**
- **Credential exposure clean** — backup `.env` = **0** across `backups`/`hermes-backup`/`state-snapshots`/`.openclaw`; no `bws_cache.json`/`.secret_cache`; AGENTS.md UTF-8 **no BOM** (home copy absent); `google_token.json` + both `auth.json` ACLs = Owner/SYSTEM/Administrators only (no `Everyone`/`BUILTIN\Users`). **PASS.**
- **Dual-`.env` divergence persists** — active AppData root 46-char token vs home-root `~/.hermes/.env` 13-char stale token. **FAIL (persistent ≥3 cycles).**
- **Live `.env`-reader scripts persist** — broad literal-`.env` scan of home/workspace/Vault finds ~550 `.py` referencing `.env`/env vars (incl. many dated one-off send scripts created 09/11–09/13 and skill helpers; prior ~22 was a narrower count). Recent one-off send scripts observed. **FAIL (persistent ≥3 cycles).**
- **Cron delivery** — **55 jobs**: **25 silent** (13 `local` + 12 `origin`); ~30 explicit Telegram targets (7×:14, 6×:20, 4×:4, 2×:16/:26/:10/DM, 1×:2/:8/:28 + 2 no-thread).

## Findings by Area

### 1. Credential Exposure — CLEAN caches/backups/ACLs; dual-root + `.env`-reader debt persists
| Item | Status |
|------|--------|
| `bws_cache.json` / `.secret_cache` | **PASS** — absent in both roots |
| Backup `.env` (backups/hermes-backup/state-snapshots/.openclaw) | **PASS** — 0 |
| AGENTS.md (workspace copy) | **PASS** — UTF-8, no BOM; home copy absent |
| `google_token.json` ACL | **PASS** — SYSTEM/Administrators/User only |
| `auth.json` ACL (both roots) | **PASS** — SYSTEM/Administrators/User only |
| WhatsApp session `creds.json` | **PASS** — present & paired |
| Active AppData gateway token | **PASS/VALID** — bot-authorized ops OK, no rejection |
| Home-root `~/.hermes/.env` token | **WARN/FAIL-debt** — 13-char stale divergent root |
| Live `.env`-reader scripts | **FAIL (PERSISTS ≥3 cycles)** — broad scan ~550 incl. dated one-offs + skill helpers |

### 2. Channel Integrity — STABLE (gateway recovered; both Telegram + WhatsApp live)
- **Telegram gateway** — ✅ **PASS**: PID 13848 live, `gateway_state=connected`, live inbound/outbound + command registration today.
- **Active token** — ✅ PASS (bot-authorized ops succeeded; no rejection in fresh logs).
- **WhatsApp** — ✅ **connected & paired** (live `creds.json`, adapter `connected`).
- **Cron delivery** — ⚠️ WARN: 25/55 silent (13 `local` + 12 `origin`).

### 3. Recent Security Events — NO ACTIVE THREAT
- **No token compromise**: no `InvalidToken`/`rejected by the server`/`Unauthorized` (except isolated Vercel MCP) in live AppData logs.
- **Vercel MCP 401 Unauthorized** (4× 13/09, confirmed in `agent.log` tail) — connector/workspace auth on `mcp.vercel.com`; isolated to one provider, not a Telegram credential failure. **PERSISTS (WARN).**
- **Nous Portal key exp 09:21 today (~23 min at 08:58)** — auto-refresh enabled, gateway healthy → refresh path available. **WARN.**
- **Gateway restart 08:26** — clean scheduler replacement (PID 27652→13848, `state_db_integrity: ok`), not a crash loop.

## CRITICAL Escalations
None this cycle. No finding of severity ≥ critical; existing FAIL items are **persistent security debt (≥3 cycles)**, none newly escalated this run.

## FAIL Findings
| ID | Severity | Description | Persistent? |
|----|----------|-------------|-------------|
| 1 | **high (≥3 cycles)** | **Dual-`.env` divergence** — AppData root valid; home-root `~/.hermes/.env` stale (13-char) & referenced by task scripts. | Yes |
| 2 | **high (≥3 cycles)** | **Live `.env`-reader scripts** (~550 broad) + dated one-off send scripts reference `.env`. | Yes |
| 3 | **medium (≥3 cycles)** | **25/55 cron jobs deliver silent** (13 `local` + 12 `origin`). | Yes |

## WARN Findings
1. Nous Portal access/key expiry **09:21 today** — ~23 min at audit; auto-refresh enabled; gateway healthy → expected OK.
2. **25/55 silent cron delivery** (13 `local` + 12 `origin`).
3. Home-root `.env` token stale/partial — consolidate or retire the divergent root.
4. **Vercel MCP 401 Unauthorized** (4× 13/09, persists) — re-authenticate Vercel workspace connection.
5. **godmode/red-teaming jailbreak scripts** (May 31) reading `.env`/OpenRouter keys — review necessity.

## Remediation Priority
1. **HIGH** — Consolidate/retire home-root `~/.hermes/.env` (stale 13-char token) to remove dual-root divergence; align task scripts to AppData valid env.
2. **HIGH** — Rewrite/retire `.env`-reader scripts (esp. dated one-off send scripts); remove or gate godmode/red-teaming jailbreak tooling if not actively used.
3. **MED** — Re-point 25 silent cron jobs to explicit topic targets.
4. **MED** — Confirm Nous Portal key auto-refresh at 09:21 expiry; re-authenticate Vercel MCP connector (401).

## Trend Comparison
| Item | 13/09 | 14/09 (07:10) | This run (14/09 08:39) | Trend |
|---|---|---|---|---|
| Gateway | ✅ UP (PID 24272) | ✅ UP both TG+WA (27652) | ✅ UP both connected (PID 13848) | **Stable** |
| AppData token | valid | valid (getMe ok) | valid (bot-auth ops OK) | Stable |
| Home token | revoked | stale/partial 13-char | stale/partial 13-char | No Change |
| Backup `.env` | 0 | 0 | 0 | Good |
| Live `.env`-readers | ~22 + godmode | ~22 + godmode | broad ~550 + dated one-offs | **Worse (broadened scope)** |
| Cron silent | 25/~53 | 25/55 | 25/55 | No Change |
| WhatsApp | connected & paired | connected & paired | connected & paired | Stable |
| Nous key exp | 07:46 | 07:54 | 09:21 | Stable (auto-refresh) |
| Vercel MCP 401 | — | 4× (NEW) | 4× (persists) | **No Change (debt)** |

**Persistent security debt (≥3 cycles):** dual `.env` divergence, live `.env`-reader scripts, silent cron delivery. Gateway + token health debt **cleared**.

## Retention Note
Retention applied against the directive path (`Vault\System\Assistant\`): same-day re-run supersedes the 07:10 `SECURITY_AUDIT_2026-09-14.md` (kept as the designated 14/09 record). Rolling window kept at ≤7 files (5 present: 09/06, 09/07, 09/11, 09/13, 09/14) — no files older than 7 days to purge; no duplicate same-day files retained.

## Delivery
Summary delivered to Telegram topic 20 ("Memory Review"). Active AppData token used (gateway healthy). Home-root stale token NOT used.

---
*Masked: all secrets printed as provider-prefix + truncated. No full tokens echoed.*