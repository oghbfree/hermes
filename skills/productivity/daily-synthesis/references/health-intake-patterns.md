# Health Intake Patterns — Reference

## Channel Migration (May 15, 2026 — Confirmed, Day 2 Sustaining)

**Pattern:** When WhatsApp is unavailable, H shifts health logging to Telegram topics directly.

**Evidence:**
- May 8-14: 0/6 health responses despite 100% prompt delivery (WhatsApp Day 12-18)
- May 15: 6/6 responses — H logged meals directly in Telegram topic 2 (H health) and topic 4 (Mum health). **BREAKTHROUGH.**
- May 16: 6/6 prompts delivered, Day 2 of new pattern — sustaining confirmed.
- H did NOT respond to individual health check prompts — instead posted full-day meal summaries in the topics

**Implication:** Health intake crons should be considered as **reading from Telegram topic logs**, not just expecting direct prompt responses. The prompts serve as reminders, but the actual data entry happens in the topics.

**File Sync Gap:** Telegram topic entries are NOT automatically written back to HEALTH_LOG files. As of May 16, HEALTH_LOG files still show last entries at May 8 (H) and May 7 (Comfort) despite 2 days of Telegram logging. Two parallel tracking systems exist. This needs an automated sync or manual reconciliation.

## Gap Escalation Language (from SKILL.md)

| Gap | Term | Clinical Action |
|-----|------|-----------------|
| 1-2 days | "gap" | Note in synthesis |
| 3-4 days | "compliance concern" | Flag prominently |
| 5+ days | "compliance collapse" | Escalate to direct follow-up |
| 6+ days (elderly) | "clinical risk" | Direct human follow-up required |
| 8+ days (elderly) | "CRITICAL clinical risk" | Immediate direct human follow-up |

## Gap Closure Reporting

When a gap closes after 5+ days:
1. Label it **BREAKTHROUGH** in the synthesis
2. Identify the trigger (channel shift, user action, etc.)
3. Note as an emerging pattern if repeatable
4. Update trend metrics (compliance rate, gap days)

## Known Vitals Baselines

- **H:** BP 130/65, Pulse 74 (May 8) — normal range
- **Comfort (Mum, 91):** BP 119/67, Pulse 87 (May 7) — normal range, hip ache noted

## Topic Mapping

| Topic | ID | Purpose |
|-------|-----|---------|
| H health | 2 | H's daily health intake |
| Mum health | 4 | Comfort's daily health intake |

**Note:** Topic IDs differ from AGENTS.md (which references 50/51). The cron delivery targets (2 and 4) are authoritative.
