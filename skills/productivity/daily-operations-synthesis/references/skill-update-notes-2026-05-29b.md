# Skill Update Notes — 2026-05-29b

## New Patterns Detected This Session (Evening Synthesis Run)

### Cron Schedule Drift (May 29)

**Observation:** Two jobs fired at wrong times today:
- `health-check-morning` (`4 8 * * *`) fired at **00:53** (expected ~08:15) — off by ~7h20m
- `mum-health-morning` (`4 8 * * *`) first run at **00:54** (expected ~08:17), then ran correctly at 08:17

**Interpretation:** This suggests either:
1. The cron scheduler is running in UTC but jobs were created with local-time expectations
2. A DST transition or timezone config change occurred on the host
3. The scheduler process was restarted and temporarily used UTC before picking up local TZ

**Action:** Flag as schedule drift in reports. Not a per-job failure — a systemic scheduler config issue. H should check `hermes cron` scheduler timezone settings.

### health-check-evening Delivery Success Pattern

**Observation:** `health-check-evening` (19:02) ran OK and actually delivered via the cron `deliver` field to `telegram:123286468:2`. The topic was not found, so it fell back to private chat (message_id 486).

**Key insight:** Jobs with `deliver: "telegram:CHAT_ID:THREAD_ID"` route via the cron gateway — this is the **correct** delivery path. Jobs that try to use `send_message` tool calls fail because that tool is not available in cron context. 

**Rule:** 
- If a job's `deliver` field targets Telegram correctly → the job WILL deliver its final response text automatically. Don't ask the agent to use `send_message` for delivery.
- If a job uses `send_message` in its prompt as the delivery mechanism → it WILL FAIL in cron. The fix is to change the prompt to just produce the text as its response and let the `deliver` field handle routing.

### Send_message Unavailability in Cron (Confirmed Across 6+ Jobs)

Jobs that fail with "send_message not available":
- dad-health-morning (08:17)
- dad-health-afternoon (15:52 — timed out before reaching send_message)
- dad-health-evening (19:30)
- mum-health-evening (19:02 — though deliver field saved it)
- mum-health-morning 00:54 run (HTTP 400 on send_message)

Jobs where `deliver` field worked instead:
- health-check-evening (19:02) ✅
- mum-health-morning 08:17 run ✅ (delivered to topic, though thread_id 4 not found → main chat)

**Takeaway:** The `deliver` field is the reliable cron delivery mechanism. `send_message` tool calls in prompts are unreliable. When writing/reviewing cron job prompts for Telegram-dependent jobs, prefer prompts that say "produce the message as your response" over "use send_message to post to Telegram."

### Security FAIL Count: 7→3 Scope Consolidation

**Morning (06:12):** 7 FAIL / 12 WARN
**Evening (18:13):** 3 FAIL / 4 WARN

**Not remediation** — the same underlying issues exist. The evening audit just counted differently. The 3 remaining FAILs are:
1. FAL_KEY duplicated in `.env`
2. Credential files world-readable (644)
3. Memory tool broken in cron context

The 4 FAILs that disappeared into the count were likely: request dumps (still growing), AGENTS.md BOM, PII redaction, dual Telegram tokens — these were probably reclassified as WARN or INFO in the evening run.

### Compound Risk: Backup + Connection Error

Backup failed with Connection error at 00:50 today. This is the **6th consecutive day** without a verified backup (last good: May 23). During the same connection window (00:49-09:01), 5 other jobs also failed. This is a compound risk: workspace may have changes that aren't captured anywhere.

**Action in reports:** When backup fails during a connection error cluster, flag as "🔴 COMPOUND RISK: Backup failed during connection window — workspace sync unverified for 6+ days."

### H in Ghana — Operational Context Change

H confirmed presence in Ghana at 00:50 UTC via Telegram. This means:
- Comfort care model shifts from remote prompts to direct observation
- H's timezone context is now GMT+0 (Accra) vs UTC+1 (London)
- WhatsApp importance increases (primary Ghana communication channel)
- Interactive sessions may different timing patterns

**Action:** Note "H in Ghana" in health section when confirmed. Adjust Comfort risk assessment — physical presence mitigates data gap.
