# SKILL: Daily System Briefing Architect

## DESCRIPTION
Aggregates environmental data, financial rates, system health, and memory logs into a structured daily briefing for the #briefing Telegram topic and archival.

## CAPABILITIES
- Real-time Web Search (Weather & FX)
- File System Operations (Memory & Task Queues)
- System Log Analysis (Cron History)
- Telegram Bot API Integration
- Markdown Journaling

## WORKFLOW

### 1. Data Retrieval Phase
- **Weather**: Search for "Current weather in Peckham, London". Extract Temp, Condition, and High/Low.
- **Finance**: Search for "GBP to GHS exchange rate". Compare today's rate against the value stored in the most recent `memory/briefings/` file to determine the "Trend".
- **Logs**:
    - Read `memory/$(date +%Y-%m-%d).md` (Today's plan).
    - Read `memory/$(date -d 'yesterday' +%Y-%m-%d).md` (Yesterday's log).
    - Read `memory/projects.md` and `tasks-queue.md`.
    - Retrieve logs from the local cron engine for the last 24h.

### 2. Formatting Phase
Compile the data into the following template:

🦞 **OPENCLAW DAILY BRIEFING**
📅 [Full Date] | ⏰ [Time] GMT
🌤️ **PECKHAM WEATHER:** [Current temp] [Condition] [High/Low]
💷 **EXCHANGE RATE:** £1 = [X] GHS | Trend: [up/down/stable]
📡 **SYSTEM STATUS:** [Check connectivity for Gateway, WhatsApp, Telegram] | Last memory flush: [Date] | Active Crons: [Count]
🌙 **YESTERDAY PROGRESS:** [Summary from yesterday's memory file]
⏰ **OVERNIGHT CRONS (Last 12h):** [List Cron Name | Time | Status]
🎯 **TODAYS PRIORITIES:** [Top 3 from tasks-queue.md]
📅 **SCHEDULED TODAY:** [List scheduled crons from system config]
🚧 **PENDING DECISIONS:** [Unresolved items from memory/tasks-queue]
⚠️ **BLOCKERS:** [Failures/Missed items]
📊 **BUSINESS PULSE:**
- John: [Last update]
- Sammy: [Last update]
- Ghana Supplier: [Status]
- Akoma Robotics: [Status]
- 2Real Shop: [Status]
🧠 **MEMORY SNAPSHOT:** [New rules, formulas, and learning captures from the last 24h]

### 3. Execution Phase
1. **POST** the compiled message to Telegram Group `-1003620024352` under Topic `2`.
2. **SAVE** the exact content of the post to `memory/briefings/BRIEFING-$(date +%Y-%m-%d).md`.

## ERROR HANDLING
- If a file is missing (e.g., today's memory file), note it as "FILE NOT FOUND" in the briefing and proceed.
- If the Web Search fails, use the last known data and tag with "(CACHED)".