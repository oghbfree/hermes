# Assistant — Environment & Technical Setup

Hardware, tools, quirks, and gotchas. Read when troubleshooting or configuring.

---

## Hardware

- Primary: Windows 10 (Hermes desktop GUI)
- Python: 3.11.15 (system), pip→python3.14, uv installed.

## Services

- **Hermes Desktop** — active profile `default`.
- **OpenClaw WhatsApp Gateway** — expected on port 18789. **DOWN since 2026-05-23**.
- **Obsidian** — vault at `Vault/`.

## Key Paths

| Resource | Path |
|----------|------|
| Vault root | `C:\Users\User\.hermes\workspace\Vault` |
| Daily notes | `Vault/Daily/YYYY-MM-DD.md` |
| System assistant files | `Vault/System/Assistant/` |
| Hermes hot memory | `C:\Users\User\.hermes\memories\MEMORY.md` |
| Hermes user profile | `C:\Users\User\.hermes\memories\USER.md` |
| Hermes state DB | `C:\Users\User\AppData\Local\hermes\state.db` (locked when Hermes desktop runs) |
| Content assets | `Vault/business/Content/content-assets/` |

## Known Issues & Patterns

- **WhatsApp Gateway Down** — OpenClaw on 18789 unavailable since 2026-05-23. All Ghana supplier outreach queued, not delivered. Restoration is #1 blocker.
- **state.db Lock** — `state.db` locked by old gateway process when Hermes desktop is running. Must close Hermes desktop before deleting `state.db`, `state.db-shm`, `state.db-wal`.
- **Hermes Audit Retention** — Security audits max 7 days, then delete. Same-outcome duplicates can be deleted immediately.
- **Backup Pointer** — Daily backup `latest` pointer is a directory (symlink repair failed on Windows/MSYS). Use the dated backup folder directly.
- **Model Fallback** — Active: `openrouter/owl-alpha`. Fallback: `openrouter/qwen/qwen-turbo`.

## Troubleshooting Steps

1. Gateway down: restart OpenClaw service, verify port 18789 open.
2. state.db lock: close Hermes desktop → delete `state.db` + shm/wal → restart Hermes.
3. Missing daily note: create with frontmatter + sections per vault rules.
4. Orphaned notes: check graph view, add wiki-links from relevant daily notes or MOCs.

---

*Last updated: 2026-06-23*
