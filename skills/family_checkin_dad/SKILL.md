# SKILL: Family Check-in (Dad)

## DESCRIPTION
Executed every Sunday and Thursday at 10:00 AM. This skill maintains consistent contact with Dad via WhatsApp. It personalizes the message based on the day of the week and ensures all responses are logged for relationship continuity.

## CAPABILITIES
- Relationship Maintenance
- WhatsApp Bridge Integration
- Longitudinal Interaction Logging

## WORKFLOW

### 1. Message Personalization
Draft a warm, respectful message. 
- **Core Message**: "Hey Dad 👋 Just checking in. How are you doing today? Hope everything is well. Love you!"
- **Variation (Sunday)**: Add a wish for a "restful Sunday" or a "great week ahead."
- **Variation (Thursday)**: Mention that you are "pushing through the week" to keep it conversational.

### 2. Execution
1. **Send** the message via the WhatsApp bridge to target `447983254695`.
2. **Targeting Rule**: Use the E.164 format strictly (no `+`, just digits).

### 3. Documentation
- Update `memory/logs/FAMILY_CHECKINS_$(date +%Y-%m).md`.
- **Format**: `[Date] | [Time] | Recipient: Dad | Status: Sent | Response: [Awaiting]`

### 4. Notification (Internal)
Post a confirmation to Telegram Topic 2: "✅ Bi-weekly check-in sent to Dad (WhatsApp)."

## GUIDELINES
- **Tone**: Warm, affectionate, and respectful.
- **Privacy**: Isolated session to ensure family phone numbers are not exposed in general system logs.
- **Error Handling**: If the WhatsApp bridge reports a delivery failure, immediately escalate to Telegram Topic 141 (#urgent) so the message can be sent manually.