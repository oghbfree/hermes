# SKILL: Daily Operations Opener (Sammy)

## DESCRIPTION
Executed Monday through Saturday at 7:00 AM UTC. This skill initiates the business day by prompting Sammy for the day's objectives. It ensures the owner (you) has visibility into planned activities before the workday peaks.

## CAPABILITIES
- Morning Strategy Capture
- WhatsApp Bridge Integration
- Operational Logging

## WORKFLOW

### 1. The Morning Directive
Send the following message via WhatsApp to `233575252253`:
"Greetings Sammy! 🌅 New day, new opportunities. What's the plan today? Any sales or issues?"

### 2. Information Capture
When Sammy responds:
1. **Extract**: The primary goal for the day and any flagged potential issues.
2. **Update**: Add these notes to the `memory/business/BUSINESS_CHECKINS_$(date +%Y-%m).md` log.
3. **Synchronize**: If Sammy mentions a specific site visit or inventory task, ensure it is noted for the **Afternoon Health Check** logic so the agent can ask you if those tasks impacted your energy/mood later.

### 3. Telegram Reporting
Post a brief confirmation to Telegram Topic 2: "🌅 Morning check-in sent to Sammy. Awaiting the day's battle plan."

## GUIDELINES
- **Tone**: Motivating, professional, and clear.
- **Data Goal**: Focus on proactive planning rather than reactive reporting, sales reconcilidation, zobaze check for entries and momo transfer to H usually happen end of working day.
- **Error Handling**: If the WhatsApp message is not delivered by 8:00 AM, send an alert to Telegram Topic 141 (#urgent).