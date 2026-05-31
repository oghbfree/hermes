# Skill Update Notes — 2026-05-28

**Source session:** nightly-consolidation (03:00 May 28, 2026)
**Trigger:** Observed patterns and gaps during daily processing run

## New Pitfalls to Embed

These should be folded into the main SKILL.md pitfalls list during the next manual edit (the patch tool has char-encoding issues with this file on disk):

### Security Audit Persistence Gap
The security-policy-check cron (every 6h) writes audit files to `~/.hermes/memories/security/` (global) but NOT to `~/.hermes/workspace/memories/security/` (workspace). During synthesis or consolidation, always check both paths. If the audit exists in global but not workspace, copy it to workspace. If neither path has today's audit, reconstruct it from `~/.hermes/cron/output/73f447bae072/YYYY-MM-DD_*.md`. This has been a recurring gap — audits from May 26, 27, and 28 were all missing from workspace until the nightly consolidation manually saved them.

### Background Tool Restrictions Limit Audit Depth
The security-policy-check cron may run with `read_file`, `write_file`, `patch`, and `execute_code` blocked ("Background review denied non-whitelisted tool"). When this happens, the audit completes with tool workarounds but may have missed file-based checks. If the audit report notes tool denials, flag that audit depth was reduced. The audit may still produce valid findings from log files it can access via `terminal` or `execute_code`.

### Security Audit File Path in Data Sources Section
The SKILL.md Data Sources section 4 says: "`~/.hermes/memories/security/SECURITY_AUDIT_YYYY-MM-DD.md` (today's — note: security cron writes to `~/.hermes/memories/security/`, NOT `workspace/memories/security/`)". This is correct but incomplete — the synthesis/consolidation should ALSO check `workspace/memories/security/` since that's where it expects to find files. Update this note to say: check BOTH paths, prefer workspace, fall back to global, reconstruct from cron output if neither exists.
