# Security Audit — 06 September 2026

**Date:** 06/09/2026
**Run by:** internal cron / Hermes Agent (default profile)
**Overall:** **DEGRADED** — Gateway **DOWN** (no process running; last activity 09/05 20:26 = non-retryable startup conflict: Telegram token rejected + WhatsApp not paired → clean exit). **Active AppData token VALID** (live `getMe` ok:true → `Ogaitchhermesbot`; ~560 historical InvalidToken/Unauthorized hits in gateway.log, latest rejection logged 09/05 20:26). **WhatsApp NOT paired** (creds.json absent — REGRESSION, was paired 03/09). Backup `.env` **0**, credential caches **clean**, legacy `google_token` **11 (-1)**, AGENTS.md **no BOM**. **Persisting debt:** ~19 live `.env`-reader scripts (home-root referencing revoked-token `.env`), credential divergence (home token revoked 404), 25/55 cron jobs silent delivery. **No active credential compromise** (token valid at probe time).

**Report path:** `C:\Users\User\.hermes\workspace\Vault\System\Assistant\SECURITY_AUDIT_2026-09-06.md`
**Telegram delivery target:** Topic 20 (`-1003784520976:20`, "Memory Review"). Gateway down → direct Bot API (AppData token, VALID).

---

## Summary

- **Gateway DOWN** — no `gateway`/python process running; `gateway.log` last write **09/05 20:26** with a **non-retryable startup conflict**: `telegram: Telegram bot token rejected ...; whatsapp: WhatsApp enabled but not paired`. Gateway exited cleanly. ~34 h idle at audit (07:00). **FAIL — gateway-mediated delivery blocked.**
- **AppData Telegram token CURRENTLY VALID** — live `getMe` → `{"ok":true}` (`Ogaitchhermesbot`, id 8277244378). **However**, gateway.log shows the SAME token (`827724...1UJE`) **rejected by the server** at 09/05 20:26; `.env` mtime (08/18) unchanged since, so the valid-now result vs logged rejection is contradictory — **token validity should be re-confirmed before relying on it.** WARN.
- **WhatsApp NOT paired** — `~/.hermes/whatsapp/session/creds.json` absent. **REGRESSION** vs 03/09 (creds present then). Channel non-functional. FAIL.
- **Credential exposure clean** — backup `.env` = **0** (all trees), `bws_cache.json` / `.secret_cache` **absent** (both roots), AGENTS.md **UTF-8, CRLF, no BOM** (workspace copy; main file absent), home `google_token.json` absent. PASS.
- **Legacy google_token copies** — **11** (10 hermes-backup + 1 internal), down from 12. WARN (persisting, but improving).
- **Live `.env`-reader scripts (FAIL debt)** — **~19 live files** in home-root tree: root `send_health_check.py`, `telegram_direct_send.py`, `telegram_create_topic.py`, `telegram_post_file.py`; `workspace/scripts/` `send_ghana_report.py`, `ghana_telegram_report.py`, `memory_review_telegram.py`; `Vault/.../mum/health/*checkin*.py` (multiple) + `tmp_afternoon_send.py`; `Vault/business/2real/.../ghana_telegram_report.py`; `Vault/family/H/health/send_evening_checkin.py`. All read `~/.hermes/.env` whose token is **REVOKED (404)** → these direct-send scripts would fail today. AppData workspace scan: skill helper scripts (comfyui/google-workspace/linear/godmode) reference `.env` legitimately — not flagged.
- **Cron delivery** — **55 jobs** (APPDATA source-of-truth): **25 silent** (13 `local` + 12 `origin`), 30 explicit Telegram targets (7×:14, 6×:20, 4×:4, etc.). WARN.
- **Nous Portal** — access/key expiry **2026-09-06 07:45:32** (~45 min from audit 07:00) — WARN; auto-refresh enabled.

## Findings by Area

### 1. Credential Exposure — PARTIAL (caches/backups clean; FAIL debt persists)
| Item | Status |
|------|--------|
| `bws_cache.json` / `.secret_cache` | **PASS** — absent both roots |
| Backup `.env` (all trees) | **PASS** — 0 |
| AGENTS.md BOM / invisible chars | **PASS** — UTF-8, no BOM (workspace copy; main absent) |
| Active runtime token (AppData) | **PASS/VALID** — getMe ok (`Ogaitchhermesbot`); re-confirm after 09/05 rejection |
| Home-root `~/.hermes/.env` token | **WARN** — revoked (HTTP 404); dormant divergent root |
| Legacy google_token copies | **WARN** — 11 (10 hermes-backup + 1 internal), -1 |
| Live `.env`-reader scripts | **FAIL (PERSISTS, ≥3 cycles)** — ~19 home-root/workspace/Vault, referencing revoked home token |

