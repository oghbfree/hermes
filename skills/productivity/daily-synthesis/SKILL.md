---
name: daily-synthesis
description: >
  Compile daily briefings and integrated syntheses from health logs, business updates,
  team status, and learning points — covering both the morning tactical briefing (06:36)
  and the nightly deep synthesis (22:05).
---

# Daily Synthesis — Briefing & Compilation

This umbrella covers TWO distinct cron jobs that share the same data-gathering approach
but differ in format, length, and depth.

## Cron Jobs Covered

| Job | Schedule | ID | Length | Purpose |
|-----|----------|-----|--------|---------|
| `daily-system-briefing` | 36 6 * * * (06:36) | `7ccae58aa436` | <500 words | Tactical ops briefing → topic 10 |
| `integrated-daily-synthesis` | 5 22 * * * (22:05) | `1ce4c6b6f727` | Full report | Deep synthesis + insight files → topic 10 |

## Data Sources (shared by both)

Health, business, and team data is split across Hermes-native storage and OpenClaw
legacy files. **Always check both locations.**

### Health Data
- **Primary (canonical):** `~/.openclaw/workspace/memory/HEALTH_LOG_2026-MM.md` (H) and `HEALTH_LOG_MUM_2026-MM.md` (Comfort) — these are the authoritative health log files as of May 2026
- **Legacy/fallback:** `~/.hermes/health/HEALTH_LOG_2026-MM.md` — may exist if migration occurred, but check OpenClaw paths first
- **Post-restructure (May 15+):** After the filing restructure, also check `~/.hermes/memories/health/H/` and `~/.hermes/memories/health/mum/` for older entries. The canonical files remain in `~/.openclaw/workspace/memory/`.
- **Telegram topic entries (May 15+):** H has shifted to logging health data directly in Telegram topics (topic 2 for H, topic 4 for Mum). These entries may NOT be written back to HEALTH_LOG files. Check gateway.log for inbound health messages and note the discrepancy as a "file sync gap" if Telegram entries exist but files are stale.

### Business Data
- Legacy: `~/.openclaw/workspace/memory/business/BUSINESS_CHECKINS_2026-MM.md`
- Legacy: `~/.openclaw/workspace/memory/business/GHANA_SUPPLIER_*` (if exists)

### System State
- Cron jobs: `hermes cron list` → check `last_run_at` and `last_status`
- Gateway: `hermes gateway status` — check PID; read `~/.hermes/logs/gateway.log` for errors
- Previous outputs: `~/.hermes/cron/output/*/YYYY-MM-DD_*.md`
- Sessions: `session_search` for today's cron runs and user responses

## Steps (shared preamble)

### 0. Discover Available Data
- **Use `session_search` first** — it IS available in cron sessions. Search for today's topics: `health logs business updates daily synthesis` to find recent sessions. This is the fastest way to discover what happened today.
- Read health log files from both Hermes and OpenClaw locations
- Read business check-in file
- Check `hermes cron list` for system health
- **Read gateway.log** (`~/.hermes/logs/gateway.log`) — this is the PRIMARY source for:
  - Connectivity issues (WhatsApp/Telegram errors, restarts)
  - **User activity**: inbound messages reveal what H discussed, decided, or shared today (files, topics, decisions). Extract key user actions and include in synthesis.
- Read all today's cron output files from `~/.hermes/cron/output/*/` — list directories, then read each today's output `.md` file
- Check previous synthesis or briefing output files for trend context
- **Note:** `session_search` tool does NOT exist in this environment. Do not attempt to call it. Use file reads and gateway logs instead.

---

## A. MORNING BRIEFING — daily-system-briefing (06:36)

**Goal:** A single, actionable brief under 500 words. No file writing — the final response
IS the deliverable.

### Format (required)

