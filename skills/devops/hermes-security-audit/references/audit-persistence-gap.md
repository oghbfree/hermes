# Security Audit Persistence Gap — 2026-05-28

## Issue

The security-policy-check cron job (every 6h, job ID `73f447bae072`) generates audit reports and delivers them to Telegram, but the audit file is NOT reliably saved to `workspace/memories/security/`. 

## Root Cause

The cron writes to `~/.hermes/memories/security/` (global path) but the synthesis/consolidation jobs look in `~/.hermes/workspace/memories/security/` (workspace path). Additionally, background tool restrictions may block `write_file` during the audit, preventing the file from being saved at all.

## Evidence

- May 26 audit: Not in workspace (only in cron output)
- May 27 audit: Not in workspace (only in cron output)  
- May 28 audit: Not in workspace until nightly consolidation manually saved it
- Last workspace audit before May 28: SECURITY_AUDIT_2026-05-25.md

## Fix

During nightly consolidation (03:00), always:
1. Check `workspace/memories/security/SECURITY_AUDIT_YYYY-MM-DD.md` exists
2. If not, check `~/.hermes/memories/security/SECURITY_AUDIT_YYYY-MM-DD.md`
3. If found in global but not workspace, copy to workspace
4. If neither exists, reconstruct from `~/.hermes/cron/output/73f447bae072/YYYY-MM-DD_*.md`

## Long-Term Fix Needed

Either:
- Fix the security-policy-check cron to write to BOTH paths, OR
- Add a post-audit step that copies the file to workspace, OR
- Have the cron save to workspace directly (the path it should use)
