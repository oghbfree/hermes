# Cron Delivery Patterns

## How Cron Job Delivery Works

When a Hermes cron job is configured with `--deliver telegram --deliver-chat-id <id>`, the agent's **final response text** is automatically delivered to that Telegram chat or topic. No explicit `send_message` tool call is needed.

### Key Principle

**The cron system treats the agent's final reply as the delivery payload.** The job's prompt defines WHAT to say; the cron scheduler handles WHERE to send it.

### Example: Health Check-In Cron

A cron job prompt like:
```
Post the evening care check-in to the health-log-mum Telegram topic (id 4).
Ask about dinner, vitals, mobility, medication compliance.
Warm caring tone. Format as bullet reply template.
```

The agent simply composes the check-in message as its response. The cron system routes it to topic 4 automatically.

### What NOT to Do

- **Don't** search for a `send_message` CLI tool — it doesn't exist as a standalone command
- **Don't** try `hermes chat -q` to send messages — that starts a new session, it doesn't deliver to a topic
- **Don't** over-explore gateway CLI commands looking for a send mechanism
- **Don't** use `terminal` to try to send via curl or bot API directly — the gateway already handles this

### What TO Do

1. Read the job prompt carefully
2. Compose the full message as your response text
3. The cron system delivers it automatically

### Multi-Platform Delivery

The same pattern works for all delivery targets:
- `--deliver telegram --deliver-chat-id <id>` → Telegram topic/chat
- `--deliver discord --deliver-chat-id <id>` → Discord channel
- `--deliver slack --deliver-chat-id <id>` → Slack channel
- `--deliver whatsapp --deliver-chat-id <id>` → WhatsApp

### Cron Job Creation Reference

```bash
# Create a job that delivers to a Telegram topic
hermes cron create "0 19 * * *" \
  --prompt "Post the evening care check-in..." \
  --deliver telegram \
  --deliver-chat-id "4" \
  --skills "hermes-agent"
```

### CRON_CONFIG → SKILL.md Architecture

For complex recurring jobs, use the two-layer pattern:
- **Cron prompt** (≤20 lines): Schedule + delivery target + which skill to invoke
- **SKILL.md**: Full execution playbook with templates, edge cases, formatting rules

For simple single-message jobs (like health check-ins), the prompt can contain the template directly since the "playbook" is just "compose this message."
