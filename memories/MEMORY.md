# MEMORY.md

Durable facts from periodic daily-processing runs.

_facts below are limited to verified findings. Last refreshed: 2026-07-04._

## System
- MEMORY.md baseline recreated from verified workspace state.
- workspace/AGENTS.md flagged with BOM (U+FEFF invisible unicode) — do not trust guidance until manually reviewed and BOM stripped.
- Config-dir mismatch expected on Windows: `~/.hermes/config` points to Hermes config dir, not workspace.
- Canonical vault path: `C:\Users\User\.hermes\workspace\Vault\`.
- Python full path: `C:\Users\User\AppData\Local\Programs\Python\Python314\python.exe` (uv-managed cp311 on PATH).
- Obsidian skill confirmed vault at `C:\Users\User\.hermes\workspace\Vault\`.
- request_dump archives: keep `sessions.json` and `session_cron_*`; move request dumps older than 7 days to `.archive/`.
- Security reports may land in either `workspace/memories/security/` or `workspace/Vault/System/Assistant/` — check both.
- **Integrated-daily-synthesis job `b743d3f0cbdf` NOT in active jobs.json** — last ran Jun 20. Missing since Jun 21.
- **Gateway DEAD since Jun 18 (16 days as of Jul 4)** — PID not running, logs frozen. DNS healthy. Needs `hermes gateway restart`.
    - Gateway state can oscillate within a day (recovery was observed mid-Jul 3 but dead again within 90 min).
- **Daily backup job (`586aebcd5e57`) runs 23:03 — SUCCEEDED Jul 4 02:08 (28,496 files, all integrity checks passed).**
- **Security-policy-check (`1b7107630fe3`) every 6h — Jul 4 CRITICAL FAIL (7 FAIL, 6 WARN).**
- **27/40 cron jobs silently undelivered (25 origin + 2 local) — all blocked by dead gateway.**
- **WhatsApp unpaired 63+ days — creds.json missing, manual QR re-pair via phone required.**

## Missing/Blank Master Files
- No MEMORY.md before 2026-06-25.
- No INTEGRATED_INSIGHTS since 2026-06-23 (synthesis job missing).
- No `workspace/memories/insights/` dir — insights under `Vault/insights/` or missing.
- H health log: vitals not recorded since Jun 1, symptoms not logged since Jun 27.

## Verified Inventory (2026-07-04)

### New/Modified in Past 24h
- `SECURITY_AUDIT_2026-07-04.md` — CRITICAL FAIL (6 FAIL, 1 CRITICAL escalation: 27 .env backup copies, **worsened** from 26)
- `HEALTH_LOG_2026-07-03.md` — H log generated (template only, NO entries — 21 days post-shock)
- `APPLICATIONS-REPORT-2026-07-03.md` — +1 construction (Woedzagbagba Bright Kwame), 61 total applicants
- `sheets-raw-2026-07-03.json` — Fresh Google Sheets pull
- `morning_check_2026-07-03.py` — Mum morning check script
- `DAILY_PROCESSING_REPORT_2026-07-03.md` — Yesterday's report
- `backup_20260704_020859/` — Daily backup directory (28,496 files)
- MEMORY.md (this file) — refreshed 2026-07-04

### Cron Outputs Jul 3-4
- **Security audit** (Jul 4 02:08) — CRITICAL FAIL. Highlights:
  - **CRITICAL:** 27 backup .env copies with live secrets (up from 26 — worsened)
  - FAIL: workspace/AGENTS.md BOM still present
  - FAIL: Gateway dead 16 days
  - FAIL: WhatsApp unpaired 63+ days
  - FAIL: 27/40 cron jobs silent delivery
  - FAIL: 16+ workspace scripts read .env directly
  - WARN: Config drift (v29 active vs v32 latest)
  - WARN: Integrated-daily-synthesis job missing
  - **IMPROVED:** bws_cache.json clean (5th consecutive), main AGENTS.md gone (removed), DNS healthy (both Telegram + OpenRouter resolve), google_token.json ACL clean, no InvalidToken events
- **Daily backup** (Jul 4 02:08) — SUCCESS (28,496 files, all databases & config intact)
- **Health check-evening** (Jul 4 02:26) — Posted check-in to H Telegram topic

### Other Active Status
- **2Real inventory sync**: 12+ runs/day, stable DNS, all successful.
- **Mum (Comfort)**: Jul 2 had full 3 check-ins (morning, midday, evening). Morning: slept okay, ate, constipation resolved, mood good. Midday: ate eba + okro stew, rested. Evening: no log content available.
- **H health**: 21 days post-electrical shock — no medical evaluation documented. Vitals unrecorded since Jun 1. Meals unlogged since Jun 27 (though template shows Jul 2 breakfast/lunch/dinner in yesterday's summary).
- **Farm**: No check-ins since Jul 1. Waterlogged fields, 2 missing goats, Kalidou removed — all unresolved.
- **Recruitment**: 61 total applicants (+1). Nurses 45 (24 NMC), Construction 11 (+1 Woedzagbagba Bright Kwame), Facilitators 3, Financial Literacy 2.
- **Daily backup**: Recovered and stable (succeeded Jul 4 after Jul 1 failure).

## Confirmed Operational Flags

- 2Real agent system fully operational — 3 active cron loops, stable DNS, all syncs successful.
- WhatsApp gateway UNPAIRED since ~May (63+ days) — session dir empty. Bridge process non-functional.
- **Gateway DEAD (16 days)** — DNS now healthy but gateway not restarted. No cron deliveries since Jun 18.
- **Integrated-daily-synthesis job MISSING** from jobs.json — not running since Jun 20.
- Config drift: v29 active vs v32 latest (3 versions behind, narrowed from 9).
- Telegram topic 20 (Memory Review) exists and accepts messages (verified Jul 4 audit successfully posted).
- Mum midday/evening check-ins RECOVERED Jul 2 (all 3 present after prior gaps).
- H health: 21 days since electrical shock (Jun 12) — medical evaluation STILL PENDING.
- Farm emergency: No check-ins since Jul 1. Unresolved: waterlogging, 2 missing goats, Kalidou removed.
- Recruitment: 61 total applicants (+1 construction). Nurses strongest pipeline (45, 24 NMC).