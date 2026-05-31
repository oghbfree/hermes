---
name: daily-operations-synthesis
description: Compile cross-domain daily synthesis reports for the Hermes Agent operational ecosystem — health tracking, business operations, team status, security posture, and system health. Triggered by the nightly integrated-daily-synthesis cron or when H asks for a "daily briefing" or "status report". Produces structured markdown reports saved to memories/insights/ and posted to Telegram briefing topic.
---

# Daily Operations Synthesis

Compile the integrated daily synthesis — a cross-domain status report covering all operational threads.

## When to Use

- **Morning briefing cron** (`daily-system-briefing`, 06:36 UTC+1) — first thing H sees, scannable, focuses on today's priorities
- **Nightly synthesis cron** (`integrated-daily-synthesis`, 22:05 UTC+1) — comprehensive retrospective of the day
- When H asks for "daily briefing", "status report", "how did today go"
- After major incidents (security events, system failures, health red flags)
- Weekly review (as input to weekly learning review)

## Morning Briefing vs Nightly Synthesis

| | Morning Briefing (06:36) | Nightly Synthesis (22:05) |
|---|---|---|
| **Purpose** | Today's priorities at a glance | Full retrospective |
| **Tone** | Scannable, action-oriented | Analytical, comprehensive |
| **Health section** | Current gap + risk level | Full trend table + clinical analysis |
| **Cron section** | SLA stats + pending first-runs | Full job log + error analysis |
| **Business section** | Status only | Detailed breakdown |
| **Security section** | FAIL count + trend | Full FAIL/WARN/OK tables |
| **Length** | ~400-500 words body | ~600-800 words body |
| **Key section** | TODAY'S PRIORITIES | LEARNING METRICS & PATTERNS |
| **Delivery** | Topic 10 (briefing) | Topic 10 (briefing) |

## Data Sources

Read in this order. Each source informs a section of the report.

### 1. Health Logs
- H: Check BOTH paths — `C:\\Users\\User\\HEALTH_LOG_YYYY-MM.md` (root) AND `memories/health/H/HEALTH_LOG_YYYY-MM.md`. Use whichever has the most recent entries. **The `memories/health/H/` path is typically the most up-to-date** — H's entries are written there by the health-check cron jobs. The root path may lag.
- Comfort: `memories/health/mum/health-log.md` (current) or latest dated file in `memories/health/mum/`. Also check `C:\\Users\\User\\CARE_LOG_COMFORT_YYYY-MM.md` if referenced.
- Dad: `C:\\Users\\User\\.hermes\\workspace\\FAMILY_INSIGHTS_DAD.md` for medical context. Check `C:\\Users\\User\\CARE_LOG_DAD_YYYY-MM.md` for daily care log entries.
- Check cron output for delivery failures (DNS errors, connection errors) — a failed delivery means no prompt was sent, which is different from a non-response.
- **Distinguish `[SILENT]` from errors:** A cron returning `[SILENT]` means the agent had no data to report (e.g., no carer data source). A `RuntimeError` or `Connection error` means the delivery mechanism failed. These are different signals — `[SILENT]` = no content, error = delivery broken.

### 2. Business Checkins
- `memories/business/BUSINESS_CHECKINS_YYYY-MM.md`
- WhatsApp gateway status from latest security audit or `gateway_state.json`

### 3. Cron Output Files (Past 24 Hours)
- `~/.hermes/cron/output/*/YYYY-MM-DD_*.md`
- Read ALL output files from today
- **Failed jobs** have `## Error` section instead of `## Response` — these are critical signals
- **Successful jobs** have `## Response` — summarize key findings

