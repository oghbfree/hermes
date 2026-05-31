---
name: business-operations-tracking
description: "Track and manage business operations pipelines — recruitment (job applications in Google Sheets) and supplier outreach (procurement research files, WhatsApp inquiry delivery). Use when checking pipeline status, detecting new entries since last check, preparing outreach messages, or posting status reports to Telegram. Both sub-pipeline skills have been consolidated into this umbrella."
version: 1.0.0
---

# Business Operations Tracking

Track and manage business operations pipelines using file-based state, cron-driven differential checks, and Telegram delivery.

## Sub-Pipelines

| Pipeline | Domain | Data Source | Delivery |
|----------|--------|-------------|----------|
| `recruitment` | Job applications via Google Sheets | Google Sheets API | Telegram topic 20 |
| `supplier` | Supplier research + WhatsApp outreach | GHANA_SUPPLIER_RESEARCH.md | Telegram procurement topic |

Each pipeline has its own detailed reference file with workflow, data schemas, and domain specifics.

## Shared Pattern

Both pipelines follow the same operational pattern:

1. **Read state file** — Load last-check JSON to know what's been processed
2. **Read data source** — Google Sheets or markdown research file
3. **Detect changes** — New rows, status changes since last check
4. **Prepare actions** — Filter/rank candidates or prepare inquiry messages
5. **Update state file** — Write back new checkpoint
6. **Deliver report** — Post structured summary to configured Telegram target

## Shared Pitfalls

- **File paths change across migrations.** Always verify paths with `find` if primary location returns empty.
- **Cron jobs may deliver to wrong channel.** Always verify the `deliver` field points to the correct Telegram chat/topic.
- **WhatsApp bridge may be offline.** When offline, still prepare and update files — just flag as undeliverable.
- **Memory tool may be unavailable in cron sessions.** Use file-based persistence only.
- **`patch` tool for markdown tables.** Always include enough unique context in `old_string` to avoid non-unique matches.

## Related Skills

- `daily-operations-synthesis` — cross-domain daily briefing that includes business operations status
- `google-workspace` — Google Sheets API auth and CLI commands (used by recruitment pipeline)
- `elder-care-operations` — health check-in templates (also uses cron + file-based tracking)

## Reference Files

- `references/recruitment-tracking.md` — Full recruitment pipeline: sheet IDs, column mappings, candidate ranking criteria, state file schema, report template, known blockers
- `references/supplier-outreach-tracking.md` — Full supplier pipeline: research file format, inquiry templates, WhatsApp bridge checks, status table format, key suppliers
