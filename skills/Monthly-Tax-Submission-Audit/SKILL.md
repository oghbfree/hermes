# SKILL Monthly-Tax-Submission-Audit

## Context

This skill is designed to verify if a specific individual (John) has fulfilled their tax reporting obligations for the previous month. It acts as a gatekeeper for financial compliance.

## Logic Flow

1. Context Initialization Determine the reporting period (typically the calendar month preceding the current trigger date).
2. Data Retrieval Query the primary submission portal or internal tracking spreadsheet for a Submitted timestamp associated with the Monthly Tax Return.
3. Cross-Reference Check the email inboxsent folder for a confirmation receipt from the tax authority if the portal status is ambiguous.
4. Validation Confirm that the submitted document matches the expected format and period.

## Definition of Done (DoD)

The system confirms a valid submission exists for the previous month.
In the event of a missing submission, a notification is dispatched.
The audit trail is logged with a timestamp and reference ID.

## Error Handling \& Escalation

Status MissingIncomplete
Action Send a high-priority nudge to John via the primary communication channel.
Repeat Daily until the 7th of the month.
Status Access Denied
Action Log a system error; notify the Automation Architect that credentials for the tax portal need refreshing.

## Knowledge Base

Tax Year 2026
Standard Form Form 10-M (Monthly Return)
Contact Reference john.doe@example.com

