# Security Audit — 2026-05-14 00:12 UTC (New Focused Format)

**Score: 5 FAIL / 3 PASS — Security posture: DEGRADED**

This audit used a new, more focused methodology than previous runs. Previous audits (May 11-13) used a broad 9-category checklist. This run focused on credential exposure depth with fewer categories.

## FAIL Items

### FAIL 1: Exposed Credentials on Desktop (CRITICAL)
- **File:** `C:\Users\User\Desktop\.env` (permissions: 644)
- **Contents:** GROQ_API_KEY, OPENROUTER_API_KEY, BRAVE_SEARCH_API_KEY (fully exposed), GOOGLE_API_KEY, WHISPER_API_KEY, SAG_API_KEY, OPENCLAW_HOOKS_TOKEN (fully exposed), GOG_ACCOUNT, TELEGRAM_BOT_TOKEN (partially masked)
- **Risk:** Desktop is highly accessible. Any process/user can harvest all API keys.
- **Remedy:** Move to `~/.hermes/` or `~/.openclaw/`, set permissions to 600, delete Desktop copy.
- **Age:** Chronic since May 11 (4+ consecutive audits)

### FAIL 2: Google OAuth Credentials Exposed (CRITICAL)
- **File:** `C:\Users\User\.openclaw\google-sheets-creds.json` (permissions: 644)
- **Contents:** refresh_token, client_id, client_secret (all exposed in plaintext)
- **Risk:** Refresh token grants persistent access to Google Sheets. Combined with client_id/secret, attacker can fully impersonate the OAuth app.
- **Remedy:** Restrict to 600. Rotate OAuth client secret and revoke refresh token immediately.
- **Age:** New finding (not detected by previous audit format)

### FAIL 3: Duplicate OAuth Client Secret (HIGH)
- **File:** `C:\Users\User\.openclaw\credentials\oauth-client.json` (permissions: 644)
- **Contents:** Same client_secret as google-sheets-creds.json
- **Risk:** Redundant exposure increases attack surface.
- **Remedy:** Consolidate and restrict permissions to 600.
- **Age:** New finding

### FAIL 4: .env Backup Files with Historical Secrets (HIGH)
- **Files:** `C:\Users\User\.openclaw\.env.backup` (511 bytes), `C:\Users\User\.openclaw\.env.backup.20260401-150621` (584 bytes)
- **Risk:** Backup files may contain older API keys/tokens. The `.env.backup.20260401` file is larger than current, suggesting additional secrets no longer in active config.
- **Remedy:** Encrypt or delete old backups.
- **Age:** New finding

### FAIL 5: Conflicting Telegram Bot Tokens (HIGH)
- **Tokens found across 3 environments:**
  - `~/.hermes\.env` → token starting `827724` (Hermes gateway token)
  - `C:\Users\User\Desktop\.env` → token starting `835929`
  - `~/.openclaw\.env` → token starting `835929`
- **Risk:** Two different bot tokens in use. The `835929` token may be an unmanaged/rogue bot.
- **Remedy:** Verify which token is intended active. Revoke unused token via @BotFather.
- **Age:** New finding

## PASS Items
- Channel/gateway integrity: Telegram and WhatsApp both connected at gateway level
- SSH key exposure: `~/.ssh/` contains only `known_hosts`, no private keys
- Core config file permissions: Acceptable on Windows (644 default, NTFS ACLs provide real control)

## Methodology Note
This audit used a focused credential-exposure methodology (5 checks) vs. the previous broad methodology (9+ checks including git history, tirith, session dumps). The new format found 3 new FAIL items (Google OAuth, .env backups, conflicting tokens) that the old format missed entirely. Both formats are valid -- the focused format goes deeper on credential exposure while the broad format covers more surface area. Future audits should ideally combine both approaches.
