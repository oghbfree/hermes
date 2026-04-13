# SKILL: Relationship Manager (Kanzoni)

## DESCRIPTION
Executed every Tuesday at 7:00 AM UTC. This skill handles the weekly check-in with Kanzoni. It focuses on maintaining rapport and opening the door for business or family updates through a warm, consistent WhatsApp message.

## CAPABILITIES
- WhatsApp Bridge Integration
- Automated Relationship Maintenance
- Interaction Logging

## WORKFLOW

### 1. Message Preparation
Draft the weekly message. While the core intent is "Any updates?", vary the phrasing slightly each week to maintain a natural feel:
- **Option A**: "Hey Kanzoni! How are you doing? How's the family? Hope everything is going well. Any updates on your end?"
- **Option B**: "Good morning Kanzoni, hope you're having a great start to the week. How's everyone at home? Just checking in to see how things are moving."

### 2. Delivery
1. **Send** the selected message via the WhatsApp bridge to target `233248957794`.
2. **Targeting Rule**: Ensure no "+" prefix is used unless required by your specific Gateway provider (usually `233...` is sufficient).

### 3. Reporting & Logging
1. **Archive**: Log the message sent and the timestamp to `memory/logs/business_interactions.md`.
2. **Notification**: Post a silent confirmation to Telegram Topic 2: "✅ Tuesday check-in sent to Kanzoni (WhatsApp)."

## GUIDELINES
- **Tone**: Friendly, casual, yet professional.
- **Channel**: WhatsApp ONLY.
- **Error Handling**: 
    - If the "Delivering to WhatsApp" error persists, the Librarian must log the specific error code and alert the #urgent topic 141 on Telegram.
    - If Kanzoni replies, the agent should flag the reply in the next **Daily Briefing** under "Pending Decisions" or "Business Pulse."