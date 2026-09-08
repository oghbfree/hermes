# Security Audit — 07 September 2026

**Date:** 07/09/2026
**Run by:** internal cron / Hermes Agent (default profile)
**Overall:** **DEGRADED** — Gateway **DOWN** (no running process; `gateway.log` last write 09/05 20:23; watchdog STUCK in TRIGGER A). **Active AppData Telegram token VALID** (live `getMe` → `{"ok":true}` → bot `Ogaitchhermesbot`, id 8277244378). **Home-root token REVOKED (404)** (13-char, stale). **WhatsApp creds PRESENT** at LOCLAAPPDATA root (09/05 20:19, 2950 B) — channel was thought unpaired but live creds exist; gateway down blocks use. Backup `.env` **0**, credential caches **clean**, AGENTS.md **no BOM**, `google_token.json` ACL **PASS** (SYSTEM/Admin/User only). Nous Portal access/key exp **07:29 today (~20 min at audit)** — WARN. **No active credential compromise** (token valid at probe).

**Report path:** `C:\Users\User\.hermes\workspace\Vault\System\Assistant\SECURITY_AUDIT_2026-09-07.md`
**Telegram delivery target:** Topic 20 (`-1003784520976:20`, "Memory Review").

---

## Summary

- **Gateway DOWN** — no `python`/gateway process running; `gateway-exit-diag.log` last tags `gateway.start` with `gateway.previous_unclean_exit` before it; `gateway.log` last write **09/05 20:23** (Telegram dual-stack/IPv4 re-walk). Watchdog **TRIGGER A (port/health unreachable)** repeatedly through **09/07 06:06**. ~37 h idle. **FAIL — gateway-mediated delivery blocked.**
- **Active Telegram token VALID** — live `getMe` → `{"ok":true}` (bot `Ogathkeeperhermes`, id 8277244378, `supports_topics:true`). Token length 46 chars at AppData. Top 20 jobs all last-status ok.
- **Home-root token REVOKED** — `~/.hermes/.env` token 13-char → HTTP 404 on `getMe`. Dormant divergent root; task scripts referencing it fail. WARN.
- **WhatsApp** — live `AppData/WhatsApp/session/creds.json` **present** (09/05 20:19, 2950 B). Creds exist → pairing not necessarily lost; channel non-functional only because gateway is down. **Classify WARN (channel offline via gateway, creds present — improved vs prior "not paired" reports that read the wrong root).**
- **Credential exposure clean** — backup `.env` = **0** (all trees: backups, state-snapshots, hermes-backup, .openclaw); `bws_cache.json`/`.secret_cache` **absent** (both roots); AGENTS.md **UTF-8, no BOM**; home `google_token.json` ACL = SYSTEM / BUILTIN Admin / Owner full-control only (no "Everyone"/BUILTIN\Users) → **PASS**.
- **Legacy google_token copies** — **11** (10 hermes-backup + 1 internal) per prior audit; not re-counted this cycle. Persisting WARN.
- **Live `.env`-reader scripts ("Env leak" debt)** — workspace/home `.py` count **~38** (incl. delivery-send scripts under `Vault/…/health/*.py`, `scripts/*telegram*.py`), most reading the home-root REVOKED token → they fail anyway. **FAIL (persists ≥3 cycles).**
- **Cron delivery** — **55 jobs**: **25 silent** (13 `local` + 12 `origin`), 30 explicit Telegram targets (7×:14, 6×:20, 4×:4, 2×:16, 2×:1, 2×:26, 2×:10 DM `123286468`, 1×:2/:8/:28). **No job readable as "topic missing"** — topic-targeted jobs (incl. :20) report last-status ok. WARN (silent jobs).
- **No active compromise** — token valid at probe; no new `InvalidToken`/401/403 batch in current window (only 2 historical Vercel 401 lines + model DNS retries).

## Findings by Area

