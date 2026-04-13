# SKILL: Field Intel & Ground Updates (John)

## DESCRIPTION
Executed Monday through Friday at 8:00 AM Accra Time. This skill maintains a direct pulse on "on-the-ground" activities by prompting John for immediate situational updates.

## CAPABILITIES
- Ground Intelligence Gathering
- WhatsApp Delivery Bridge
- Longitudinal Business Logging

## WORKFLOW

### 1. The Field Inquiry
Send the following message via WhatsApp to `233233352252`:
"Greetings John! 👋 How be? Whats the latest? Any updates?"

### 2. Data Capture & Logging
When John responds:
1. **Identify**: stock intel, technical progress, or "ground" friction mentioned.
2. **Log**: Record the details in `memory/business/BUSINESS_CHECKINS_$(date +%Y-%m).md`.
   - **Format**: `[Date] | [Time] | Person: John | Update: [Ground Intel] | Status: [Action Required/Info Only]`

### 3. Cross-Referencing
- If John reports a technical blocker, add it to `tasks-queue.md` with the tag `⚠️ FIELD ISSUE`.

### 4. Reporting
Post a brief confirmation to Telegram Topic 2: "🌍 Field check-in sent to John. Monitoring for ground updates."

## GUIDELINES
- **Tone**: Casual, rhythmic ("How be?"), and grounded.
- **Timezone Awareness**: Africa/Accra (GMT+0).
- **Error Handling**: If delivery fails, escalate to Telegram Topic 141 (#urgent).