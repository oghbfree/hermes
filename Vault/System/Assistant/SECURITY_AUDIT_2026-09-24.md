# SECURITY AUDIT — 2026-09-24 (15:51 GMT)

**Overall:** **CRITICAL / DEGRADED** — Telegram gateway **DOWN**, live bot token **revoked** (HTTP 404 on `getMe`; rejected by server 15/09 & 22/09). **Credential exposure otherwise CLEAN** (backup `.env` = 0, no `.secret_cache`/`bws_cache.json`, AGENTS.md no BOM, `google_token.json` ACL PASS). Carried/escalating: workspace `.py`-env-reader leak surface (≥30 files), dual-`.env` divergence, WhatsApp unpaired, 26 silent cron deliveries, Topic 20 absent from ACTIVE channel directory.

**Delivery target:** Topic 20 (`-1003784520976:20`, "Memory Review") — present in **legacy** home-root `channel_directory.json` but **absent from the ACTIVE** `AppData/Local/hermes/channel_directory.json`. Token revoked → **delivery would fail regardless**.

---

## 1. Credential Exposure

| Check | Status | Detail |
|---|---|---|
| Backup `.env` copies | **PASS** | 0 across `~/.hermes/backups`, `state-snapshots`, `~/hermes-backup`, `~/.openclaw` (maxdepth 3–4) |
| `bws_cache.json` / `.secret_cache` | **PASS** | absent |
| `AGENTS.md` BOM | **PASS** | workspace UTF-8, no BOM (CRLF only); main `~/.hermes/AGENTS.md` absent |
| `google_token.json` ACL | **PASS** | `icacls`: SYSTEM/Administrators/`User` `(I)(F)` only — no Everyone/BUILTIN\Users |
| Dual `.env` roots | **WARN** | BOTH `~/.hermes/.env` (1030B) AND `AppData/Local/hermes/.env` (552B) exist, diverging key sets (BWS, GOOGLE, BRAVE, WHISPER, SAG home-only vs XAI, WHATSAPP_* policies AppData-only). Divergence risk. |
| Workspace `.py` env-readers | **FAIL (ESCALATING)** | ≥30 files under `workspace/` + `~/.hermes/` match `.env`/`TELEGRAM_BOT_TOKEN`/`dotenv` patterns (delivery/checkin utilities in `workspace/scripts/`, `Vault/family/mum/health/`, `Vault/family/H/health/`). Persistent leak surface. |

## 2. Channel Integrity

| Check | Status | Detail |
|---|---|---|
| Telegram gateway | **DOWN (CRITICAL)** | No gateway python process running. `gateway.log` last entry 22/09 13:52:19. Log stale; PID dead. |
| Live bot token | **REVOKED (CRITICAL)** | `getMe` on home-root token → `{"ok":false,"error_code":404,"description":"Not Found"}`. Gateway log confirms *"token `827724...1UJE` was rejected by the server"* (15/09 & 22/09), gateway exited cleanly. **All Telegram delivery broken until rotation.** |
| Gateway-exit-diag | **PASS (no crash-loop)** | 0 `asyncio.run.exception`; last start 22/09 13:52 `SystemExit(78)` = clean exit on token-reject conflict, not module crash. |
| Network/DNS | **PASS** | `api.telegram.org` reachable — failures are credential, not infra. |
| WhatsApp | **FAIL (carried)** | enabled but not paired, no `creds.json`; rejected at gateway startup. |
| Topic 20 integrity | **WARN** | Present in legacy `~/.hermes/channel_directory.json` (thread 20 = "Memory Review") but **NOT in ACTIVE** `AppData/.../channel_directory.json` (lists 5885,2,10,1,14,9367,8,45047,45734,3225,18,45145,45116,44760 — no 20). Can't verify via API (token revoked). |

## 3. Recent Security Events

- **Telegram token rejected/revoked** — 15/09 05:45 and 22/09 13:52: gateway adapter logged `token rejected by the server`; gateway exited cleanly both times, never reconnected. **This is a credential-security event (potential compromise/rotation) — immediate @BotFather rotation required.**
- No `InvalidToken` in rotated logs beyond above (rejection captured as adapter ERROR, not python InvalidToken raise).
- No unauthorized-access, breach, or multi-provider crash markers in `agent.log`/`errors.log` tail.
- Nous Portal/gateway auth carried concern; provider keys present (OPENROUTER, FIRECRAWL, GOOGLE, BWS, XAI AppData).

## 4. Cron Delivery Audit (jobs.json, AppData root)

- **Total jobs: 56.** `deliver=origin/None: 13` | `deliver=local: 13` → **26 silent deliveries (46%)**. Telegram-targeted: 30 (topics 1,2,4,8,10,14,16,18,20,26,28 + `123286468`). Topic 20 targeted by **6 jobs** — all broken while token revoked.
- `hermes status` job count vs `jobs.json` discrepancy: rely on jobs.json (56) as ground truth.

## 5. Trend vs 2026-09-23

| Item | 23/09 | 24/09 | Trend |
|---|---|---|---|
| Telegram gateway | DOWN | DOWN | No Change (persistent) |
| Live token | REJECTED | REVOKED (404) | No Change (persistent, ≥3 cycles → **escalated CRITICAL debt**) |
| Backup `.env` copies | 0 | 0 | Good (clean) |
| Workspace `.py` readers | 39–45 | ≥30 | Slight improvement but persistent debt, **WARN→FAIL carried** |
| google_token ACL | PASS | PASS | Good |
| Nous Portal auth | FAIL | FAIL (carried) | No Change |

## Recommended Actions (priority)

1. **CRITICAL** — Rotate Telegram token via @BotFather; update **live** `AppData/Local/hermes/.env` `TELEGRAM_BOT_TOKEN`; verify `getMe` → `{"ok":true}`; restart gateway (`hermes gateway run --replace`).
2. **FAIL** — Delete/refactor ≥30 workspace `.py` scripts reading `.env`/token directly (move to Hermes-native delivery or env-injected config).
3. **WARN** — Reconcile dual `.env` roots to the single active AppData root.
4. **WARN** — Re-register Topic 20 in ACTIVE `channel_directory.json` once token restored.
5. **FAIL (carried)** — Pair WhatsApp via `hermes whatsapp` when convenient.