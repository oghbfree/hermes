#!/usr/bin/env python3
"""
Backup Verification Script
===========================
Run this after copying files to verify SHA256 integrity.
Detects the "live file" problem and re-copies mismatched files.

Usage: python3 scripts/verify-backup.py
"""

import os, hashlib, shutil, json, sys
from datetime import datetime


HERMES = os.path.expanduser("~/.hermes")
DATE_TAG = datetime.now().strftime("%Y-%m-%d")
BACKUP = os.path.expanduser(f"~/hermes-backup/{DATE_TAG}")

# Source → backup path mapping
FILE_MAP = {
    "memories/MEMORY.md": "memories/MEMORY.md",
    "memories/USER.md": "memories/USER.md",
    "config.yaml": "config/config.yaml",
    "auth.json": "config/auth.json",
    "contacts.json": "config/contacts.json",
    "CONTACTS.md": "config/CONTACTS.md",
    "SOUL.md": "config/SOUL.md",
    "channel_directory.json": "config/channel_directory.json",
    "cron/jobs.json": "cron/jobs.json",
    "state.db": "state/state.db",
    "kanban.db": "state/kanban.db",
    "gateway_state.json": "state/gateway_state.json",
}

DIR_MAP = ["skills", "sessions", "logs"]


def sha256_file(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def verify_copy(src, dst):
    """Copy src→dst, verify SHA256, return True if match."""
    shutil.copy2(src, dst)
    return sha256_file(src) == sha256_file(dst)


def verify():
    if not os.path.exists(BACKUP):
        print(f"❌ Backup directory not found: {BACKUP}")
        return False

    all_pass = True
    re_copied = []

    # Verify individual files
    for src_rel, dst_rel in FILE_MAP.items():
        src = os.path.join(HERMES, src_rel)
        dst = os.path.join(BACKUP, dst_rel)

        if not os.path.exists(src):
            print(f"⚠️  {src_rel:42s} SOURCE MISSING")
            continue
        if not os.path.exists(dst):
            print(f"🔴 {src_rel:42s} BACKUP MISSING")
            all_pass = False
            continue

        sha_src = sha256_file(src)
        sha_dst = sha256_file(dst)
        size = os.path.getsize(src)

        if sha_src == sha_dst:
            print(f"✅ {src_rel:42s} {size:>8,} bytes")
        else:
            # Re-copy and re-verify
            if verify_copy(src, dst):
                print(f"♻️  {src_rel:42s} {size:>8,} bytes (re-copied, PASS)")
                re_copied.append(src_rel)
            else:
                print(f"🔴 {src_rel:42s} FAIL after re-copy")
                all_pass = False

    # Verify directories
    for name in DIR_MAP:
        src = os.path.join(HERMES, name)
        dst = os.path.join(BACKUP, name)
        if not os.path.exists(src) or not os.path.exists(dst):
            print(f"🔴 {name}/: MISSING")
            all_pass = False
            continue

        src_files = set()
        for root, dirs, files in os.walk(src):
            for f in files:
                rel = os.path.relpath(os.path.join(root, f), src)
                src_files.add(rel)

        dst_files = set()
        for root, dirs, files in os.walk(dst):
            for f in files:
                rel = os.path.relpath(os.path.join(root, f), dst)
                dst_files.add(rel)

        if src_files != dst_files:
            missing = src_files - dst_files
            extra = dst_files - src_files
            print(f"🔴 {name}/: FILE MISMATCH (missing={len(missing)}, extra={len(extra)})")
            all_pass = False
            continue

        failures = []
        re_copied_dir = []
        for f in src_files:
            sf = os.path.join(src, f)
            df = os.path.join(dst, f)
            if sha256_file(sf) != sha256_file(df):
                if verify_copy(sf, df):
                    re_copied_dir.append(f)
                else:
                    failures.append(f)

        if failures:
            print(f"🔴 {name}/: {len(failures)}/{len(src_files)} files FAIL after re-copy")
            all_pass = False
        else:
            extra = f" ({len(re_copied_dir)} re-copied)" if re_copied_dir else ""
            print(f"✅ {name}/: {len(src_files)} files, all checksums match{extra}")

    # Summary
    print()
    if all_pass:
        print(f"✅ ALL CHECKS PASSED ({len(re_copied)} files re-copied)")
    else:
        print(f"🔴 INTEGRITY ISSUES REMAIN")

    # Save manifest
    manifest = {
        "backup_date": DATE_TAG,
        "backup_path": BACKUP,
        "verified_at": datetime.now().isoformat(),
        "all_checksums_pass": all_pass,
        "files_re_copied": re_copied,
    }
    manifest_path = os.path.join(BACKUP, "backup_manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"Manifest: {manifest_path}")

    return all_pass


if __name__ == "__main__":
    success = verify()
    sys.exit(0 if success else 1)