# SKILL Nightly Memory Consolidation & Vector Sync

## DESCRIPTION
Executed daily at 300 AM London Time. This is the system's Deep Sleep phase where it processes all raw interactions from the previous 24 hours and converts them into structured long-term intelligence.

## CAPABILITIES
- Log Parsing & Categorization
- Master File Maintenance (MEMORY.md, RULES.md, FORMULAS.md)
- Vector Database Embedding (via memory_flush.py)

## WORKFLOW

### 1. Raw Data Extraction
Scan the following locations for data generated in the last 24 hours
- Sessions `C:\Users\User\.openclaw\agents\main\sessions\`
- Daily File `memory$(date +%Y-%m-%d).md`
- HealthBusiness Logs All automated check-in responses from the previous day.

### 2. Categorization Logic
Extract and sort information into these Intelligence Buckets
- Projects Status updates for Akoma Robotics, 2Real, Farm, Property, and Geriatric Care.
- Biometrics Final health trends from the EOD synthesis.
- Logic New rules for `RULES.md` and success patterns for `FORMULAS.md`.
- Tasks Move completed items from `tasks-queue.md` to archives; add new discovered tasks.

### 3. Master File Updates
Directly append or modify the following files in the workspace
- `MEMORY.md` Update the Status of the World section.
- `projects.md` Update the specific Last Updated timestamps and status strings.
- `tasks-queue.md` Re-prioritize based on today's blockers.

### 4. Journal Creation
Generate `memory/briefings/JOURNAL-$(date +%Y-%m-%d).md`.
Include Summary of the day, key decisions, people contacted, and a Tomorrow's Focus section.

### 5. Vector Sync (The Flush)
Execute the local Python script `python memory_flush.py`.
This ensures that when you ask the AI a question tomorrow, it has remembered everything from today via RAG (Retrieval-Augmented Generation).

### 6. System Confirmation
Post to Telegram Topic 2
🧠 Memory Consolidation Complete
- Master Files Updated MEMORY, projects, tasks, rules, formulas.
- Journal Saved to `briefings`.
- Vector DB Synced and Embedded.
- Status Ready for 0630 Daily Briefing.

## GUIDELINES
- Persona The Librarian (Archivist Mode).
- Criticality This task must run before the 0630 Daily Briefing.
- Error Handling If `memory_flush.py` fails, post a CRITICAL error to Telegram Topic 141 (#urgent).