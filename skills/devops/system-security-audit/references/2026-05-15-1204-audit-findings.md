# System Security Audit — 2026-05-15 12:04 UTC

## Score: 5 FAIL / 4 PASS — Security posture: DEGRADED

## FAIL Items

### CRITICAL
1. **Google OAuth Token Expired** (REPEAT — 2nd consecutive audit, escalated)
   - ~/.hermes/google_token.json shows expiry: 2026-05-15T08:00:48Z — expired ~3.1 hours ago
   - refresh_token is present but refresh flow may be broken
   - Affects: Gmail, Drive, Calendar, Sheets, Contacts API access
   - REMEDY: Verify Google Cloud Console OAuth client is active; test token refresh manually

2. **Conflicting Bot Tokens Between .hermes and .openclaw** (REPEAT)
   - .hermes/.env token prefix: 82772443... suffix: ...ugM8
   - .openclaw/.env token prefix: 83592902... suffix: ...Sxsw
   - Two different tokens indicates partially-applied rotation or unmanaged bot
   - hermes-backup copies match .hermes (82772443...)
   - REMEDY: Consolidate to single bot token; remove old token from .openclaw/.env

3. **Duplicate Google OAuth Credential Storage** (REPEAT — 6th+ consecutive audit, CHRONIC)
   - Same client_secret stored in THREE locations:
     1. ~/.hermes/google_client_secret.json
     2. ~/.hermes/google_token.json (also contains active refresh_token)
     3. ~/.openclaw/credentials/oauth-client.json
   - Expands attack surface unnecessarily
   - REMEDY: Consolidate to single location; delete duplicates

### HIGH
4. **World-Readable Credential Files** (REPEAT — 6th+ consecutive audit, CHRONIC)
   - All sensitive files show mode 644 (rw-r--r--) via MSYS stat
   - Affected: ~/.hermes/.env, ~/.hermes/auth.json, ~/.hermes/google_client_secret.json, ~/.hermes/google_token.json, ~/.hermes/config.yaml, ~/.openclaw/.env, ~/.openclaw/credentials/oauth-client.json
   - Windows ACLs grant Full Control to SYSTEM, Administrators, and User — but POSIX bits are 644
   - REMEDY: icacls <file> /inheritance:r /grant:r "%USERNAME%:(F)" for each file

5. **Security Scan Output Files Tracked in Git** (REPEAT)
   - 185 .txt files tracked in ~/.openclaw/workspace
   - memory/Security/ directory contains 100+ security scan output files (security_check_*.txt, security_scan_*.txt, etc.)
   - These files may contain API keys, tokens, and private data from past scans
   - REMEDY: Add memory/Security/ to .gitignore; remove tracked files from git history

## PASS Items
- Channel integrity: Telegram home (123286468), group (-1003784520976) with 16 topics, no orphaned channels
- Gateway state: Telegram connected, WhatsApp connected (updated 2026-05-14T18:12Z)
- redact_secrets: true — active in config.yaml
- tirith_enabled: false (not applicable on Windows)
- Ollama key NTFS ACL: properly restricted to SYSTEM+Admins+User (MSYS 644 is false positive, confirmed again)
- .gitconfig clean — no embedded credentials
- No private keys found outside ~/.ssh/ and ~/.ollama/

## WARN Items
- ~/hermes-backup/ directory has inheritance-enabled Full Control for SYSTEM+Admins+User — backups contain .env files with secrets
- ~/.gitignore does not exist — risk of accidentally committing .env files
- 7 request_dump_*.json files persist in sessions/ (contain full API request/response payloads)
- 179 session files in ~/.hermes/sessions/ (up from 159+ in previous audit — growth of 20)
- redact_pii: false — should be true if processing personal/health data (GDPR/privacy compliance)
- Log files (agent.log, errors.log, gateway.log, maintenance-2026-05-13.log) contain token/secret references

## Platform States (for delta tracking)
- Telegram: connected (updated 2026-05-14T18:12Z)
- WhatsApp: connected (updated 2026-05-14T18:12Z)
- No regressions detected

## Session Count
- Total sessions: 179 (up from 159 in previous audit)
- Request dumps: 7 files (up from 6 in previous audit)

## Delta from Previous Audit (2026-05-15 06:04 UTC)
- PERSISTING: World-readable credential files (6th+ consecutive audit, CHRONIC)
- PERSISTING: Duplicate Google OAuth credential storage (6th+ consecutive audit, CHRONIC)
- PERSISTING: Conflicting bot tokens between .hermes and .openclaw
- PERSISTING: Security scan output files in git (185 .txt files)
- PERSISTING: Session dump files (7 files, no cleanup)
- PERSISTING: Google OAuth token expired (now 3.1 hours past expiry)
- NEW: Session count grew from 159 to 179 (+20)
- NEW: Request dump count grew from 6 to 7 (+1)

## Notes
- This audit ran as cron job at 2026-05-15 12:04 UTC
- ⚠️ REMEDIATION FATIGUE: 3 FAIL items unresolved for 6+ consecutive audits
- The file permissions and duplicate credential findings have persisted across 6+ consecutive audits with zero remediation
- The Google token expiry has worsened (from 8 hours to 3.1 hours past expiry since last audit — actually improved slightly, but still expired)
- No improvement since first audit on 2026-05-12. Automated detection is working but remediation is not happening.
