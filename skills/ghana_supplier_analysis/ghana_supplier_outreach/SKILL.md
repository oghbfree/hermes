# SKILL: Ghana Supplier Outreach Manager

## DESCRIPTION
Executed Monday through Friday at 9:00 AM. This skill manages the procurement pipeline for dashboard suppliers in Ghana. It identifies the next lead, prepares the communication, and updates the research log to maintain a clean outreach history.

## CAPABILITIES
- File-based Lead Management
- Automated Outreach Drafting
- Status Tracking & Logging

## WORKFLOW

### 1. Lead Identification
Read the file `GHANA_SUPPLIER_RESEARCH.md`. 
- Search for the first supplier entry that does not have a "Contacted Date" or is marked as "Status: Pending".
- Extract: Company Name, Contact Person, WhatsApp/Email, and specific Dashboard Type they provide.

### 2. Inquiry Drafting
Prepare a professional inquiry message based on the following template:

"Hello [Contact Person/Company Name], I am reaching out from OpenClaw regarding your [Dashboard Type] services. We are looking to establish a reliable supply chain for our projects. Could you provide your current lead times and a wholesale price list? Looking forward to your response."

### 3. Execution & Notification
1. **Post** the drafted message and the supplier's contact details to Telegram Topic 2.
2. **Action Required**: Tag the user to confirm if the message should be sent via the Gateway's WhatsApp/Email bridge.

### 4. Update Research Log
Immediately update `GHANA_SUPPLIER_RESEARCH.md`:
- Change Status to: "Inquiry Sent".
- Add Timestamp: "[YYYY-MM-DD HH:MM]".
- Note: "Awaiting user confirmation to bridge message."

## GUIDELINES
- **Tone**: Professional, business-oriented, and proactive.
- **Data Integrity**: Never contact the same supplier twice within a 30-day window unless a follow-up is specifically scheduled.
- **Error Handling**: If no uncontacted suppliers remain in the list, post a notification to Telegram: "⚠️ GHANA_SUPPLIER_RESEARCH: Lead list exhausted. Please add new leads."