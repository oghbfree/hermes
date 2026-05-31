# Skill Update Notes — 2026-05-30

## New Patterns Detected This Session (Morning Briefing Cron Run)

### OpenRouter HTTP 429 Rate Limit Clusters (Distinct from Connection Errors)

**Observation:** `daily-backup` (23:03) and `janet-friday-checkin` (20:32) both failed with `RuntimeError: HTTP 429: Provider returned error` — the provider is rate-limiting the `openrouter/owl-alpha` model ("temporarily rate-limited upstream" from Stealth provider).

**Distinction from Connection Error clusters:**
- **Connection error** = network-level failure (DNS, TLS, TCP). Check gateway.log for `httpx.ConnectError` or `httpx.ReadError`.
- **HTTP 429** = provider-side throttling. The request reached the server but was rejected due to rate limits. Check errors.log for `RateLimitError` and `HTTP 429`.

**Implication:** During a 429 window, retrying does NOT help — the provider is explicitly telling you to back off. Jobs that fail with 429 should NOT be retried within the same hour. The scheduler's built-in retry (3 attempts) just burns tokens.

**Action in reports:** Group 429 failures under "Rate Limit Throttle" (distinct from "Connection Failure"). Note the affected jobs and the time window. If >2 jobs fail with 429 in the same hour, flag as "🔴 OpenRouter rate limit throttle — N jobs affected."

**SLA impact:** A 429-induced backup failure is less urgent than a connection-error-induced backup failure. The provider usually recovers within 1-2 hours. If backup fails with 429, it will likely succeed on the next day's run. Flag as "backup delayed, not lost."

### Health Data Gap >7 Days = Clinical Risk Escalation

**Observation:** No self-health entries since May 23 (7-day gap). Mum's last detailed entry also May 23. The health-check cron jobs are running (showing `ok` status) but the actual health data is not being captured/archived.

**Thresholds for escalation:**
- 0-3 days gap: normal (weekend, travel)
- 4-6 days gap: flag as "⚠️ Health data gap — N days"
- 7+ days gap: flag as "🔴 Extended health data gap — N days. Clinical trend analysis impossible."

**Root cause hypothesis:** The health-check cron jobs deliver prompts to Telegram (topic 2 for H, topic 4 for mum). H responds in Telegram. But the responses may not be getting archived back into the HEALTH_LOG files. The gap could be in the *intake* side (H didn't respond) or the *archive* side (responses weren't saved). Check the cron output for the most recent health-check returns — if prompts were delivered but no response was captured, the archive workflow needs fixing.

**Note for future runs:** When health gap exceeds 7 days, include a specific recommendation: "Archive workflow for health responses may be broken — verify that health-check cron job responses are being saved to HEALTH_LOG files, not just delivered to Telegram."

### saturday-content-performance Error Status

**Observation:** The `saturday-content-performance` job (09:11 Saturday) shows `last_status: error` in jobs.json. This job was previously OK.

**Action:** Check today's cron output for this job after 09:11 UTC+1. If it failed, include in "Today's issues" section. If it hasn't run yet (timestamp is from a previous Saturday), note as "pending — runs at 09:11."

### dad-health-afternoon Error Status

**Observation:** `dad-health-afternoon` (13:30) shows `last_status: error`. This is separate from the previously-documented timeout pattern and the skill config mismatch. The error root cause needs investigation — check today's cron output for the specific error string.

**Previously documented dad failures:**
- Timeout (>600s idle): prompt too complex
- `elder-care-dad` skill not found: config mismatch
- `send_message` unavailable: use `deliver` field instead

**This session:** New `error` status — check if it's a new failure mode or one of the above recurring.

### Systemic Pattern Summary (May 29-30)

| Failure Mode | Affected Jobs | Root Cause | Urgency |
|---|---|---|---|
| HTTP 429 (rate limit) | daily-backup, janet-friday-checkin | OpenRouter provider throttle | Low (self-recovers) |
| Connection error cluster | See May 29 notes | Network/TLS | Medium |
| Skill config mismatch | dad-health-morning, dad-health-evening | elder-care-dad → elder-care-operations | High (persistent) |
| Health data gap | H self-log, mum log | Archive workflow or intake gap | High (7+ days) |
| Discord spam | N/A (platform adapter) | No token configured | Low (cosmetic) |
| Content performance error | saturday-content-performance | Unknown (check output) | Medium |
| WhatsApp gateway process not running | All 8 WhatsApp jobs | OpenClaw process dead, port 18789 not listening (29+ days) | HIGH — blocks all business comms |

## Skills Updated This Session (sammy-morning-check cron run)

### business-operations-tracking — `references/supplier-outreach-tracking.md`
- **Added Section 2b: Business Operator Check-in Messages** with reusable templates for Sammy (2Real shop) and John (field ops) morning messages, including rotation variations and rules for each.
- **Added pitfall: contacts.json phone numbers are partially redacted** — always use `CONTACTS.md` for full unredacted numbers when the gateway comes back.
- **Added pitfall: WhatsApp phone format for Baileys gateway API** — `233XXXXXXXXX@s.whatsapp.net` (no `+` prefix).

### daily-operations-synthesis — `references/whatsapp-bridge-failure-protocol.md`
- **Patched "Log the Attempt" (Step 2): Added extended outage compaction guidance.** After 5+ consecutive identical failures, agents should update the existing entry's date stamp and counter rather than appending full duplicate blocks. This prevents the log file from growing into repetitive noise. Full entries resume when the failure mode changes.

## New Patterns Detected This Session (sammy-morning-check cron run)

### WhatsApp Gateway Process Not Running (Distinct from Session Expired)

**Observation:** The OpenClaw gateway process is not running — `ps aux | grep openclaw` returns nothing, port 18789 not listening. This is different from "session expired" (where the gateway IS running but WhatsApp is logged out). The gateway-restart.log shows last restart was May 4 — the process has been dead for 26+ days.

**Diagnostic distinction:**
- **Gateway process dead** → `ps aux | grep openclaw` empty, port 18789 not listening. Fix: H must start gateway.cmd from Windows.
- **Gateway running but session expired** → process exists, port listening, but gateway log shows "Logged out." Fix: delete session dir + QR re-pair.
- **Gateway running, session valid, but WhatsApp disconnected** → process exists, port listening, log shows connection errors. May self-recover or need gateway restart.

**In reports, always specify which of the three states was observed** — don't just say "WhatsApp down."

### sammy-morning-check: 8+ Consecutive Identical Failures

**Observation:** The sammy check-in log (`workspace/memories/business/checkins/sammy.md`) has 8 identical failure entries. Each run appends a full block with the same "WhatsApp bridge offline" message. This makes the log harder to read over time.

**Fix applied:** Updated the whatsapp-bridge-failure-protocol to use compact logging during extended outages (update date + counter, collapse prior identical entries). Future runs of sammy-morning-check should use this compact format.
