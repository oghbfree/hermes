# WORKFLOW_AUTO.md - Automated Startup Workflow

This file defines what happens automatically on startup and every 48 hours.
Executor: **orchestrator** (primary). All output logged to `memory/YYYY-MM-DD.md` and #cron-status.

---

## On Startup

### Step 1 â€” Smart Memory Load (do this first, in order)
1. Check `memory/` directory exists â€” create if missing (Rule #9)
2. Read `memory/projects.md` (~1K tokens) â€” project registry
3. Read `MEMORY.md` (~3K tokens) â€” curated long-term memory
4. Read `SOUL.md` â€” identity and constraints
5. Read `USER.md` â€” who you're helping
6. **Do NOT load daily notes at startup** (Rule #16 â€” archive only, on-demand)
7. **Do NOT run vector search at startup** (on-demand only)

> Total startup context: ~4K tokens. If this exceeds 5K, investigate and fix.

### Step 2 â€” Verify Workspace
- Check all critical files exist: `AGENTS.md`, `SOUL.md`, `USER.md`, `MEMORY.md`, `memory/projects.md`
- Verify `memory/` directory is writable (write + delete test file per Rule #9)
- Check gateway connectivity on `:18789`
- Verify model providers are available (deepseek primary)
- Verify `GEMINI_API_KEY` is set in environment (required for vector embeddings)

### Step 3 â€” Vector Memory Sync
- Check: vector-flush-tracker.json (Do NOT run script on startup. Wait for 48h cron.)
- `total_stored = 0` is fine â€” means nothing changed since last flush (Rule #17)
- Log result to daily note

### Step 4 â€” Load Agent Context
- Confirm orchestrator persona and responsibilities (from AGENTS.md)
- Confirm operational freedoms are active
- Check `memory/heartbeat-state.json` exists â€” Create with current Unix timestamp for ALL fields â€” never create with null values

### Step 5 â€” Report Status
- Log startup completion with timestamp to `memory/YYYY-MM-DD.md`
- Report any errors or missing dependencies to log file only (Do not send to #cron-status unless critical failure)
- Document current state

---

## Workflow: Telegram Message with System Prompt

**Trigger:** Incoming Telegram message from any topic

**Steps:**
1. Extract: `message.topicId` (or `message.chatId` if group-level) from message metadata
2. Execute: `skill:telegram_get_prompt topicId={topicId}`
3. Receive and Check result: `{ status: 'ok', systemPrompt, topicName, groupId }`
4. Load: `systemPrompt` from result
5. Construct context: `[systemPrompt] + [user message]`
6. Process: Normal agent response loop
7. Return: Response to same topic/group

**Example:**
Incoming: Topic 50, message "energy 7"
Step 1: Extract topicId = 50
Step 2: skill:telegram_get_prompt topicId=50
Step 3: { status: 'ok', systemPrompt: "You are managing daily clinical health intake..." }
Step 4: Load the prompt
Step 5: Context = "[prompt] + Morning energy check: 7/10"
Step 6: Agent processes with health-clinical behavior
Step 7: Response posted to topic 50

**Error handling:** If `status !== 'ok'`, respond in topic with error message.

**Topics covered:**
- 1: health-log
- 2: general
- 28: cron-status
- 29: memory-review
- 47: code-execution
- 50: health-clinical
- 51: care-clinical
- 139: learning-insights
- 140: daily-briefing
- 141: health-weekly
- 357: business-operations
- 358: construction-projects
- 359: recruitment
- 364: content-calendar


## Every 48 Hours

### Step 1 â€” Memory Maintenance
1. Read recent daily notes (`memory/YYYY-MM-DD.md`, last 3 days) â€” on-demand, this is the one context where loading them is correct
2. Identify significant learnings, decisions, and events worth keeping
3. Update `MEMORY.md` with distilled insights (max 400 lines â€” trim if over, per Rule #18 spirit)
4. Update `memory/projects.md` with any status changes â€” keep under 80 lines (Rule #18)
5. Run `memory_flush.py` to re-embed updated files (Rule #17)

### Step 2 â€” Workspace Audit
- Check file organisation and path validity
- Verify all critical files are present and readable
- Check `memory/` is clean (no orphaned `.tmp` or `.lock` files from interrupted writes)
- Verify `vector-flush-tracker.json` exists and is valid JSON
- Generate brief audit report â†’ log to daily note only

### Step 3 â€” Agent Health Check
- Test critical skills: `openai-whisper-api`, `nano-banana-pro`, `sag`, `gh-issues`
- Verify gateway responding on `:18789`
- Verify Telegram and WhatsApp connections active
- Report any failures (non-blocking)

### Step 4 â€” Index Updates
- Update `MASTER_INDEX.md` if it exists
- Refresh file catalogs
- Document any changes to workspace structure

---

## Key Checks

### Memory System
```
âœ“ memory/ directory exists and is writable
âœ“ memory/projects.md exists and is under 80 lines
âœ“ MEMORY.md loads without errors and is under 400 lines
âœ“ MEMORY.md + projects.md total < 5K tokens
âœ“ vector-flush-tracker.json is valid
âœ“ GEMINI_API_KEY is set in environment
âœ“ memory_flush.py runs without error
```

### Workspace
```
âœ“ AGENTS.md readable
âœ“ SOUL.md readable
âœ“ USER.md readable
âœ“ RULES.md readable
âœ“ HEARTBEAT.md exists
âœ“ WORKFLOW_AUTO.md readable (this file)
```

### Integrations
```
âœ“ Gateway responding on :18789
âœ“ Telegram connection active
âœ“ WhatsApp paired
âœ“ Web search enabled (Brave API)
âœ“ PostgreSQL (openclaw_memory) reachable
âœ“ pgvector extension installed
```

---

## Error Reporting

If any check fails:
1. Log the error with timestamp to `memory/YYYY-MM-DD.md`
2. Document which system failed and why
3. Suggest recovery steps (reference relevant RULES.md rule by number)
4. Continue with remaining checks â€” non-blocking
5. Report summary to #cron-status at end

---

## Success Criteria

Startup succeeds if:
- Memory system initialised (projects.md + MEMORY.md loaded)
- Workspace accessible and writable
- Gateway responding
- No critical blockers (vector DB or GEMINI_API_KEY failures are critical)

---

## Execution Requirements

- **Triggered by:** OpenClaw startup and every 48h timer
- **Output:** memory/YYYY-MM-DD.md (Silent)
- **Error handling:** Log errors, don't crash â€” graceful degradation
- **Token budget:** Startup must stay under 5K tokens loaded context

---

Last Updated: 2026-03-06
Status: Active
