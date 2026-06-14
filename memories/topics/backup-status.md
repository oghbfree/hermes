# Backup Status

## Latest

- **2026-06-08:** SUCCESS — 743 files, ~348 MB, all SHA-256 verified ✅
- **Previous good:** 2026-06-06 — 743 files, ~348 MB
- **Stale since:** Current (backup is fresh)

## Backup Inventory

| Date | Size | Status |
|------|------|--------|
| 2026-05-27 | 521 MB | ⚠️ Exceeds 7-day retention |
| 2026-06-01 | 300 MB | ⚠️ Exceeds 7-day retention |
| 2026-06-03 | 320 MB | ⚠️ Exceeds 7-day retention |
| 2026-06-04 | 337 MB | ✅ Within retention |
| 2026-06-06 | 348 MB | ✅ Within retention |
| 2026-06-08 | 348 MB | ✅ Within retention (latest) |

**Total backup storage:** ~2.2 GB across 6 snapshots
**Recommendation:** Prune 2026-05-27, 2026-06-01, 2026-06-03 (older than 7 days)

## Credential Warning

All backups contain unencrypted credentials (`.env`, `google_token.json`, `auth.json`). This is an expanded attack surface. See `memories/security/SECURITY_AUDIT_2026-06-08.md` §FAIL-1.

## Related

- See also: [[cron-status]], [[security-audit]]
