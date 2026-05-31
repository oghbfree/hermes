# System Security Audit — 2026-05-16 06:04 UTC

## Score: 5 FAIL / 5 PASS — Security posture: DEGRADED

## FAIL Items

### CRITICAL
1. **Google OAuth Token Expired** (REPEAT — 4th consecutive audit, escalated)
   - ~/.hermes/google_token.json shows expiry: 2026-05-15T08:00:48Z — expired ~22 hours ago
   - refresh_token is present but token file has NOT been modified since creation (mtime: 08:00:49)
   - Token expiry worsened from 9.1h (18:04 audit) to 22h — refresh flow is NOT auto-refreshing
   - Affects: Gmail, Drive, Calendar, Sheets, Contacts API access
   - REMEDY: Verify Google Cloud Console OAuth client is active; test token refresh manually

2. **Conflicting Bot Tokens Between .hermes and .openclaw** (REPEAT — 4th+ consecutive audit)
   - .hermes/.env token prefix: 827724...
   - .openclaw/.env token prefix: 835929...
   - Two different tokens indicates partially-applied rotation or unmanaged bot
   - REMEDY: Consolidate to single bot token; remove old token from .openclaw/.env

3. **Duplicate Google OAuth Credential Storage** (REPEAT — 8th+ consecutive audit, CHRONIC)
   - Same client_secret stored in FOUR locations:
     1. ~/.hermes/google_client_secret.json
     2. ~/.hermes/google_token.json (also contains active refresh_token)
     3. ~/.openclaw/credentials/oauth-client.json
     4. ~/AppData/Roaming/gogcli/credentials.json
   - REMEDY: Consolidate to single location; delete duplicates

### HIGH
4. **World-Readable Credential Files** (REPEAT — 8th+ consecutive audit, CHRONIC)
   - All sensitive files show mode 644 (rw-r--r--) via MSYS stat
   - Affected: ~/.hermes/.env, ~/.hermes/auth.json, ~/.hermes/google_client_secret.json, ~/.hermes/google_token.json, ~/.hermes/config.yaml, ~/.hermes/contacts.json, ~/.hermes/state.db, ~/.openclaw/.env, ~/.openclaw/credentials/oauth-client.json
   - REMEDY: icacls <file> /inheritance:r /grant:r "%USERNAME%:(F)" for each file

5. **Security Scan Output Files Tracked in Git** (REPEAT — 4th+ consecutive audit)
   - 185 .txt files tracked in ~/.openclaw/workspace
   - memory/Security/ directory contains security scan output files (security_check_*.txt, security_scan_*.txt, etc.)
   - These files may contain API keys, tokens, and private data from past scans
   - REMEDY: Add memory/Security/ to .gitignore; remove tracked files from git history

## PASS Items
- Channel integrity: Telegram home (123286468), group (-1003784520976) with 16+ topics, no orphaned channels
- Gateway state: Telegram connected (updated 2026-05-15T23:07Z), WhatsApp connected (updated 2026-05-15T23:07Z) — NO regressions
- redact_secrets: true — active in config.yaml
- tirith_enabled: false (not applicable on Windows)
- Ollama key NTFS ACL: properly restricted to SYSTEM+Admins+User (MSYS 644 is false positive, confirmed again)
- .gitconfig clean — no embedded credentials
- No private keys found outside ~/.ssh/ and ~/.ollama/
- No .env files on Desktop (only .env.example in gogcli)
- No .env backup files found
- hermes-backup directory ACL: restricted to SYSTEM+Admins+User (no broad group access)

## WARN Items
- 11 request_dump_*.json files persist in sessions/ (contain full API request/response payloads) — increased from 7
- 209 session files in ~/.hermes/sessions/ (up from 185 in previous audit — growth of +24)
- redact_pii: false — should be true if processing personal/health data (GDPR/privacy compliance)
- Log files (agent.log, errors.log, gateway.log, gateway-stdio.log, maintenance-*.log) contain token/secret references
- ~/.gitignore does not exist at home directory level

## Platform States (for delta tracking)
- Telegram: connected (updated 2026-05-15T23:07:12Z)
- WhatsApp: connected (updated 2026-05-15T23:07:13Z)
- No regressions detected

## Session Count
- Total sessions: 209 (up from 185 in previous audit — growth of +24)
- Request dumps: 11 files (up from 7 in previous audit — growth of +4)

## Delta from Previous Audit (2026-05-15 18:04 UTC)
- PERSISTING: World-readable credential files (8th+ consecutive audit, CHRONIC)
- PERSISTING: Duplicate Google OAuth credential storage (8th+ consecutive audit, CHRONIC)
- PERSISTING: Conflicting bot tokens between .hermes and .openclaw
- PERSISTING: Security scan output files in git (185 .txt files, unchanged)
- PERSISTING: Google OAuth token expired (worsened from 9.1h to 22h past expiry)
- NEW: Request dump count increased from 7 to 11 (+4)
- NEW: Session count grew from 185 to 209 (+24)
- UNCHANGED: Platform states stable (Telegram + WhatsApp both connected)
- UNCHANGED: hermes-backup ACL properly restricted

## Notes
- This audit ran as cron job at 2026-05-16 06:04 UTC
- ⚠️ REMEDIATION FATIGUE: 5 FAIL items unresolved for 8+ consecutive audits
- The file permissions and duplicate credential findings have persisted across 8+ consecutive audits with zero remediation
- The Google token expiry has worsened significantly (9.1h → 22h past expiry) — the refresh flow is not working
- Request dump count increased from 7 to 11 — no cleanup mechanism running
- No improvement since first audit on 2026-05-12. Automated detection is working but remediation is not happening.
