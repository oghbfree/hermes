# System Security Audit — 2026-05-15 00:04 UTC

## Score: 5 FAIL / 10 PASS — Security posture: DEGRADED

## FAIL Items

### CRITICAL
1. **Exposed Google OAuth Client Secret in oauth-client.json** (REPEAT — 4th consecutive audit)
   - File: `~/.openclaw/credentials/oauth-client.json` — contains full client_secret
   - Permissions: 644 (world-readable)
   - REMEDY: Rotate the secret in Google Cloud Console; restrict file to 600; move out of workspace

2. **Exposed Google OAuth Client Secret in google_client_secret.json** (REPEAT)
   - File: `~/.hermes/google_client_secret.json` — contains full client_secret (same value as oauth-client.json)
   - Permissions: 644 (world-readable)
   - REMEDY: Rotate the secret in Google Cloud Console; restrict file to 600

3. **Conflicting Bot Tokens Across .env Files** (REPEAT)
   - `~/.hermes/.env` has token starting with 827724... (active)
   - `~/.openclaw/.env` has token starting with 835929... (different/old)
   - Two different tokens indicates partially-applied rotation or unmanaged bot
   - REMEDY: Decommission old bot token; remove from `~/.openclaw/.env`

### HIGH
4. **Ollama Private Key World-Readable** (REPEAT — 4th consecutive audit, UNRESOLVED x4)
   - File: `~/.ollama/id_ed25519` — MSYS reports 644
   - NTFS ACL check: Only SYSTEM, Administrators, and User have FullControl (proper ACLs)
   - However, MSYS tools see it as world-readable which is a hygiene concern
   - REMEDY: Restrict ACL to current user only (remove BUILTIN\Administrators if not needed)

5. **Session Dump Files Persist** (REPEAT)
   - 6 request_dump files in `~/.hermes/sessions/` containing full API request/response payloads
   - Oldest from 2026-05-10, newest from 2026-05-12
   - REMEDY: Delete old request_dump files; add cleanup cron job

## PASS Items
- `.hermes/.env` — properly redacted values (redact_secrets=true working)
- `.hermes/config.yaml` — no embedded secrets; redact_secrets=true
- Gateway state — Telegram and WhatsApp both connected (updated 2026-05-14T18:12Z)
- Channel directory — 15 Telegram topics, all under group -1003784520976, no unknown channels
- `redact_secrets: true` — active
- `allow_private_urls: false` — restricted
- `GATEWAY_ALLOW_ALL_USERS=false` — gateway user restriction active
- Desktop .env — no longer present (resolved since last audit)
- .env backup files — no longer present (resolved since last audit)
- Git history — no .env, .key, .pem, or credential files tracked in git history
- `tirith_enabled: false` — not applicable on Windows (no false flag)

## Platform States (for delta tracking)
- Telegram: connected (updated 2026-05-14T18:12:02Z)
- WhatsApp: connected (updated 2026-05-14T18:12:02Z)
- No regressions from previous audit

## Session Count
- Total sessions: 159
- Request dumps: 6 (unchanged from last audit)

## Delta from Previous Audit (2026-05-14 18:04 UTC)
- RESOLVED: Desktop .env exposure (item #4 from previous audit) — file no longer exists
- RESOLVED: .env backup files (item #2 from previous audit) — files no longer present
- PERSISTING: Google OAuth client_secret exposure (now 4th consecutive audit)
- PERSISTING: Ollama key permissions (now 4th consecutive audit, UNRESOLVED x4)
- PERSISTING: Session dumps (still 6 files, no cleanup)
- NEW: Conflicting bot tokens between .hermes/.env and .openclaw/.env
- Previous audit noted 4 FAIL; this audit finds 5 FAIL (3 carryover + 1 new + 1 re-discovered)

## Notes
- This audit ran as cron job security-watchdog at 2026-05-15 00:04 UTC
- The Ollama key NTFS ACL is actually properly restricted (SYSTEM/Admins/User only), so the MSYS 644 reading is a false positive for actual access — but still flagged for hygiene
- The Google OAuth client_secret is the most sensitive finding — it grants persistent API access to Google services
- Two copies of the same client_secret exist: one in .openclaw/credentials/ and one in .hermes/
- The gogcli credentials.json in AppData/Roaming also contains the same client_secret
