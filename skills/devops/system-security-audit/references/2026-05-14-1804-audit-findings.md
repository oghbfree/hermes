# System Security Audit — 2026-05-14 18:04 UTC

## Score: 4 FAIL / 11 PASS — Security posture: DEGRADED

## FAIL Items

### CRITICAL
1. **Exposed Google OAuth Client Secret in client_secret.json** (NEW)
   - Files: `~/.openclaw/workspace/client_secret.json` and `~/.openclaw/credentials/oauth-client.json`
   - Both contain full Google OAuth client_secret in plaintext
   - Permissions: 644 (world-readable)
   - REMEDY: Rotate the secret in Google Cloud Console; restrict files to 600; remove from workspace path

### HIGH
2. **.env Backup Files Contain Full Unredacted Secrets** (NEW)
   - Files: `~/.openclaw/.env.backup` and `~/.openclaw/.env.backup.20260401-150621`
   - Contain full API keys: BRAVE_SEARCH_API_KEY, GOOGLE_API_KEY, WHISPER_API_KEY, SAG_API_KEY, OPENCLAW_HOOKS_TOKEN
   - The active `.env` properly redacts values, but backups do not
   - REMEDY: Delete backups or move to encrypted storage; add `.env*` to `.gitignore`

3. **Ollama Private Key World-Readable** (REPEAT — 3rd consecutive audit)
   - File: `~/.ollama/id_ed25519` — permissions 644
   - Private key should be 600
   - REMEDY: `chmod 600 ~/.ollama/id_ed25519` or restrict ACLs to current user only

### MEDIUM
4. **Desktop .env Contains Full Unredacted Secrets** (NEW)
   - File: `~/Desktop/.env` — contains full API keys (GROQ, OPENROUTER, BRAVE, GOOGLE, WHISPER, SAG, OPENCLAW_HOOKS_TOKEN)
   - Desktop is high-exposure (cloud sync, file explorer visibility, search indexing)
   - REMEDY: Move secrets to `~/.hermes/.env` only; delete `~/Desktop/.env`

## PASS Items
- `.hermes/.env` — properly redacted values
- `.hermes/auth.json` — redacted token
- `.hermes/config.yaml` — no embedded secrets; security.redact_secrets=true
- Telegram channel directory — 15 topics configured, all under group -1003784520976
- Gateway state — Telegram and WhatsApp both connected
- WhatsApp credentials — creds.json present, app-state keys intact
- SSH directory — only known_hosts (no private keys stored there)
- `gogcli/.env.example` — placeholder values only
- `privacy.redact_pii` — false (acceptable default)
- `approvals.mode: manual` — command approval prompts enabled
- `GATEWAY_ALLOW_ALL_USERS=false` — gateway user restriction active

## Platform States (for delta tracking)
- Telegram: connected (updated 2026-05-13T20:52:52Z)
- WhatsApp: connected (updated 2026-05-13T20:52:52Z)
- No regressions from previous audit

## Session Count
- Not counted this run (methodology focused on credential exposure)

## Delta from Previous Audit (12:15 UTC)
- Previous FAIL items #2 (overly permissive file permissions) and #3 (session dumps) and #4 (log file credential leakage) were NOT re-checked this run — they may still be present
- Previous FAIL item #1 (Ollama key) confirmed still present — now at 3 consecutive audits (UNRESOLVED x3)
- 3 new FAIL items added: client_secret.json exposure, .env backup exposure, Desktop .env exposure
- If all previous FAIL items persist, total unresolved count is 7

## Notes
- This audit ran as cron job security-watchdog; final response delivered to Telegram topic 20
- Methodology this run: focused on credential exposure scanning (Phase 1), did not re-check session dumps or log files (Phase 6)
- The Google OAuth client_secret finding is particularly sensitive — it grants persistent access to Google Sheets API
