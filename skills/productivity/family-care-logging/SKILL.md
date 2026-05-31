---
name: family-care-logging
description: Receive, parse, and log family health check-in updates from Telegram replies. Compiles structured daily care logs (meals, vitals, pain, mood, medications) into monthly markdown files. Triggered when H replies to cron health check-ins with meal/vitals data.
version: 1.0.0
author: hermes-agent
triggers:
  - H replies to a health check-in cron with meal, vitals, or symptom data
  - H says "breakfast", "lunch", "dinner" with food/drink items in health context
  - H reports pain levels, blood pressure, pulse, or medication status
  - User asks to compile or review care logs
  - Weekly/monthly care summary is requested
platforms: [windows]
---

# Family Care Logging

## Overview

Receive ad-hoc health updates from H (replying to cron check-in prompts in Telegram), parse the data, and compile structured daily care logs into monthly markdown files. Currently used for Comfort (H's mum, 91).

## Source of Data

- **Cron jobs** post check-in prompts to Telegram topic (health-log-mum, id 4 in the Orchestrator group; or the equivalent topic in H's main group).
- **H replies** in the Telegram topic with meal names, drinks, vitals, pain levels.
- Replies are forwarded to this session as "Cronjob Response" messages with H's reply text.
- **H may also send images** (e.g., photos of meals, pill organizers). Vision analysis may not be available depending on the active model — if `vision_analyze` fails, ask H to describe the image in text.

## How to Parse a Reply

H's replies are short and casual. Extract:

1. **Meal items** — food and drink listed (e.g., "two boiled eggs drink fennel tea" → breakfast: 2 boiled eggs + fennel tea)
2. **Vitals** — blood pressure, pulse, temperature (if provided)
3. **Pain** — level (0-10) and location
4. **Medications** — confirmation of meds taken
5. **Mood/notes** — any extra context

### Parsing Rules
- "Drink X" → fluids entry
- Food items separated by commas, "and", or line breaks → list as bullet items
- If no vitals are mentioned, log as "Not reported" (don't prompt again in the reply)
- If H sends an image and vision fails, say: "Can't see the image clearly — can you tell me what's there?"
- **Never ask H to fill in a template.** Just log what's given and move on.

## Log File Format

Save to: `~/.openclaw/workspace/memory/CARE_LOG_<NAME>_YYYY-MM.md`

### Daily Entry Template

```markdown
## Day, Date

### 🌅 Morning (HH:MM)
- **Breakfast:** [items]
- **Fluids:** [drinks]
- **Appetite:** Good / Moderate / Poor
- **Vitals:** [BP/pulse/temp] or Not reported
- **Pain:** [level/10, location] or None reported
- **Mood:** [note]
- **Medications:** Confirmed / Not confirmed
- **Notes:** [any extra context]

### 🌤️ Afternoon (HH:MM)
- **Lunch:** [items]
- **Fluids:** [drinks]
- **Vitals:** [if reported]
- **Pain:** [if reported]
- **Notes:** [context]

### 🌙 Evening (HH:MM)
- **Dinner:** [items]
- **Fluids:** [drinks]
- **Vitals:** [if reported]
- **Pain:** [if reported]
- **Notes:** [context]

### 📊 Daily Summary
- **Meals:** [X/3] — [appetite summary]
- **Hydration:** [Good/Fair/Poor]
- **Pain:** [summary]
- **Mood:** [summary]
- **Red Flags:** [any concerns or None]
- **Overall:** [one-line assessment]
```

## Response Style

When logging an update, reply with:
1. ✅ Brief confirmation of what was logged (1 line)
2. Any red flags if present (concise)
3. **Do NOT** send a template for H to fill in — they already replied with the data
4. **Do NOT** ask follow-up questions unless there's a critical gap (e.g., "Mum collapsed" with no context)

## Compiling Full Day Logs

When you have 2+ entries for the same day:
1. Open the monthly log file
2. Update the relevant daily section with new data
3. Recompute the Daily Summary
4. Tell H: "Updated today's care log — [X] meals logged, [summary]"

## Weekly Summary

The `health-weekly-review-mum` cron job handles weekly analysis. If asked to compile manually:
1. Read the past 7 days from the monthly log
2. Identify trends: appetite changes, pain patterns, hydration concerns
3. Flag any red flags for H
4. Post summary to the health-log-mum Telegram topic

## Telegram Delivery (How to Post Check-Ins)

When posting check-in prompts to Telegram topics via the Bot API, see `references/telegram-bot-api-cron.md` for the full pattern, chat IDs, and troubleshooting.

**The reliable pattern — write JSON to a temp file, use `curl -d @file`:**

```bash
TOKEN=$(grep TELEGRAM_BOT_TOKEN ~/.hermes/.env | cut -d= -f2-)
TMPFILE=$(mktemp /tmp/tg_payload.XXXXXX.json)
cat > "$TMPFILE" << 'ENDJSON'
{
  "chat_id": "-1003784520976",
  "message_thread_id": <TOPIC_ID>,
  "text": "<MESSAGE_BODY>",
  "parse_mode": "HTML"
}
ENDJSON
curl -s -X POST "https://api.telegram.org/bot${TOKEN}/sendMessage" \
  -H "Content-Type: application/json" \
  -d @"$TMPFILE"
rm -f "$TMPFILE"
```

**Why this pattern:** Passing JSON directly in the shell command fails when the message contains parentheses, emoji, or special characters — bash interprets them as syntax. Writing to a temp file and using `@` bypasses all escaping issues entirely.

**Topic IDs:**
| Topic | ID |
|-------|----|
| health-log-mum (Comfort) | 4 |
| health-log (H) | 2 |
| briefing | 10 |
| memory-review | 20 |

**Token location:** `~/.hermes/.env` → `TELEGRAM_BOT_TOKEN`
**⚠️ The `.env` file is hex-encoded — `grep` will NOT work.** Use `od -A n -t x1 ~/.hermes/.env` to decode first, or use the Python extraction method. See `references/telegram-bot-api-cron.md` for both methods.

**Do NOT** use inline JSON with `curl -d '{...}'` for messages containing emoji or parentheses — it will silently fail or produce shell syntax errors.

## Templates

| Template | Path | Use |
|----------|------|-----|
| Morning check-in (Comfort) | `templates/morning-checkin-comfort.md` | 08:04 morning care prompt |
| Afternoon check-in (Comfort) | `templates/afternoon-checkin-comfort.md` | 13:00 midday care prompt |
| Evening check-in (Comfort) | `templates/evening-checkin-comfort.md` | 19:00 evening care prompt |
| Evening check-in (H) | `templates/evening-checkin-h.md` | 19:00 evening health prompt for H |

## Pitfalls

1. **Don't re-prompt H for data.** They gave you what they gave you. Log it and stop.
2. **Don't send templates back to H.** The cron job already sent the template. H is replying to it. Your job is to log, not re-ask.
3. **Vision failures are normal.** The active model may not support image input. Ask for text description instead of retrying vision.
4. **Cron delivery errors (401, etc.)** from the Orchestrator side don't mean the message didn't reach H. H may still reply in this topic.
5. **Don't create a new file for each entry.** Append/update within the monthly file.
6. **Time zones:** H is in London (Europe/London). Log times in London time.
7. **Multiple people:** Currently only Comfort. If logging for others, use separate files: `CARE_LOG_<NAME>_YYYY-MM.md`.
8. **Don't use inline JSON for Telegram API calls.** Always use the temp-file + `curl -d @file` pattern above.
9. **`send_message` tool is NOT available in cron jobs.** Even though `messaging` is listed under `platform_toolsets.cli`, cron sessions don't get the `send_message` native tool. Always use the Telegram Bot API — either via `curl` (Method 1) or Python `urllib` via `execute_code` (Method 2) as documented in `references/telegram-bot-api-cron.md`.

## File Locations

| File | Path |
|------|------|
| Monthly care log | `~/.openclaw/workspace/memory/CARE_LOG_COMFORT_YYYY-MM.md` |
| Log template | Use the daily entry template in this skill's Overview section |
| Weekly summaries | Generated by cron, posted to Telegram topic |

## Verification

Before saving:
- [ ] Date and time correct (London timezone)
- [ ] All mentioned food/drink items captured
- [ ] Vitals logged if provided, "Not reported" if not
- [ ] No template text sent back to H
- [ ] File saved/updated successfully
