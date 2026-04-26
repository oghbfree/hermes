# SKILL: Daily Goodnight Rotation (Ebony)

## DESCRIPTION
Executed daily at 10:00 PM UTC. This skill selects a message from a pre-defined rotation to maintain a fresh, loving connection with Ebony and the boys.

## WORKFLOW

### 1. Message Selection (The Rotation)
The agent will rotate through the following options based on the day of the week or a random seed to ensure variety:

* **Option A:** "Goodnight my love 🌙 Hope you and the boys had a good day. Miss you. Sleep well ❤️"
* **Option B:** "Thinking of you all before I head to bed. Hope the boys are settled. Sleep tight, my love. 🕊️"
* **Option C:** "Sending love across the miles. Can't wait until we're all together again. Goodnight and sweet dreams to you and the kids. 😘"
* **Option D:** "Just checking in to say goodnight. You're always in my thoughts. I hope your day was beautiful. Love you! ❤️✨"
* **Option E:** "Rest well, my love. Tell the boys I'm thinking of them. See you in my dreams. 🌙💤"

### 2. Dispatch
1.  **Send** the selected message via WhatsApp to `233546081608`.
2.  **Ensure** only one message is sent per session.

### 3. Documentation & Tracking
- Log the specific variation sent in `memory/logs/FAMILY_CHECKINS_$(date +%Y-%m).md`.
- **Format:** `[Date] | [Time] | Recipient: Ebony | Variation: [A-E] | Status: Sent`

### 4. Notification
Post a status update to Telegram Topic 2: "❤️ Rotated Goodnight message sent to Ebony."