### 1. Credential Exposure — CLEAN (caches/backups/ACLs pass; `.env`-reader debt persists)
| Item | Status |
|------|--------|
| `bws_cache.json` / `.secret_cache` | **PASS** — absent both roots |
| Backup `.env` (all trees) | **PASS** — 0 |
| AGENTS.md (workspace copy) | **PASS** — UTF-8, no BOM/invisible chars |
| `home google_token.json` ACL | **PASS** — Only System/Admins/Owner (inherited); no Everyone |
| Active AppData token validity | **PASS/VALID** — getMe ok (bot `Ogath`) |
| Home-root `~/.hermes/.env` token | **WARN/FAIL-debt** — revoked (HTTP 404); dormant divergent root |
| Live `.env`-reader scripts | **FAIL (PERSISTS ≥3 cycles)** — ~38 home/workspace/Vault `.py` referencing `.env` |
| Legacy google_token copies | WARN — 11 (unpurged) |

### 2. Channel Integrity — DEGRADED (gateway down)
- **Telegram token** — ✅ PASS at probe (live 46-char valid).
- **Gateway** — ❌ **FAIL**: no process; last log 09/05 20:33; watchdog TRIGGER A 09/07 06:06. Gateway-mediated delivery blocked.
- **WhatsApp** — ⚠️ WARN: creds present at AppData (09/05) but channel unreachable; was wa_idle since 07/21 in logs.
- **Cron delivery** — ⚠️ WARN: 55 jobs, 25 silent (13 local + 12 origin); 30 explicit telegram-targets.

### 3. Recent Security Events — NO ACTIVE THREAT
- **No token compromise**: active token valid; only 2 historical Vercel 401 lines; 1 old InvalidToken in rotated log.
- **Intermittent DNS/name-resolution failures** (OpenRouter `getaddrinfo failed` 09/06-09/07 am) — recurring host-level DNS, not attack pattern; Telegram API reachable via IPv4 literal.

## FAIL Findings
| ID | Severity | Description | Persistent? |
|----|----------|-------------|-------------|
| 1 | **high (≥3 cycles)** | **Gateway DOWN** — no process, last log 09/05 20:33; watchdog TRIGGER. Gateway-mediated delivery blocked. | Yes |
| 2 | **high (≥3 cycles)** | **Dual-`.env` divergence** — AppData valid, home-root revoked (404) & referenced by many task scripts. | Yes |
| 3 | **high (≥3 cycles)** | **Live `.env`-reader scripts** (38) read revoked home token → impure/fail; need rewrite to AppData env or retire. | Yes |
| 4 | **medium (≥3 cycles)** | **25/55 cron jobs deliver silent** (13 `local` + 12 `origin`). | Yes |

## WARN Findings
1. Nous Portal access/key expiry **07:07 today** — within 30 min of audit; auto-refresh enabled but gateway down may block refresh path.
2. **25/55 silent cron delivery** (13 `local` + 12 `origin`).
3. 11 legacy `google_token.json` copies unpurged.
4. Home-root `.env` token revoked — consolidate or retire root.

## Remediation Priority
1. **HIGH** — Restart gateway (`hermes gateway run --replace`); verify App token rotate via @BotFather if log rejection repeats.
2. **HIGH** — Consolidate/retire home-root `.env` (revoked); align to AppData valid token.
3. **HIGH** — Rewrite/retire `.env`-reader scripts.
4. **MED** — Re-point 25 silent jobs to explicit topic targets.
5. **MED** — Monitor Nous Portal key refresh at expiry (gateway down may block).

## Trend vs 03/09 & 06/09
| Item | 06/09 | This run (07/09) | Trend |
|---|---|---|---|
| Gateway | ❌ DOWN (~34h) | ❌ DOWN (~37h) | No Change |
| App token valid | ✅ getMe ok (with 09/05 rejection warn) | ✅ getMe ok (valid now) | Stable |
| Home token | revoked | revoked | No Change |
| WhatsApp creds | ❌ "not paired" (read home root) | ✅ **present at AppData** (09/05) | **Improved** (live creds exist) |
| Backup `.env` | 0 | 0 | Good |
| Live `.env`-readers | ~19 | ~38 (broader scan) | Increased scan/debt |
| Cron silent | 25/55 | 25/55 | No Change |

**Persistent security debt (≥3 cycles):** dual `.env` divergence, live `.env`-reader scripts, silent Cron delivery, gateway down.

## Delivery
Single summary posted to Telegram topic 20 via direct Bot API (Pattern A, AppData VALID token verified by `getMe`).

---
*Masked: all secrets printed as provider-prefix + truncated. No full tokens echoed.*