# SKILL: Family Check-in (Mum)

## DESCRIPTION
Executed every Sunday and Wednesday at 10:00 AM. This skill ensures consistent, high-quality connection with Mum. It synthesizes recent personal wins and business progress into a warm, conversational WhatsApp message.

## CAPABILITIES
- Contextual Personalization
- Multi-Language Nuance (English/Ghanaian Context)
- Relationship Maintenance

## WORKFLOW

### 1. Context Retrieval
Read the following to find "conversation starters":
- `memory/$(date +%Y-%m-%d).md` (Check today's mood/energy).
- `memory/insights/` (Scan the last 3 days for "Key Wins").
- `memory/projects.md` (Check for progress on Ghana-based projects or Akoma).

### 2. Message Composition
Draft a warm, respectful message. 
- **Structure**: Greeting -> Personal/Business Update -> Inquiry about her well-being.
- **Variation**: 
    - **Sunday**: Focus on blessings for the new week and reflection.
    - **Wednesday**: Focus on mid-week momentum and quick updates.
- **Contextual Note**: If there is significant progress on the Ghana supplier front, mention that "things are moving well with the business in Ghana."

### 3. Execution
1. **Send** the message via the WhatsApp bridge to `233503654902`.
2. **Log** the message sent and the timestamp to `memory/logs/family_interactions.md`.

### 4. Notification (Internal)
Post a brief confirmation to Telegram Topic 2: "✅ Sent bi-weekly check-in to Mum via WhatsApp."

## GUIDELINES
- **Tone**: Respectful, warm, and son-like. Avoid sounding like an AI bot; use natural phrasing.
- **Language**: English (Standard/Ghanaian nuance where appropriate).
- **Privacy**: Keep personal family details within this isolated session.
- **Error Handling**: If the WhatsApp bridge is disconnected, post an URGENT alert to Telegram Topic 141 so the message can be sent manually.