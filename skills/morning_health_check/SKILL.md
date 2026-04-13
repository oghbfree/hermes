# SKILL: Morning Health Check Librarian

## DESCRIPTION
Initiates the morning health logging sequence at 08:00 AM. This skill prompts the user for specific health metrics and prepares the environment to catch and parse the response into the health tracking database.

## CAPABILITIES
- Proactive Messaging (Telegram)
- Structured Data Collection
- Contextual Awareness (Librarian Persona)

## WORKFLOW

### 1. The Morning Prompt
Post the following message exactly to the #health-log topic:

"🌅 **Morning Health Check** - Please log your breakfast and current vitals. 

**Format for your reply:**
Breakfast: [what you ate]
Drink: [what you drank]
Symptoms: [none or list]
Severity: [1-5]
Energy: [1-5]
Notes: [anything unusual]"

### 2. Data Expectation
- After posting, the agent should remain "primed" to receive a response.
- When the user replies, the agent must validate that all fields (Breakfast, Symptoms, Severity, Energy) are present.

### 3. Archive Logic (Internal)
- Once the user provides the data, extract the values.
- Append the entry to `memory/health/LOG-$(date +%Y-%m).md` in a table format:
  | Date | Breakfast | Symptoms | Sev | Energy | Notes |
  |------|-----------|----------|-----|--------|-------|
  | $(date) | ... | ... | ... | ... | ... |

## GUIDELINES
- **Persona**: Maintain the "Librarian" persona—organized, helpful, and precise.
- **Tone**: Encouraging but professional.
- **Channel Restriction**: Use Telegram Group -1003620024352 Topic 50 only.