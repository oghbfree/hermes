# Kanban Dashboard / API Debugging

## Architecture Reminder

When `kanban.dispatch_in_gateway: true` (the default for most setups), Kanban runs **embedded inside the Hermes gateway process**. There is no standalone Kanban HTTP server.

- Kanban DB: `~/.hermes/kanban.db`
- Kanban workspaces: `~/.hermes/kanban/workspaces/`
- Gateway logs: `~/.hermes/logs/gateway.log`
- Config section: `kanban:` and `kanban_decomposer:` in `~/.hermes/config.yaml`

The dashboard UI is served by the gateway itself and talks to Kanban APIs over the same connection.

---

## Error: "Unexpected token '<', \"<!doctype \"... is not valid JSON"

This error means the dashboard's API request received an HTML page instead of JSON. Common causes:

### Cause 1: No HTTP port listening
The gateway process may be running but not exposing its web interface.

```bash
# Check gateway process is running
ps aux | grep hermes | grep -v grep   # POSIX
tasklist | grep hermes                 # Windows

# Check if ANY HTTP port is listening on localhost
netstat -ano | grep LISTENING | grep -E ":(3277[0-9]|3000|5000|8000|18789) "  # Windows
ss -tlnp | grep -E ":(3277[0-9]|3000|5000|8000) "                                # Linux

# Try the gateway directly
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:<port>/
```

If no HTTP port is listening, the gateway may need a restart:
```bash
hermes gateway restart
```

### Cause 2: Wrong URL / port
The dashboard may be configured to hit a port that's no longer active. Check what URL the dashboard is configured to use and verify it matches what the gateway is serving.

### Cause 3: Auth/redirect serving HTML
If the endpoint is reachable but returns a login page or redirect HTML, the session cookie/auth may have expired.

### Cause 4: Gateway just restarted
The dispatcher embedded in the gateway needs time to initialize after restart. Wait ~60 seconds after gateway restart before expecting the dashboard to work.

---

## Diagnostic Sequence

1. **Verify gateway process is alive**: `ps aux | grep hermes` or `tasklist | grep hermes`
2. **Check gateway logs** for kanban dispatcher status: `grep -i kanban ~/.hermes/logs/gateway.log | tail -10`
3. **Verify DB exists and is non-empty**: `ls -la ~/.hermes/kanban.db`
4. **Check kanban worker logs**: `ls -la ~/.hermes/kanban/logs/` (worker execution logs)
5. **Check for kanban dispatcher crashes**: Look for `crashed=` in gateway log kanban lines — non-zero means workers are crashing
6. **Check kanban stats**: `hermes kanban stats`
7. **Check board list**: `hermes kanban boards list`

## Common Recovery

If the dispatcher shows `crashed > 0` repeatedly in gateway logs:
1. Check the specific worker log in `~/.hermes/kanban/logs/` for the failing task
2. Check if it's a model/provider issue (rate limits, auth failures)
3. `hermes gateway restart` to reset dispatcher state
4. `hermes kanban reclaim <task_id>` to reset stuck running tasks

If `spawned > 0` and `crashed == 0` but the dashboard still shows HTML:
- The issue is likely on the HTTP serving side, not the Kanban dispatcher
- Check if the dashboard `public_url` in config.yaml is set correctly
- Try `hermes gateway restart`
