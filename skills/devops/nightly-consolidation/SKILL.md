---
name: nightly-consolidation
description: >
  Process daily session logs from the past 24 hours. Extract significant learnings,
  decisions, and events. Update master intelligence files. Consolidate into long-term
  memory. Post summary to the memory-review Telegram topic.
version: 1.0.0
author: Hermes Agent
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [cron, memory, consolidation, intelligence, daily-review, sessions]
    related_skills: [daily-synthesis, system-security-audit, system-backup]
---

# Nightly Consolidation — Session Log Intelligence Review

Process all daily session logs from the past 24 hours, extract significant learnings,
decisions, and events, update master intelligence files, consolidate into long-term
memory, and post a summary to the memory-review Telegram topic (id 20).

## Trigger Conditions

- Cron job `nightly-consolidation` (schedule: `0 3 * * *`, ID: `661bee8a8f5c`)
- User asks to "review today's sessions" or "process daily logs"

## Cron Job Config

| Field | Value |
|-------|-------|
| Job ID | `661bee8a8f5c` |
| Schedule | `0 3 * * *` (3:00 AM Europe/London) |
| Delivery | `telegram:-1003784520976:20` (memory-review topic) |
| Model | Inherits from cron config |

## Procedure

### 1. Discover Sessions (Past 24 Hours)

Use `session_search` with multiple queries to surface all relevant activity:

```
session_search(query="YYYY-MM-DD", limit=10)           # today's sessions
session_search(query="cron output results", limit=10)   # cron job outputs
session_search(query="error fix deploy", limit=5)       # technical events
session_search(query="health business briefing", limit=5) # domain events
```

Also scan cron output files directly:
```bash
ls -lt ~/.hermes/cron/output/*/YYYY-MM-DD_*.md | head -30
```

### 2. Read Key Cron Outputs

> **Cron health audit procedure**: For a detailed walkthrough of how to audit cron job execution health (SLA calculation, error categorization, recovery actions), see `references/cron-health-audit-procedure.md`. That reference covers the `cron-status-report` job specifically; this skill covers the broader nightly consolidation.

Read the most important cron output files from the review period. Priority order:

1. **nightly-consolidation** (previous run) — last synthesis
2. **daily-backup** — backup status (PASS/FAIL)
3. **security-watchdog** — latest security audit findings
4. **daily-system-briefing** — morning briefing
5. **integrated-daily-synthesis** — evening synthesis
6. **cron-status-report** — system health audit
7. **health checks** (H morning/afternoon/evening, Mum morning/afternoon/evening)
8. **ghana-supplier-outreach** — supplier activity
9. **job-applications-check** — recruitment status

For each output, note: status (ok/failed), key findings, blockers, metrics.

### 3. Read Existing Intelligence Files

Check for previously generated synthesis files:
- `~/.openclaw/workspace/memory/YYYY-MM-DD-synthesis.md` — previous daily synthesis
- `~/.openclaw/workspace/memory/insights/INTEGRATED_INSIGHTS_YYYY-MM-DD.md` — previous insights

These provide trend context (e.g., "WhatsApp Day 12" → "WhatsApp Day 13").

**Health log files:** Check BOTH locations:
- `~/.openclaw/workspace/memory/HEALTH_LOG_2026-05.md` — H's health log (canonical after May 15 restructure)
- `~/.openclaw/workspace/memory/HEALTH_LOG_MUM_2026-05.md` — Mum's health log
- `~/.hermes/memories/health/H/` and `~/.hermes/memories/health/mum/` — may contain older entries from before restructure

**⚠️ Filing restructure warning:** The May 15 2026 session restructured `~/.hermes/memories/` from 20+ subdirectories into a cleaner hierarchy. File locations for health logs, business files, and other intelligence artifacts may shift between runs. If a expected file is not found at the documented path, search for it: `find ~/.hermes/memories ~/.openclaw/workspace/memory -name "*HEALTH*" -o -name "*synthesis*" 2>/dev/null`. Always note in the synthesis if files were found at non-standard paths.

### 4. Extract Significant Learnings

