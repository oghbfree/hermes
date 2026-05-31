# Real Backup Report — 2026-05-11

This is a production backup report from the daily-backup cron job. Shows the actual structure, file sizes, and the "live file re-copy" pattern in action.

## Initial Backup

The backup copied 7 categories of data to `~/hermes-backup/2026-05-11/`:

| Category  | Files | Size  |
|-----------|-------|-------|
| Memories  | 2     | 2.7 KB |
| Config    | 7     | 31 KB  |
| State     | 3     | 7.9 MB |
| Cron      | 1     | 36 KB  |
| Skills    | 540   | 7.3 MB |
| Sessions  | 31    | 7.4 MB |
| Logs      | 6     | ~500 KB |

## Verification Results (First Pass)

After the initial copy, SHA256 verification showed 3 failures — all "live" files that changed during the backup:

```
🔴 state.db — 7,839,744 bytes — FAIL (SHA256 mismatch)
🔴 sessions/session_cron_c2d685f3b8e5_20260511_230320.json — FAIL (live session log being appended)
🔴 logs/agent.log — FAIL (append-only log being written)
🔴 logs/errors.log — FAIL (append-only log being written)
```

## Re-copy and Final Verification

The 4 failing files were re-copied and re-verified. All passed on second attempt:

```
✅ state.db — 7,839,744 bytes (re-verified)
✅ sessions/session_cron_c2d685f3b8e5_20260511_230320.json — 198,595 bytes (re-verified)
✅ logs/agent.log — 477,978 bytes (re-verified)
✅ logs/errors.log — 115,706 bytes (re-verified)
```

## Final Results

```
✅ FINAL STATUS: ALL 15 checks PASSED
Total data: 21.6 MB (589 files)
Backup location: C:\Users\User/hermes-backup/2026-05-11
```

## Key Takeaway

The re-copy pattern is essential. Without it, the initial verification will always show false failures for `state.db`, current session, and streaming logs. These are not corruption — they are files that legitimately changed in the ~2-3 seconds between file copy and checksum calculation.