# Nightly Memory Consolidation

## Overview
Automated nightly job that consolidates all daily chat sessions into organized knowledge files.

## Schedule
- **Time**: 2:00 AM daily
- **Channel**: Telegram #briefing

## What It Does

### 1. Session Processing
- Reads all session logs from `C:\OpenClaw\.openclaw\agents\main\sessions\`
- Filters for today's conversations only
- Extracts structured information from JSONL files

### 2. Information Extraction & Categorization

**Projects:**
- Akoma Robotics updates
- 2Real Enterprises activity
- Farm operations
- Property developments
- Geriatric Care agency planning

**Decisions Made:**
- Business choices
- Technical decisions
- Partnership agreements

**People Contacts:**
- John (employee)
- Sammy (employee)  
- Ben (farm manager)
- Matthias (site supervisor)
- Hughie (associate)
- Eric (garage tenant)
- Janet (friend)
- Kwasi (apiary manager)

**Business Intelligence:**
- Prices in GHC/Cedis/GBP
- Supplier information
- Lead generation
- Market data

**Tasks & Action Items:**
- Pending to-dos
- Completed tasks
- Follow-up requirements

**Rules & Lessons:**
- New operational rules
- Lessons learned
- Best practices

**Success Patterns:**
- What worked well
- Effective formulas
- Successful approaches

### 3. File Updates

**Primary Files:**
- `MEMORY.md` - Long-term memory updates
- `memory/projects.md` - Project status updates
- `tasks-queue.md` - Task management
- `RULES.md` - Operational rules
- `FORMULAS.md` - Success patterns

**Daily Files:**
- `memory/[YYYY-MM-DD].md` - Daily summary
- `memory/briefings/JOURNAL-[YYYY-MM-DD].md` - Consolidated journal

**Reports:**
- `memory/consolidation/CONSOLIDATION-[YYYY-MM-DD].md` - Detailed report

### 4. Vector DB Sync
Runs `memory_flush.py` to embed all changes into the vector database for semantic search.

### 5. Telegram Notification
Posts summary to `#briefing` channel:
```
?? Nightly consolidation complete for [date]
Updated: X files
Decisions: X captured
Tasks: X added
Journal: [path]
Vector DB synced. Ready for tomorrow.
```

## Installation

1. Copy the nightly-consolidation folder to your workspace skills directory
2. Configure the cron job in OpenClaw
3. Ensure Telegram bot has access to #briefing channel
4. Test the script manually before enabling cron

## Manual Run

```powershell
powershell -File "C:\OpenClaw\.openclaw\workspace\skills\nightly-consolidation\nightly-consolidation.ps1"
```

## Configuration

Edit `cron-config.json` to adjust:
- Schedule (cron format)
- Timeout (default: 3600 seconds = 1 hour)
- Telegram channel/topic

## Dependencies

- PowerShell 5.1+
- Python 3.x (for memory_flush.py)
- OpenClaw with Telegram integration
- Access to session logs directory

## Troubleshooting

- Check `memory/consolidation/CONSOLIDATION-[DATE].md` for detailed logs
- Verify Telegram bot permissions for #briefing channel
- Ensure all session files are readable
- Check that memory_flush.py runs without errors

## Maintenance

- Review consolidation reports weekly
- Archive old journal files monthly
- Clean up duplicate entries in MEMORY.md quarterly
- Update project patterns as new projects begin
