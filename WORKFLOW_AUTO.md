# WORKFLOW_AUTO.md - Automated Startup Workflow

This file defines what happens automatically on startup and every 48 hours.
Executor: **Librarian** (primary). All output logged to `memory/YYYY-MM-DD.md` and #cron-status.

---

## On Startup

### Step 1 — Smart Memory Load (do this first, in order)
1. Check `memory/` directory exists — create if missing (Rule #9)
2. Read `memory/projects.md` (~1K tokens) — project registry
3. Read `MEMORY.md` (~3K tokens) — curated long-term memory
4. Read `SOUL.md` — identity and constraints
5. Read `USER.md` — who you're helping
6. **Do NOT load daily notes at startup** (Rule #16 — archive only, on-demand)
7. **Do NOT run vector search at startup** (on-demand only)

> Total startup context: ~4K tokens. If this exceeds 5K, investigate and fix.

### Step 2 — Verify Workspace
- Check all critical files exist: `AGENTS.md`, `SOUL.md`, `USER.md`, `MEMORY.md`, `memory/projects.md`
- Verify `memory/` directory is writable (write + delete test file per Rule #9)
- Check gateway connectivity on `:18789`
- Verify model providers are available (DeepSeek primary, Gemini fallback)
- Verify `GEMINI_API_KEY` is set in environment (required for vector embeddings)

### Step 3 — Vector Memory Sync
- Run: `python3 ~/.openclaw/workspace/skills/vector-memory/scripts/memory_flush.py`
- `total_stored = 0` is fine — means nothing changed since last flush (Rule #17)
- Log result to daily note

### Step 4 — Load Agent Context
- Confirm Librarian, Cruncher, Architect personas and responsibilities (from AGENTS.md)
- Confirm operational freedoms are active
- Check `memory/heartbeat-state.json` exists — create with empty lastChecks if missing

### Step 5 — Report Status
- Log startup completion with timestamp to `memory/YYYY-MM-DD.md`
- Report any errors or missing dependencies (non-blocking — log and continue)
- Document current state

---

## Every 48 Hours

### Step 1 — Memory Maintenance
1. Read recent daily notes (`memory/YYYY-MM-DD.md`, last 3 days) — on-demand, this is the one context where loading them is correct
2. Identify significant learnings, decisions, and events worth keeping
3. Update `MEMORY.md` with distilled insights (max 400 lines — trim if over, per Rule #18 spirit)
4. Update `memory/projects.md` with any status changes — keep under 80 lines (Rule #18)
5. Run `memory_flush.py` to re-embed updated files (Rule #17)

### Step 2 — Workspace Audit
- Check file organisation and path validity
- Verify all critical files are present and readable
- Check `memory/` is clean (no orphaned `.tmp` or `.lock` files from interrupted writes)
- Verify `vector-flush-tracker.json` exists and is valid JSON
- Generate brief audit report → log to daily note + #cron-status

### Step 3 — Agent Health Check
- Confirm all 3 agents can be spawned
- Test critical skills: `openai-whisper-api`, `nano-banana-pro`, `sag`, `gh-issues`
- Verify gateway responding on `:18789`
- Verify Telegram and WhatsApp connections active
- Report any failures (non-blocking)

### Step 4 — Index Updates
- Update `MASTER_INDEX.md` if it exists
- Refresh file catalogs
- Document any changes to workspace structure

---

## Key Checks

### Memory System
```
✓ memory/ directory exists and is writable
✓ memory/projects.md exists and is under 80 lines
✓ MEMORY.md loads without errors and is under 400 lines
✓ MEMORY.md + projects.md total < 5K tokens
✓ vector-flush-tracker.json is valid
✓ GEMINI_API_KEY is set in environment
✓ memory_flush.py runs without error
```

### Workspace
```
✓ AGENTS.md readable
✓ SOUL.md readable
✓ USER.md readable
✓ RULES.md readable
✓ HEARTBEAT.md exists
✓ WORKFLOW_AUTO.md readable (this file)
```

### Agent Systems
```
✓ Librarian can read/write files
✓ Cruncher can analyse data
✓ Architect can plan workflows
✓ All model providers responding
```

### Integrations
```
✓ Gateway responding on :18789
✓ Telegram connection active
✓ WhatsApp paired
✓ Web search enabled (Brave API)
✓ PostgreSQL (openclaw_memory) reachable
✓ pgvector extension installed
```

---

## Error Reporting

If any check fails:
1. Log the error with timestamp to `memory/YYYY-MM-DD.md`
2. Document which system failed and why
3. Suggest recovery steps (reference relevant RULES.md rule by number)
4. Continue with remaining checks — non-blocking
5. Report summary to #cron-status at end

---

## Success Criteria

Startup succeeds if:
- Memory system initialised (projects.md + MEMORY.md loaded, flush run)
- Workspace accessible and writable
- At least 2 of 3 agents functional
- Gateway responding
- No critical blockers (vector DB or GEMINI_API_KEY failures are critical)

---

## Execution Requirements

- **Triggered by:** OpenClaw startup and every 48h timer
- **Executor:** Librarian (primary)
- **Output:** `memory/YYYY-MM-DD.md` + #cron-status
- **Error handling:** Log errors, don't crash — graceful degradation
- **Token budget:** Startup must stay under 5K tokens loaded context

---

Last Updated: 2026-03-06
Status: Active
