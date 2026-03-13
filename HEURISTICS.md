# HEURISTICS.md - Decision Shortcuts

Quick IF/THEN rules that remove decision fatigue. Updated monthly.
When a recurring decision is made 3+ times, encode it here.

---

## 🧠 Memory System

### Which memory layer to load?
- IF: Heartbeat or startup → THEN: `MEMORY.md` + `memory/projects.md` only (~4K tokens)
- IF: Asked about specific past work → THEN: Load relevant `memory/YYYY-MM-DD.md` on-demand
- IF: Semantic question about past decisions → THEN: Run `memory_search.py`
- IF: Tempted to bulk-load daily notes at startup → THEN: Stop. Rule #16.

### When to run memory_flush.py?
- IF: Heartbeat → THEN: Always (idempotent — `total_stored=0` is fine)
- IF: Just wrote to `MEMORY.md` → THEN: Immediately after
- IF: Just added a new rule or formula → THEN: Immediately after
- IF: Auto-curation cron just ran → THEN: Built-in, automatic
- IF: Just completed a weekly review → THEN: After updating RULES.md + FORMULAS.md

### Is MEMORY.md getting too long?
- IF: MEMORY.md > 400 lines → THEN: Trim before next write; auto-curation will handle at Wed/Sun
- IF: projects.md > 80 lines → THEN: Archive completed/dead projects immediately (Rule #18)
- IF: Startup context > 5K tokens → THEN: Investigate what's being loaded; fix Rule #16 violation

---

## ⏰ Scheduling

### Cron job vs heartbeat?
- IF: Exact timing matters (9:00 AM sharp) → THEN: Cron
- IF: Multiple checks can batch together → THEN: Heartbeat
- IF: Output delivers directly to a channel → THEN: Cron
- IF: Task needs isolation from main session → THEN: Cron
- IF: Needs recent conversational context → THEN: Heartbeat
- IF: One-shot reminder → THEN: Cron

### How often to check things?
- IF: Fast-changing (messages, alerts) → THEN: Every heartbeat
- IF: Slow-changing (calendar, weather) → THEN: 2-4x per day
- IF: Stable (docs, indexes) → THEN: Weekly audit
- IF: Time is 23:00–08:00 and not urgent → THEN: Stay silent (HEARTBEAT_OK)

---

## 🤖 Model Selection

### Which model for which task?
- IF: Complex reasoning, planning, general tasks → THEN: DeepSeek (primary)
- IF: Cost-sensitive or broad/simple tasks → THEN: Gemini Flash Lite
- IF: Memory embeddings → THEN: Gemini `gemini-embedding-001` (fixed, not swappable)
- IF: Primary model unavailable → THEN: Fall back to Gemini Flash Lite (Rule #10)

---

## 💾 File Operations

### Before any file write:
- IF: Writing to a critical file (MEMORY.md, jobs.json, projects.md) → THEN: Atomic write (Rule #3)
- IF: Migrating or reformatting a file → THEN: Backup first (Rule #7)
- IF: Directory might not exist → THEN: Check and create first (Rule #2)
- IF: Multiple agents could write simultaneously → THEN: Use file locking (Rule #13)

### After any memory file write:
- IF: Wrote to any `.md` in workspace or `memory/` → THEN: Run `memory_flush.py` (Rule #17)
- IF: Flush errors → THEN: Check `GEMINI_API_KEY` is set; check PostgreSQL is running

---

## 🔴 Error Handling

### Error severity — how fast to fix?
- IF: Data lost, exposed, or credentials visible → THEN: Critical — fix immediately (Rule #1)
- IF: Vector DB out of sync with memory files → THEN: Critical — run flush immediately (Rule #17)
- IF: Feature broken, agent can't complete task → THEN: High — fix today
- IF: Performance degraded but functional → THEN: Medium — fix this week
- IF: Nice-to-have broken → THEN: Low — add to backlog

### When to ask vs act?
- IF: Action is reversible and within workspace → THEN: Act freely
- IF: Action sends data outside the machine → THEN: Ask first
- IF: Action is destructive (delete, overwrite without backup) → THEN: Ask first
- IF: Uncertain about user intent → THEN: Ask once, clearly

---

## 💬 Communication

### Group chat — speak or stay silent?
- IF: Directly mentioned or asked → THEN: Respond
- IF: Can add genuine value → THEN: Respond
- IF: Just casual banter between humans → THEN: HEARTBEAT_OK
- IF: Someone already answered → THEN: HEARTBEAT_OK
- IF: Response would just be "yeah" or "nice" → THEN: HEARTBEAT_OK
- IF: Platform supports reactions and acknowledgement is enough → THEN: React, don't reply

### Which notification channel?
- IF: Cron job output → THEN: Telegram #cron-status
- IF: Critical failure or urgent alert → THEN: WhatsApp (allowlist only)
- IF: Always, for audit trail → THEN: Also log to `memory/YYYY-MM-DD.md`

---

## 📋 Learning System

### Rules vs Formulas vs Heuristics?
- IF: Prevents a bad outcome → THEN: Rule (add to `RULES.md`)
- IF: Achieves a good outcome repeatedly → THEN: Formula (add to `FORMULAS.md`)
- IF: Simplifies a recurring decision → THEN: Heuristic (add here)
- IF: Uncertain if it works yet → THEN: Mark experimental in daily note; retest next week

### When to add a new heuristic?
- IF: Made the same decision 3+ times manually → THEN: Encode it here
- IF: Decision took >30 seconds to make → THEN: Consider encoding it
- IF: Heuristic has been wrong 3+ times → THEN: Revise or remove it

---

**Total Heuristics**: 7 categories
**Status**: Active
**Last Updated**: 2026-03-06
**Next Review**: Monthly (1st of month) — Librarian updates during Monthly Evolution Review