```
📋 DAILY BRIEFING — Tuesday DD Month YYYY

HEALTH | 🔴/🟡/🟢 [status emoji]
- H: [last known food, BP, energy, gap days since last log]
- Comfort (Mum): [last known vitals, meals, meds, gap days, mobility]
- Trend: [rolling observation]
- 🔴 RED: [specific health risk flag]

BUSINESS | 🟡/🟢/🔴 [status emoji]
- 2Real Shop: [sales, orders, WhatsApp contact status]
- Akoma: [pipeline, content plans, execution status]
- Construction: [site-specific: Senya, Kokomlemle, Koko, farm]
- Supply chain: [suppliers contacted, quotes received, untouched count]
- Recruitment: [new applicants, pipeline bottlenecks]

TEAM | 🟡/🟢/🔴 [status emoji]
- Sammy: [last contact, EOD check status]
- John: [field ops status]
- Kanzoni: [supplier relationships]
- Matthias: [construction oversight]
- System: [cron health, dashboard, gateway]

BLOCKERS | 🔴 [N] CRITICAL
[numbered list, brief description per blocker]

TODAY'S ACTIONS | 🎯
[numbered list, action-oriented]
```

### Rules for gap reporting
- **If no data exists for today:** Report the gap honestly. Count days since last entry.
  Never fabricate or imply data exists when it doesn't. Frame it as a compliance/engagement issue.
- **If a channel is down (WhatsApp, Telegram):** State it explicitly and date the outage.
  Count days since the channel broke — e.g. "WhatsApp dead (Day 12)".
- **If team members haven't checked in:** Report last contact date, not silence as "all clear".

### Critical items to always check
1. **WhatsApp gateway status** — read gateway.log for `✓ whatsapp connected` or `✗ whatsapp`
2. **Health compliance rate** — count how many of today's 6 health prompts (3 for H, 3 for Mum) received responses
3. **Last cron execution timestamps** — `hermes cron list` → check `last_run_at`
4. **Google Sheets auth** — if recruitment is stalled, flag the auth issue
5. **Previous synthesis** — read last cron output for trend data (e.g., `~/.hermes/cron/output/*/YYYY-MM-DD_*.md`)

---

## B. NIGHTLY SYNTHESIS — integrated-daily-synthesis (22:05)

**Goal:** Deep compilation. Write insight files. Full report to topic 10.
- **Health Logs:** Primary canonical paths are `C:\\Users\\User\\.openclaw\\workspace\\memory\\HEALTH_LOG_2026-MM.md` and `HEALTH_LOG_MUM_2026-MM.md`. Also check `~/.hermes/memories/health/H/` and `~/.hermes/memories/health/mum/` for entries from before the May 15 restructure. If neither file has entries for today, check gateway.log for Telegram topic health messages (H logs in topic 2, Mum in topic 4) — entries may exist only in Telegram and not in files.
- **Business Updates:** Read from `C:\\Users\\User\\.openclaw\\workspace\\memory\\business\\BUSINESS_CHECKINS_2026-MM.md` and any supplier analysis files (`GHANA_SUPPLIER_*`)

- **Learning Points:** Read from `C:\\Users\\User\\.openclaw\\workspace\\LEARNING_SYSTEM.md` and check `memory/YYYY-MM-DD-synthesis.md` for existing data
- **Cron Execution:** Run `hermes cron list` to see last run timestamps; check agent.log for actual execution records
- **Gateway Logs:** Check `C:\\Users\\User\\.hermes\\logs\\gateway.log` for errors, restarts, Telegram connectivity issues
- **Previous Insights:** Read the last INTEGRATED_INSIGHTS file at `memory/insights/INTEGRATED_INSIGHTS_YYYY-MM-DD.md`

### 2. Identify Today's Data
Read today's cron output files from `~/.hermes/cron/output/*/`:
- List all subdirectories, then read each `YYYY-MM-DD_*.md` file for today's date
- Morning briefing output (delivered to topic 10)
- Health check outputs (topics 2, 4)
- Business/supplier updates (topic 1)
- Security watchdog output (topic 20) — **compare with previous audit to track remediation delta**
- Job applications check (topic 28)
- Any other jobs that fired today
- **Gateway log**: extract H's activity — messages sent, topics discussed, files shared, decisions made. Include a "User Activity" section in the synthesis.

