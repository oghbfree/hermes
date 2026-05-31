# Cron Delivery to Telegram — Patterns & Pitfalls

## How Cron Delivery Works

Cron jobs deliver their output via the `deliver` field in the job config. The agent's final response text IS the delivery. There is NO separate send step.

**Correct pattern:** Put the user-facing content directly in your final response. The system auto-delivers it.

**Wrong pattern:** Trying to use `send_message` tool or `hermes message send` CLI — both fail in cron context.

## No `send_message` Tool in Cron

The `send_message` tool (part of the `messaging` toolset) is **not available in cron jobs**. The `messaging` toolset is only enabled for interactive platforms (cli, telegram, etc.), not for cron.

## No `hermes message send` CLI

There is no `hermes message send` subcommand. The CLI has no messaging subcommand at all. Attempting it fails with:
```
hermes: error: argument command: invalid choice: 'message'
```

## Delivery Targets

| Target | Format | Example |
|--------|--------|---------|
| Telegram topic | `telegram:chat_id:topic_id` | `telegram:-1003784520976:10` |
| Telegram chat | `telegram:chat_id` | `telegram:-1003784520976` |
| Origin (current chat) | `origin` or omit | — |
| All channels | `all` | — |

## Finding Chat/Topic IDs

From `gateway.log`:
```
grep "inbound message" ~/.hermes/logs/gateway.log | grep "2026-05-20" | head -5
```

The log shows `chat=-1003784520976` and topic IDs are in the session key: `agent:main:telegram:group:-1003784520976:3225` → topic 3225.

**Known topic IDs (as of May 2026):**

| Topic | ID | Purpose |
|-------|----|---------|
| general | 1 | Dad health check-ins |
| health-log | 2 | H's personal health |
| health-log-mum | 4 | Comfort's clinical care log |
| to-do-list | 8 | Brain dump processing |
| briefing | 10 | Daily briefings & synthesis reports |
| property | 12 | UK property management |
| farm | 14 | Farm operations |
| action-lab | 16 | Action lab |
| kids | 18 | Kids |
| memory-review | 20 | Memory review |
| content-calendar | 26 | Content calendar |
| jobs | 28 | Cron jobs & system health |
| agent-hermes | 424 | Direct coordination with Agent Hermes |
| akoma-robotics | 866 | Akoma Robotics operations |
| 2-real-enterprises | 928 | 2 Real Enterprises operations |

**Group:** `-1003784520976` (Hermes agent supergroup)

## Telegram Topic Threading

When delivering to a Telegram topic, the `deliver` field must include the `:topic_id` suffix. Without it, the message goes to the general chat (or fails with "Thread not found" if the group requires topics).

**Recurring error:** `Telegram] Thread 2 not found, retrying without message_thread_id` — this means a cron job is trying to deliver to topic 2 which doesn't exist. Check the job's `deliver` field.

## [SILENT] Suppression

If a cron job has nothing to report, respond with exactly `[SILENT]` (nothing else). This suppresses delivery. Never combine `[SILENT]` with content.

## Synthesis Report Delivery

For the integrated-daily-synthesis cron (22:05):
- **Primary output:** The agent's final response = the synthesis report
- **Delivery target:** Configured in the cron job's `deliver` field (typically `telegram:-1003784520976:10`)
- **File backup:** Also save to `memories/insights/INTEGRATED_INSIGHTS_YYYY-MM-DD.md`
- **Do NOT** attempt to send via `send_message` or CLI — just produce the report as your response

## Posting to a Specific Topic via Bot API (When `deliver` Is `origin`)

When a cron job's `deliver` field is set to `origin` (not a Telegram target) but you need to post to a specific Telegram topic, use the Bot API directly via `execute_code`:

```python
import os, json, urllib.request, urllib.error

# Read bot token
env_path = os.path.expanduser("~/.hermes/.env")
token = None
with open(env_path, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line.startswith("TELEGRAM_BOT_TOKEN="):
            token = line.split("=", 1)[1].strip()
            break

# Post to topic
chat_id = "-1003784520976"
message_thread_id = 28  # jobs topic

payload = json.dumps({
    "chat_id": chat_id,
    "message_thread_id": message_thread_id,
    "text": report_text
}, ensure_ascii=False).encode("utf-8")

url = f"https://api.telegram.org/bot{token}/sendMessage"
req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json; charset=utf-8"})

with urllib.request.urlopen(req, timeout=30) as resp:
    result = json.loads(resp.read().decode())
    if result.get("ok"):
        print(f"SUCCESS: msg_id={result['result']['message_id']}")
```

**⚠️ `parse_mode: "HTML"` pitfall:** Including `parse_mode: "HTML"` in the JSON body can cause HTTP 400 errors when combined with `message_thread_id` on some topics. If you get a 400, retry the same request WITHOUT `parse_mode` (send as plain text). Never drop `message_thread_id` — that's what routes to the correct topic.

**⚠️ Character limit:** Telegram messages have a 4096-character limit. For longer reports, either truncate or split into multiple messages (post sequentially with a short delay between them).

**⚠️ Rate limiting:** Don't fire multiple Bot API calls in rapid succession. If posting multiple messages, add a small delay (`time.sleep(1)`) between calls.