### 4. Security Audit
- `~/.hermes/memories/security/SECURITY_AUDIT_YYYY-MM-DD.md` (today's — note: security cron writes to `~/.hermes/memories/security/`, NOT `workspace/memories/security/`)
- Or from the security-policy-check cron output directories
- **⚠️ FAIL count variance:** The security-policy-check job runs every 6 hours and may produce DIFFERENT FAIL counts across runs on the same day (e.g., 8→7→6). This is normal — different audit runs may skip checks that already passed or weight items differently. Do not treat small same-day FAIL count changes as meaningful trends. Compare against the most recent run only, and only flag a trend when the same new FAIL item appears across 2+ consecutive days.

- **⚠️ Scope consolidation vs. remediation:** When the FAIL count drops significantly between morning and evening runs (e.g., 7 FAIL at 06:12 → 3 FAIL at 18:13), check whether the drop is due to actual fixes or just scope consolidation. The evening run may count fewer categories while the underlying issues remain identical. In reports, note "3 FAIL (evening) / 7 FAIL (morning) — scope consolidation, not remediation" until H actually addresses items. Only claim remediation when specific FAIL items are confirmed resolved.

- **Cron schedule drift detection:** If a cron job fires at an unexpected time (e.g., health-check-morning at 00:53 instead of 08:15), this indicates a timezone or schedule drift issue. The `*-morning` jobs with schedule `4 8 * * *` should fire at ~08:04 UTC+1. A 00:53 timestamp suggests the scheduler interpreted the cron expr as UTC instead of local time, or there was a DST transition issue. Flag as "⚠️ Schedule drift detected — job fired at XX:XX, expected YY:YY" in reports so H can investigate the scheduler timezone config.

- **Telegram topic delivery fallback is NOT a failure:** When a cron job's `deliver` field is set to `telegram:CHAT_ID:THREAD_ID` and the topic doesn't exist, the system gracefully falls back to delivering to the main chat. The `last_delivery_error` field will say "configured thread_id N for telegram:CHAT_ID was not found; delivered without thread_id". This is **expected behavior**, not an error. Do not flag it as a delivery failure in reports. Only flag it if H confirms the topic was intentionally created and should exist — then the chat config needs updating, not the job.

- **`deliver` field ≠ `send_message` tool:** The reliable cron delivery path is the job's `deliver` field (set in jobs.json), which routes the agent's final response to the correct Telegram chat/topic. Jobs whose prompts say "use send_message to post" WILL FAIL in cron because that tool is unavailable. Fix: change the prompt to produce the response text directly and let `deliver` handle routing. See `references/skill-update-notes-2026-05-29b.md` for the full pattern analysis.

- **dad-health-afternoon timeout pattern:** The `dad-health-afternoon` job (13:30) can fail with `TimeoutError: idle for 1524s (limit 600s)` — this means the agent got stuck in API error recovery (usually 3 retries) and exceeded the 10-minute idle timeout. This is NOT the same as a Connection error or a send_message failure. It indicates the job's prompt is too complex for the retry budget — the agent spends all its time retrying API calls instead of producing a response. Fix: simplify the job prompt or add `"no_agent": true` with a script-based approach.

### 5. System Health
- `~/.hermes/cron/jobs.json` — parse for: total jobs, success rate, failed jobs, new jobs
- Disk: `df -h /c`
- Session count: count `session_YYYYMMDD*` files in `~/.hermes/sessions/`

## Report Structure

### Morning Briefing Format (06:36)

```
# 📋 DAILY SYSTEM BRIEFING — Day, Date
**Generated:** Time | **System:** Hermes version
**Delivery:** Telegram Topic 10

## 🖥️ SYSTEM HEALTH SUMMARY
(Table: metric | value | status emoji)

## ⏱️ CRON SLA STATS
- Total enabled, jobs that fired, success/fail counts, SLA %
- Jobs pending first run today (table)
- Today's cron job log (compact)

## ❤️ HEALTH STATUS
- H: last entry date, gap days, clinical risk
- Comfort: last entry date, gap days, clinical risk
- Health trend (compact table)

## 💼 BUSINESS OPERATIONS
- WhatsApp status
- 2Real / Supply Chain / Content (one line each)

## 🔒 SECURITY POSTURE
- FAIL count + trend, key new findings

## 🚨 KEY ISSUES
- Numbered list, 5-7 items, with severity emojis

## 📌 TODAY'S PRIORITIES
- 🔴 Critical (2-3 items)
- 🟡 Important (3-4 items)
- 🟢 Routine (2-3 items)

## 📊 WEEKLY OVERVIEW
(Compact table: day | health | key events)

*Footer: System status line | Next briefing time*
```

### Nightly Synthesis Format (22:05)

```
# Integrated Daily Synthesis — YYYY-MM-DD (Day)

**Period:** YYYY-MM-DD 00:00 → 22:05 UTC+1
**Generated:** YYYY-MM-DD 22:05 UTC+1

## 1. Health Status
  - H: responses, gap days, clinical risk
  - Comfort: responses, gap days, clinical risk
  - Dad: check-ins delivered (prompts posted), responses received, clinical risk
  - Trend analysis (table comparing last 3-5 days)

## 2. Business Operations
  - WhatsApp status (up/down/retrying)
  - 2Real Shop / Construction / Supply Chain
  - Content pipeline status
  - Business checkin log entries

## 3. Team Status
  - Active team members and channel status
  - Recruitment pipeline
  - Communication assessment (Telegram vs WhatsApp)

## 4. Security Posture
  - FAIL items (carried from previous + new)
  - Remediated items (still holding)
  - Security trend

## 5. System Health
  - Cron execution summary table
  - Today's job log (each job: ✅/❌ + brief note)
  - System resources (disk, sessions)
  - Error log summary

## Priority Actions for Tomorrow
  - Top 5-7 actionable items, prioritized by severity

## Learning Metrics & Key Insights
  - Quantitative snapshot (table: metric vs last 3-5 days)
  - Emerging patterns (2-3 paragraphs of analysis)
```

## Key Metrics to Track

| Metric | Source | Good Direction |
|--------|--------|----------------|
| Health responses (H) | Cron output + health logs | ↑ More |
| Health responses (Comfort) | Cron output + health logs | ↑ More |
| Dad check-ins delivered | Cron output (topic 1) | ↑ More (target: 3/3) |
| WhatsApp uptime | Gateway state | ↑ More |
| Cron SLA | jobs.json `last_status` | ↑ Higher % |
| Security FAIL count | Security audit | ↓ Fewer |
| Disk usage | `df -h` | ↓ Lower % |
| Session count | File count | ↓ Fewer (cleanup) |

## Output

- **Save to:** `memories/insights/INTEGRATED_INSIGHTS_YYYY-MM-DD.md`
- **Post to:** Telegram briefing topic (topic 10, group -1003784520976)
- **Format:** Structured markdown with tables for quantitative data

## Pitfalls

- **Two briefing formats exist.** The 06:36 morning briefing is scannable and action-oriented. The 22:05 nightly synthesis is comprehensive and analytical. Don't produce a 600-word essay at 06:36 — H hasn't had coffee yet.
- **Health log paths are fragmented.** H's health log exists at `C:\Users\User\HEALTH_LOG_YYYY-MM.md` (root, canonical) AND `memories/health/H/HEALTH_LOG_YYYY-MM.md`. Always check both and use the most recent. Comfort's log is at `memories/health/mum/health-log.md`.
- **⚠️ FAIL count variance:** The security-policy-check job runs every 6 hours and may produce DIFFERENT FAIL counts across runs on the same day (e.g., 8→7→6). This is normal — different audit runs may skip checks that already passed or weight items differently. Do not treat small same-day FAIL count changes as meaningful trends. Compare against the most recent run only, and only flag a trend when the same new FAIL item appears across 2+ consecutive days.

- **⚠️ Scope consolidation vs. remediation:** When the FAIL count drops significantly between morning and evening runs (e.g., 7 FAIL at 06:12 → 3 FAIL at 18:13), check whether the drop is due to actual fixes or just scope consolidation. The evening run may count fewer categories while the underlying issues remain identical. In reports, note "3 FAIL (evening) / 7 FAIL (morning) — scope consolidation, not remediation" until H actually addresses items. Only claim remediation when specific FAIL items are confirmed resolved.

- **Cron schedule drift detection:** If a cron job fires at an unexpected time (e.g., health-check-morning at 00:53 instead of 08:15), this indicates a timezone or schedule drift issue. The `*-morning` jobs with schedule `4 8 * * *` should fire at ~08:04 UTC+1. A 00:53 timestamp suggests the scheduler interpreted the cron expr as UTC instead of local time, or there was a DST transition issue. Flag as "⚠️ Schedule drift detected — job fired at XX:XX, expected YY:YY" in reports so H can investigate the scheduler timezone config.

- **Telegram topic delivery fallback is NOT a failure:** When a cron job's `deliver` field is set to `telegram:CHAT_ID:THREAD_ID` and the topic doesn't exist, the system gracefully falls back to delivering to the main chat. The `last_delivery_error` field will say "configured thread_id N for telegram:CHAT_ID was not found; delivered without thread_id". This is **expected behavior**, not an error. Do not flag it as a delivery failure in reports. Only flag it if H confirms the topic was intentionally created and should exist — then the chat config needs updating, not the job.

- **`deliver` field ≠ `send_message` tool:** The reliable cron delivery path is the job's `deliver` field (set in jobs.json), which routes the agent's final response to the correct Telegram chat/topic. Jobs whose prompts say "use send_message to post" WILL FAIL in cron because that tool is unavailable. Fix: change the prompt to produce the response text directly and let `deliver` handle routing. See `references/skill-update-notes-2026-05-29b.md` for the full pattern analysis.

- **dad-health-afternoon timeout pattern:** The `dad-health-afternoon` job (13:30) can fail with `TimeoutError: idle for 1524s (limit 600s)` — this means the agent got stuck in API error recovery (usually 3 retries) and exceeded the 10-minute idle timeout. This is NOT the same as a Connection error or a send_message failure. It indicates the job's prompt is too complex for the retry budget — the agent spends all its time retrying API calls instead of producing a response. Fix: simplify the job prompt or add `"no_agent": true` with a script-based approach.
- **Cron output timestamps:** Filename uses local time; file header `Run Time` is authoritative.
- **Failed jobs matter:** A job with `## Error` is a signal, not noise. Always report failures.
- **New jobs haven't run:** Jobs created today with no `last_run_at` are expected — not failures.
- **Dad health check-ins now operational:** Since ~May 19, the 3 daily dad health check-in cron jobs (morning 08:07, afternoon 13:30, evening 19:30) post structured prompts to Telegram topic 1. Track these as "prompts delivered" (not responses) in the health section. Dad's check-ins are separate from H's and Comfort's — they are carer-facing prompts, not self-reported data.
- **Dad care log path:** The daily care log is `C:\Users\User\CARE_LOG_DAD_YYYY-MM.md` (root, NOT in `.hermes/workspace/`). The medical context/summary is in `C:\Users\User\.hermes\workspace\FAMILY_INSIGHTS_DAD.md`. Don't confuse the two — the care log has the daily check-in templates; the insights file has conditions/meds/contacts.
- **DNS failures are systemic:** If one job fails with `getaddrinfo`, all jobs at that time likely failed. Check others. `httpx.ReadError` on Telegram API is a different (newer) failure mode — also self-recurring but indicates network instability.
- **WhatsApp-dependent jobs will fail silently:** If the OpenClaw gateway (port 18789) is down, jobs that depend on WhatsApp will error. Report the dependency, not just the error. The gateway runs as a Windows service via `gateway.cmd` and manages the `@openclaw/whatsapp` plugin — it cannot be restarted from cron. See `references/whatsapp-bridge-failure-protocol.md` for full details.
- **First-run job failures are normal:** When a cron job runs for the first time (no prior `last_run_at`), it may fail due to provider rate limits, missing context, or setup issues. A first-run failure is NOT a critical signal — note it but don't escalate. Only escalate if the job fails on its 3rd+ consecutive run with the same error.
- **health-check-evening has joined health-check-afternoon as a failing job:** As of May 25, `health-check-evening` (19:00) now fails with `Connection error` (previously it returned `[SILENT]`). Track it alongside `health-check-afternoon` as a distinct recurring failure. Both are H-facing health prompt jobs that previously returned `[SILENT]` (no content) but are now actively erroring — this indicates a delivery mechanism degradation, not a data availability issue.
- **dad-health-evening skill-not-found failure:** As of May 25, `dad-health-evening` fails with `skill not found, skipping — Skill 'elder-care-dad' not found.` The skill name referenced in the cron job config (`elder-care-dad`) does not match the actual installed skill (`elder-care-operations`). This is a config mismatch, not a code bug — the cron job definition needs its skill reference updated. Flag this as a KEY ISSUE until H corrects the skill name in the job config.
- **mum-health-evening vs morning/afternoon:** The evening mum check-in frequently returns `[SILENT]` (no data source available) while morning/afternoon produce templates. This is expected — do not report `[SILENT]` evening as a failure. Only flag if morning or afternoon check-ins fail to deliver their prompt.
- **Don't re-read full session JSONs:** Use `session_search` for user activity summaries. Session JSONs are 100KB+ each.
- **Synthesis supersedes earlier versions:** If a nightly consolidation ran at 03:00, this 22:05 synthesis should be more comprehensive.
- **integrated-daily-synthesis itself can fail:** This job (22:05) depends on the same OpenRouter provider as all other jobs. If it failed yesterday, do not attempt to "chain" from yesterday's missing report — just overwrite with today's comprehensive version. Check for yesterday's file before writing, but don't error if it's absent.
- **Save to BOTH locations:** Write the report to both `~/.hermes/memories/insights/INTEGRATED_INSIGHTS_YYYY-MM-DD.md` AND `~/.hermes/workspace/memories/insights/INTEGRATED_INSIGHTS_YYYY-MM-DD.md`. The workspace copy is the primary reference; the global copy ensures persistence across workspace resets.
- **`execute_code` is blocked in cron sessions:** Python `execute_code` is denied at runtime in cron mode ("Cron jobs run without a user present to approve it"). Do NOT attempt to use it from any cron job — including synthesis, consolidation, or status reports. Use `terminal`, `read_file`, `search_files`, `patch`, and other standard tools instead. This also means you cannot use `execute_code` to call the Telegram Bot API from cron — produce your response as final text and let `deliver` handle routing.

- **Memory tool unavailable in cron sessions:** The `memory` tool returns "Memory is not available" when running as a cron job. Do NOT attempt to write memory entries during synthesis or consolidation — they will fail silently or error. Rely on file-based persistence only (`memories/insights/`, `memories/security/`, `memories/MEMORY.md`).
- **`session_search` errors in cron sessions:** The `session_search` tool returns a hard error (\"not available\" or permission denied) in cron context — it is not silently blocked. Do NOT retry it. Use `grep "inbound message" ~/.hermes/logs/gateway.log | grep 'YYYY-MM-DD'` to reconstruct today's user activity timeline, then supplement with `session_search` only in interactive (non-cron) sessions.
- **Gateway log for user activity:** When `session_search` is unavailable, use `grep "inbound message" ~/.hermes/logs/gateway.log` to reconstruct today's user activity timeline. Filter by date and platform as needed.
- **Python on Windows MSYS:** The `python` command is not on PATH in MSYS bash on Windows. Use `python3` or the full venv path (`/c/Users/User/AppData/Local/hermes/hermes-agent/.venv/Scripts/python.exe`). Better: use `execute_code` for any non-trivial parsing — it handles the venv automatically.
- **Two MEMORY.md files exist.** `~/.hermes/memories/MEMORY.md` (global, injected into every session) AND `~/.hermes/workspace/memories/MEMORY.md` (workspace-specific). Update BOTH during consolidation. The global one should be more compact; the workspace one can have more operational detail.
- **Archive directory is `sessions/.archive/`, not `memories/archive/`.** Old session files (both `.jsonl` and `session_cron_*.json`) go to `~/.hermes/sessions/.archive/`. Do NOT move them to `memories/archive/` — that directory is for insight/analysis archives, not session data.
- **Nightly consolidation (03:00) produces a report, not [SILENT].** The 03:00 job always produces a processing report saved to `workspace/DAILY_PROCESSING_REPORT_YYYY-MM-DD.md`. Only use `[SILENT]` if there is genuinely nothing new to report (all jobs healthy, no new issues, no sessions to process).
- **Gateway log for Telegram errors:** Check `~/.hermes/logs/gateway.log` for the most recent entries to assess Telegram connectivity. `httpx.ReadError` entries that self-recover within 5-15s are transient; persistent patterns indicate DNS or network config issues.
- **Error log tail:** The errors.log is large (20,000+ lines). Use `tail` or `offset` near the end to get recent entries. Focus on `WARNING` and `ERROR` lines with timestamps in the last 24h.
- **No `hermes message send` CLI subcommand:** There is no `hermes message send` command. The CLI has no messaging subcommand at all. To deliver from a cron job, the cron job's `deliver` field must be set to the correct Telegram target (e.g., `telegram:-1003784520976:10` for topic 10). The agent's final response text IS the delivery — put the user-facing content directly in the response. Do NOT attempt `hermes message send`, `hermes telegram send`, or any variant — they will all fail with "invalid choice". To inspect cron execution history, use `hermes cron list` (shows last_run_at + last_status per job) combined with reading `~/.hermes/logs/agent.log` and `~/.hermes/logs/errors.log` directly. The `hermes cron status` command only checks if the gateway scheduler is running.
- **MSYS path mangling with `node -e`:** When running inline Node.js via `node -e "..."` in MSYS bash, Windows paths like `/c/Users/...` get mangled to `C:\c\Users\...`. Workaround: write a temporary `.js` file with `write_file` and then run it with `node /tmp/script.js`. Same issue affects inline Python with `python3 -c "..."`.
- **`jobs.json` field names:** The fields are `last_run_at` (ISO 8601 timestamp, not `last_run`) and `last_status` (values: `"ok"` or `"error"`, not `"failed"`). Jobs that have never run simply lack the `last_run_at` key entirely (it's absent, not `null`). Use `grep -oP '"last_run_at":\s*"[^"]*"'` to extract reliably.
- **`execute_code` is blocked in cron sessions:** Python `execute_code` is denied at runtime in cron mode ("Cron jobs run without a user present to approve it"). Do NOT attempt to use it from any cron job — including synthesis, consolidation, or status reports. Use `terminal`, `read_file`, `search_files`, and other standard tools instead.

- **Cron-status-report is self-referential:** The `cron-status-report` job (this job) runs at 09:00 daily and produces a Daily Cron Status Report. When auditing cron health, exclude this job from the "jobs that ran" count to avoid circularity, or note it explicitly as "self."
- **WhatsApp bridge failure protocol:** When the WhatsApp bridge is down, all WhatsApp-dependent cron jobs (ebony-goodnight, mum-checkin, dad-checkin, sammy-check, john-check, etc.) will fail. Follow the protocol in `references/whatsapp-bridge-failure-protocol.md`: check bridge health first, draft messages even when down, log attempts, report via Telegram with explicit "NOT SENT" status. Never mark a WhatsApp send as successful unless the bridge confirmed delivery.

- **Posting to Telegram topics via Bot API from cron:** When the cron job's `deliver` field is `origin` (not a Telegram target) and you need to post to a specific Telegram topic, use `execute_code` with Python's `urllib.request` to call the Bot API directly. Read the bot token from `~/.hermes/.env` (key `TELEGRAM_BOT_TOKEN`). Format: `https://api.telegram.org/bot{token}/sendMessage` with JSON body `{"chat_id": "-1003784520976", "message_thread_id": <topic_id>, "text": "..."}`. Important: `parse_mode: "HTML"` may cause HTTP 400 errors when combined with `message_thread_id` on some topics. If you get a 400, retry without `parse_mode` (send as plain text). Never drop `message_thread_id` — that's what routes to the correct topic.

- **health-check-evening escalated from SILENT to error:** As of May 26-27, `health-check-evening` (19:00) now fails with `RuntimeError: Connection error` — it previously returned `[SILENT]` (no content). This is a delivery mechanism degradation, not a data issue. Track as a distinct recurring error. If it persists 3+ consecutive days, investigate whether the Telegram API endpoint or network path is failing for the 19:00 time window specifically.

- **Telegram topic 2 (health) may not exist:** `health-check-morning` (08:18) attempted to deliver to `telegram:123286468:2` but topic 2 was not found, so it fell back to the main chat. The health channel is supposed to be topic 2, but it may not exist in the current chat config. This means H's health check prompts go to the main chat instead of a dedicated health topic. Note this delivery fallback in health summaries — "delivered to main chat (topic not found)" is not a failure, but it means health prompts mix with general messages. If H confirms topic 2 was intentionally removed, update the health-check-morning cron job's target chat_id to remove `:2`.

- **Use `ls` not `read_file` to find cron output files:** Cron output filenames use local time with dashes (e.g., `2026-05-27_19-00-44.md`), and guessing exact filenames via `read_file` fails repeatedly. Always use `terminal` with `ls` first to enumerate actual files, then read. MSYS path resolution for wildcards in `read_file` is unreliable. Pattern: `ls /c/Users/User/.hermes/cron/output/<job-id>/2026-05-27*` → iterate results.

- **Evening health check jobs (all) now failing with Connection error:** As of May 26-27, BOTH `health-check-evening` (topic 2) and `mum-health-evening` (topic 4) fail with `RuntimeError: Connection error`. The `health-check-afternoon` (13:00) ran OK on May 26 — so the failure is specific to the 19:00 run, not all health check jobs. This pattern (both evening jobs failing simultaneously) suggests a transient network/API issue at that time of day rather than a per-job config problem. Track as one combined "evening health check delivery failure" in synthesis reports, not two separate root causes.

- **health-check-afternoon escalated to send_message unavailable:** As of May 26-27, `health-check-afternoon` (13:02) now fails because `send_message` tool is genuinely unavailable in some cron session contexts — the agent responds with a "no send_message tool available" message rather than `[SILENT]` or a connection error. This is distinct from the evening `Connection error` pattern. When the output contains phrases like "I don't have a `send_message` tool available in my current toolset" or "My available tools don't include Telegram", the actual delivery mechanism (auto-response via `deliver` field) is the path, not send_message. Note this as "❌ Failed — send_message unavailable" in reports, distinct from "⚠️ SILENT" and "❌ Connection error".

- **dad-health-morning ALSO affected by skill config mismatch:** The `elder-care-dad` → `elder-care-operations` mismatch affects BOTH `dad-health-morning` (08:07) AND `dad-health-evening` (19:30), not just the evening job. Morning output shows BOTH the skill-not-found warning AND send_message unavailability. Track both dad failures as having the same root cause (skill name config mismatch) until H corrects the skill reference in both cron job configs.

- **Connection error clusters indicate systemic failure:** When 3+ jobs fail with `RuntimeError: Connection error` within a 2-hour window, this is a **systemic connectivity issue** (OpenRouter API, TLS, or gateway network), NOT independent per-job failures. Group under one "Systemic Connection Failure" issue in reports — don't list each job separately. Check `gateway.log` for TLS errors in the failure window. A Cron SLA drop >20% from the previous day with a shared error string = systemic flag. See `references/skill-update-notes-2026-05-29.md` for SLA collapse thresholds and the May 29 cluster case study.

- **Backup failure during connection error window = compound risk:** When the daily backup fails with Connection error, the workspace may also be unsynced. 5+ days without verified backup during a connection outage is a data loss window — flag as COMPOUND RISK in consolidation reports. Verify workspace file integrity if backup has been failing.

- **WhatsApp creds.json missing (not just stale session):** There are two distinct WhatsApp failure modes: (1) Session expired/stale — gateway shows "Logged out. Delete session and restart to re-authenticate." — fix: delete session dir + restart gateway.cmd. (2) creds.json entirely missing — gateway shows "WhatsApp is enabled but not paired (no creds.json)" or similar — fix: full QR re-pair via `hermes whatsapp`. Mode 2 is worse; deleting the session directory alone will not fix it. Check the gateway log or job output for "no creds.json" vs "Logged out" to distinguish. Report the exact mode in synthesis.

- **Security audit scope expansion causes same-day FAIL count jumps:** The security-policy-check job's audit scope can expand across runs on the same day (e.g., 6 FAIL → 13 FAIL) when new check categories are activated. This is NOT the same as new breaches — it's previously-undetected items that were already present. When comparing FAIL counts across audits, check whether NEW FAIL items appeared or whether the same items are just being counted under expanded categories. The skill's existing "FAIL count variance" pitfall covers run-to-run variance; this is specifically about scope expansion that can double the FAIL count in a single day. Treat scope-expansion jumps as "scope expanded" not "WORSENED" in trend analysis.

- **OpenRouter HTTP 429 rate limit clusters are distinct from Connection Error clusters:** When jobs fail with `RuntimeError: HTTP 429`, the provider is throttling — the network is fine but the server is rejecting requests. Do NOT group 429 failures under "Connection Error" in reports. Track as a separate "Rate Limit Throttle" category. Unlike connection errors (which indicate network/DNS issues), 429s usually self-recover within 1-2 hours. A 429-induced backup failure is "backup delayed" not "backup lost." See `references/skill-update-notes-2026-05-30.md` for the full distinction.

- **Health data gap escalation thresholds:** 0-3 days = normal. 4-6 days = flag as "⚠️ Health data gap." 7+ days = flag as "🔴 Extended health data gap — clinical trend analysis impossible." When gap exceeds 7 days, recommend checking the archive workflow — health-check cron responses may be delivered to Telegram but not saved back to HEALTH_LOG files. See `references/skill-update-notes-2026-05-30.md` for gap analysis methodology.

## Related Skills

- `elder-care-operations` — health check-in templates, care log format, escalation paths
- `hermes-security-audit` — security audit methodology, FAIL item tracking
- `kanban-worker` — task board sync, brain dump parsing

## Reference Files

- `references/cron-output-parsing.md` — cron output structure, parsing patterns, `[SILENT]` vs error distinction
- `references/health-log-paths.md` — health log file paths for H, Comfort, and Dad with cron job mapping
- `references/nightly-consolidation.md` — 03:00 nightly consolidation workflow (file processing, intelligence updates, archiving)
- `references/morning-briefing-cron.md` — 06:36 morning briefing cron details, data gathering order, format differences
- `references/cron-delivery-telegram.md` — Telegram delivery from cron: how it works, what doesn't, finding chat IDs, [SILENT] suppression
- `references/whatsapp-bridge-failure-protocol.md` — WhatsApp bridge health checks, fallback procedures, outage patterns
- `references/skill-update-notes-2026-05-29.md` — Connection error cluster pattern, backup/connection compound risk, SLA collapse thresholds, request dump growth tracking, dad-health-morning dual failure mode
- `references/skill-update-notes-2026-05-29b.md` — Cron schedule drift, deliver_field vs send_message distinction, security scope consolidation, H in Ghana operational context
- `references/skill-update-notes-2026-05-30.md` — HTTP 429 rate limit clusters vs connection errors, health data gap escalation thresholds, content-performance and dad-health-afternoon error tracking
