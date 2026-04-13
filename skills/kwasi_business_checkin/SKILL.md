# SKILL: Strategic Relationship Manager (Kwasi)

## DESCRIPTION
Executed every Thursday at 08:25 UTC. This skill manages the connection with Kwasi, specifically tracking the progress of the apiary (bees) and mushroom ventures. It features an "Anti-Spam" check to ensure messages are not sent more than once a week.

## CAPABILITIES
- Log Auditing & Frequency Control
- WhatsApp Bridge Integration
- Business Venture Tracking (Agri-tech)

## WORKFLOW

### 1. Frequency Audit
1. **Read**: `memory/logs/FAMILY_CHECKINS_$(date +%Y-%m).md`.
2. **Scan**: Look for "Recipient: Kwasi" or "Kwasi" in the last 7 days.
3. **Decision**: 
    - If a message was sent in the last 7 days: **SKIP** execution. Log "SKIPPED - Recent contact" to the internal system log and notify Telegram Topic 2.
    - If no contact found: **PROCEED** to Step 2.

### 2. Message Dispatch
Send the following message via WhatsApp to `233247582932`:
"Greetings Kwasi, hope you're well. How are things going? How's the apiary and mushroom business coming along?"

### 3. Documentation
- **Log**: Append to `memory/logs/FAMILY_CHECKINS_$(date +%Y-%m).md`.
- **Format**: `[Date] | [Time] | Recipient: Kwasi | Status: Sent | Topic: Apiary/Mushrooms`

### 4. Notification
Post a status update to Telegram Topic 2:
- If sent: "✅ Weekly inquiry sent to Kwasi (Apiary & Mushroom update)."
- If skipped: "⏭️ Kwasi check-in skipped (Contacted within last 7 days)."

## GUIDELINES
- **Tone**: Respectful, encouraging, and entrepreneurial.
- **Data Capture**: If Kwasi provides numbers or milestones regarding the mushroom/apiary business, ensure these are summarized in the next **Daily Synthesis**.
- **Error Handling**: If the WhatsApp bridge fails, alert Telegram Topic 141 (#urgent).