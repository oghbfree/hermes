# System Security Audit — 2026-05-14 06:04 UTC

**Score: 7 FAIL / 9 PASS — Security posture: DEGRADED**

## FAIL Items

### FAIL 1: Desktop/.env — Full unmasked credentials on Desktop (CRITICAL)
- **File:** `C:\Users\User\Desktop\.env` (permissions: 644, 584 bytes)
- **Contents:** GROQ_API_KEY, OPENROUTER_API_KEY, BRAVE_SEARCH_API_KEY (fully exposed), GOOGLE_API_KEY, WHISPER_API_KEY, SAG_API_KEY, OPENCLAW_HOOKS_TOKEN (fully exposed), GOG_ACCOUNT, TELEGRAM_BOT_TOKEN (partially masked)
- **Risk:** Desktop is highly accessible. Any process/user can harvest all API keys.
- **Remedy:** Move to `~/.hermes/` or `~/.openclaw/`, set permissions to 600, delete Desktop copy.
- **Age:** Chronic since May 11 (5+ consecutive audits)

### FAIL 2: SSH Private Key in Wrong Location, World-Readable (CRITICAL)
- **File:** `C:\Users\User\.ollama\id_ed25519` (permissions: 644, 387 bytes)
- **Contents:** OpenSSH Ed25519 private key
- **Risk:** Private key is in `.ollama/` instead of `.ssh/`, and is world-readable (644). Previous audits incorrectly reported PASS because they only checked `~/.ssh/`.
- **Remedy:** Move to `~/.ssh/id_ed25519`, set permissions to 600.
- **Age:** NEW (not detected by previous audit methodology — key was outside ~/.ssh/)

### FAIL 3: All .env Files World-Readable (HIGH)
- **Files:** `.hermes/.env` (644), `.openclaw/.env` (644), `Desktop/.env` (644)
- **Risk:** Credential files readable by all users/processes.
- **Remedy:** `chmod 600` on all .env files.
- **Age:** Chronic since May 11

### FAIL 4: .env Backup Files with Historical Secrets (HIGH)
- **Files:** `.openclaw/.env.backup` (511 bytes), `.openclaw/.env.backup.20260401-150621` (584 bytes)
- **Risk:** Backup files may contain older API keys/tokens no longer in active config.
- **Remedy:** Encrypt or delete old backups.
- **Age:** Chronic since May 11

### FAIL 5: Conflicting Telegram Bot Tokens (HIGH)
- **Tokens found:** `~/.hermes/.env` → token starting `827724` (Hermes gateway) | `Desktop/.env` and `~/.openclaw/.env` → token starting `835929`
- **Risk:** Two different bot tokens in use. The `835929` token may be an unmanaged/rogue bot.
- **Remedy:** Verify which token is intended active. Revoke unused token via @BotFather.
- **Age:** Chronic since May 14 00:12 audit

### FAIL 6: contacts.json and state.db World-Readable (MEDIUM)
- **Files:** `contacts.json` (644, 8KB), `state.db` (644, 38MB)
- **Risk:** Full contact details and complete session state readable by all users.
- **Remedy:** `chmod 600 contacts.json state.db`
- **Age:** NEW

### FAIL 7: redact_pii: false While Processing Personal Data (MEDIUM)
- **Config:** `privacy.redact_pii: false` in config.yaml
- **Risk:** PII redaction disabled despite processing health logs, phone numbers, and personal data. Inconsistent with `security.redact_secrets: true`.
- **Remedy:** Set `privacy.redact_pii: true`
- **Age:** NEW

## PASS Items
- auth.json references credentials via env vars (not hardcoded) ✓
- GATEWAY_ALLOW_ALL_USERS=false (access control enabled) ✓
- allow_private_urls=false in both browser and security sections ✓
- WhatsApp group_policy=allowlist ✓
- Telegram/Discord require_mention=true ✓
- No secrets exposed in running process environment ✓
- Gateway running (gateway.lock, gateway.pid present) ✓
- Channel directory integrity verified (no unknown channels) ✓
- No .netrc or credentials.json in .hermes/ ✓

## Platform States
- Telegram: connected (group -1003784520976 with 12 topics, DM 123286468)
- Discord: configured but no active channels
- WhatsApp: configured (dm_policy=open, group_policy=allowlist)
- Slack: configured but no active channels

## Notes
- Google OAuth credentials (`~/.openclaw/credentials/google-sheets-creds.json`, `oauth-client.json`) were flagged in the 00:12 UTC audit but not re-verified this run. Treat as still active until confirmed otherwise.
- execute_code sandbox confirmed fully isolated — cannot read any host filesystem paths. Use terminal tool for all file reads on this Windows host.
