# Security Audit — 18 August 2026 (Evening Re-run)

**Date:** 18/08/2026 (same-day evening re-run of 00:10 + morning + afternoon audits; `-evening` suffix per retention policy)
**Run by:** internal cron / Hermes Agent (default profile)
**Overall:** **FAIL** (persistent credential-leak debt — `bws_cache.json` plaintext cache + live `.env`-reader scripts + `.env.bak` remain). Telegram token **VALID**, gateway **UP** (PID 16640), backup `.env` copies **stable (13)**. No new credential compromise. Topic 20 verified delivering (**message_id 10612**).

**Report path:** `C:\Users\User\.hermes\workspace\Vault\System\Assistant\SECURITY_AUDIT_2026-08-18-evening.md`

---

## Summary

- **Telegram bot token VALID** — direct `getMe` → `{"ok":true}`, `@Ogaitchhermesbot`. No current `InvalidToken` in window.
- **Topic 20 (Memory Review) VERIFIED** — `getChat` → supergroup `is_forum:true`. Direct `sendMessage` to thread 20 succeeded (**message_id 10612**). Functional delivery target.
- **Gateway UP (confirmed)** — `hermes status` PID **16640**, confirmed alive via `tasklist`. `errors.log` shows clean start; Telegram connected; WhatsApp `fatal`. (PIDs churn between audit runs — 11516→16640; treat as normal replacement unless a concurrent duplicate is confirmed.)
- **Backup `.env` copies STABLE** — **13 total** (2 `~/.hermes/backups` + 10 `~/hermes-backup` + 1 `~/.openclaw`), flat vs afternoon (13).
- **Plaintext cache persists (CRITICAL)** — `bws_cache.json` (1224 bytes, updated 18/08 09:32) holds plaintext service keys (FIRECRAWL, OPENROUTER, TELEGRAM_BOT_TOKEN, etc.). ACL is OS-restricted but the content is plaintext and survives `.env` rotation.
- **Live `.env`-reader scripts persist** — ~31 total (27 workspace `*.py` + 4 `~/.hermes/*.py`). Flat vs afternoon.
- **Live `.env.bak`** — plaintext backup (25 KB, dated 19/07) sitting in the live home directory (HIGH).
- **Channels affected:** WhatsApp **non-functional** (fatal `whatsapp_not_paired`, no `creds.json` — manual QR re-pair required). Discord paused/unused.
- **Cron delivery:** 56 jobs; **29 silent** (14 `local` + 15 `origin`), 27 explicit `telegram:` targets (3 → topic 20).

## Findings by Area

### 1. Credential Exposure — **FAIL**

| Item | Status |
|------|--------|
| Backup `.env` copies | **FAIL (STABLE)** — 13 total (2 backups, 0 snapshots, 10 hermes-backup, 1 openclaw), flat vs afternoon |
| Plaintext cache `bws_cache.json` | **FAIL** — present (1224 B, 18/08 09:32), plaintext service keys |
| Live `.env`-reading scripts | **FAIL** — 4 `~/.hermes/*.py` + 27 workspace → ~31 total |
| `~/.hermes/.env.bak` (live) | **FAIL** — plaintext `.env` backup in live home dir |
| `google_token.json` ACL | **PASS** — icacls: SYSTEM/Administrators/User `(I)(F)` only; no Everyone/Users |
| `.secret_cache` | **PASS** (absent) |
| AGENTS.md BOM | **PASS** — main `~/.hermes/AGENTS.md` absent; workspace copy clean UTF-8, no BOM |
| Dual `.env` roots | **WARN** — both `~/.hermes/.env` (24.9 KB) and `AppData\Local\hermes\.env` (552 B) exist → divergence risk |

Verdict: **FAIL** (critical cache + reader scripts + live `.env.bak` persist; backup copies stable-not-declining).

### 2. Channel Integrity — **FAIL** (partial)

- **Telegram (token)** — ✅ PASS: valid via `getMe`. Topic 20 ("Memory Review") present and delivering.
- **Gateway process** — ✅ PASS (UP): PID 16640 alive; Telegram connected; clean start this cycle.
- **WhatsApp** — ❌ FAIL: fatal `whatsapp_not_paired`, no `creds.json`; manual QR re-pair required.
- **Cron delivery** — ⚠️ WARN: 56 jobs → 27 explicit `telegram:` targets (3 topic 20), **29 silent** (14 `local` + 15 `origin`).
- **Dual-process note:** PIDs churn each audit (24152/7908 → 11516 → 16640); treat as normal replacement unless two gateway processes confirmed concurrently.

### 3. Recent Security Events — **PASS**

