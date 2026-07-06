# Issues & Fixes Log

Append-only record of system issues, technical failures, and their resolutions.

Format: Symptom → Root Cause → Fix → Status

---

## 2026-05-23 | Ghana WhatsApp Gateway Down

- **Symptom**: No supplier WhatsApp messages delivered; inquiries queued.
- **Root Cause**: OpenClaw gateway on port 18789 unreachable since 2026-05-23.
- **Fix**: Restoration of OpenClaw gateway required. Auto-trigger bulk-send of queued supplier inquiries once restored.
- **Status**: DOWN (60+ days as of 2026-06-23).

## 2026-06-23 | state.db Locked by Old Gateway Process

- **Symptom**: `C:\Users\User\AppData\Local\hermes\state.db` (198MB) locked and undeletable.
- **Root Cause**: Old Hermes gateway process still holding file lock.
- **Fix**: Close Hermes desktop app, then manually delete `state.db`, `state.db-shm`, `state.db-wal`.
- **Status**: Resolved (manual cleanup pending).

## 2026-06-23 | System Backup Process Terminated

- **Symptom**: Background backup process killed (SIGTERM, exit -15).
- **Command**: `chmod +x .../backup_system.sh && backup_system.sh`
- **Root Cause**: Process exceeded allowed runtime/memory or external kill signal.
- **Fix**: Investigate backup script duration/output; rerun if needed or add timeout/logging.
- **Status**: Open (needs investigation).

---

*No other entries yet.*
