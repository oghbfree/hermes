# Health Check [SILENT] Pattern — What It Means

## The Problem

Many elder care and health check cron jobs return `[SILENT]` instead of errors. This happens because:

1. **`send_message` tool unavailable in cron sessions** — The health check jobs (mum-health-morning, health-check-morning, dad-health-morning, etc.) are designed to use `send_message` to post prompts to Telegram. When `send_message` is unavailable, the agent responds with `[SILENT]` to indicate "I have no tool to deliver with."

2. **Job technically succeeds** — `last_status: "ok"` and `last_error: null`. The cron system sees no failure. But the health prompt never reached Telegram.

3. **This is different from:**
   - **Delivery error** — `last_status: "error"` with a runtime/DNS/connection error. The job crashed.
   - **Empty data source** — Agent ran but found no new data (e.g., no new brain dumps). `[SILENT]` here means "nothing new to report."
   - **This case** — Agent ran, composed the prompt, but couldn't deliver it because the delivery tool doesn't exist. `[SILENT]` here means "delivery infrastructure missing."

## How to Detect

Check the Response section in the cron output file:

```
## Response

I'll send the morning health check... However, I don't have access to a 
`send_message` tool in my current environment...

[SILENT]
```

If the response text mentions `send_message` being unavailable → this is a **delivery tool gap**, not an empty data source.

## Jobs Affected (as of 2026-05-24)

| Job | Schedule | Affected? | Notes |
|-----|----------|-----------|-------|
| mum-health-morning | 08:04 daily | ✅ Yes | Returns [SILENT] |
| mum-health-afternoon | 13:00 daily | ⚠️ Partial | Text composed but send_message not called |
| mum-health-evening | 19:00 daily | ⚠️ Partial | Sometimes delivers via final response |
| health-check-morning | 08:04 daily | ✅ Yes | Returns [SILENT] |
| health-check-afternoon | 13:00 daily | ⚠️ Partial | Sometimes delivers via final response |
| health-check-evening | 19:00 daily | ✅ Yes | Returns [SILENT] |
| dad-health-morning | 08:07 daily | ✅ Yes | Returns [SILENT] |
| dad-health-afternoon | 13:30 daily | ✅ Yes | Returns [SILENT] |
| dad-health-evening | 19:30 daily | ✅ Yes | Returns [SILENT] |

## What It Means for the Synthesis

In the integrated daily synthesis:
- Count `[SILENT]` health checks as **"prompts NOT delivered"** — a health monitoring infrastructure gap
- Do NOT count them as cron errors (they're not — `last_status: "ok"`)
- Report separately: "X of Y health prompts failed to deliver due to send_message tool gap"
- The weekly review jobs are NOT affected — they generate reports as their final response which the cron system auto-delivers