For each session/output, extract:

- **Critical events**: migrations, outages, failures, security findings, user approvals
- **Decisions made**: user approvals, configuration changes, new jobs created
- **Metrics changes**: health compliance rate, cron SLA, security FAIL count, backup status
- **New blockers**: anything that wasn't blocked before
- **Resolved blockers**: anything that was fixed

### 5. Update Master Intelligence Files

Write/update two files:

**A. Daily Synthesis** → `~/.openclaw/workspace/memory/YYYY-MM-DD-synthesis.md`
- System Health (gateway, WhatsApp, cron execution, backup)
- Health & Care (H status, Mum status, trends, red flags)
- Business Operations (sales, supplier progress, blockers)
- Key Metrics (table)
- Action Items (priority-ordered)

**B. Integrated Insights** → `~/.openclaw/workspace/memory/insights/INTEGRATED_INSIGHTS_YYYY-MM-DD.md`
- System Migration Status
- Health Tracking compliance metrics
- Business Progress
- Recruitment Bottlenecks
- Learning Metrics Snapshot (table)
- Top 3 System Blockers
- Emerging Patterns
- Rules & Heuristics

### 6. Compose Telegram Summary

The final response IS the delivery to topic 20. Format:

```
🧠 Daily Intelligence Synthesis
Period: YYYY-MM-DD → YYYY-MM-DD
Delivery: Memory-Review (Topic 20)

🔴 CRITICAL EVENTS
[numbered, with dates/times]

🟡 ONGOING / DEGRADED
[numbered]

🟢 NORMAL OPERATIONS
[numbered]

📊 KEY METRICS
[table]

📋 ACTION ITEMS
[priority-ordered with 🔴/🟡 indicators]
```

Keep the full report under 1500 words. The Telegram message has a 4096-character limit — if the report exceeds it, prioritize critical and ongoing sections.

## Pitfalls

1. **Memory tool unavailable in cron context.** The `memory` tool returns "Memory is not available" in cron environments. Do NOT rely on it. Write all persistence to files (`~/.openclaw/workspace/memory/`). This is expected behavior, not a bug.

2. **Session search returns summaries, not full transcripts.** `session_search` returns session previews/summaries. For full details, read the cron output files at `~/.hermes/cron/output/<job_id>/YYYY-MM-DD_HH-MM-SS.md`.

3. **Cron output files use MSYS paths.** On Windows, cron output paths are like `/c/Users/User/.hermes/cron/output/...`. Both MSYS and native Windows paths work in `read_file`.

4. **Previous synthesis may not exist.** On the first run, there may be no prior synthesis or insights file. Handle gracefully — create from scratch.

5. **Telegram delivery is automatic.** The final response text is delivered to topic 20 by the Hermes gateway. Do NOT attempt to send a separate Telegram API message.

6. **skill_manage file_path constraint.** When updating skills from within this cron job, never pass `file_path='SKILL.md'` — it will be rejected. Use `patch` without `file_path` (defaults to SKILL.md), or `write_file` with paths under `references/`, `scripts/`, `templates/`, or `assets/`.

7. **Trend tracking.** Always compare current metrics against the previous synthesis to identify trends (improving/declining/stable). A metric without trend context is less actionable.

8. **WhatsApp status changes.** WhatsApp connectivity can change between audits. Always check the latest gateway state and note the day count of any outage. This is the single most impactful system health indicator.

9. **Health intake compliance.** Track consecutive days of zero health intake. After 3+ days, escalate language from "gap" to "compliance collapse" or "clinical concern." After 5+ days, flag as rising clinical risk.

10. **Security audit delta.** Compare current security FAIL count against previous audit. Note if items were remediated, new items appeared, or count is unchanged. Unchanged findings across 3+ audits = remediation fatigue. **IMPORTANT: The security-watchdog cron job may change audit methodology between runs** (e.g., from "9 PASS / 9 FAIL" broad format to "5 FAIL / 3 PASS" focused format). When the format changes, do NOT treat it as an improvement or degradation — compare the actual findings, not the scores. A shift from "9 FAIL" to "5 FAIL" with identical core findings is a methodology change, not remediation. Always read the actual FAIL items, not just the score.

