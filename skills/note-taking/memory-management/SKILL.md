---
name: memory-management
description: "Restructure and organize Hermes Agent memory files — split flat MEMORY.md into topic subdirectories, maintain a master index with status, distribute facts to relevant files, use wikilinks for cross-references. Use when H asks to 'tidy up memory', 'categorize memory', 'organize topics', or when MEMORY.md grows past ~2,200 chars and needs restructuring."
---

# Memory Management

Restructure flat memory dumps into a topic-based filesystem for fast context retrieval.

## When to Use

- H says "tidy up memory", "categorize memory", "organize topics", "split memory into files"
- MEMORY.md main file exceeds ~2,200 chars and contains multiple unrelated topics
- A session produces facts that belong in different domains (business, family, health, etc.)
- H asks "where do I find X" — answer should be a file path, not a flat list

## Architecture

```
.hermes/workspace/memories/
├── MEMORY.md              ← master INDEX only (not a dump)
├── MEMORY_ARCHIVE.md      ← overflow trimmed entries
├── USER.md                ← H's profile, preferences, contacts
├── business/              ← all business ops
│   ├── 2real/             ← SOPs, content pipeline, brand assets
│   ├── checkins/          ← staff check-in notes
│   ├── construction/      ← construction projects
│   └── farming/           ← farm operations
├── family/                ← family care
│   ├── AUTOBIOGRAPHY_COMFORT.md
│   └── FAMILY_INSIGHTS_DAD.md
├── health/                ← health tracking
│   ├── H/                 ← H's daily health logs
│   ├── mum/               ← mum's daily health logs
│   └── weekly/            ← weekly synthesis reports
├── jobs/                  ← recruitment pipeline
│   ├── APPLICATIONS-REPORT-*.md
│   └── RECRUITMENT_SUMMARY.md
├── people/                ← staff/contacts (John.md, Sammy.md, etc.)
├── procurement/           ← supplier research, shipping
├── security/              ← security audit reports
├── insights/              ← daily integrated synthesis reports
└── topics/                ← cross-cutting topics
    ├── whatsapp-status.md
    ├── ghana-move.md
    ├── finance.md
    ├── cron-status.md
    ├── backup-status.md
    ├── security-audit.md
    ├── property-project.md
    └── research-notes.md
```

## Principles

1. **MEMORY.md = index only.** Never dump facts here. List topics with status indicators and file paths.
2. **One fact, one home.** Each piece of information goes in exactly one topic file. Cross-reference with `[[wikilinks]]`.
3. **Sensitive data stays in root.** Financial debts, account numbers, and sensitive personal data stay in the root MEMORY.md (injected context) — not in topic files that might be synced or shared.
4. **Status indicators.** Use ✅ (current), ⚠️ (stale/gap), 🔴 (critical/outage) in the index table.
5. **Wikilinks for cross-references.** Use `[[topic-name]]` syntax — Obsidian-compatible if the workspace is opened as a vault.

## Procedure

### 1. Audit existing memory

Read the current MEMORY.md (both `.hermes/memories/MEMORY.md` and `.hermes/workspace/memories/MEMORY.md`). Identify distinct topics.

### 2. Map topics to directories

- Existing subdirectory? → append to relevant file in that directory
- New topic? → create `topics/<topic-name>.md`
- Sensitive (financial, credentials)? → keep in root MEMORY.md only

### 3. Create/update topic files

Each topic file should:
- Start with a `# Title`
- Contain all relevant facts for that topic
- End with a `## Related` section with `[[wikilinks]]` to related topics
- Be self-contained (readable without the index)

### 4. Rewrite MEMORY.md as index

```markdown
# MEMORY.md — Topic Index

| Topic | File | Status |
|---|---|---|
| Business | `memories/business/` | ✅ Current |
...

## Quick Status
- 🔴 Critical items one-liner
- ⚠️ Warning items one-liner
```

### 5. Update root MEMORY.md (injected context)

The `.hermes/memories/MEMORY.md` file is injected into every session. Keep it compact:
- One paragraph per major domain
- Key facts only (not exhaustive)
- `[[links]]` or file paths to topic files for detail
- Sensitive data (debts, accounts) lives here

## Status Indicators

| Icon | Meaning |
|---|---|
| ✅ | Current, up to date |
| ⚠️ | Stale gap, needs attention |
| 🔴 | Critical, action required |
| 💤 | Dormant, no recent activity |

## Wikilink Conventions

- `[[topic-name]]` — links to another topic file
- Use lowercase, hyphenated names matching file names
- Obsidian resolves these natively if workspace is opened as vault

## Pitfalls

- **Don't duplicate facts across files.** One source of truth. Cross-reference instead.
- **Don't put sensitive data in topic files.** Debts, account numbers, API keys stay in root MEMORY.md.
- **Don't forget to update both MEMORY.md files.** `.hermes/memories/MEMORY.md` (injected) and `.hermes/workspace/memories/MEMORY.md` (workspace index) serve different purposes.
- **Don't create a new subdirectory for every small topic.** Use `topics/` for cross-cutting concerns. Only create new top-level directories for major domains with multiple files.

## Verification

After restructuring:
- [ ] MEMORY.md (root) is compact (< 2,200 chars) with links to topic files
- [ ] MEMORY.md (workspace) has a complete topic index table
- [ ] Each topic file is self-contained with `## Related` wikilinks
- [ ] No sensitive data in topic files
- [ ] Status indicators reflect current state

## Related Skills

- `obsidian` — for vault path resolution and wikilink usage
- `system-backup` — backup memory files after major restructuring