### 2. Channel Integrity — DEGRADED (gateway down, WhatsApp unpaired)
- **Gateway** — ❌ **FAIL**: no process; last log 09/05 20:26 (startup conflict exit). ~34 h down.
- **Telegram (active AppData token)** — ✅ PASS at probe: getMe ok; but 09/05 rejection recorded → classify WARN/suspect.
- **WhatsApp** — ❌ **FAIL / REGRESSION**: creds.json absent, not paired (was paired 03/09).
- **Cron delivery** — ⚠️ WARN: 55 jobs → 25 silent (13 `local` + 12 `origin`), 30 telegram-targeted; gateway down blocks gateway-mediated delivery.

### 3. Recent Security Events — NO ACTIVE COMPROMISE (channel outage; token rejection to monitor)
- **Token rejection event 09/05 20:26** — gateway.log: `The token ... was rejected by the server`; ~560 InvalidToken/Unauthorized entries historical in gateway.log. **Current getMe ok:true** — no active compromise, but reconcile the 09/05 rejection vs current validity (token rotation/confirmation recommended).
- **No** new provider 401/403 batch (prior Vercel 401 not re-observed).
- **No unauthorized-access / breach markers** this window.

## FAIL Findings
| ID | Severity | Description | Persistent? |
|----|----------|-------------|-------------|
| 1 | high (PERSISTS, ≥3 cycles) | **Gateway DOWN** — no process; last 09/05 20:26 startup conflict (token rejected + WhatsApp not paired); gateway-mediated delivery blocked | Yes |
| 2 | high (PERSISTS, ≥3 cycles) | **~19 live `.py` scripts read `.env` directly** (home-root workspace/Vault/root), referencing a REVOKED token | Yes |
| 3 | high (PERSISTS, ≥3 cycles) | **Credential divergence: dual `.env` roots** — AppData valid; home-root REVOKED (404) but referenced by task scripts | Yes |
| 4 | medium (PERSISTS, ≥3 cycles) | **25/55 cron jobs silent delivery** (13 `local` + 12 `origin`) | Yes |
| 5 | medium (NEW) | **WhatsApp NOT paired** — creds.json absent (regression, was paired 03/09) | No |

## WARN Findings
| ID | Description |
|----|-------------|
| 1 | AppData token rejection logged 09/05 20:26 but live getMe ok:true — contradictory; re-confirm/rotate before relying on it |
| 2 | Nous Portal access/key expiry **07:45 today** (~45 min at audit) — confirm auto-refresh (gateway down may affect refresh path) |
| 3 | 11 legacy `google_token.json` copies (not purged) |
| 4 | Home-root `.env` token revoked — dormant root should be consolidated or retired |
| 5 | 25/55 cron jobs silent delivery |

## CRITICAL Escalations
None escalated this cycle (all 5 FAILs are monitored persistence debt; the 4 consistent items remain high/medium ≥3 cycles as persistent security debt).

## Trend Comparison (vs 03/09 audit)
| Item | 03/09 | This run (06/09) | Trend |
|---|---|---|---|
| Gateway | ❌ DOWN (~14 h, DNS) | ❌ DOWN (~34 h, startup conflict token+whatsapp) | No Change (root cause shifted) |
| Telegram token valid (active) | ✅ getMe ok | ✅ getMe ok (but 09/05 rejection logged) | Stable ⚠ |
| Home-root token | revoked (404) | revoked (404) | No Change |
| WhatsApp | ✅ paired (creds 01/09) | ❌ **NOT paired** | **Degraded (regression)** |
| `bws_cache` / caches | clean | clean | Good (sustained) |
| Backup `.env` | 0 | 0 | Good (sustained) |
| Legacy google_token | 12 | 11 | Improving (-1) |
| Live `.env` readers | ~18 | ~19 | No Change (debt) |
| Cron silent | 25/55 | 25/55 | No Change |
| Vercel MCP auth | resolved | not re-observed | Stable |

**Persistent security debt (≥3 cycles):** live `.env`-reader scripts; credential divergence (dual roots); silent cron delivery; gateway down.

## Remediation Priority
1. **HIGH (URGENT)** — Restart gateway (`hermes gateway run --replace`). Reconcile AppData token: live getMe ok but 09/05 rejected; rotate via @BotFather if in doubt. Fix WhatsApp pairing (QR) — gateway currently aborts on "not paired".
2. **HIGH** — Rewrite/retire `.env`-reader scripts (home root); they read a REVOKED token and fail anyway. Delete dated one-offs.
3. **HIGH** — Align home-root `~/.hermes/.env` with valid AppData token, or retire stale root.
4. **MED** — Purge legacy `google_token.json` (11 copies).
5. **MED** — Re-point 25 silent cron jobs to explicit topic targets; confirm Nous Portal refresh at 07:45.

## Delivery
Gateway down → summary posted to Telegram topic 20 via **direct Bot API** (Pattern A, AppData token VALID at probe — verified `getMe` ok; will re-verify before send). If token now rejects, delivery fails → report boundary.

## Retention Note
Report in `Vault/System/Assistant/` per job directive; rolling 7-day window. 5 prior reports present (08/24, 08/28, 08/31, 09/01, 09/03) + today = 6 files, distinct dates. No cleanup required.

---
*Masked: all secrets shown as provider-prefix + truncated form. No full tokens echoed.*