### 3. Compile Synthesis
Update `memory/YYYY-MM-DD-synthesis.md` with today's full picture:
- System Health (gateway status, WhatsApp, cron execution report)
- Health & Care (H status, Mum status, trends, red flags)
- Business Operations (sales, supplier progress, blockers)
- Recruitment (new applicants, pipeline status)
- Learning Capture (metrics table, what worked, what failed, emerging patterns)
- Action Items (priority-ordered)

### 4. Create Insights File
Write to `memory/insights/INTEGRATED_INSIGHTS_YYYY-MM-DD.md`:
- System Migration Status (if applicable)
- Health Tracking compliance metrics
- Business Progress
- Recruitment Bottlenecks
- Learning Metrics Snapshot (table)
- Top 3 System Blockers
- Emerging Patterns

### 5. Post to Telegram
The final response of the cron job is automatically delivered to topic 10 (briefing).
Format the output as:

```
📋 **Integrated Daily Synthesis — Monday DD Mon YYYY**

**HEALTH** | **BUSINESS** | **SYSTEM** | **BLOCKERS** | **ACTIONS**

[concise sections with key numbers, trends, and priority actions]
```

## Pitfalls
- Memory tool is unavailable in cron environment — don't rely on it. Write all persistence to files.
- **Canonical persistence path:** All cron-generated intelligence files should be written to `~/.openclaw/workspace/memory/` (create subdirectories as needed: `memory/insights/`, `memory/business/`, etc.). This is the canonical long-term storage location that survives across sessions. Do NOT write intelligence files only to `~/.hermes/` — that directory is platform-managed and may be overwritten during upgrades.
- **Create the insights directory if it doesn't exist.** The path `~/.openclaw/workspace/memory/insights/` may not exist yet. Create it before writing the first INTEGRATED_INSIGHTS file.
- tirith_security fails on Windows — benign, ignore
- Gateway logs may only show current session; older gateway-session data may be in gateway.log or gateway-stdio.log
- Cron jobs without "last run" timestamp doesn't mean they didn't run — check agent.log for execution evidence
- Schedule is 22:05 UTC+1 (Europe/London) — runs after evening health checks complete
- Use both `.openclaw\\workspace\\` files (legacy data) and `.hermes\\` logs (new platform data)
- **Empty day:** If no health intake, business updates, or learning points exist for today, don't force-fill — report the gap honestly. The synthesis should flag compliance collapse as a finding, not pretend data exists.
- **WhatsApp status:** Check whether WhatsApp gateway is connected. If broken (common state), note that all WhatsApp-dependent cron jobs (EOD checks, family check-ins) are silently failing.
- **AGENTS.md BOM vulnerability.** The file `~/.hermes/AGENTS.md` contains an invisible U+FEFF (byte-order-mark) character at the start. The system flags this as a potential injection vector and blocks the file. This causes repeated warnings in every session that reads AGENTS.md. Fix: save the file as UTF-8 without BOM. Until fixed, ignore the BOM warning — it's a known issue, not a new attack.

