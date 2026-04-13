# SKILL: Recruitment Pipeline & Lead Screener

## DESCRIPTION
Executed daily at 08:00 AM. This skill automates HR overhead by pulling new applicant data from multiple Google Sheets, identifying priority candidates (Drivers/Nurses), and archiving interview intel from the field.

## CAPABILITIES
- Google Sheets Integration (`gog` tools)
- Differential State Checking (New Rows Only)
- Priority Lead Scoring (Driving/Notes)

## WORKFLOW

### 1. Data Acquisition (Google Sheets)
Access the `2realenterprisesgh@gmail.com` account and read:
- **Financial Literacy**: `1GUdkRPkD5b68WorxepfMUmHjbggGu6NggWPO87tFFA8`
- **Construction**: `1Od-tUpf02eGfirjFvtUHgojsYRq2JA20IJAMOETCE4k`
- **Facilitators**: `1jxpEQRYh08pUlCQHbKygVL8vtP5CWqHupRWYx5xtQCU`
- **Nurses**: `1JKAQMF1eUotpqp61Dd_0bbkteRe3oOB-oLwLMMdyOq4`

### 2. State Comparison
Compare raw data against `workspace/jobs/last-check-[role].json`. 
- **Identify**: Only rows with index > `lastProcessedRow`.
- **Nurses Specific**: Parse the "Driving" column. If `YES`, flag as `🚨 PRIORITY: DRIVER`. 
- **Interview Intel**: Capture the "John's Notes" column for the Nursing sheet.

### 3. File Generation & Archiving
1. **Categorized Logs**: Save individual files to `workspace/jobs/[role]/$(date +%F)-new.md`.
2. **Master Report**: Compile `workspace/jobs/APPLICATIONS-REPORT-$(date +%F).md` with full candidate profiles and John’s raw notes.
3. **State Update**: Write the new high-water mark (last row index) back to the `.json` state files.

### 4. Notification Logic
Post to **Telegram Topic 359 (#jobs)**:
- **If New Data**: 
  "📋 **APPLICATIONS - $(date +%F)**
  - Financial Literacy: [X] new
  - Construction: [X] new
  - Facilitators: [X] new
  - Nurses: [X] new ([Y] Drivers | [Z] w/ Notes)
  Full Report: `APPLICATIONS-REPORT-$(date +%F).md`"
- **If Zero Data**: "Applications $(date +%F) - No new submissions today."

## GUIDELINES
- **Confidentiality**: Professional handling of applicant PII (Personally Identifiable Information).
- **Accuracy**: Ensure John's interview notes are captured exactly as written without AI summarization to maintain raw field data.
- **Error Handling**: If Google API fails or permissions are revoked, alert Telegram Topic 141 (#urgent).