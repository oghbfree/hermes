# EVOLUTION.md - Agent Evolution History

This file tracks how the system changes over time. Updated monthly by Librarian during Monthly Evolution Review.
Each entry is a snapshot of what changed, why, and what improved.

---

## 2026-03 (March)
**Status**: Memory system upgrade — 4-layer stack installed and operational

### System Changes
- Installed 4-layer memory stack:
  - Layer 1: `memory/YYYY-MM-DD.md` — raw daily archives (load on-demand)
  - Layer 2: `MEMORY.md` — curated long-term brain (load every heartbeat)
  - Layer 3: `memory/projects.md` — project registry (load every heartbeat)
  - Layer 4: PostgreSQL + pgvector (`openclaw_memory`) — semantic vector search (on-demand)
- Smart loading implemented: ~4K tokens at startup vs ~20K+ previously (~80% savings)
- Twice-weekly MEMORY.md auto-curation cron added (Wed & Sun 05:00 Europe/London)
- Vector DB operational: Gemini `gemini-embedding-001` embeddings, 768-dim
- `memory_flush.py` added to every heartbeat sequence (idempotent)
- All workspace files updated to reflect new memory architecture

### New Rules Added
- Rule #16: Never load daily notes at startup
- Rule #17: Vector DB must stay in sync with memory files
- Rule #18: projects.md must stay under 80 lines

### New Formulas Added
- Formula #11: Smart Memory Load Verification

### New Files Created
- `HEURISTICS.md` — decision shortcuts (standalone file at workspace root)
- `EVOLUTION.md` — this file
- `memory/projects.md` — project registry seed
- `skills/vector-memory/scripts/` — 4 Python scripts for vector memory

### Agent Changes
- **Librarian**: Now owns `memory_flush.py` at every heartbeat; owns monthly evolution review
- **All agents**: Load only `projects.md` + `MEMORY.md` at startup (enforced by Rule #16)
- **Auto-curation cron**: Replaces manual weekly MEMORY.md edits

### Metrics
- Startup token cost: ~20K → ~4K (80% reduction)
- Rules documented: 15 → 18 (+3)
- Formulas documented: 10 → 11 (+1)
- Heuristic categories: 0 → 7
- Vector DB: Operational

### Major Learnings
1. Token budget discipline requires rules, not just intentions — Rule #16 enforces it
2. Vector DB drift is silent and dangerous — Rule #17 prevents it
3. File size limits on always-loaded files compound into big savings over time
4. The learning loop (daily → weekly → curation → vector) is self-sustaining once seeded

### Next Month's Focus
- Confirm auto-curation cron is running cleanly (check #cron-status logs)
- Populate `memory/projects.md` with all active projects
- Run first weekly pattern extraction using vector search (Formula #2 updated process)
- Begin tracking learning system metrics in weekly JSON format

---

## 2026-02 (February)
**Status**: Consolidation phase — stability fixes and learning infrastructure built

### System Changes
- Added `LEARNING_SYSTEM.md` — iterative learning framework
- Implemented `RULES.md` with initial 15 rules from real failures
- Created `FORMULAS.md` with 10 validated success patterns
- Automated daily learning capture via scheduled tasks
- Added daily self-audit cron (07:00 Europe/London → #cron-status)
- Added quarterly review crons (Q2: 30 Jun, Q3: 30 Sep)
- Added yearly memory review cron (31 Dec → #memory-review-channel)

### Agent Changes
- **Librarian**: Improved memory file organisation; automated daily log creation
- **Cruncher**: Added structured failure analysis capability
- **Architect**: Moved to weekly strategic review (was quarterly)

### Rules Added (February)
- Rule #1: Never expose credentials in logs
- Rule #2: Always validate file paths before operations
- Rule #3: Memory writes must be atomic
- Rule #4: Never block on external APIs
- Rule #5: Always validate user input
- Rule #6: Document breaking changes immediately
- Rule #7: Test migrations before deployment
- Rule #8: Config validation before startup
- Rule #9: Memory directory must exist and be writable
- Rule #10: Never assume external services are available
- Rule #11: Learning capture must be automated
- Rule #12: File size limits for transcription
- Rule #13: Concurrency requires locking
- Rule #14: Config keys must be consistent
- Rule #15: Recovery must be faster than prevention
- Rule #101: The Deadlock Reset

### Formulas Validated (February)
- Formula #1: Daily Learning Capture
- Formula #2: Weekly Pattern Extraction
- Formula #3: Hypothesis-Test-Document Loop
- Formula #4: Failure-to-Rule Conversion
- Formula #5: Decision Heuristic Encoding
- Formula #6: Automated Validation Before Action
- Formula #7: Backup-Test-Deploy Pattern
- Formula #8: Iterative Improvement Cycle
- Formula #9: Multi-Channel Notification Pattern
- Formula #10: The 5-Minute Focus Block

### Metrics
- System uptime: 94% → 98%
- Error recovery time: 30 min → 5 min
- Knowledge retention: 60% → 95%
- Daily learning capture compliance: 90%
- Rules documented: 0 → 15
- Formulas documented: 0 → 10

### Major Learnings
1. Memory organisation is the foundation — everything else depends on it
2. Failure documentation prevents repeat mistakes more reliably than memory alone
3. Automation enables consistency; manual discipline eventually breaks down
4. Weekly synthesis beats random knowledge accumulation

### Critical Issues Fixed
1. Config validation (Rule #8) — prevented agent initialisation failures
2. Memory file corruption (Rule #3) — atomic writes eliminate data loss
3. WhatsApp integration (Rule #10) — retry/queue logic prevents silent message loss
4. Concurrent write corruption (Rule #13) — file locking implemented

---

## Adding New Monthly Entries

At the start of each month, Librarian runs the Monthly Evolution Review:

1. Read `learning/monthly/YYYY-MM.md` synthesis
2. Read last 4 weekly reviews from `learning/weekly/`
3. Summarise agent changes, system changes, new rules/formulas
4. Update metrics (compare to previous month)
5. Add new entry at TOP of this file (most recent first)
6. Run `memory_flush.py` after updating
7. Report completion to #cron-status

---

**Last Updated**: 2026-03-06
**Next Review**: 2026-04-01 (Monthly Evolution Review)
**Maintained by**: Librarian