- No `InvalidToken` / token revocation in current window (historical InvalidToken only in rotated `agent.log.1/2`, `errors.log.2`; token currently valid).
- **Unauthorized user blocked (08-13)** — `[Telegram] Blocked unauthorized user 5146706699` — permission control functioning.
- Transient DNS failures (08-13, `getaddrinfo failed` → fallback IP) — host-level; recovered; gateway healthy since.
- OpenRouter 401 "Missing Authentication header" on 08-04 (historical) — resolved; OpenRouter key currently valid.
- No multi-provider simultaneous failure; no breach markers.
- **Nous Portal refresh token rejected** — ⚠️ WARN: auth provider offline (rejected refresh token), not credential compromise.

## FAIL Findings

| ID | Severity | Description | Evidence |
|----|----------|-------------|----------|
| 1 | critical | Plaintext credential cache `bws_cache.json` (service keys) | `~/.hermes/cache/bws_cache.json` |
| 2 | high | Live `.py` scripts read `.env` directly (~31 total) | 4 `~/.hermes/*.py` + 27 workspace |
| 3 | high | `~/.hermes/.env.bak` plaintext backup in live dir | `~/.hermes/.env.bak` |
| 4 | medium | WhatsApp channel non-functional (unpaired) | no `creds.json`; fatal state |
| 5 | medium | 13 backup `.env` copies remain (STABLE, not declining) | 2+10+1 across backup trees |

## WARN Findings

| ID | Description |
|----|-------------|
| 1 | 29/56 cron jobs silent delivery (14 `local` + 15 `origin`) |
| 2 | Nous Portal refresh token rejected — auth offline |
| 3 | Dual `.env` roots (`~/.hermes/.env` + `AppData\Local\hermes\.env`) — divergence risk |
| 4 | Gateway PID churn (11516 → 16640) — monitor for true dual-instance |

## Trend Comparison (vs afternoon audit 18/08)

| Item | Afternoon | This run (evening) | Trend |
|---|---|---|---|
| Telegram token valid | ✅ | ✅ | No Change (good) |
| Gateway online | ✅ UP (11516) | ✅ UP (16640) | No Change (good) |
| Topic 20 delivery | verified (msg 10605) | ✅ verified (msg 10612) | No Change (good) |
| WhatsApp paired | ❌ | ❌ | No Change |
| Backup `.env` copies | 13 | **13** | No Change (stable) |
| `bws_cache.json` | present | present | No Change (critical) |
| Live `.env` readers | ~32 | ~31 | No Change |
| Cron silent delivery | 27/46 | 29/56 | WARN (proportion stable) |
| InvalidToken in window | none | none | No Change (good) |
| Google token ACL | PASS | PASS | No Change (good) |

## Remediation Priority

1. **CRITICAL** — Purge `bws_cache.json` (plaintext secrets; survives `.env` rotation).
2. **HIGH** — Delete `~/.hermes/.env.bak`; decommission/rewrite the ~31 `.env`-reader scripts to use Hermes-injected env.
3. **MEDIUM** — Remove remaining 13 backup `.env` copies (2 hermes/backups, 10 hermes-backup, 1 openclaw).
4. **MEDIUM** — Re-pair WhatsApp (manual QR); re-authenticate Nous Portal.
5. **MEDIUM** — Re-point 29 silent `origin`/`local` cron jobs to explicit topic targets.

## Retention Note

- **Same-day re-run** → `-evening` suffix. Today now has 4 files (00:10 base, `-morning`, `-afternoon`, `-evening`).
- Recommend full-file dedupe: keep only the latest dated file per day (policy). Drop files older than 7 days.

## Attachments / Evidence

- `hermes status` → Gateway `✓ running` (manual process), PID 16640 (alive via tasklist).
- Direct `getMe` → `ok:true`, `@Ogaitchmesbot`.
- `getChat -1003784520976` → supergroup, `is_forum:true`.
- `sendMessage` thread 20 → **message_id 10612** (topic 20 = Memory Review).
- `gateway_state.json` → state connected (Telegram), fatal (WhatsApp).
- `icacls` google_token.json → SYSTEM/Administrators/User only (PASS).
- Cron: 56 jobs → 29 silent (14 local + 15 origin); 27 telegram-targeted (3 topic 20).
- Backup `.env`: 2 (backups) + 0 (snapshots) + 10 (hermes-backup) + 1 (openclaw) = 13; plus live `.env.bak`.
- `bws_cache.json` — 1224 B plaintext service keys, 18/08 09:32 update.
- Unauthorized user `5146706699` blocked 08-13.

---

*Masked: all secrets represented by provider-prefix + truncated form. No full tokens echoed.*