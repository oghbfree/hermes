# System Security Audit — 2026-05-16 12:04 UTC

## Score: 5 FAIL / 6 PASS — Security posture: DEGRADED

## FAIL Items

### CRITICAL
1. **Google OAuth Token Expired** (REPEAT — 5th consecutive audit, escalated)
   - ~/.hermes/google_token.json shows expiry: 2026-05-16T08:03:39Z — expired ~3 hours ago
   - Token WAS refreshed since last audit (previous: 2026-05-15T08:00:48Z, now: 2026-05-16T08:03:39Z)
   - However the new token already expired after ~1 hour — refresh flow is barely keeping up or failing
   - mtime: 2026-05-16 08:03:40 (file written once at token creation, no subsequent refresh)
   - Affects: Gmail, Drive, Calendar, Sheets, Contacts API access
   - REMEDY: Verify Google Cloud Console OAuth client is active; test token refresh manually

2. **Conflicting Bot Tokens Between .hermes and .openclaw** (REPEAT — 5th+ consecutive audit)
   - .hermes/.env token prefix: 827724...ugM8
   - .openclaw/.env token prefix: 835929...Sxsw
   - Two different tokens indicates partially-applied rotation or unmanaged bot
   - hermes-backup copies match .hermes/.env (827724...)
   - REMEDY: Consolidate to single bot token; remove old token from .openclaw/.env

3. **Duplicate Google OAuth Credential Storage** (REPEAT — 9th+ consecutive audit, CHRONIC)
   - Same client_secret stored in FOUR locations:
     1. ~/.hermes/google_client_secret.json
     2. ~/.hermes/google_token.json (also contains active refresh_token)
     3. ~/.openclaw/credentials/oauth-client.json
     4. ~/AppData/Roaming/gogcli/credentials.json
   - REMEDY: Consolidate to single location; delete duplicates

### HIGH
4. **World-Readable Credential Files** (REPEAT — 9th+ consecutive audit, CHRONIC)
   - All sensitive files show mode 644 (rw-r--r--) via MSYS stat
   - Affected: ~/.hermes/.env, ~/.hermes/auth.json, ~/.hermes/google_client_secret.json, ~/.hermes/google_token.json, ~/.hermes/config.yaml, ~/.hermes/contacts.json, ~/.hermes/state.db, ~/.openclaw/.env, ~/.openclaw/credentials/oauth-client.json
   - NTFS ACLs show proper restriction to SYSTEM+Admins+User (MSYS 644 is false positive)
   - However, MSYS-level permissions remain 644 — any MSYS process can read these
   - REMEDY: icacls <file> /inheritance:r /grant:r "%USERNAME%:(F)" for each file

5. **Security Scan Output Files Tracked in Git** (REPEAT — 5th+ consecutive audit)
   - 185 .txt files tracked in ~/.openclaw/workspace
   - memory/Security/ directory contains security scan output files (security_check_*.txt, security_scan_*.txt, etc.)
   - These files may contain API keys, tokens, and private data from past scans
   - REMEDY: Add memory/Security/ to .gitignore; remove tracked files from git history

## PASS Items
- Channel integrity: Telegram home (123286468), group (-1003784520976) with 16+ topics, no orphaned channels
- Gateway state: Telegram connected (updated 2026-05-16T05:43Z), WhatsApp connected (updated 2026-05-16T05:43Z) — NO regressions
- redact_secrets: true — active in config.yaml
- tirith_enabled: false (not applicable on Windows)
- Ollama key NTFS ACL: properly restricted to SYSTEM+Admins+User (MSYS 644 is false positive, confirmed again)
- hermes-backup .env ACL: properly restricted to SYSTEM+Admins+User (no broad group access)
- .gitconfig clean — no embedded credentials
- No private keys found outside ~/.ssh/ and ~/.ollama/
- No .env files on Desktop (only .env.example in gogcli)
- No .env backup files found
- AGENTS.md BOM: detected (EF BB BF) — Hermes platform blocks loading (confirmed working)

## WARN Items
- 11 request_dump_*.json files persist in sessions/ (contain full API request/response payloads) — unchanged from last audit
- 226 session files in ~/.hermes/sessions/ (up from 209 in previous audit — growth of +17)
- redact_pii: false — should be true if processing personal/health data (GDPR/privacy compliance)
- Log files (agent.log, errors.log, gateway.log, gateway-stdio.log, maintenance-*.log) contain token/secret references
- ~/.gitignore does not exist at home directory level
- google-credentials.json in .openclaw/credentials/ contains only client_id (less sensitive) but has BOM

## Platform States (for delta tracking)
- Telegram: connected (updated 2026-05-16T05:43:38Z)
- WhatsApp: connected (updated 2026-05-16T05:43:38Z)
- No regressions detected — both platforms stable

## Session Count
- Total sessions: 226 (up from 209 in previous audit — growth of +17)
- Request dumps: 11 files (unchanged from previous audit)

## Delta from Previous Audit (2026-05-16 06:04 UTC)
- PERSISTING: World-readable credential files (9th+ consecutive audit, CHRONIC)
- PERSISTING: Duplicate Google OAuth credential storage (9th+ consecutive audit, CHRONIC)
- PERSISTING: Conflicting bot tokens between .hermes and .openclaw
- PERSISTING: Security scan output files in git (185 .txt files, unchanged)
- IMPROVED: Google OAuth token was refreshed (expiry moved from 2026-05-15 to 2026-05-16) — but new token already expired ~3h ago
- UNCHANGED: Request dump count stable at 11
- NEW: Session count grew from 209 to 226 (+17)
- UNCHANGED: Platform states stable (Telegram + WhatsApp both connected)
- UNCHANGED: hermes-backup ACL properly restricted
- UNCHANGED: Ollama key ACL properly restricted

## Notes
- This audit ran as cron job at 2026-05-16 12:04 UTC
- ⚠️ REMEDIATION FATIGUE: 5 FAIL items unresolved for 9+ consecutive audits
- The file permissions and duplicate credential findings have persisted across 9+ consecutive audits with zero remediation
- The Google token was refreshed since last audit (improvement) but the new token already expired after ~1 hour — the refresh flow is barely keeping up
- Request dump count stable at 11 — no cleanup mechanism running
- AGENTS.md BOM detected again (EF BB BF) — Hermes platform correctly blocks loading it
- No improvement since first audit on 2026-05-12. Automated detection is working but remediation is not happening.
