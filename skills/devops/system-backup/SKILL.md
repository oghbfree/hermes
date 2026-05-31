---
name: system-backup
description: "Backup and verify critical Hermes Agent workspace files — config, databases, skills, cron jobs, memory files, and session data. Use when running scheduled cron backups, on-demand backup, or before major system changes (updates, migrations). Handles both Windows and POSIX path environments correctly."
---

# System Backup

Backup critical `.hermes` workspace files to a dated local backup directory with integrity verification.

## When to Use

- Scheduled cron backup jobs
- Before system updates or migrations
- On-demand "back up my workspace" requests

## Source and Destination

| | Path |
|---|---|
| **Source** | `C:/Users/User/.hermes/` (native Windows) or `/c/Users/User/.hermes/` (MSYS terminal only) |
| **Destination** | `C:/Users/User/hermes-backup/YYYY-MM-DD/` (use today's date) |

## Critical Path Rule — execute_code vs terminal

**This is the #1 pitfall.** The `execute_code` Python sandbox uses **native Windows paths** (`C:/Users/User/...`). The `terminal` tool uses **MSYS/POSIX paths** (`/c/Users/User/...`). They are NOT interchangeable.

When running backup Python scripts via `execute_code`:
- ✅ Use `C:/Users/User/.hermes/config.yaml`
- ❌ Do NOT use `/c/Users/User/.hermes/config.yaml` (returns False from `os.path.exists()`)

When checking files via `terminal`:
- ✅ Use `/c/Users/User/.hermes/config.yaml`
- ❌ Do NOT use `C:/Users/User/.hermes/config.yaml` (bash doesn't recognise it)

## File Selection

### Always include

| Category | Files | Notes |
|---|---|---|
| Config | `config.yaml`, `.env`, `.hermes_history` | Core configuration |
| Identity | `SOUL.md`, `auth.json`, `google_token.json` | Auth & identity |
| State | `state.db`, `memory_store.db`, `kanban.db` | Main DB files only (see exclusions below) |
| Sessions | `sessions/sessions.json` | Session index (not individual `.jsonl` files unless specifically requested) |
| Memory | `memories/` directory | MEMORY.md, USER.md, insights/, security/ |
| Skills | `skills/` directory | All SKILL.md, DESCRIPTION.md, reference files |
| Cron | `cron/jobs.json` | Job definitions |
| Channels | `channel_directory.json`, `gateway_state.json` | Platform routing state |

### Always exclude

| Pattern | Reason |
|---|---|
| `*.db-wal`, `*.db-shm` | Transient SQLite journal files — will corrupt backup if copied live |
| `*.lock` | Lock files are transient |
| `.archive/` directories | Already-archived content |

### Large directories to skip in walk

When walking `skills/`, skip: `.git`, `__pycache__`, `node_modules`, `.venv`, `.hub`, `.curator_backups`

## Procedure

1. **Create dated backup directory**: `C:/Users/User/hermes-backup/YYYY-MM-DD/{config,memory,skills,cron,sessions,state}`
2. **Copy files** using `shutil.copy2()` (preserves metadata)
3. **Verify integrity**: Compute SHA-256 of each source file and its destination copy; check they match
4. **Generate report**: Write `backup-report.txt` and `manifest.json` to the backup directory

## Verification

After copying, verify:
- SHA-256 checksums match for every file
- No files are 0 bytes (unless the source was also 0 bytes)
- Report any mismatches or missing files explicitly in the output

## Output

Always produce a structured report with:
- Timestamp (UTC)
- File count and total bytes
- Per-file listing with sizes
- List of any errors or hash mismatches
- Final SUMMARY line with STATUS

## References

- [references/path-mapping.md](references/path-mapping.md) — detailed path mapping reference with proof, examples, and sandbox details

## Example

```python
# Typical execute_code backup script structure
import os, hashlib, shutil, json, time

SOURCE = "C:/Users/User/.hermes"  # Windows native path for execute_code
BACKUP = "C:/Users/User/hermes-backup/2026-05-27"

def sha256(f):
    h = hashlib.sha256()
    with open(f, 'rb') as fh:
        for chunk in iter(lambda: fh.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()

def safe_copy(src, dst_dir, label=""):
    os.makedirs(dst_dir, exist_ok=True)
    dst = os.path.join(dst_dir, os.path.basename(src))
    shutil.copy2(src, dst)
    assert sha256(src) == sha256(dst), f"Hash mismatch: {src}"
```

## Pitfalls

- **Plaintext credentials in backups**: `.env`, `google_client_secret.json`, `google_token.json`, and `auth.json` contain full API keys and OAuth tokens. Backing them up to an unencrypted local directory **expands the attack surface**. After Bitwarden migration (see `hermes-security-audit` §1h-2), these files will no longer contain plaintext secrets. Until then, either (a) exclude them from backups, (b) encrypt the backup directory, or (c) accept the risk and rotate keys regularly. **Do NOT copy them to any cloud-synced folder.**
- **Wrong path style in execute_code**: Using `/c/Users/...` instead of `C:/Users/...` causes `os.path.exists()` to return `False` silently. Every file will appear to "not exist" and the backup will report 0 files.
- **Including WAL/SHM files**: SQLite WAL files are copy-inconsistent without a checkpoint. Exclude them.
- **Walking too many files**: The skills directory can have 100+ entries. Cap the walk with `max_files=80` to keep execution within sandbox limits.
- **Heredoc + `&` in terminal**: Multi-line strings with `&` in `terminal()` heredocs trigger the "foreground command uses backgrounding &" error. Use `execute_code` instead for Python scripts.
