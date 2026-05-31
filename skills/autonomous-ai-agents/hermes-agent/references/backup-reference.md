# Hermes Agent Backup Reference

## Full Backup Script (Bash / git-bash on Windows)

Run this from a terminal to perform a complete backup of Hermes critical files:

```bash
#!/bin/bash
# hermes-backup.sh — Full backup of Hermes Agent critical files
# Works on Linux, macOS, and Windows (git-bash / MSYS)

set -euo pipefail

BACKUP_BASE="${HOME}/.hermes/backups"
TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
BACKUP_DIR="${BACKUP_BASE}/${TIMESTAMP}"
SRC="${HOME}/.hermes"

echo "=== Hermes Agent Backup: ${TIMESTAMP} ==="
echo ""

# Create directory structure
mkdir -p "${BACKUP_DIR}"/{config,memories,skills,workspace,cron,state}

# --- Config files ---
echo "[1/6] Copying config files..."
cp "${SRC}/config.yaml" "${BACKUP_DIR}/config/" 2>/dev/null || echo "  SKIP: config.yaml"
cp "${SRC}/.env" "${BACKUP_DIR}/config/" 2>/dev/null || echo "  SKIP: .env"
cp "${SRC}/auth.json" "${BACKUP_DIR}/config/" 2>/dev/null || echo "  SKIP: auth.json"
cp "${SRC}/channel_directory.json" "${BACKUP_DIR}/config/" 2>/dev/null || true
cp "${SRC}/gateway_state.json" "${BACKUP_DIR}/config/" 2>/dev/null || true
cp "${SRC}/processes.json" "${BACKUP_DIR}/config/" 2>/dev/null || true
cp "${SRC}/SOUL.md" "${BACKUP_DIR}/config/" 2>/dev/null || true

# --- Memories ---
echo "[2/6] Copying memories..."
cp "${SRC}/memories/"*.md "${BACKUP_DIR}/memories/" 2>/dev/null || true
cp -r "${SRC}/memories/security" "${BACKUP_DIR}/memories/" 2>/dev/null || true

# --- Cron ---
echo "[3/6] Copying cron jobs..."
cp "${SRC}/cron/jobs.json" "${BACKUP_DIR}/cron/" 2>/dev/null || true

# --- State ---
echo "[4/6] Copying state database..."
cp "${SRC}/state.db" "${BACKUP_DIR}/state/" 2>/dev/null || echo "  SKIP: state.db"

# --- Workspace key files ---
echo "[5/6] Copying workspace files..."
WS="${SRC}/workspace"
for f in AGENTS.md SOUL.md IDENTITY.md TASKS.md tasks-queue.md TOOLS.md CONTACTS.md PROPERTY_PROJECT_SYSTEM.md; do
  cp "${WS}/${f}" "${BACKUP_DIR}/workspace/" 2>/dev/null || true
done
cp -r "${WS}/.archive" "${BACKUP_DIR}/workspace/" 2>/dev/null || true
cp -r "${WS}/memories" "${BACKUP_DIR}/workspace/" 2>/dev/null || true

# --- Skills ---
echo "[6/6] Copying user skills..."
cp -r "${SRC}/skills" "${BACKUP_DIR}/" 2>/dev/null || true

# --- Manifest ---
echo ""
echo "Writing manifest..."
cat > "${BACKUP_DIR}/MANIFEST.txt" << EOF
BACKUP MANIFEST
===============
Date: $(date -u +%Y-%m-%d\ %H:%M:%S\ UTC)
Location: ${BACKUP_DIR}

CONTENTS:
  config/       - Config files (config.yaml, .env, auth.json, etc.)
  memories/     - MEMORY.md, USER.md, security audits
  cron/         - jobs.json (all scheduled jobs)
  state/        - state.db (point-in-time snapshot)
  workspace/    - AGENTS.md, SOUL.md, tasks, archives
  skills/       - User custom skills

TOTAL: $(find "${BACKUP_DIR}" -type f | wc -l) files
SIZE: $(du -sh "${BACKUP_DIR}" 2>/dev/null | awk '{print $1}')
EOF

# --- Integrity check ---
echo ""
echo "=== Integrity Check ==="
ERRORS=0
for f in config.yaml .env auth.json channel_directory.json SOUL.md; do
  ORIG="${SRC}/${f}"
  BAK="${BACKUP_DIR}/config/${f}"
  if [ -f "${ORIG}" ] && [ -f "${BAK}" ]; then
    ORIG_HASH=$(md5sum "${ORIG}" 2>/dev/null | awk '{print $1}')
    BAK_HASH=$(md5sum "${BAK}" 2>/dev/null | awk '{print $1}')
    if [ "${ORIG_HASH}" = "${BAK_HASH}" ]; then
      echo "  OK: ${f}"
    else
      echo "  MISMATCH: ${f}"
      ERRORS=$((ERRORS + 1))
    fi
  fi
done

# state.db expected mismatch if gateway running
if [ -f "${SRC}/state.db-wal" ] && [ $(stat -c%s "${SRC}/state.db-wal}" 2>/dev/null || echo 0) -gt 0 ]; then
  echo "  NOTE: state.db WAL active — checksum mismatch expected (this is OK)"
fi

echo ""
if [ $ERRORS -eq 0 ]; then
  echo "=== BACKUP COMPLETE — All checks passed ==="
else
  echo "=== BACKUP COMPLETE — ${ERRORS} integrity warning(s) ==="
fi
echo "Location: ${BACKUP_DIR}"
echo "Size: $(du -sh "${BACKUP_DIR}" 2>/dev/null | awk '{print $1}')"
echo "Files: $(find "${BACKUP_DIR}" -type f | wc -l)"
```

## Cron Job for Automated Backups

Create a nightly backup cron job via the `cronjob` tool:

```
action: create
name: nightly-hermes-backup
schedule: "0 23 * * *"
prompt: "Run system backup. Duplicate all critical workspace and memory files to the local backup directory. Verify integrity. Report backup status including file counts and any errors."
```

## Restoration

To restore from a backup:

```bash
# Stop gateway first
hermes gateway stop

# Restore config
cp ~/.hermes/backups/<timestamp>/config/config.yaml ~/.hermes/
cp ~/.hermes/backups/<timestamp>/config/.env ~/.hermes/

# Restore state
cp ~/.hermes/backups/<timestamp>/state/state.db ~/.hermes/

# Restore workspace
cp ~/.hermes/backups/<timestamp>/workspace/AGENTS.md ~/.hermes/workspace/

# Restart gateway
hermes gateway start
```

**Important:** Always stop the gateway before restoring `state.db` to avoid corruption.
