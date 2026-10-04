---
title: SOP — How to Write a New SOP
date: 2026-10-03
tags:
  - sop
  - meta
---

# SOP — SOP Creation Standard
> Trigger: any task done twice without documentation, or a new recurring workflow.

## Filing
1. Name: `SOP-<DOMAIN>-<NAME>.md` in `Vault/SOPs/`.
2. Frontmatter: title, date, tags (sop + domain).
3. Add a wikilink entry to [[00_INDEX]] under the right section — the index is the map; an unlinked SOP doesn't exist.

## Required sections (short is fine)
- **Trigger** — what event starts this SOP
- **Flow** — numbered steps, decision points explicit
- **Never-do** — hard prohibitions with the "instead"
- **Escalation** — what goes to H and how
- **References** — wikilinks to trackers, masters, templates

## Quality bar
- One pass, zero ambiguity: a new agent reading only this note + [[AGENTS_READ_FIRST]] must execute correctly.
- Numbers (times, SLAs, thresholds, prices) are explicit — "soon", "regularly", "as needed" are banned.
- If reality and SOP diverge, update the SOP the day you discover it — living document, no forks, no copies.

## Review
Domain SOPs get re-read whenever a related routine changes (new tool, new staff, new doctor's orders). Mark date in frontmatter when revised.