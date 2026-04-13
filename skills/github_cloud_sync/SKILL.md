# SKILL: GitHub Cloud Memory Sync

## DESCRIPTION
Executed weekly on Sundays at 23:00. This skill pushes the system's "State" and "Memory" to a private GitHub repository, ensuring encrypted off-site redundancy for all critical business and health logic.

## CAPABILITIES
- Version Control Management
- Cloud Redundancy
- Change-set Verification

## WORKFLOW

### 1. Repository Preparation
- Access the root directory of the OpenClaw workspace.
- Run `git status` to verify the repository is initialized and the remote is set.

### 2. Staging & Committing
- **Stage**: `git add memory/` `git add workspace/` `git add skills/` `git add LEARNING_SYSTEM.md`.
- **Note**: Ensure `.gitignore` is correctly configured to exclude sensitive API keys or large `\tmp\` logs.
- **Commit**: Execute `git commit -m "Weekly memory backup $(date +%F)"`.

### 3. Remote Push
- Execute `git push origin main` (or your active branch).
- **Authentication**: Ensure the machine has a stored Personal Access Token (PAT) or SSH key to avoid prompt-blocking the cron.

### 4. Logging & Verification
1. **Verify**: Check the return code of the push command.
2. **Log**: Update `memory/logs/BACKUP_LOG.md` with the GitHub commit hash.
3. **Notify**: Post to **Telegram Topic 2 (#cron-status)**:
   "☁️ **GitHub Sync Successful**
   - Commit: `Weekly memory backup $(date +%F)`
   - Scope: Memory, Workspace, Skills
   - Status: Remote Synchronized"

## GUIDELINES
- **Persona**: The Librarian (Security/Archivist mode).
- **Security**: Never push raw logs that haven't been audited by the `security-watchdog` skill.
- **Error Handling**: 
    - If a merge conflict or authentication error occurs, log it as **CRITICAL**.
    - Notify Telegram Topic 141 (#urgent): "🚨 GITHUB SYNC FAILED: [Error Detail]. Manual intervention required."