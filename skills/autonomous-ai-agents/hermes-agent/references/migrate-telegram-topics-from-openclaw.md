# Migrating Telegram Topics from OpenClaw to Hermes

When migrating from OpenClaw, its Telegram topic configuration — group ID, topic-to-prompt mappings, per-topic system prompts — lives outside the OpenClaw profile files. The `hermes claw migrate` command handles USER/SOUL/MEMORY/etc. but doesn't transfer Telegram topic prompts.

## What to Extract

OpenClaw stores Telegram config in two places:

1. **`~/.openclaw/openclaw.json`** — group ID, topic enablement, bot token
2. **`~/.openclaw/workspace/telegram-system-prompts.json`** — per-topic system prompts

## Step-by-Step

### 1. Extract the group ID and topic structure

```python
import json
with open("~/.openclaw/openclaw.json") as f:
    config = json.load(f)

telegram = config["channels"]["telegram"]
group_id = list(telegram["groups"].keys())[0]      # e.g. "-1003620024352"
topics = telegram["groups"][group_id]["topics"]     # {"1": {"enabled": true}, ...}
bot_token = telegram["botToken"]                     # for reference
```

### 2. Extract per-topic system prompts

```python
with open("~/.openclaw/workspace/telegram-system-prompts.json") as f:
    prompts_data = json.load(f)

topics_prompts = prompts_data["groups"]["main_group"]["topics"]
group_prompt = prompts_data["groups"]["main_group"]["systemPrompt"]
```

The prompts JSON has this structure:
```
{"groups": {"main_group": {
  "id": "-1003620024352",
  "systemPrompt": "...",       ← group-level prompt (used when no topic match)
  "topics": {
    "50": {
      "name": "health-clinical",
      "systemPrompt": "..."    ← topic-specific prompt
    }, ...
  }
}}}
```

### 3. Build Hermes channel_prompts YAML

Use YAML **literal block scalars** (`|`) for multiline prompts — much cleaner than quoted strings with `\n`:

```yaml
telegram:
  reactions: false
  allowed_chats: "-1003620024352"
  channel_prompts:
    # Group-level fallback prompt (key = group chat ID)
    "-1003620024352": |
      You are the master operations AI...

    # Per-topic prompts (key = thread/topic ID string)
    "1": |
      # Topic 1 - health-log
      You manage daily health logging...
    "50": |
      # Topic 50 - health-clinical
      Daily clinical health intake...
```

Keys in `channel_prompts` are:
- **thread_id string** (e.g. `"50"` or `"2"`) → applied when a message arrives in that forum topic
- **group chat ID** (e.g. `"-1003620024352"` or `"-1003784520976"`) → applied as fallback when a group message has no topic thread, or when a topic has no matching key

### Real-World Topic ID Mapping (from actual migration)

OpenClaw topic IDs often differ from the Hermes group's because Telegram auto-assigns them when topics are created. Map them by name:

| Topic Name | OpenClaw ID | Hermes Group ID |
|---|---|---|
| #general | 2 | 1 |
| #health-log | 50 | 2 |
| #health-log-mum | 51 | 4 |
| #container | — (new) | 6 |
| #to-do-list | 1272 | 8 |
| #briefing | 140 | 10 |
| #property | 357 | 12 |
| #farm/construction | 358 | 14 |
| #action-lab | 139 | 16 |
| #kids | — | 18 |
| #memory-review | 29 | 20 |
| #content-calendar | 364 | 26 |
| #jobs | 359 | 28 |
| **Group** | -1003620024352 | -1003784520976 |

**Get actual IDs:** Use @getidsbot on Telegram, or check Hermes gateway logs when a topic message arrives. Topic IDs are assigned in creation order (first topic = 1, second = 2, etc.) but Telegram may skip numbers if topics are deleted/recreated.

### Cluster Routing Pattern

Some OpenClaw topics can be merged into broader Hermes topics:

| Merged From (OpenClaw) | Into Hermes Topic | Reason |
|---|---|---|
| cron-status (28) + code-execution (47) + security logs | #memory-review (20) | All system health/maintenance |
| learning-insights (139) + daily-briefing (140) | #briefing (10) | Briefing + strategy bundled |
| construction (358) + farm operations | #farm (14) | Site updates combined |
| health-weekly (141) | internal cron in respective health topics | Weekly review per health channel |

Hermes resolves prompts via `resolve_channel_prompt()` in `gateway/platforms/base.py`: exact match on channel (thread) ID first, then fallback to parent group ID.

### 4. Bot token considerations

OpenClaw and Hermes likely use **different bot tokens**. You have two options:

- **A)** Add Hermes's bot as an admin to the Telegram group (works alongside OpenClaw)
- **B)** Copy OpenClaw's bot token to Hermes (disables OpenClaw Telegram — only one polling client per token)

Set the token in `~/.hermes/.env`:
```
TELEGRAM_BOT_TOKEN=835929...your_token
```

### 5. Restart gateway

```bash
hermes gateway restart
```

## Verification Checklist

Use these checks to confirm the migration is already in place (useful when the bot was recently added and you need to determine if config was done):

1. **Check `allowed_chats`** — `grep allowed_chats ~/.hermes/config.yaml` should show the new group ID.
2. **Check `channel_prompts`** — `grep -c 'channel_prompts' ~/.hermes/config.yaml` should return 1, and the block below should have topic keys matching the Hermes group's topic IDs.
3. **Verify bot token** — `grep TELEGRAM_BOT_TOKEN ~/.hermes/.env` should show the correct token.
4. **Check gateway is running** — `hermes gateway status` shows a PID.
5. **Topic count match** — Count the topic keys in `channel_prompts` (excluding the group-level key). It should match the number of topics in the Hermes group.

If all five pass, the migration is complete. Only a gateway restart (`hermes gateway restart`) is needed if the config was recently patched while the gateway was already running.

## Pitfalls

- **Quoted multi-line prompts break YAML.** Always use `|` block scalars for prompts with embedded newlines. Never inline them as `"long prompt\nwith\nbreaks"`.
- **Channel prompt comments are fine but not standard YAML.** If a prompt line starts with `#`, YAML treats it as a comment. The prompts above avoid that by putting comments on their own `# Topic N - name` line, which is outside the block scalar.
- **Gateway restart is required.** `channel_prompts` is read at gateway startup, not reloaded per-message.
- **OpenClaw runs as Node.js** — its process must be stopped or its Telegram polling disabled before Hermes can use the same bot token.