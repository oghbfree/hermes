# SKILL: Debt Recovery Escalation (Jnr)

## DESCRIPTION
Executed every 3 days. This skill manages a 5-stage escalation ladder designed to recover funds within a 14-day window. It increases verbal urgency as the deadline nears while maintaining professional boundaries.

## WORKFLOW

### 1. Track Iteration
Check `memory/logs/FAMILY_CHECKINS_$(date +%Y-%m).md` to count how many "Jnr Debt" reminders have been sent in the current 14-day cycle.

### 2. The Escalation Ladder
Select the message based on the iteration count:

* **Iteration 1 (Day 1):** "Greetings, hope you're well. Just wanted to reach out — would be good to sort things out ASAP."
* **Iteration 2 (Day 4):** "Hey, just following up on my last message. I really need to get that matter sorted sooner rather than later. Let me know your plan for today."
* **Iteration 3 (Day 7):** "Reaching out again as I haven't heard back. We’re halfway through the two weeks I mentioned. I need you to prioritize getting this settled now."
* **Iteration 4 (Day 10):** "It's been 10 days and no progress. This is becoming urgent on my end. Please get in touch today so we can finalize the payment."
* **Iteration 5 (Day 13 - FINAL):** "This is the final reminder before the 14-day deadline. I’ve tried to keep this open, but I need the funds sorted by tomorrow. Please update me immediately."

### 3. Execution & Logging
1.  **Send** the selected message via WhatsApp to `447727185361`.
2.  **Log**: Update `memory/logs/FAMILY_CHECKINS_$(date +%Y-%m).md`.
    - **Format**: `[Date] | Iteration: [1-5] | Status: Sent | Response: [None/Received]`

### 4. Critical Alerting
If **Iteration 4 or 5** is sent without a response to previous messages:
- **Ping Telegram Topic 141 (#urgent)**: "⚠️ JNR ESCALATION: Stage [4/5] sent. No response received in 10+ days. Immediate manual follow-up recommended."

## GUIDELINES
- **Tone:** Start collaborative, end firm/urgent.
- **Geography:** London Time (GMT/BST).
- **Reset Logic:** If a response indicating "Payment Sent" is logged in the business/family logs, the Librarian must **Disable** this cron immediately.