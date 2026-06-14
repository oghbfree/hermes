# HEURISTICS.md - Decision Shortcuts

Quick IF/THEN rules that remove decision fatigue. Updated monthly.
When a recurring decision is made 3+ times, encode it here.


## Single Source of Truth":

-For flush schedule: HEURISTICS.md is authoritative. Any other file saying otherwise is stale."
"For model selection: openclaw.json is authoritative. AGENTS.md and HEURISTICS.md must match it.
---

## ðŸ§  Memory System

### Which memory layer to load?
- IF: Heartbeat or startup â†’ THEN: `MEMORY.md` + `memory/projects.md` + `SOUL.md` only (~4K tokens).
- IF: Asked about specific past work â†’ THEN: Load relevant `memory/YYYY-MM-DD.md` on-demand only.
- IF: Semantic question about past decisions â†’ THEN: Run `memory_search.py` (Vector DB).
- IF: Tempted to bulk-load daily notes at startup â†’ THEN: **STOP. Rule #16 violation.** Do not load files > 50 lines at startup.


### When to run memory_flush.py?
- IF: Time is 03:00 â†’ THEN: Run full memory_flush.py (Daily Sync).
- IF: Any other time â†’ THEN: Queue and wait for 03:00. EXCEPTION: Vector DB sync failure (Rule #17) â€” flush immediately, then log to #cron-status.
- IF: Just added a new rule or formula â†’ THEN: Log to file, but wait for 03:00 flush.

### Is MEMORY.md getting too long?
- IF: MEMORY.md > 400 lines â†’ THEN: Trim before next write; auto-curation will handle at Wed/Sun
- IF: projects.md > 80 lines â†’ THEN: Archive completed/dead projects immediately (Rule #18)
- IF: Startup context > 5K tokens â†’ THEN: Investigate what's being loaded; fix Rule #16 violation

---

## â° Scheduling

### Cron job vs heartbeat?
- IF: Exact timing matters (9:00 AM sharp) â†’ THEN: Cron
- IF: Multiple checks can batch together â†’ THEN: Heartbeat
- IF: Output delivers directly to a channel â†’ THEN: Cron
- IF: Task needs isolation from main session â†’ THEN: Cron
- IF: Needs recent conversational context â†’ THEN: Heartbeat
- IF: One-shot reminder â†’ THEN: Cron

### How often to check things?
- IF: Fast-changing (messages, alerts) â†’ THEN: Every heartbeat
- IF: Slow-changing (calendar, weather) â†’ THEN: 2-4x per day
- IF: Stable (docs, indexes) â†’ THEN: Weekly audit
- IF: Time is 23:00â€“08:00 and not urgent â†’ THEN: Stay silent (HEARTBEAT_OK)

---

## ðŸ¤– Model Selection (Orchestrator Logic)

**Model Choice:** Use `openrouter/deepseek/deepseek-v3.2` for everything. -

### ðŸ›¡ï¸ Global Fallback & Memory Rules
- **IF: Any model fails or hits a rate limit**
  - â†’ **ACTION:** Re-route the task to `openrouter/qwen/qwen-turbo` as the universal backup.
- **Memory Embeddings (Vector DB):** - â†’ **USE:** `sentence-transformers/all-MiniLM-L6-v2` for all semantic search tasks.
- **Compaction Rule:** - â†’ **IF:** Context usage exceeds the set floor (10,000 tokens remaining) â†’ **THEN:** Run `memory_flush.py` to summarize and clear the buffer before continuing.


## ðŸ’¾ File Operations

### Before any file write:
- IF: Writing to a critical file (MEMORY.md, jobs.json, projects.md) â†’ THEN: Atomic write (Rule #3)
- IF: Migrating or reformatting a file â†’ THEN: Backup first (Rule #7)
- IF: Directory might not exist â†’ THEN: Check and create first (Rule #2)
- IF: Multiple agents could write simultaneously â†’ THEN: Use file locking (Rule #13)

### After any memory file write:
- IF: Wrote to any .md â†’ THEN: Log the write and STOP. Wait for daily sync.
- IF: Flush errors â†’ THEN: Check `GEMINI_API_KEY` is set; check PostgreSQL is running

---

## ðŸ”´ Error Handling

### Error severity â€” how fast to fix?
- IF: Data lost, exposed, or credentials visible â†’ THEN: Critical â€” fix immediately (Rule #1)
- IF: Vector DB out of sync with memory files â†’ THEN: Critical â€” run flush at 03:00
- IF: Feature broken, agent can't complete task â†’ THEN: High â€” fix today
- IF: Performance degraded but functional â†’ THEN: Medium â€” fix this week
- IF: Nice-to-have broken â†’ THEN: Low â€” add to backlog

### When to ask vs act?
- IF: Action is reversible and within workspace â†’ THEN: Act freely
- IF: Action sends data outside the machine â†’ THEN: Ask first
- IF: Action is destructive (delete, overwrite without backup) â†’ THEN: Ask first
- IF: Uncertain about user intent â†’ THEN: Ask once, clearly

---

## ðŸ’¬ Communication

### Group chat â€” speak or stay silent?
- IF: Directly mentioned or asked â†’ THEN: Respond
- IF: Can add genuine value â†’ THEN: Respond
- IF: Just casual banter between humans â†’ THEN: HEARTBEAT_OK
- IF: Someone already answered â†’ THEN: HEARTBEAT_OK
- IF: Response would just be "yeah" or "nice" â†’ THEN: HEARTBEAT_OK
- IF: Platform supports reactions and acknowledgement is enough â†’ THEN: React, don't reply

### Which notification channel?
- IF: Cron job output â†’ THEN: Telegram #cron-status
- IF: Critical failure or urgent alert â†’ THEN: WhatsApp (allowlist only)
- IF: Always, for audit trail â†’ THEN: Also log to `memory/YYYY-MM-DD.md`

---

## ðŸ“‹ Learning System

### Rules vs Formulas vs Heuristics?
- IF: Prevents a bad outcome â†’ THEN: Rule (add to `RULES.md`)
- IF: Achieves a good outcome repeatedly â†’ THEN: Formula (add to `FORMULAS.md`)
- IF: Simplifies a recurring decision â†’ THEN: Heuristic (add here)
- IF: Uncertain if it works yet â†’ THEN: Mark experimental in daily note; retest next week

### When to add a new heuristic?
- IF: Made the same decision 3+ times manually â†’ THEN: Encode it here
- IF: Decision took >30 seconds to make â†’ THEN: Consider encoding it
- IF: Heuristic has been wrong 3+ times â†’ THEN: Revise or remove it

---

**Total Heuristics**: 7 categories
**Status**: Active
**Last Updated**: 2026-03-06
**Next Review**: Monthly (1st of month)