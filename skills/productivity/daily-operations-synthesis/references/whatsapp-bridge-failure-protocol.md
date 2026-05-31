# WhatsApp Bridge Failure Handling Protocol

**Applies to:** All WhatsApp-dependent cron jobs (ebony-goodnight, mum-checkin, dad-checkin, sammy-check, john-check, kanzoni-check, janet-check, jnr-payment-reminder, and any future WhatsApp messaging jobs).

## Architecture (Updated 2026-05-22)

WhatsApp messaging now runs through the **OpenClaw gateway** (`@openclaw/whatsapp` plugin v2026.5.4, using Baileys 7.0.0-rc.9), NOT a standalone bridge.js process.

| Component | Old (pre-2026-05) | Current |
|---|---|---|
| Process | `node bridge.js --port 3000` | OpenClaw gateway (`openclaw gateway --port 18789`) |
| Port | 3000 | 18789 |
| Plugin | None (standalone script) | `@openclaw/whatsapp` npm package |
| Session dir | `~/.hermes/whatsapp/session/` | `~/.openclaw/credentials/whatsapp/` |
| Bridge log | `~/.hermes/whatsapp/bridge.log` | `~/.openclaw/logs/` |
| Config | `~/.hermes/whatsapp/` | `~/.openclaw/openclaw.json` → `channels.whatsapp` |
| Start command | `node bridge.js` | `gateway.cmd` or Windows Task "OpenClaw Gateway" |

**Key implication:** The old `curl http://127.0.0.1:3000/health` check is obsolete. The new gateway does not expose a `/health` endpoint on port 3000. Port 3000 may still appear in old logs but is no longer the active transport.

## Gateway Health Check (Always Do This First)

Before attempting any WhatsApp send, check if the OpenClaw gateway is running:

```bash
# Check if gateway process is running
ps aux | grep -i openclaw | grep -v grep
# OR check if port 18789 is listening
netstat -an | grep 18789 | grep LISTENING
```

**Possible outcomes:**
- **Process running + port 18789 listening** → Gateway is up. WhatsApp *should* be connected (the plugin auto-connects on startup).
- **No process / port not listening** → Gateway is down. Skip to fallback below.

**Quick gateway log check:**
```bash
tail -10 ~/.openclaw/logs/gateway-restart.log
```

Look for:
- `✅ WhatsApp connected!` → WhatsApp channel is active
- `❌ Logged out` → Session expired, needs QR scan via OpenClaw control UI
- Recent restart timestamps → Gateway was recently restarted

**Check WhatsApp auth state:**
```bash
ls -la ~/.openclaw/credentials/whatsapp/
# Should show session directories like `default/` or phone-number dirs
```

## Critical: Gateway Cannot Be Started from Cron

The OpenClaw gateway **cannot be started from a cron bash (MSYS) environment.** It exits immediately with "stdin is not a tty" because it requires a proper terminal or Windows service context.

**To restart the gateway, H must:**
1. Run `C:\Users\User\.openclaw\gateway.cmd` directly from Windows (double-click or cmd.exe), OR
2. Start the "OpenClaw Gateway" Windows scheduled task, OR
3. Run from a proper terminal: `node "C:\Users\User\AppData\Roaming\npm\node_modules\openclaw\dist\index.js" gateway --port 18789`

**Do NOT attempt to start the gateway from a cron job** — it will fail silently.

## When Gateway Is DOWN — Fallback Protocol

When the gateway is unreachable, follow this protocol for **all WhatsApp-dependent jobs**:

### 1. Draft the Message Anyway
Compose the full message as if it will be sent. This ensures the message is ready when the gateway comes back.

### 2. Log the Attempt
Write a log entry to the relevant checkin file. **During extended outages (5+ consecutive identical failures), don't append a full new block per run — just update the existing entry's date stamp and increment the failure counter.** This prevents the checkin log from growing into a wall of identical entries. Example of the compact pattern:

```
## 2026-05-30 (Saturday)
- **Status**: FAILED — WhatsApp bridge offline (Day 29)
- **Consecutive failures**: [8] — last failure 2026-05-30 07:02 UTC+1
- **Root cause**: No OpenClaw process, port 18789 not listening

[Prior entries collapsed — 7 previous consecutive failures (May 19-29), same root cause]
```

**Restart full entry logging** when the failure mode changes (e.g., gateway comes back but session expires, or gateway process running but WhatsApp disconnected). Each *distinct* failure mode gets its own block.

### 3. Report via Telegram
Since the cron delivery target is Telegram (not WhatsApp), the agent's response will be delivered to Telegram. Use this format:

```
[JOB NAME] — YYYY-MM-DD HH:MM
Status: NOT SENT (OpenClaw gateway down)

Drafted message for [recipient]:
"[full message text]"

Gateway status: Port 18789 not listening, no openclaw process found
Action needed: H must restart gateway.cmd from Windows
```

### 4. Do NOT Mark as Successful
Never report a WhatsApp send as successful unless the gateway confirmed delivery. If the gateway is down, the message was NOT sent — be explicit about this.

## When Gateway Is UP — Send Protocol

When the gateway is running, WhatsApp messages are sent through the OpenClaw gateway's channel system. The exact send mechanism depends on how the gateway exposes its API:

**Option A: Via gateway API (if available)**
```bash
curl -s --max-time 10 -X POST http://127.0.0.1:18789/api/send \
  -H "Content-Type: application/json" \
  -d '{"channel": "whatsapp", "to": "<phone>@s.whatsapp.net", "message": "<text>"}'
```

**Option B: Via gateway hooks (if configured)**
The OpenClaw gateway may expose webhook endpoints for outbound messaging. Check `~/.openclaw/openclaw.json` for hook configuration.

**Option C: Via OpenClaw CLI**
```bash
openclaw send --channel whatsapp --to <phone> --message "<text>"
```

**If the send endpoint is unknown or `send_message` tool is unavailable:** The `send_message` tool does NOT exist as a native tool in cron environments. The gateway may also not expose a direct send API to cron jobs. In this case:
1. Draft the message
2. Log the attempt to the relevant care log file (e.g., `C:\Users\User\CARE_LOG_DAD_YYYY-MM.md`) — NOT just the cron output dir
3. Report via Telegram with the drafted message text
4. Note in the report that the correct send mechanism needs to be determined

**Recipient phone formats:**
- Ebony: Check `~/.openclaw/openclaw.json` → `channels.whatsapp.accounts` for the configured number
- Mum (Comfort): +233****2252
- Dad (Robert): +447****4695 (UK number — full number partially redacted in contacts.json; use care log or FAMILY_INSIGHTS_DAD.md for complete number)
- Others: Check `~/.hermes/contacts.json` or `~/.hermes/CONTACTS.md`

**Phone number redaction caveat:** Some contacts in `contacts.json` have redacted numbers (showing `+447****4695` instead of full digits). If the full number is needed for WhatsApp sending, check the care log files (`CARE_LOG_*_YYYY-MM.md`), `FAMILY_INSIGHTS_DAD.md`, or `CONTACTS.md` for the unredacted version. The redacted form is sufficient for logging and identification but not for actual API calls.

## Known Instability Patterns

| Pattern | Meaning | Action |
|---------|---------|--------|
| `Logged out` in logs | Session expired | H must scan QR code via OpenClaw UI |
| `Connection closed (reason: 428)` | Rate limit / temp ban | Wait for auto-reconnect |
| Gateway process exits immediately | stdin not a tty (cron env) | Start from Windows, not cron |
| Port 18789 not listening | Gateway crashed or not started | Restart gateway.cmd from Windows |
| Port 3000 references in old logs | Legacy bridge, no longer active | Ignore — new gateway uses 18789 |
| `allowlist_mismatch` | Sender not in allowlist | Check `openclaw.json` → `channels.whatsapp.allowFrom` |

## Extended Outage Pattern

The WhatsApp gateway has historically gone down for **weeks at a time**. During extended outages:
- Continue drafting messages and logging them daily
- Report the outage in the daily synthesis
- Do NOT stop trying the health check — the gateway may come back at any time
- Flag the outage as a KEY ISSUE in synthesis reports until resolved
- The gateway log at `~/.openclaw/logs/gateway-restart.log` tracks restart attempts

## Cron Jobs Affected by WhatsApp Outage

| Job ID | Name | Recipient | Priority |
|--------|------|-----------|----------|
| 43a5af4a446d | ebony-goodnight | Ebony (wife) | Personal |
| (various) | mum-checkin | Comfort (mum) | Health |
| (various) | dad-checkin | Robert (dad) | Health |
| (various) | sammy-check | Sammy | Business |
| (various) | john-check | John | Business |
| (various) | kanzoni-check | Kanzoni | Business |
| (various) | janet-check | Janet | Business |
| (various) | jnr-payment-reminder | Jnr | Business |

## Related Skills

- `supplier-outreach-tracking` — has bridge health check patterns (note: still references old port 3000, needs updating)
- `daily-operations-synthesis` — reports WhatsApp status in daily briefings
- `elder-care-operations` — health check-in templates for mum/dad