- **Weekly health reviews (first run: Sunday May 17).** The `health-weekly-review-h` and `health-weekly-review-mum` cron jobs are scheduled for Sunday 09:06. These are their FIRST EVER executions. Verify the job prompts are populated and the delivery targets (topics 2 and 4) are correct before Sunday.
- **Data fragmentation:** Health logs, business check-ins, and supplier data may still live exclusively in the OpenClaw workspace (`~/.openclaw/workspace/memory/`) if migration is incomplete. Always fall back to OpenClaw paths before declaring data unavailable.
- **session_search tool IS available.** The `session_search` tool works in cron sessions. Use it as the FIRST step in synthesis to discover today's sessions, then supplement with cron output file reads and gateway logs. This is more efficient than blindly reading directories.
- **500-word hard cap for morning briefing:** The morning brief must stay under 500 words. Use compact emoji prefixes, avoid prose paragraphs, and let the format (single-line bullet points) do the work. Nightly synthesis has no length limit.
- **Empty cron prompts produce false successes — now confirmed persistent.** `ghana-supplier-outreach` (ID `00d4f0e3d9aa`) and `ghana-steering-verification` (ID `4cadf4e4945e`) have run with empty/missing prompts on multiple consecutive days. When a cron job produces a generic response ("Hi! I'm OWL..."), a synthesis report instead of domain output, or [SILENT], treat it as a **persistent configuration error** — not a successful execution. Flag it every day until fixed. Do not stop reporting it after one day.
- **Agent explaining limitations instead of outputting deliverable — confirmed recurring.** Some cron agents (notably `mum-health-afternoon` / ID `4399b4d83d57`) produce a report *about* the message ("I don't have send_message tool...") or output the message as formatted text in the response body, instead of recognizing that the final response IS the auto-delivered message. The correct pattern is: the final response IS the deliverable. Do not append meta-commentary about delivery limitations. Just output the message content.
- **Health gap escalation language.** Use escalating language for health intake gaps: 1-2 days = "gap", 3-4 days = "compliance concern", 5+ days = "compliance collapse", 6+ days for elderly care recipient = "clinical risk — escalate to direct human follow-up", 8+ days for elderly care recipient = "CRITICAL clinical risk — immediate direct human follow-up required".
- **Security remediation tracking.** When comparing security audit results across runs, explicitly report the delta: which FAIL items were remediated, which are new, which are chronic. After 8+ audits with zero remediation, the first remediation is a significant event — report it prominently. Check for deleted files (Desktop `.env`, `.env.backup*`, workspace `client_secret.json`) as evidence of remediation.
- **Gateway log for user activity.** The gateway.log (`~/.hermes/logs/gateway.log`) records all inbound Telegram messages with timestamps, user, and message content. Use this to construct a "User Activity Today" section in the nightly synthesis — what H discussed, what files were shared, what decisions were made. This is more reliable than trying to recall from memory.
- **Gateway log reading efficiency.** The gateway.log can be very large (2000+ lines / 280KB+). Do NOT read the entire file. For today's activity, read from the end using `offset` parameter (e.g., `offset=2700` for the last ~100 lines). For a full-day synthesis, read the last 200-300 lines which covers the current session window.
- **Health gap closure reporting.** When a health intake gap closes (e.g., from 9+ days zero to 6/6 responses), report this as a **BREAKTHROUGH** — not just a status update. Identify the trigger (e.g., "H shifted to Telegram topic logging") and note it as an emerging pattern. Gap closure after 5+ days is a significant event.
- **WhatsApp bridge crash pattern.** WhatsApp may briefly reconnect (showing `✓ whatsapp connected`) then crash minutes later (`WhatsApp bridge process exited unexpectedly (code 1)`). This is NOT a stable reconnection — report it as "fragile" or "brief reconnection, bridge unstable." A stable connection persists for hours. Check for the crash pattern in gateway.log when WhatsApp status is uncertain.
- **Pre-existing synthesis file.** The nightly consolidation cron (03:00) may have already written a partial `memory/YYYY-MM-DD-synthesis.md` and `memory/insights/INTEGRATED_INSIGHTS_YYYY-MM-DD.md` for today. The nightly synthesis (22:05) should **replace** these with the full-day version, not skip writing because a file exists. Always write the final synthesis regardless of prior partial files.

- **Backup failure patterns.** Two distinct backup failure modes have been observed: (1) `RuntimeError: Provider returned error` — transient provider issue, usually self-heals on next run; (2) `RuntimeError: Error code: 401 - Missing Authentication header` — credential/auth issue, requires manual investigation of API keys in `~/.hermes/.env`. A 401 error is always CRITICAL and should be escalated immediately. A transient provider error is HIGH but may resolve on its own. Track the streak: 3+ consecutive passes = healthy, any failure = investigate, 401 = urgent.

## Verification
- Confirm synthesis file written at `memory/YYYY-MM-DD-synthesis.md`
- Confirm insights file written at `memory/insights/INTEGRATED_INSIGHTS_YYYY-MM-DD.md`
- Verify cron list shows `integrated-daily-synthesis` with updated "last run" timestamp

## Reference Files
- `references/cron-reference.md` — verified cron job IDs, Telegram topic IDs, security findings tracker, and file paths. Read this at the start of each synthesis run to avoid re-discovering IDs.
- `references/health-intake-patterns.md` — health gap escalation language, channel migration patterns (WhatsApp → Telegram), gap closure reporting, and known vitals baselines. Consult when synthesizing health sections.