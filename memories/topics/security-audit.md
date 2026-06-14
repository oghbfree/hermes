# Security Audit Summary

## Latest: 2026-05-29

**6 FAIL / 11 WARN / rest PASS**

### FAIL Items
1. Request dumps (164 files)
2. Dual Telegram bot tokens
3. Backup credential leakage
4. PII redaction disabled
5. Firecrawl key leaked in gateway.log
6. 3 failed cron jobs

### WARN Items
- FAL_KEY duplicate
- Google OAuth expired
- send_audit.py bypass
- AGENTS.md BOM (U+FEFF)
- State.db growth
- WhatsApp unpaired

### Status
**Zero remediation of findings since May 15.**

## Audit Files

- `memories/security/SECURITY_AUDIT_2026-05-29.md` (latest)
- `memories/security/SECURITY_AUDIT_2026-05-28.md`
- `memories/security/SECURITY_AUDIT_2026-05-25.md`
- `memories/security/SECURITY_AUDIT_2026-05-20.md`
- `memories/security/SECURITY_AUDIT_2026-05-19.md`

## Related

- See also: [[backup-status]], [[cron-status]]
