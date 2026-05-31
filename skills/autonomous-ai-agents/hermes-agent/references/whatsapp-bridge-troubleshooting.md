# WhatsApp Bridge Architecture & Troubleshooting

## How WhatsApp Integration Works

The Hermes WhatsApp adapter uses a **bridge pattern**:

1. **Gateway process** (Python, PID from `hermes gateway status`) manages the lifecycle
2. **Node.js bridge process** runs the actual WhatsApp Web client (Baileys library)
3. **Bridge script** at `C:\Users\<user>\AppData\Local\hermes\hermes-agent\scripts\whatsapp-bridge\bridge.js` on Windows installs
4. **Session data** stored in the bridge's `sessions/` or `store/` subdirectory (creds.json, pre-keys, sender-keys, etc.)

## Configuration

In `~/.hermes/.env`:
- `WHATSAPP_MODE=self-chat` — gateway manages the bridge directly via Baileys
- `WHATSAPP_ENABLED=true` — enable WhatsApp integration
- `WHATSAPP_ALLOWED_USERS=...` — comma-separated allowed sender IDs

In `~/.hermes/config.yaml`:
- `whatsapp.allow_from` — list of allowed sender phone numbers (E.164 format with `+`)
- `whatsapp.dm_policy` — `open` | `allowlist` | `disabled`
- `whatsapp.group_policy` — `open` | `allowlist` | `disabled`

## Diagnosing Bridge Issues

### Check gateway logs for WhatsApp errors
```bash
grep -i "whatsapp\|bridge" ~/.hermes/logs/gateway.log | tail -30
```

Key log lines indicating successful startup:
```
INFO gateway.platforms.whatsapp: [Whatsapp] Bridge found at ...\bridge.js
INFO gateway.run: ✓ whatsapp connected
```

Key log lines indicating failure:
```
INFO gateway.platforms.whatsapp: [whatsapp] Killed stale bridge PID ... from pidfile
ERROR gateway.run: ✗ whatsapp error: whatsapp connect timed out after 30s
INFO gateway.run: Starting reconnection watcher for N failed platform(s): ..., whatsapp
```

### Check if bridge process is running
```bash
# On Windows, check the gateway log for bridge PID
grep "bridge" ~/.hermes/logs/gateway.log | grep "PID\|pidfile" | tail -5
```

## Failure Modes

### ⚠️ CONNECT TIMEOUT (30s) — Session Expired / Needs QR Re-auth

**This is the most common failure mode after a period of WhatsApp outage.**

Symptoms in `~/.hermes/logs/gateway.log`:
```
ERROR gateway.run: ✗ whatsapp error: whatsapp connect timed out after 30s
INFO gateway.run: Starting reconnection watcher for N failed platform(s): discord, whatsapp
```

The gateway starts the bridge process, the bridge attempts to connect to WhatsApp's servers, but the existing session credentials are stale/expired, so the connection never completes within the 30-second timeout window.

**Recovery procedure:**

1. **Stop the gateway:**
   ```powershell
   hermes gateway stop
   ```

2. **Clear the stale WhatsApp session data:**
   The session is at `~/.hermes/whatsapp/session/` (NOT in the bridge scripts dir).
   Backup first, then clear. If the session directory has thousands of files
   (Baileys can accumulate 8000+), use Python to avoid shell timeouts:
   ```python
   import os, shutil
   session = os.path.expanduser("~/.hermes/whatsapp/session")
   backup = os.path.expanduser("~/.hermes/whatsapp/session-backup-expired")
   if not os.path.exists(backup):
       shutil.copytree(session, backup)
   shutil.rmtree(session)
   os.makedirs(session)
   ```
   The critical missing file indicating "not paired" is `creds.json`.

3. **Restart the gateway:**
   ```powershell
   hermes gateway start
   ```

4. **Pair via `hermes whatsapp`** — the log will show:
   ```
   WARNING [WhatsApp] WhatsApp is enabled but not paired (no creds.json ...)
   Run `hermes whatsapp` to pair
   ```
   Run `hermes whatsapp` manually in a terminal to get the QR code, or watch
   the gateway log for the QR. Scan with WhatsApp (Settings → Linked Devices).

5. **Verify connection:**
   ```powershell
   Get-Content "$env:USERPROFILE\\.hermes\\logs\\gateway.log" -Tail 20
   # Look for: INFO gateway.run: ✓ whatsapp connected
   ```

