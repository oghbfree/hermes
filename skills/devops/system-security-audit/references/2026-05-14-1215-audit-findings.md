# System Security Audit — 2026-05-14 12:15 UTC

## Score: 4 FAIL / 10 PASS — Security posture: DEGRADED

## FAIL Items

### CRITICAL
1. **Exposed Ollama private key** — `~/.ollama/id_ed25519` has permissions 644 (world-readable). Full Ed25519 private key in plaintext.
   - REMEDY: `chmod 600` or restrict ACLs to current user only.

### HIGH
2. **Overly permissive sensitive file permissions** — `.env`, `auth.json`, `config.yaml`, `whatsapp/session/creds.json` all at 644 (world-readable). `.env` contains OPENROUTER_API_KEY, TELEGRAM_BOT_TOKEN, FIRECRAWL_API.
   - REMEDY: `chmod 600` on all sensitive files.

3. **Credentials in session dump files** — 6 `request_dump_*.json` files in `~/.hermes/sessions/` contain api_key/token/secret references in plaintext.
   - REMEDY: Review and purge old session dumps.

### MEDIUM
4. **Credential references in log files** — `agent.log`, `errors.log`, `gateway.log`, `maintenance-*.log` contain secret/token references.
   - REMEDY: Rotate credentials appearing in logs.

## PASS Items
- Channel Integrity: Telegram + WhatsApp both connected
- Gateway: Running (PID 15880), no errors
- Windows Firewall: ON for all profiles
- No exposed secrets in process list
- Hermes gateway + Ollama bound to localhost only
- security.redact_secrets: true (enabled)
- SMB/RPC listening — expected for Windows
- All 13 cron jobs enabled and reporting ok

## Platform States (for delta tracking)
- Telegram: connected (updated 2026-05-13T20:52:52Z)
- WhatsApp: connected (updated 2026-05-13T20:52:52Z)

## Session Count
- Total session files: ~90 (session_*.json)
- Request dump files: 6

## Notes
- This audit ran as a cron job; final response delivered automatically to Telegram topic 20
- Previous audit (06:04 UTC same day) had same 4 FAIL items — all persist unresolved
- Age: All 4 FAIL items now at 2+ consecutive audits (REPEAT)
