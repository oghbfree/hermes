# SKILL: Ghana Steering Conversion Verifier

## DESCRIPTION
Executed every Wednesday at 11:00 AM Accra Time. This skill performs technical vetting of suppliers listed in `GHANA_SUPPLIER_RESEARCH.md`, specifically focusing on their ability to handle RHD to LHD steering and dashboard conversions.

## CAPABILITIES
- Technical Requirement Verification
- Supply Chain Vetting
- Structured Data Logging

## WORKFLOW

### 1. Identify Target Supplier
Scan `GHANA_SUPPLIER_RESEARCH.md` for the next supplier where:
- "Steering Conversion Verified" is FALSE or BLANK.
- "Dashboard Change Verified" is FALSE or BLANK.

### 2. Technical Inquiry Drafting
Prepare a specific technical inquiry for the identified supplier:
"Hello, we are verifying technical partners for our upcoming projects. Regarding your conversion services:
1) Are you equipped to perform full RHD to LHD steering rack conversions?
2) Do you provide the dashboard shell and components for LHD conversion?
3) What is the average total cost and lead time for a standard conversion?
Please provide details so we can update our approved supplier list."

### 3. Execution & Routing
1. **Post** the drafted inquiry and the supplier's contact info (WhatsApp/Phone) to Telegram Topic 2.
2. **Note**: If the OpenClaw Gateway has active WhatsApp/Email tools, flag for user approval to send automatically.

### 4. Record Maintenance
Update the supplier's entry in `GHANA_SUPPLIER_RESEARCH.md`:
- Set Status to: "Verification Pending".
- Add Timestamp: "[YYYY-MM-DD HH:MM] Verification Request Sent".

## GUIDELINES
- **Persona**: The Librarian (Methodical and detail-oriented).
- **Timezone**: Africa/Accra (GMT+0).
- **Technical Accuracy**: Ensure the distinction between "Steering Rack" and "Dashboard Shell" is maintained in all logs; these are two separate verification points.
- **Error Handling**: If all current suppliers are already verified, notify Telegram Topic 2: "✅ All current Ghana suppliers are steering-verified. No further action required."