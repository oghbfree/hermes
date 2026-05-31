# System Security Audit — 2026-05-17 00:04 UTC

## Score: 9 FAIL / 10 PASS — Security posture: DEGRADED

## FAIL Items

### CRITICAL
1. **Sensitive Files World-Readable (644)** (REPEAT — 11th+ consecutive audit, CHRONIC)
   - ~/.hermes/.env, ~/.hermes/auth.json, ~/.hermes/config.yaml, ~/.hermes/google_client_secret.json, ~/.hermes/whatsapp/session/creds.json (2955 bytes), ~/.hermes/state-snapshots/20260515-194826-pre-update/.env, ~/AppData/Roaming/gogcli/credentials.json
   - NTFS ACLs show proper restriction (MSYS 644 is false positive), but MSYS-level permissions remain 644
   - REMEDY: icacls to restrict to owner-only for each file

2. **Google OAuth Client Secret in Plaintext (4 locations)** (REPEAT — 11th+ consecutive audit, CHRONIC)
   - ~/.hermes/google_client_secret.json
   - ~/.hermes/google_token.json (contains client_secret + active refresh_token)
   - ~/.openclaw/credentials/oauth-client.json
   - ~/AppData/Roaming/gogcli/credentials.json — same client_id + client_secret
   - REMEDY: Revoke in Google Cloud Console; consolidate to OS keychain; delete duplicate copies

3. **Stale State-Snapshot .env with Live Keys** (REPEAT — 11th+ consecutive audit, CHRONIC)
   - ~/.hermes/state-snapshots/20260515-194826-pre-update/.env (440 bytes, 644)
   - Contains partially-masked but extractable API keys
   - REMEDY: Delete state-snapshot .env or rotate all keys

4. **Duplicate .env Store (stale)** (REPEAT — 11th+ consecutive audit, CHRONIC)
   - ~/.openclaw/.env (288 bytes, 644) — different TELEGRAM_BOT_TOKEN (835929... vs 827724...)
   - REMEDY: Delete ~/.openclaw/.env after confirming 827724 token is active

5. **WhatsApp Session Credentials World-Readable** (REPEAT — 11th+ consecutive audit, CHRONIC)
   - ~/.hermes/whatsapp/session/creds.json (2955 bytes, 644)
   - REMEDY: Restrict to owner-only access

6. **AGENTS.md BOM Injection (both copies)** (REPEAT — 11th+ consecutive audit, CHRONIC)
   - ~/.hermes/AGENTS.md — UTF-8 BOM (EF BB BF) detected, Hermes platform blocks loading
   - ~/.openclaw/workspace/AGENTS.md — UTF-8 BOM (EF BB BF) detected, Hermes platform blocks loading
   - REMEDY: Remove BOM from both files; investigate how BOM is being re-introduced

### HIGH
7. **Google OAuth Token Expired 15.1h** (REPEAT — 11th+ consecutive audit, CHRONIC)
   - ~/.hermes/google_token.json expiry: 2026-05-16T08:03:39Z (15.1h ago)
   - File mtime: 2026-05-16 08:03:40 (never refreshed since creation)
   - Refresh flow has NEVER executed — token written once, never updated
   - All Google API integrations (Gmail, Drive, Calendar, Sheets, Contacts) may be silently failing
   - REMEDY: Check Google Cloud Console OAuth client status; force token refresh; verify refresh_token is valid

8. **Conflicting Bot Tokens** (REPEAT — 11th+ consecutive audit, CHRONIC)
   - ~/.hermes/.env: TELEGRAM_BOT_TOKEN = 827724...
   - ~/.openclaw/.env: TELEGRAM_BOT_TOKEN = 835929... (different token)
   - hermes-backup/*/config/.env: all use 827724... (consistent with main)
   - REMEDY: Determine which token is active; delete the other .env or align tokens

### MEDIUM
9. **send_audit.py Leftover** (REPEAT — 11th+ consecutive audit, CHRONIC)
   - ~/.hermes/send_audit.py (5183 bytes, dated May 12) — contains hardcoded stale report
   - REMEDY: Delete after confirming it's a leftover

## PASS Items
- File permissions (NTFS ACLs): All sensitive files properly restricted to SYSTEM + Administrators + User
- Channel integrity: 19 Telegram channels/topics registered, all known
- Gateway state: Telegram connected, WhatsApp connected (no regressions)
- redact_secrets: true
- tirith_enabled: false (not applicable on Windows)
- Desktop .env: deleted (remediated since May 14)
- .env backup files on Desktop: deleted (remediated since May 14)
- .gitconfig: clean
- SSH: No keys configured (informational — no SSH-based access expected)
- Ollama key: NTFS ACL properly restricted

## Platform States
- Telegram: connected
- WhatsApp: connected
- No regressions from previous audit

## Delta from Previous Audit (2026-05-16 18:04 UTC)
- PERSISTING: All 8 previous FAIL items remain unresolved
- NEW: AGENTS.md BOM now flagged for BOTH copies (~/.hermes/ and ~/.openclaw/workspace/) — previously only ~/.hermes/ was checked
- Google token expiry worsened: 15.1h (was ~60h in previous audit — token was re-created but refresh flow still never runs)
- Session count: 240 (previous: 226, delta: +14 — normal growth)
- Request dumps: 12 (previous: 8, delta: +4)
- .txt files in workspace: 185 (unchanged)
- No new remediation since May 14 burst

## Notes
- ⚠️ REMEDIATION FATIGUE: 9 FAIL items unresolved for 11+ consecutive audits
- No improvement since first audit on 2026-05-12
- Google token refresh flow has NEVER executed (mtime equals creation time) — this is the most impactful finding as it affects all Google API integrations
