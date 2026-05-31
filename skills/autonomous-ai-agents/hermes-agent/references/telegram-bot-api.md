# Telegram Bot API — Direct Send from Cron/CLI Context

## Problem

The `send_message` tool (messaging toolset) fails in cron jobs and CLI-only sessions with:

```
{"error": "Platform 'telegram' is not configured. Set up credentials in ~/.hermes/config.yaml or environment variables."}
```

This happens even when the gateway is running and Telegram is connected. The `send_message` tool routes through the gateway's internal channel directory, which is only populated for gateway-managed sessions — not for cron or standalone CLI runs.

## Solution: Direct Bot API via Python urllib

Read the bot token from `~/.hermes/.env` and call the Telegram Bot API directly.

### Pattern

```python
import os, json, urllib.request

# 1. Read token from .env
env_path = os.path.join(os.path.expanduser("~"), ".hermes", ".env")
token = None
with open(env_path, "r", encoding="utf-8") as f:
    for line in f:
        if line.strip().startswith("TELEGRAM_BOT_TOKEN="):
            token = line.strip().split("=", 1)[1].strip()
            break

# 2. Build payload — use ensure_ascii=False for emoji, encode as UTF-8
payload = json.dumps({
    "chat_id": "<chat_id>",          # e.g. "-1003784520976"
    "message_thread_id": <topic_id>,  # integer, omit for no topic
    "text": "<message text>"
}, ensure_ascii=False).encode("utf-8")

# 3. Send
url = f"https://api.telegram.org/bot{token}/sendMessage"
req = urllib.request.Request(
    url,
    data=payload,
    headers={"Content-Type": "application/json; charset=utf-8"},
    method="POST"
)
with urllib.request.urlopen(req, timeout=15) as resp:
    result = json.loads(resp.read().decode("utf-8"))
    # result["ok"] == True on success
    # result["result"]["message_id"] has the sent message ID
```

### Key Details

- **`message_thread_id`** is the Telegram topic ID (integer). Omit for channels without topics.
- **`chat_id`** for supergroups is negative, e.g. `-1003784520976`.
- **Always use `ensure_ascii=False`** in `json.dumps()` — emoji and non-ASCII chars will corrupt the request otherwise (Telegram returns HTTP 400 "strings must be encoded in UTF-8").
- **Always `.encode("utf-8")`** on the payload — do not pass a string to `data=`.
- The token is in `~/.hermes/.env` as `TELEGRAM_BOT_TOKEN=...` — never hardcode it.

### Finding chat_id and topic_id

From `~/.hermes/config.yaml`, the `telegram.channel_prompts` dict maps topic IDs to prompt strings. The Telegram channel ID is under `telegram.allowed_chats` or can be found in the config's top-level keys. Example:

```yaml
telegram:
  allowed_chats: -1003784520976, -1003620024352
  channel_prompts:
    '2': "# Topic 2 - health-log\n..."
    '10': "# Topic 10 - briefing\n..."
```

Here `-1003784520976` is the supergroup chat ID, and `'2'` is the topic ID for health-log.

### message_thread_id Pitfall: Private Chats vs Supergroup Topics

The cron delivery target format `telegram:<chat_id>:<thread_id>` includes a third segment (e.g. `telegram:123286468:2`). Do **not** blindly pass this as `message_thread_id` to the Bot API.

- `message_thread_id` is **only valid for supergroup topics**. Telegram rejects it with HTTP 400 on private chats.
- If the target is a private chat (`chat.id > 0` in Telegram's scheme), omit `message_thread_id` entirely.
- If the target is a group/supergroup (`chat.id < 0`), `message_thread_id` is valid — but only if that topic actually exists.
- **Safe pattern**: try sending *without* `message_thread_id` first. Telegram delivers to the main chat. If the recipient uses topics, they may have a default topic or the message lands in the general topic.

When debugging a 400 error, always inspect the error body first:

```python
except urllib.error.HTTPError as e:
    body = e.read().decode("utf-8")
    print("HTTP Error:", e.code, body)
```

### When to Use This

- Cron jobs that need to send to Telegram topics
- CLI-only sessions where `send_message` fails
- Any context where the gateway's channel directory is not available

### When NOT to Use This

- Interactive gateway sessions (use `send_message` tool — it handles media, reactions, etc.)
- When you need to send media files (use `send_message` with `MEDIA:` prefix in gateway context)
