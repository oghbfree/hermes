# System Security Audit — 2026-05-15 18:04 UTC

## Score: 5 FAIL / 4 PASS — Security posture: DEGRADED

## FAIL Items

### CRITICAL
1. **Google OAuth Token Expired** (REPEAT — 3rd consecutive audit, escalated)
   - ~/.hermes/google_token.json shows expiry: 2026-05-15T08:00:48Z — expired ~9.1 hours ago
   - refresh_token is present but token file has NOT been modified since creation (mtime: 08:00:49)
   - Token expiry worsened from 3.1h (12:04 audit) to 9.1h — refresh flow is NOT auto-refreshing
   - Affects: Gmail, Drive, Calendar, Sheets, Contacts API access
   - REMEDY: Verify Google Cloud Console OAuth client is active; test token refresh manually; check if any Google API calls are actually failing

2. **Conflicting Bot Tokens Between .hermes and .openclaw** (REPEAT)
   - .hermes/.env token prefix: 827724... suffix: ...ugM8
   - .openclaw/.env token prefix: 835929... suffix: ...Sxsw
   - Two different tokens indicates partially-applied rotation or unmanaged bot
   - hermes-backup copies match .hermes (827724...)
   - REMEDY: Consolidate to single bot token; remove old token from .openclaw/.env

3. **Duplicate Google OAuth Credential Storage** (REPEAT — 7th+ consecutive audit, CHRONIC)
   - Same client_secret stored in FOUR locations:
     1. ~/.hermes/google_client_secret.json
     2. ~/.hermes/google_token.json (also contains active refresh_token)
     3. ~/.openclaw/credentials/oauth-client.json
     4. ~/AppData/Roaming/gogcli/credentials.json
   - Expands attack surface unnecessarily
   - REMEDY: Consolidate to single location; delete duplicates

### HIGH
4. **World-Readable Credential Files** (REPEAT — 7th+ consecutive audit, CHRONIC)
   - All sensitive files show mode 644 (rw-r--r--) via MSYS stat
   - Affected: ~/.hermes/.env, ~/.hermes/auth.json, ~/.hermes/google_client_secret.json, ~/.hermes/google_token.json, ~/.hermes/config.yaml, ~/.hermes/contacts.json, ~/.hermes/state.db, ~/.openclaw/.env, ~/.openclaw/credentials/oauth-client.json
   - Windows ACLs grant Full Control to SYSTEM, Administrators, and User — but POSIX bits are 644
   - REMEDY: icacls <file> /inheritance:r /grant:r "%USERNAME%:(F)" for each file

5. **Security Scan Output Files Tracked in Git** (REPEAT)
   - 185 .txt files tracked in ~/.openclaw/workspace
   - memory/Security/ directory contains security scan output files (security_check_*.txt, security_scan_*.txt, etc.)
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
- No .env files on Desktop (only .env.example in gogcli)
- No .env backup files found

## WARN Items
- ~/hermes-backup/ directory has inheritance-enabled Full Control for SYSTEM+Admins+User — backups contain .env files with secrets
- ~/.gitignore does not exist at home directory level — risk of accidentally committing .env files
- 7 request_dump_*.json files persist in sessions/ (contain full API request/response payloads) — unchanged
- 185 session files in ~/.hermes/sessions/ (up from 179 in previous audit — growth of +6)
- redact_pii: false — should be true if processing personal/health data (GDPR/privacy compliance)
- Log files (agent.log, errors.log, gateway.log, maintenance-2026-05-13.log, maintenance-2026-05-15.log) contain token/secret references

## Platform States (for delta tracking)
- Telegram: connected (updated 2026-05-14T18:12Z)
- WhatsApp: connected (updated 2026-05-14T18:12Z)
- No regressions detected

## Session Count
- Total sessions: 185 (up from 179 in previous audit)
- Request dumps: 7 files (unchanged from previous audit)

## Delta from Previous Audit (2026-05-15 12:04 UTC)
- PERSISTING: World-readable credential files (7th+ consecutive audit, CHRONIC)
- PERSISTING: Duplicate Google OAuth credential storage (7th+ consecutive audit, CHRONIC)
- PERSISTING: Conflicting bot tokens between .hermes and .openclaw
- PERSISTING: Security scan output files in git (185 .txt files)
- PERSISTING: Session dump files (7 files, no cleanup)
- PERSISTING: Google OAuth token expired (worsened from 3.1h to 9.1h past expiry)
- NEW: Session count grew from 179 to 185 (+6)
- NEW: gogcli credentials.json confirmed as 4th duplicate OAuth secret store (same client_secret)
- UNCHANGED: Request dump count stable at 7

## Notes
- This audit ran as cron job at 2026-05-15 18:04 UTC
- ⚠️ REMEDIATION FATIGUE: 3+ FAIL items unresolved for 7+ consecutive audits
- The file permissions and duplicate credential findings have persisted across 7+ consecutive audits with zero remediation
- The Google token expiry has worsened significantly (3.1h → 9.1h past expiry) — the refresh flow is not working
- No improvement since first audit on 2026-05-12. Automated detection is working but remediation is not happening.
