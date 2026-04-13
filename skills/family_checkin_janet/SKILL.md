# SKILL: Friday Connection (Janet)

## DESCRIPTION
Executed every Friday at 8:30 PM UTC. This skill maintains a warm, natural connection with Janet, providing a soft touch-point at the end of the work week.

## WORKFLOW

### 1. Message Rotation
The agent will rotate through these options to keep the interaction natural:
* **Option A:** "Hey you. Hope your week has been good. How are you doing?"
* **Option B:** "Happy Friday! 👋 Just wanted to check in and see how your week went. Hope you're doing well."
* **Option C:** "Hey! Thinking of you—hope you've had a productive week and have some rest planned for the weekend. How are things?"

### 2. Dispatch
1. **Send** the selected message via WhatsApp to `233245531575`.
2. **Format**: Ensure no automated signatures are attached; keep it "human-to-human."

### 3. Documentation
- Update `memory/logs/FAMILY_CHECKINS_$(date +%Y-%m).md`.
- **Format**: `[Date] | [Time] | Recipient: Janet | Status: Sent | Note: Friday Warm Check-in`

### 4. Reporting
Post a status update to Telegram Topic 2: "🌸 Friday check-in sent to Janet."

## GUIDELINES
- **Tone**: Warm, casual, and supportive.
- **Privacy**: Isolated session to protect personal contact data.
- **Error Handling**: If the WhatsApp bridge reports a delivery failure, alert Telegram Topic 141 (#urgent).