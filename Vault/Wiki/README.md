# 📚 LLM Wiki — 2 Real / Owner Knowledge Base

A Hermes-managed knowledge graph in Obsidian. **WikiBot (harold profile)** ingests web links, raw notes, and concepts into this vault; it distills them into concepts, links related entries, and **prunes stale/duplicate content automatically**.

## Structure
| Folder | What lives here |
|--------|-----------------|
| `raw/` | Ingested sources: pasted links, article extractions, notes, dumps — dated, one file per item |
| `concepts/` | Distilled, reusable ideas that connect multiple raw entries |
| `queries/` | Answered questions + the cross-links WikiBot made to answer them |
| `INDEX.md` | The map — every concept, its links, and last-refreshed date |

## How to add something (for H)
1. Paste a **link** or **note** to @harold (or drop it into the WikiBot channel) with one line: `wiki add <url-or-note>`.
2. Harold extracts (web_extract/defuddle/PIL), files it under `raw/`, distils a `concept`, links it to related entries, updates `INDEX.md`.

## Auto-prune (weekly cron)
WikiBot (harold) reviews `raw/` weekly: entries older than ~90 days that are **unreferenced** (no concept links them) are moved to `raw/_archive/`. Duplicates are merged. No active concept is ever deleted without a note.

## Rule (shared with whole stack)
Raw notes live here. Concepts link them. **Memory stays short pointers; the Wiki holds the data.**