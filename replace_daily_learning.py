import sys

with open('memory/2026-03-29.md', 'r') as f:
    lines = f.readlines()

# Find start and end indices
start = -1
end = -1
for i, line in enumerate(lines):
    if line.strip() == '## Daily Learning - 2026-03-29':
        start = i
    if start >= 0 and line.strip() == '## Security Check - 2026-03-29 03:10 UTC':
        end = i
        break

if start == -1 or end == -1:
    print("Could not find section boundaries")
    sys.exit(1)

# New daily learning content
new_content = '''## Daily Learning - 2026-03-29

### What Worked Today
- Nightly consolidation process executed successfully
- All memory files reviewed and consolidated
- Daily journal created for 2026-03-29

**Formula Origin**: Formula #1 (Daily Learning Capture)

### What Failed Today
- WhatsApp Gateway 499 errors persist (from 2026-03-28)
- Telegram bot not member of authorized group
- Pending action items from previous day

**Rule Proposals**:
- Rule #25: WhatsApp Gateway 499 errors must be monitored and escalated if they exceed a threshold of 10 errors per hour.
- Rule #26: Telegram bot membership must be verified before enabling Telegram channel; run `openclaw channels status` daily to confirm.
- Rule #27: Daily learning capture must include rule proposals for each failure documented.

### Key Insights
1. System operational despite WhatsApp instability
2. Monitoring continues for error pattern recurrence
3. Structured learning capture ensures failures become actionable guards

### Tags
#learning #system-status #health-check #rule-proposal

### Metrics
- Tasks completed: Nightly consolidation (1/1)
- Errors encountered: 2 (WhatsApp 499, Telegram bot membership)
- Time to recovery: N/A (still pending)
- New rules proposed: 3
- memory_flush.py run: No (pending after writing)
'''

# Replace lines
new_lines = lines[:start] + [new_content + '\n'] + lines[end:]

# Write back
with open('memory/2026-03-29.md', 'w') as f:
    f.writelines(new_lines)

print("Daily learning entry updated.")