**Note:** `hermes gateway restart` alone (without clearing session) will NOT fix this — the gateway just retries the same expired session.

**Note for MSYS/bash terminal users:** Do NOT try to `rm -rf` the session
directory from bash — 8000+ files will hang the shell. Use the Python
snippet above via `execute_code`.

### ⚠️ GAVE UP AFTER N RECONNECT ATTEMPTS — Permanent Failure

When the gateway exhausts its retry budget:
```
WARNING gateway.run: Giving up reconnecting whatsapp after N attempts
```

See the [Escalation section](#escalation) below.

### Common failure modes table

| Symptom | Cause | Fix |
|---------|-------|-----|
| `connect timed out after 30s` | Session expired / QR re-auth needed | Stop gateway → clear sessions → restart → scan QR |
| `bridge.pid` exists but no Node process | Bridge crashed | `hermes gateway restart` |
| Port 3000 not listening | Bridge not started | Restart gateway; check `WHATSAPP_ENABLED=true` in `.env` |
| `send_message` tool unavailable in cron | `messaging` toolset not in cron | Use Telegram delivery instead; see cron messaging limitations in SKILL.md |
| WhatsApp session expired | QR code re-scan needed | Clear session dir, restart, scan QR |
| `self-chat` mode not working | `WHATSAPP_MODE` not set | Add `WHATSAPP_MODE=self-chat` to `.env` |
| `✗ whatsapp error` after gateway restart | Stale session data | Clear session folder as described above |

## ⚠️ ESCALATION: "Gave Up After N Reconnect Attempts"

**This is a CRITICAL failure mode.** When the gateway has tried to reconnect WhatsApp repeatedly and exhausts its retry budget, it logs:

```
WARNING gateway.run: Giving up reconnecting whatsapp after N attempts
```

At this point:
- `gateway_state.json` shows `"whatsapp": {"state": "retrying", "error_message": "failed to reconnect"}`
- The bridge process (bridge.js) may crash immediately on startup with exit code 1
- **All WhatsApp communication is completely down** — no incoming or outgoing messages
- The platform gets paused; run `/platform resume whatsapp` or `hermes gateway restart` to retry

### How to diagnose
```bash
# Check the gateway log for the "giving up" message
grep -i "giving up\|gave up" ~/.hermes/logs/gateway-stdio.log | tail -5

# Check bridge crash details
cat ~/.hermes/whatsapp/bridge.log

# Check gateway_state.json
cat ~/.hermes/gateway_state.json
```

### Likely causes
1. **Corrupted session files** — The `creds.json` or session files may be corrupted
2. **WhatsApp Web session expired** — WhatsApp may have invalidated the session server-side
3. **Bridge.js crash loop** — The bridge script itself has a fatal error (check `bridge.log`)
4. **Network issues** — The host cannot reach WhatsApp's servers

### Recovery steps
1. Check `~/.hermes/whatsapp/bridge.log` for the actual crash reason
2. If session corruption: try renaming the session folder to `.bak` and re-linking
3. If bridge.js error: check if the bridge script path is correct in the gateway config
4. As a last resort: follow the full QR re-auth procedure in the [Connect Timeout](#-connect-timeout-30s--session-expired--needs-qr-re-auth) section above

### Security audit implications
- When WhatsApp is permanently down, flag as **CRITICAL** (not just WARN)
- The `gateway_state.json` will show `"retrying"` with `"failed to reconnect"` — this is the permanent failure state
- Check `gateway-stdio.log` for the "giving up" message to confirm it's not just a transient issue

## Session Data

The WhatsApp session directory contains:
- `creds.json` — WhatsApp authentication credentials
- `bridge.pid` — PID of the bridge process (stale if bridge crashed)
- `app-state-sync-*.json` — WhatsApp app state
- `pre-key-*.json` — Signal protocol pre-keys
- `sender-key-*.json` — Group sender keys
- `session-*.json` — Session data per contact

**Do not delete the session folder unless you want to re-scan the QR code.** Deleting it forces full re-authentication.

## Cron Job Implications

Cron jobs **cannot** use the `send_message` tool to send WhatsApp messages. The `messaging` toolset is not available in cron context. Workarounds:
1. Set cron delivery to Telegram instead of WhatsApp
2. Have the cron job post a status report to a Telegram topic
3. Enable `messaging` toolset in the cron job's `enabled_toolsets` (may not work reliably)
