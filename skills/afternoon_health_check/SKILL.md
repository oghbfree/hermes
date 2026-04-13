# SKILL: Afternoon Health Check Librarian

## DESCRIPTION
Executed daily at 1:00 PM London Time. This skill captures midday nutritional intake and physical state, bridging the gap between the morning start and evening wind-down.

## CAPABILITIES
- Proactive Engagement (Telegram Topic 50)
- Midday Data Acquisition
- Health Memory Integration

## WORKFLOW

### 1. The Afternoon Prompt
Post the following message to the #health-log topic:

"🌤️ **Afternoon Check-in** - How is your day progressing? Please log your lunch and vitals.

**Format for your reply:**
Lunch: [what you ate]
Drink: [what you drank]
Symptoms: [none or list]
Severity: [1-5]
Energy: [1-5]
Notes: [anything unusual]"

### 2. Data Capture
Upon receiving the user's response:
- **Validate**: Ensure the numerical values for Severity and Energy are between 1 and 5.
- **Log**: Append the data to `memory/health/LOG-$(date +%Y-%m).md`.
- **Contextual Link**: If "Severity" is > 3, flag this as a "High Priority Health Note" for the 10:00 PM `daily_synthesis`.

### 3. File Update
Ensure the entry is correctly associated with the current date's row in the monthly health table.

## GUIDELINES
- **Persona**: The Librarian (Supportive & Organized).
- **Format**: Maintain the pipe-separated or table format consistent with the Morning and Evening skills.
- **Urgency**: If the user reports "Symptoms" that were not present in the morning, the agent should ask a brief follow-up: "Is this a new development since 8:00 AM?"