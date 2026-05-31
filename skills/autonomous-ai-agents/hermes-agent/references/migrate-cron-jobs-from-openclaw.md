# Migrating Cron Jobs from OpenClaw to Hermes

## Architecture: CRON_CONFIG → SKILL.md

OpenClaw's cron system follows a two-layer architecture that maps cleanly to Hermes:

| OpenClaw Layer | Purpose | Hermes Equivalent |
|---|---|---|
| **CRON_CONFIG** (jobs.json) | Schedule + trigger + delivery | `hermes cron create` prompt + delivery config |
| **SKILL.md** (skills/<name>/SKILL.md) | Execution playbook — persona, steps, format | Hermes skill loaded at job runtime via `skills` param |

**Rule of thumb:** The cron prompt stays ≤20 lines (the "what"). The skill stays unlimited (the "how").

## Step-by-Step

### 1. Extract OpenClaw Cron Jobs

OpenClaw stores jobs in `~/.openclaw/cron/jobs.json`. Each job has:

```json
{
  "id": "uuid",
  "name": "health-log-morning",
  "enabled": true,
  "schedule": {
    "kind": "cron",
    "expr": "01 8 * * *"     // cron expression: minute hour day month weekday
  },
  "payload": {
    "kind": "agentTurn",     // "agentTurn" = sends message to agent; "systemEvent" = executes prompt
    "message": "Execute skill:morning_health_check..."
  },
  "delivery": {               // optional — where output goes
    "mode": "announce",
    "channel": "telegram",
    "to": "-1003620024352",
    "topicId": 50
  }
}
```

### 2. Categorize by Delivery Channel

| Delivery | Migration Status | Notes |
|---|---|---|
| Telegram topic | ✅ Migrate now | Needs topic IDs mapped (see migrate-telegram-topics-from-openclaw.md) |
| WhatsApp | ⏳ Wait | Needs Hermes WhatsApp gateway configured first |
| Local/log | ✅ Migrate now | Results logged to file or local delivery |

### 3. Create Each Hermes Cron Job

Use `hermes cron create` with appropriate schedule syntax:

```bash
hermes cron create "01 8 * * *" \
  --name "health-log-morning" \
  --deliver telegram \
  --chat "-1003620024352" \
  --prompt "$(cat <<'PROMPT'
Post the morning health check template to Telegram topic 50 (#health-log):

"🌅 Morning Health Check — Please log your breakfast and current vitals.

Format for your reply:
Breakfast: [what you ate]
Drink: [what you drank]
Symptoms: [none or describe]
Energy: [1-10]
Sleep: [hours]
"

Log the response to the health log when received.
PROMPT
)"
```

### 4. Schedule Syntax Mapping

| OpenClaw expr | Meaning | Hermes equivalent |
|---|---|---|
| `01 8 * * *` | Daily 08:01 | `01 8 * * *` |
| `13 9 * * 1` | Monday 09:13 | `13 9 * * 1` |
| `36 06 * * *` | Daily 06:36 | `36 6 * * *` |
| `04 */6 * * *` | Every 6 hours at :04 | `4 */6 * * *` |
| `0 3 * * *` | Daily 03:00 | `0 3 * * *` |
| `0 9 * * *` | Daily 09:00 | `0 9 * * *` |

Hermes also accepts natural language schedules: `"every 2 days"`, `"every monday 9am"`, `"every 6h"`.

### 5. Delivery Mapping

Hermes cron delivery uses a single colon-delimited string format:

| OpenClaw field | Hermes delivery string |
|---|---|
| `delivery.channel: "telegram"` + `delivery.to` + `delivery.topicId` | `telegram:-1003784520976:2` (format: `platform:group_id:thread_id`) |
| Telegram **DM** (no topic/thread) | `telegram:123456789` (omit thread_id) |
| Local delivery (internal, no external channel) | `local` |
| WhatsApp (when configured) | `whatsapp:+233XXXXXXX` |

**Delivery string breakdown:** `telegram:-1003784520976:2` means:
- `telegram` — platform
- `-1003784520976` — group chat ID
- `2` — topic/thread ID within that group

Create with:
```bash
hermes cron create "01 8 * * *" \
  --name "health-log-morning" \
  --deliver "telegram:-1003784520976:50" \
  --prompt "Post the morning health check..."
```

### 6. Handling OpenClaw Skills (Playbooks)

OpenClaw stores skill playbooks in `~/.openclaw/workspace/skills/<name>/SKILL.md`. These contain the detailed workflow, persona, and format. For migration:

- **Simple jobs** (single-message check-ins, health prompts, reminders): embed the key instructions into the Hermes cron prompt directly (≤20 lines). The prompt IS the playbook for simple jobs — no separate skill file needed.

- **Complex jobs** (content planning, supplier research, synthesis reports): create a Hermes skill and reference it in the cron job via `--skills`:

```bash
hermes cron create "09 9 * * 4" \
  --name "thursday-content-akoma" \
  --skills "akoma-content-planner" \
  --prompt "Execute the akoma-content-planner skill. Generate a 7-day social media plan for Akoma Robotics based on recent project progress."
```

### 7. Job Categories from OpenClaw (with Hermes Routing)

**Health Checks (Telegram topics — daily):**

| OpenClaw Name | Schedule | Hermes Topic ID | Topic Name |
|---|---|---|---|
| `health-log-morning` | 08:01 daily | 2 | #health-log |
| `health-log-afternoon` | 13:01 daily | 2 | #health-log |
| `health-log-evening` | 19:02 daily | 2 | #health-log |
| `health-weekly-review-h` | 09:06 Sun | 2 | #health-log (internal weekly review) |
| `mum-health-morning` | 08:04 daily | 4 | #health-log-mum |
| `mum-health-afternoon` | 13:00 daily | 4 | #health-log-mum |
| `mum-health-evening` | 19:00 daily | 4 | #health-log-mum |
| `health-weekly-review-mum` | 09:06 Sun | 4 | #health-log-mum (internal weekly review) |

**Family Check-ins (WhatsApp — requires WhatsApp setup):**
- `checkin-mum` (10:18 Sun/Wed)
- `checkin-dad` (10:04 Sun/Thu)
- `ebony-goodnight` (22:04 daily)

**Business (WhatsApp — requires WhatsApp setup):**
- `sammy-morning-check` (07:02 Mon-Sat)
- `sammy-afternoon-check` (15:45 Mon-Sat)
- `john-field-check` (08:02 Mon-Fri)

**Associate Check-ins (WhatsApp — requires WhatsApp setup):**
- `kanzoni-tuesday-check` (07:07 Tue)
- `matthias-friday-check` (20:02 Fri)
- `kwasi-thursday-check` (08:25 Thu)
- `janet-friday-checkin` (20:32 Fri)
- `jnr-payment-reminder` (10:05 every 3 days)
- `Monthly-Tax-Submission-Audit` (10:47 4th)

**Content & Planning (Telegram):**

| OpenClaw Name | Schedule | Hermes Topic ID | Topic Name |
|---|---|---|---|
| `thursday-content-akoma` | 09:09 Thu | 26 | #content-calendar |
| `friday-content-2real` | 09:15 Fri | 26 | #content-calendar |
| `saturday-content-performance` | 09:11 Sat | 26 | #content-calendar |

**Business Intelligence (Telegram):**

| OpenClaw Name | Schedule | Hermes Topic ID | Topic Name |
|---|---|---|---|
| `ghana-supplier-outreach` | 09:16 Mon-Sat | 1 | #general |
| `ghana-supplier-analysis` | 10:10 Mon | 1 | #general |
| `ghana-steering-verification` | 11:11 Wed | 1 | #general |

**Briefing & Learning (Telegram):**

| OpenClaw Name | Schedule | Hermes Topic ID | Topic Name |
|---|---|---|---|
| `daily-system-briefing` | 06:36 daily | 10 | #briefing |
| `integrated-daily-synthesis` | 22:05 daily | 10 | #briefing |
| `weekly-learning-review` | 09:13 Mon | 10 | #briefing |
| `monthly-evolution` | 09:21 1st | 10 | #briefing |
| `quarterly-synthesis` | 10:37 Thu | 10 | #briefing |

**System & Maintenance (Telegram):**

| OpenClaw Name | Schedule | Hermes Topic ID | Topic Name |
|---|---|---|---|
| `cron-status-report` | 09:00 daily | 20 | #memory-review |
| `security-watchdog` | :04 every 6h | 20 | #memory-review |
| `daily-backup` | 23:03 daily | 20 | #memory-review |
| `nightly-consolidation` | 03:00 daily | 20 | #memory-review |
| `github-memory-backup` | 23:02 Sun | 20 | #memory-review |

**Jobs:**

| OpenClaw Name | Schedule | Hermes Topic ID | Topic Name |
|---|---|---|---|
| `job-applications-check` | 08:00 daily | 28 | #jobs |

## Pitfalls

- **Don't attempt WhatsApp delivery before the Hermes WhatsApp gateway is configured.** Hermes will log errors. Set those jobs up but don't enable them until the gateway is ready.
- **Telegram topic IDs must match the `channel_prompts` keys.** A message routed to thread `50` with no matching `channel_prompts["50"]` key will use the group-level fallback prompt.
- **OpenClaw skill files are Markdown** but may contain workflow-specific file paths, PowerShell/bash commands, and references to OpenClaw's internal APIs (`skill:*` calls). Edit these out when converting to Hermes cron prompts.
- **Schedule timezones.** OpenClaw cron exprs may be in a different timezone than Hermes. Hermes uses `config.timezone` (default UTC). Set `timezone: Europe/London` in config.yaml if needed.