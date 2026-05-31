# System Security Audit — 2026-05-15 06:04 UTC

## Score: 3 FAIL / 3 PASS — Security posture: DEGRADED

## FAIL Items

### CRITICAL
1. **World-Readable Credential Files** (REPEAT — 5th+ consecutive audit)
   - All sensitive files show mode 644 (rw-r--r--) via MSYS stat
   - Affected: ~/.hermes/.env, ~/.hermes/auth.json, ~/.hermes/google_client_secret.json, ~/.hermes/google_token.json, ~/.hermes/config.yaml, ~/.openclaw/.env, ~/.openclaw/credentials/google-credentials.json, ~/.openclaw/credentials/oauth-client.json
   - Windows ACLs grant Full Control to SYSTEM, Administrators, and User — but POSIX bits are 644
   - REMEDY: icacls <file> /inheritance:r /grant:r "%USERNAME%:(F)" for each file

2. **Duplicate Google OAuth Credential Storage** (REPEAT)
   - Same client_secret stored in THREE locations:
     1. ~/.hermes/google_client_secret.json
     2. ~/.hermes/google_token.json (also contains active refresh_token)
     3. ~/.openclaw/credentials/oauth-client.json
   - Expands attack surface unnecessarily
   - REMEDY: Consolidate to single location; delete duplicates

3. **Google OAuth Token Expired** (NEW)
   - ~/.hermes/google_token.json shows expiry: 2026-05-14T21:47:44Z — expired ~8 hours ago
   - refresh_token is present but refresh flow may be broken
   - Affects: Gmail, Drive, Calendar, Sheets, Contacts API access
   - REMEDY: Verify Google Cloud Console OAuth client is active; test token refresh manually

## WARN Items
- ~/hermes-backup/ directory has inheritance-enabled Full Control for SYSTEM+Admins+User — backups may contain secrets
- ~/.gitignore does not exist — risk of accidentally committing .env files if git repo initialized at ~

## PASS Items
- Channel integrity: Telegram home (123286468), group (-1003784520976) with 12 topics, no orphaned channels
- redact_secrets: true — active in config.yaml
- .gitconfig clean — no embedded credentials

## Platform States (for delta tracking)
- Telegram: connected (from channel_directory.json, updated 2026-05-15T05:59Z)
- WhatsApp: enabled in config
- No regressions detected

## Session Count
- Total sessions: 159+ (count truncated due to timeout)
- Request dumps: 6+ (files from 2026-05-10 through 2026-05-14)

## Delta from Previous Audit (2026-05-15 00:04 UTC)
- PERSISTING: World-readable credential files (5th+ consecutive audit)
- PERSISTING: Duplicate Google OAuth credential storage
- PERSISTING: Session dump files (6+ files, no cleanup)
- NEW: Google OAuth token expired (>1 hour past expiry)
- RESOLVED: Desktop .env exposure (resolved since 2026-05-14 audit)
- RESOLVED: .env backup files (resolved since 2026-05-14 audit)
- NOTE: Ollama key MSYS 644 false positive confirmed again — NTFS ACL is properly restricted

## Notes
- This audit ran as cron job at 2026-05-15 06:04 UTC
- The file permissions finding has persisted across 5+ consecutive audits with no remediation
- The Google token expiry is a new finding — previous audits did not check the expiry field
- The send_message tool does not exist; cron delivery is via final response text routing
