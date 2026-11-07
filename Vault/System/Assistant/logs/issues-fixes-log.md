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

## 2026-11-06 | Friday Matthias Logistics Check-in Not Delivered (WA Bridge Down)

- **Symptom**: Friday 20:00 UTC cron logistics check-in to Matthias (+233 54 489 8392) could not be sent.
- **Root Cause**: WhatsApp Baileys bridge on `localhost:3000` has no active LISTENER (HTTP 000; only stale TIME_WAIT sockets on the port).
- **Fix**: HUMAN REQUIRED — restart the Baileys bridge (session under default profile, `AppData/Local/hermes/whatsapp/session`). Re-send the check-in once up, or send manually.
- **Escalation**: Posted to Telegram chat `-1003784520976` Topic 2 (msg 13108). NOTE: Topic 141 (#urgent) no longer resolves ("message thread not found") — urgent routing to 141 must be corrected/re-created.
- **Status**: BRIDGE DOWN — check-in NOT DELIVERED (needs re-send).

---

- **Symptom**: Background backup process killed (SIGTERM, exit -15).
- **Command**: `chmod +x .../backup_system.sh && backup_system.sh`
- **Root Cause**: Process exceeded allowed runtime/memory or external kill signal.
- **Fix**: Investigate backup script duration/output; rerun if needed or add timeout/logging.
- **Status**: Open (needs investigation).

---

*No other entries yet.*
