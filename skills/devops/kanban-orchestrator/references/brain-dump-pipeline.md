# Brain-Dump → Kanban Pipeline Reference

## Pattern: Telegram Topic → tasks-queue.md → Kanban Board

This is the standard pipeline for turning unstructured brain dumps into executable Kanban tasks.

### Architecture

```
Telegram Topic (brain dump, voice notes, fragmented thoughts)
        ↓  (cron: 3x daily — 8AM, 6PM, midnight)
brain-dump-parser cron
  - Scans session history for new dumps
  - Extracts structured tasks (title, project, priority, due_date, flags)
  - Appends to tasks-queue.md under ## Active
        ↓  (cron: daily 9AM)
tasks-queue-sync cron
  - Reads tasks-queue.md
  - Compares with `hermes kanban list`
  - Creates new kanban cards for [ ] items
  - Marks cards done for [x] items
        ↓  (cron: daily 10AM)
tasks-md-to-kanban cron (optional, for TASKS.md master list)
  - Syncs TASKS.md → Kanban as backup/authoritative source
        ↓
Kanban dispatcher picks up ready tasks automatically
```

### Task Extraction Format (tasks-queue.md)

```markdown
## Active
* [ ] **[PROJECT] | [PRIORITY]** — Title
  → Notes: context, names, details
  → Due: date or "not specified"
  → Flag: [RESEARCH] / [DECISION] / [WAITING: name] / [REVIEW]

## Waiting On
* [ ] **[PROJECT] | [PRIORITY]** — Title
  → Waiting on: person name

## Backlog
* [ ] **[PROJECT] | [PRIORITY]** — Title

## Done
* [x] **[PROJECT] | [PRIORITY]** — Title
  → Completed: date
```

### Extraction Rules

1. Every distinct actionable item → one task
2. Title: verb phrase, under 10 words, starts with a verb
3. Project: akoma | jiji | construction | property | personal | finance | ghana-trip | family | business | tech | other
4. Priority: high / medium / low (infer from urgency language)
5. Due: extract if mentioned, otherwise null
6. Flags: [RESEARCH] needs looking into, [DECISION] needs a choice, [WAITING: name] blocked on someone, [REVIEW] unsure
7. Never drop anything — if unsure, include as [REVIEW]
8. Don't rewrite intent — preserve meaning, just structure it

### Cron Job Specs

**brain-dump-parser** (3x daily):
```
Schedule: 0 8,18,0 * * *
Prompt: Scan session history for new brain-dump messages in the configured topic.
       Extract tasks. Append to tasks-queue.md. Report what was extracted.
       If no new dumps: "No new brain dumps to process."
```

**tasks-queue-sync** (daily):
```
Schedule: 0 9 * * *
Prompt: Read tasks-queue.md. Compare with kanban board.
       Create new cards for [ ] items. Complete cards for [x] items.
       Report what changed.
```

**tasks-md-to-kanban** (daily, if TASKS.md exists):
```
Schedule: 0 10 * * *
Prompt: Read TASKS.md. Sync [ ] items to kanban, [x] items to done.
       Report what was synced.
```

### Master TASKS.md Format

For a clean master task list (separate from the queue/inbox):

```markdown
# TASKS.md — Master Task List

## 🇬🇭 Ghana Trip
- [ ] Book hotel for mum on arrival
- [ ] Arrange Plan B accommodation for mum

## 🏠 Property/Building
- [ ] Croydon — roof, windows
- [ ] Peckham — paint walls
```

Categories use emoji headers for visual scanning. Checkbox format for easy `[ ]` / `[x]` tracking.

### Pitfalls

- **Don't re-process old dumps.** Check the last extraction timestamp. Only process new messages.
- **Don't create duplicate cards.** Always `hermes kanban list` first, compare, then create only genuinely new items.
- **Don't skip the body field.** The body carries project context and notes — downstream workers need it.
- **Batch-create in groups of 5–6.** Larger batches risk timeout on the terminal tool.
- **The dispatcher needs the gateway.** If gateway isn't running, `ready` tasks never get picked up. Always verify `hermes gateway status` during setup.
