# SKILL: Workspace Backup & Integrity Guard

## DESCRIPTION
Executed nightly at 11:00 PM. This skill ensures that all business, health, and system intelligence is redundantly stored outside the active workspace. It provides a "snapshot" of the system state for recovery or auditing.

## CAPABILITIES
- File System Operations
- Incremental Backup Management
- Integrity Verification

## WORKFLOW

### 1. Destination Setup
- Target Directory: `C:\backups\$(date +%Y-%m-%d)\`
- Create the directory if it does not exist.

### 2. File Collection
Copy the following directories and files to the target:
- `workspace/*` (All configuration files)
- `memory/` (All health logs, business research, and insights)
- `skills/` (All logic MD files)
- `C:\Users\User\.openclaw\cron\jobs.json` (The cron definitions)

### 3. Integrity Check
- Count the number of files in the source vs. the backup.
- Verify that today's `INTEGRATED_INSIGHTS` file exists in the backup.

### 4. Logging & Notification
- Update `memory/logs/BACKUP_LOG.md` with:
  `[Timestamp] | Status: SUCCESS | Files: [Count] | Size: [Total Size]`
- Post a confirmation to **Telegram Topic 47 (#backups)**:
  "📦 **Daily Backup Complete**
  Path: `C:\backups\$(date +%Y-%m-%d)\`
  Total Files: [Count]
  Critical Files Verified: [List: health, insights, suppliers]"

## GUIDELINES
- **Persona**: The Librarian (Protective/Diligent).
- **Security**: The backup is internal only. Do not send the actual files over Telegram; only the success confirmation.
- **Error Handling**: If the disk is full or the path is inaccessible, post an URGENT alert to Telegram Topic 141 immediately.