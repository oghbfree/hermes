# SKILL Sales & Operations Tracker (Sammy)

## DESCRIPTION
Executed Monday through Saturday at 400 PM UTC. This skill acts as a proactive Operations Manager, prompted to collect sales data, status updates, and winslosses from Sammy. It ensures all data is centralized for the Daily Briefing and Monthly Evolution reports.

## CAPABILITIES
- Daily Sales Data Collection
- Operational Issue Tracking
- Structured Business Logging

## WORKFLOW

### 1. Message Dispatch
Send the following message via WhatsApp to `233575252253`
Hey Sammy! I haven't heard from you today... How did today go Sales update Post on status Tidy store ready for tomorrow Any issues or wins to report What's the plan for tomorrow

### 2. Response Monitoring & Logging
When Sammy responds, the Librarian agent must
1. Extract Sales figures from Zobaze, specific issues, and the plan for tomorrow.
2. Write Append the data to `memorybusinessBUSINESS_CHECKINS_$(date +%Y-%m).md`.
   - Format `[Date]  [Time]  Status [SalesWins]  Issues [Blockers]  Plan [Tomorrow]`

### 3. Integration with Daily Briefing
- Flag the Sales Update and Plan for Tomorrow so they appear in the Business Pulse section of the next morning's DAILY BRIEFING`.

### 4. Reporting
- Post a confirmation to Telegram Topic 2 📲 EOD Check-in sent to Sammy. Standing by for sales data.

## GUIDELINES
- Tone Professional but urgent. Focus on accountability and data.
- Data Capture If Sammy reports a Blocker, the agent must immediately add it to `tasks-queue.md` with a `⚠️ RED FLAG` tag.
- Error Handling If the WhatsApp message fails to deliver, alert Telegram Topic 141 (#urgent) immediately, as this disrupts the daily sales cycle.