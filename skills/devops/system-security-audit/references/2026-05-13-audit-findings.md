# System Security Audit — 2026-05-13 00:05 UTC

Automated cron-run audit. Score: 9 PASS / 9 FAIL — Security posture: **degraded**

## FAIL Items

### CRITICAL

1. **Desktop .env with Exposed API Keys (UNRESOLVED x4)**
   - Path: `~/Desktop/.env` (584 bytes, dated Mar 30)
   - Contains BRAVE_SEARCH_API_KEY, TELEGRAM_BOT_TOKEN, OPENROUTER_API_KEY, GROQ_API_KEY, GOOGLE_API_KEY, WHISPER_API_KEY, SAG_API_KEY, GOG_ACCOUNT
   - Flagged since 2026-05-11 — 4th consecutive audit without remediation
   - → REMEDY: Delete ~/Desktop/.env immediately. Rotate all exposed keys.

2. **API Keys Committed to Git History (UNRESOLVED)**
   - `groq_key.txt` tracked across 5 commits dating to 2026-03-13
   - 92+ security scan output files in `memory/Security/` with previously captured keys
   - → REMEDY: Use git filter-repo or BFG to scrub keys from history

3. **185 .txt Files Tracked in OpenClaw Workspace Git (UNRESOLVED)**
   - Passwords, credentials.xlsx, financial records in git
   - No *.txt catch-all in .gitignore
   - Includes `raw-data/Fam/Mum/Mums netgear. Password.md`
   - → REMEDY: Add *.txt to .gitignore. Remove tracked .txt files.

### HIGH

4. **Triplicate Credential Stores (UNRESOLVED)**
   - `~/.hermes/.env` (10 keys), `~/.openclaw/.env` (9 keys), `~/Desktop/.env` (9 keys)
   - Duplicate TELEGRAM_BOT_TOKEN and OPENROUTER_API_KEY across all 3
   - → REMEDY: Consolidate to ONE .env file. Delete the others.

5. **Config Files World-Readable (644 mode) (UNRESOLVED)**
   - `~/.hermes/config.yaml`, `~/.hermes/.env`, `~/.hermes/auth.json`
   - All mode 644 (rw-r--r--)
   - → REMEDY: chmod 600 on all sensitive config files.

6. **Session Request Dumps Persisting (UNRESOLVED)**
   - 6 request_dump_*.json files with full API payloads (up from 5 last audit)
   - 72 session files total (up from 57 — +15 since last audit)
   - → REMEDY: Delete request_dump_*.json files. Implement cleanup cron.

### MEDIUM

7. **Tirith Enforcement Unavailable (UNRESOLVED)**
   - `tirith_enabled: true` but `unsupported_platform` on Windows
   - → REMEDY: Set tirith_enabled: false, install alternative scanner.

8. **Google OAuth Credentials in openclaw Credentials Dir (UNRESOLVED)**
   - `~/.openclaw/credentials/google-credentials.json`
   - `~/.openclaw/credentials/oauth-client.json`
   - → REMEDY: Encrypt or restrict directory permissions to 700.

9. **No SSH Keys Configured (UNRESOLVED)**
   - `~/.ssh/` has only known_hosts, no private keys
   - → REMEDY: Generate SSH key pair if remote access needed.

## PASS Items

- Gateway running, Telegram connected
- WhatsApp CONNECTED (was "retrying" last audit — IMPROVED)
- Channel directory intact — no suspicious unknown channels
- `redact_secrets: true` configured
- `allow_private_urls: false`
- Environment variables properly masked (HERMES_SESSION_KEY, HERMES_REDACT_SECRETS)
- No leaked SSH private keys (none exist to leak)
- .env patterns in .gitignore (openclaw workspace)
- gogcli repo follows credential best practices

## Platform State Snapshot

```
telegram: connected
whatsapp: connected (IMPROVED from retrying)
discord: [] (empty)
```

## Session File Count

72 session files in `~/.hermes/sessions/` — 6 are request_dump_*.json

## Notes

- 4th consecutive audit with Desktop .env unresolved — remains CRITICAL
- Session files grew from 57 to 72 (+15) since previous audit
- WhatsApp recovered from "retrying" to "connected" since previous audit
- All 9 FAIL items from previous audit remain unresolved
- New cron request dump file detected
