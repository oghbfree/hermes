# SKILL: Project Logistics Check-in (Matthias)

## DESCRIPTION
Executed every Friday at 8:00 PM UTC. This skill manages the relationship and logistics coordination with Matthias, specifically focused on scheduling visits to New Amanful.

## CAPABILITIES
- Logistics Coordination
- WhatsApp Delivery Optimization
- Site Visit Tracking

## WORKFLOW

### 1. Message Generation
Draft a friendly Friday evening message:
"Hey Matthias! 🏁 Friday check-in! How has your week been? How's the family? When can you go to New Amanful? Let's catch up soon!"

### 2. Execution
1. **Send** via the WhatsApp bridge to target `233544898392`.
2. **Note**: The E.164 format is strictly enforced (country code 233 + number) to avoid delivery errors.

### 3. Response Logging
When a response is received, the Librarian must:
1. **Identify** the date Matthias proposes for the New Amanful trip.
2. **Update** `memory/projects.md` under the "Logistics/Site Visits" section.
3. **Log** the interaction in `memory/logs/BUSINESS_INTERACTIONS_$(date +%Y-%m).md`.

### 4. System Notification
Post a status update to Telegram Topic 2: "📲 Friday logistics check-in sent to Matthias (New Amanful coordination)."

## GUIDELINES
- **Tone**: Professional, friendly, and goal-oriented.
- **Context**: The "New Amanful" visit is a priority. If Matthias provides a date, the agent should automatically create a task in `tasks-queue.md` for that date.
- **Error Handling**: If delivery fails, escalate to Telegram Topic 141 (#urgent).