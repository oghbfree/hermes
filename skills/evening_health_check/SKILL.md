# SKILL: Evening Health Check Librarian

## DESCRIPTION
Executed daily at 7:00 PM London Time. This skill prompts the user to close out their health data for the day. This data is a primary input for the 10:00 PM `daily_synthesis` skill.

## CAPABILITIES
- Proactive Messaging (Telegram Topic 50)
- End-of-Day Data Collection
- Health Log Synchronization

## WORKFLOW

### 1. The Evening Prompt
Post the following message to the #health-log topic:

"🌙 **Evening Health Log** - Time to wrap up today's vitals.

**Format for your reply:**
Dinner: [what you ate]
Drink: [what you drank]
Symptoms: [none or list]
Severity: [1-5]
Energy: [1-5]
Mood: [1-5]
Notes: [anything unusual today]"

### 2. Data Capture & Archiving
Upon receiving the response:
- **Extract**: Food, Drink, Symptoms, Severity, Energy, Mood, and Notes.
- **Write**: Update `memory/health/LOG-$(date +%Y-%m).md`. 
- **Format**: Append as an "Evening" entry or merge with the morning row for a complete daily profile.

### 3. Preparation for Synthesis
Create a temporary "EOD Snapshot" in `memory/temp_health_snapshot.md` so the `daily_synthesis` agent (running at 10 PM) can easily pull the consolidated data without parsing the whole monthly table.

## GUIDELINES
- **Tone**: Calm, reflective, and supportive (Librarian Persona).
- **Consistency**: Ensure the 1-5 scales are captured as integers for later trend analysis in the **Weekly Review**.
- **Error Handling**: If the user does not reply by 9:00 PM, send a one-time gentle nudge: "Reminder: Please log your evening health stats before the nightly synthesis begins."