11. **Empty cron prompt detection.** When reading cron output files, check if the response is generic (e.g., "Hi! I'm OWL, how can I help?") or unrelated to the job's purpose. An empty prompt in jobs.json produces a helpful-assistant response instead of a job-specific action. Flag these in the synthesis as configuration issues requiring prompt fixes. Priority indicator: if the cron output doesn't mention the job's target topic/content, the prompt is likely empty or too thin.

12. **Synthesis file path synthesis.** The previous nightly consolidation writes synthesis to `~/.openclaw/workspace/memory/YYYY-MM-DD-synthesis.md`. However, previous runs may have used different naming (e.g., `YYYY-MM-DD.md`). When looking for prior synthesis, glob for both patterns:
```bash
ls ~/.openclaw/workspace/memory/YYYY-MM-DD*.md
```
Read the most recent one found. If neither exists, create from scratch.

13. **User Telegram session tracking.** Check for human-initiated sessions (source: "telegram") in addition to cron sessions. User sessions often contain new system setups, approvals, or decisions that aren't visible in cron outputs. The `session_search` results include these — scan for them and note any new user-established workflows,哪怕是文件还没保存的 (even if files aren't yet saved).

14. **Health log file paths shift after restructures.** After the May 15 filing restructure, health logs live at `~/.openclaw/workspace/memory/HEALTH_LOG_2026-05.md` and `HEALTH_LOG_MUM_2026-05.md`. The old paths (`health/H/`, `health/mum/`) may exist under `~/.hermes/memories/` but the canonical files are in `~/.openclaw/workspace/memory/`. Always check both locations and note which has the latest entry. If the filing system has been restructured since the last run, file locations for ANY intelligence file may have shifted — verify paths before reading.

15. **Telegram-based health intake (new pattern as of May 15).** H has shifted from responding to individual health prompts → logging meals directly in Telegram topics (topic 2 for H, topic 4 for Mum). This means: (a) compliance may be high even if cron prompt response rate is 0, (b) entries may NOT be written back to HEALTH_LOG files — check both Telegram topic history AND file contents, (c) flag when health log files are stale but Telegram intake is active as a "file sync gap" rather than "compliance collapse."

16. **Backup 401 auth failure pattern.** A `RuntimeError: Error code: 401 - Missing Authentication header` on backup indicates the API key or auth credential used by the backup process has expired or been rotated. This is distinct from the May 12 `RuntimeError: Provider returned error` (which was a transient provider issue). For 401 errors: check OpenRouter API key in `~/.hermes/.env`, verify the key hasn't expired, and check if any recent config changes modified auth headers. This is a credential issue, not a provider outage.

17. **Health cron delivery failures.** Some health check cron sessions (notably `health-check-afternoon` and `mum-health-afternoon`) may report "no Telegram tool available" — they compose the message but cannot deliver it. This happens when the cron session's toolset doesn't include `send_message`. The message is logged to the cron output file but never reaches Telegram. When you see this pattern in cron outputs, note it as a delivery failure in the synthesis, not a configuration error. The morning and evening health checks use a different delivery mechanism that works correctly.

17. **Cron-status-report log parsing.** When auditing cron execution from agent.log, use `grep "completed successfully\|Job.*failed" | grep "cron.scheduler"` to isolate job completion lines. The `hermes cron list` command gives current state but NOT historical completions — only agent.log has the full history. For error context, always cross-reference with `errors.log` and `gateway.log` since agent.log completion lines don't include error details.

## Verification

- [ ] Synthesis file written at `~/.openclaw/workspace/memory/YYYY-MM-DD-synthesis.md`
- [ ] Insights file written at `~/.openclaw/workspace/memory/insights/INTEGRATED_INSIGHTS_YYYY-MM-DD.md`
- [ ] Report covers all major sections (Critical, Ongoing, Normal, Metrics, Actions)
- [ ] Metrics include trend indicators (↑/↓/✅/🔴)
- [ ] Action items are priority-ordered with severity indicators
