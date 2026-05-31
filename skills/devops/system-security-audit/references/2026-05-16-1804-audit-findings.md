# System Security Audit — 2026-05-16 18:04 UTC

## Score: 8 FAIL / 10 PASS — Security posture: DEGRADED

## FAIL Items

### CRITICAL
1. **Sensitive Files World-Readable (644)** (REPEAT — 10th+ consecutive audit, CHRONIC)
   - ~/.hermes/.env, ~/.hermes/auth.json, ~/.hermes/config.yaml, ~/.hermes/google_client_secret.json, ~/.hermes/whatsapp/session/creds.json (2955 bytes), ~/.hermes/state-snapshots/20260515-194826-pre-update/.env, ~/AppData/Roaming/gogcli/credentials.json
   - NTFS ACLs show proper restriction (MSYS 644 is false positive), but MSYS-level permissions remain 644
   - REMEDY: icacls to restrict to owner-only for each file

2. **Google OAuth Client Secret in Plaintext (2 locations)** (REPEAT — 10th+ consecutive audit, CHRONIC)
   - ~/.hermes/google_client_secret.json
   - ~/AppData/Roaming/gogcli/credentials.json — same client_id + client_secret
   - REMEDY: Revoke in Google Cloud Console; consolidate to OS keychain; delete gogcli copy

3. **Stale State-Snapshot .env with Live Keys** (REPEAT — now explicitly checked)
   - ~/.hermes/state-snapshots/20260515-194826-pre-update/.env (440 bytes, 644)
   - Contains partially-masked but extractable API keys
   - REMEDY: Delete state-snapshot .env or rotate all keys

4. **Duplicate .env Store (stale)** (REPEAT — 10th+ consecutive audit, CHRONIC)
   - ~/.openclaw/.env (288 bytes, 644) — different TELEGRAM_BOT_TOKEN (835929... vs 827724...)
   - REMEDY: Delete ~/.openclaw/.env after confirming 827724 token is active

5. **WhatsApp Session Credentials World-Readable** (REPEAT — 10th+ consecutive audit, CHRONIC)
   - ~/.hermes/whatsapp/session/creds.json (2955 bytes, 644)
   - REMEDY: Restrict to owner-only access

### HIGH
6. **GOG OAuth Credentials in Plaintext** (REPEAT — 10th+ consecutive audit, CHRONIC)
   - ~/AppData/Roaming/gogcli/credentials.json
   - REMEDY: Revoke in Google Cloud Console; move to OS keychain

7. **No SSH Keys Configured** (REPEAT — informational)
   - ~/.ssh/ has only known_hosts — no private keys

### MEDIUM
8. **send_audit.py with Token Extraction Logic** (REPEAT — leftover)
   - ~/.hermes/send_audit.py — contains hardcoded stale report from May 12
   - REMEDY: Delete after confirming it's a leftover

## PASS Items
- Channel integrity: 16 Telegram channels/topics registered, all known
- Gateway state: Telegram connected, WhatsApp connected
- redact_secrets: true
- Desktop .env deleted (remediated since May 14)
- .env backup files deleted (remediated since May 14)
- .gitconfig clean
- AGENTS.md BOM: detected, Hermes platform blocks loading

## Platform States
- Telegram: connected
- WhatsApp: connected
- No regressions

## Delta from Previous Audit (2026-05-16 12:04 UTC)
- PERSISTING: All 8 FAIL items remain unresolved
- NEW: State-snapshot .env explicitly checked and flagged
- No new remediation since May 14 burst

## Notes
- ⚠️ REMEDIATION FATIGUE: 8 FAIL items unresolved for 10+ consecutive audits
- No improvement since first audit on 2026-05-12
