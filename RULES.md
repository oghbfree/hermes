# RULES.md - Learned Constraints from Failures

Every failure teaches a guard. This file documents what NOT to do based on real failures.

---

## Rule #1: Never Expose Credentials in Logs or Configs
- **Root Cause**: Storing secrets in plaintext configuration
- **Consequence**: Security breach risk, unauthorized API access
- **Guard**: Use environment variables for all secrets
- **Check**: Before logging/sharing, scan for patterns: `sk_`, `gsk_`, `API_KEY`, `Bearer`
- **Implementation**: 
  ```powershell
  # âœ… DO: Use environment variables
  $apiKey = $env:OPENROUTER_API_KEY
  
  # âŒ DON'T: Store in config
  # "apiKey": "sk-or-v1-..."
  ```
- **Exception**: None for critical credentials
- **Validation**: Automated key detection before any output
- **Status**: âœ… Implemented

---

## Rule #2: Always Validate File Paths Before Operations
- **Root Cause**: Assuming directory exists without checking
- **Consequence**: Task failed silently, no error handling
- **Guard**: Check path.exists() and create if needed
- **Check**: `if (!(Test-Path $path)) { mkdir $path -Force }`
- **Implementation**:
  ```powershell
  # âœ… DO: Validate and create
  $dir = "C:\Users\User\.openclaw\workspace\memory"
  if (!(Test-Path $dir)) { mkdir $dir -Force }
  
  # âŒ DON'T: Assume it exists
  # Write-Host "Writing to $dir..." # Error if dir missing
  ```
- **Exception**: Can create parent directories with `-Force` flag
- **Validation**: Test with missing paths
- **Status**: âœ… Implemented

---

## Rule #3: Memory Writes Must Be Atomic
- **Root Cause**: Process interrupted during file write
- **Consequence**: Lost all cron jobs, unrecoverable data
- **Guard**: Write to temp file, then atomic rename
- **Check**: Always use temp + rename pattern for important files
- **Implementation**:
  ```powershell
  # âœ… DO: Atomic write pattern
  $temp = "$path.tmp"
  $content | Set-Content $temp
  Move-Item $temp $path -Force
  
  # âŒ DON'T: Direct write
  # $content | Set-Content $path
  ```
- **Exception**: None for data files; safe for logs
- **Validation**: Simulate power failure during write
- **Status**: âœ… Implemented

---

## Rule #4: Never Block on External APIs
- **Root Cause**: No timeout on HTTP request to Telegram
- **Consequence**: System unresponsive for 30+ seconds
- **Guard**: Set timeouts on ALL external calls, use async
- **Check**: Every API call must have timeout < 5 seconds
- **Implementation**:
  ```javascript
  // âœ… DO: Async with timeout
  const timeout = new Promise((_, r) => 
    setTimeout(() => r(new Error('timeout')), 5000)
  );
  const result = await Promise.race([apiCall(), timeout]);
  
  // âŒ DON'T: Blocking wait
  // const result = await apiCall(); // No timeout
  ```
- **Exception**: Can retry up to 3x with exponential backoff
- **Validation**: Test with slow/unreachable API
- **Status**: âœ… Implemented

---

## Rule #5: Always Validate User Input Before Processing
- **Root Cause**: No input sanitization or bounds checking
- **Consequence**: Bot stopped responding, manual restart needed
- **Guard**: Sanitize and validate all inputs
- **Check**: Type checking, bounds validation, length limits
- **Implementation**:
  ```javascript
  // âœ… DO: Validate input
  if (!message || typeof message !== 'string' || message.length > 4096) {
    throw new Error('Invalid message');
  }
  
  // âŒ DON'T: Trust user input
  // processMessage(message); // No validation
  ```
- **Exception**: None for security-critical inputs
- **Validation**: Fuzz test with random/extreme inputs
- **Status**: âœ… Implemented

---

## Rule #6: Document Breaking Changes Immediately
- **Root Cause**: Changed config without documenting changes
- **Consequence**: Spent 4 hours debugging incompatibility
- **Guard**: Create CHANGELOG.md entry BEFORE deploying
- **Check**: Can't deploy without CHANGELOG entry
- **Implementation**:
  ```markdown
  # CHANGELOG.md
  ## [Unreleased]
  ### Changed
  - Moved API keys to environment variables
  - Updated config.schema.json
  
  ### Migration
  - Users must set OPENROUTER_API_KEY env var
  - Old config format still supported (deprecated)
  ```
- **Exception**: None for breaking changes
- **Validation**: Track deployment with CHANGELOG entry
- **Status**: âœ… Implemented

---

## Rule #7: Test Migrations Before Deployment
- **Root Cause**: Migrated live data without testing first
- **Consequence**: Lost session context, hours of recovery
- **Guard**: ALWAYS backup before migrations
- **Check**: Verify data integrity after migration
- **Implementation**:
  ```powershell
  # âœ… DO: Backup before migration
  Copy-Item "memory.json" "memory.json.backup"
  # ... run migration ...
  # Verify backup exists and is valid
  
  # âŒ DON'T: Skip backup
  # ... migrate directly ...
  ```
- **Exception**: Small data sets under 1MB don't need backup (still test)
- **Validation**: Test migration on backup data first
- **Status**: âœ… Implemented

---

## Rule #8: Config Validation Must Happen Before Startup
- **Root Cause**: Syntax error in config file undetected
- **Consequence**: Agents couldn't read their role definitions
- **Guard**: Run validation on every config change
- **Check**: `openclaw doctor` before `openclaw restart`
- **Implementation**:
  ```powershell
  # âœ… DO: Always validate
  openclaw doctor
  if ($LASTEXITCODE -ne 0) { exit 1 }
  openclaw restart
  
  # âŒ DON'T: Skip validation
  # openclaw restart # May fail mysteriously
  ```
- **Exception**: None
- **Validation**: Introduce syntax errors and catch with doctor
- **Status**: âœ… Implemented

---

## Rule #9: Memory Directory Must Exist and Be Writable
- **Root Cause**: Memory directory didn't exist
- **Consequence**: No learning capture, system state lost
- **Guard**: Create and verify memory directory on startup
- **Check**: Test write permissions before relying on directory
- **Implementation**:
  ```powershell
  # âœ… DO: Ensure directory exists
  $memDir = "C:\Users\User\.openclaw\workspace\memory"
  if (!(Test-Path $memDir)) { mkdir $memDir -Force }
  
  # Test write permission
  "test" | Out-File "$memDir/test.txt" -Force
  Remove-Item "$memDir/test.txt"
  ```
- **Exception**: None for critical memory system
- **Validation**: Test after creating directory
- **Status**: âœ… Implemented

---

## Rule #10: Never Assume External Services Are Available
- **Root Cause**: No fallback when external service down
- **Consequence**: Messages silently lost, no user notification
- **Guard**: Implement fallback for all external services
- **Check**: Queue messages when service unavailable, retry later
- **Implementation**:
  ```javascript
  // âœ… DO: Fallback to queue
  try {
    const result = await sendViaAPI(message);
    return result;
  } catch (e) {
    queueMessage(message);
    return { queued: true };
  }
  
  // âŒ DON'T: Fail if service unavailable
  // const result = await sendViaAPI(message); // Throws if API down
  ```
- **Exception**: None
- **Validation**: Test with API unavailable
- **Status**: âœ… Implemented

---

## Rule #11: Learning Capture Must Be Automated
- **Root Cause**: Relying on manual discipline
- **Consequence**: Only 40% of learnings captured, patterns missed
- **Guard**: Automate learning capture with scheduled tasks
- **Check**: Verify cron job runs and creates daily log
- **Implementation**:
  ```powershell
  # âœ… DO: Schedule daily capture
  Register-ScheduledTask -TaskName "Daily-Learning" `
    -Trigger (New-ScheduledTaskTrigger -Daily -At 21:00)
  
  # âŒ DON'T: Manual reminder
  # Reminder: "Remember to log what you learned"
  ```
- **Exception**: None for critical learning system
- **Validation**: Check daily logs exist every morning
- **Status**: âœ… Implemented

---

## Rule #12: File Size Limits Prevent Transcription Failures
- **Root Cause**: No file size validation before processing
- **Consequence**: Task hung for 5 minutes, then failed
- **Guard**: Validate file size before transcription
- **Check**: Max 50MB for fast models, 100MB for larger models
- **Implementation**:
  ```powershell
  # âœ… DO: Check file size
  $file = Get-Item "audio.mp3"
  if ($file.Length -gt 50MB) { 
    Write-Error "File too large"
    exit 1
  }
  
  # âŒ DON'T: Assume file is reasonable
  # whisper "audio.mp3" # May timeout on large file
  ```
- **Exception**: Can compress or split large files
- **Validation**: Test with various file sizes
- **Status**: âœ… Implemented

---

## Rule #13: Concurrency Requires Locking
- **Root Cause**: No file locking mechanism
- **Consequence**: Data corruption, partial writes
- **Guard**: Use file locking for shared resources
- **Check**: Lock before write, release after
- **Implementation**:
  ```javascript
  // âœ… DO: File locking
  const lockFile = file + '.lock';
  fs.writeFileSync(lockFile, JSON.stringify({pid: process.pid}));
  try {
    // ... write file ...
  } finally {
    fs.unlinkSync(lockFile);
  }
  
  // âŒ DON'T: Direct writes
  // fs.writeFileSync(file, data); // No locking
  ```
- **Exception**: None for shared data
- **Validation**: Simulate concurrent writes
- **Status**: âœ… Implemented

---

## Rule #14: Config Keys Must Be Consistent
- **Root Cause**: Manual config editing with inconsistent formatting
- **Consequence**: Agent couldn't read role definition
- **Guard**: Use schema validation for config files
- **Check**: Validate against schema before loading
- **Implementation**:
  ```javascript
  // âœ… DO: Schema validation
  const schema = {
    agents: {
      defaults: {
        model: { type: 'object', required: true },
        workspace: { type: 'string', required: true }
      }
    }
  };
  validateConfig(config, schema);
  
  // âŒ DON'T: Assume config is correct
  // const model = config.agents.defaults.model; // May be undefined
  ```
- **Exception**: None for critical configs
- **Validation**: Test with broken configs
- **Status**: â³ In Progress

---

## Rule #15: Recovery Must Be Faster Than Prevention
- **Root Cause**: No backup or recovery procedure
- **Consequence**: Lost time, lost data
- **Guard**: Automatic backups with easy recovery
- **Check**: Test recovery procedure monthly
- **Implementation**:
  ```powershell
  # âœ… DO: Automatic backup
  Copy-Item "jobs.json" "jobs.json.bak"
  
  # âœ… DO: Easy recovery
  Copy-Item "jobs.json.bak" "jobs.json"
  
  # âŒ DON'T: Manual recovery
  # "Manually reconstruct from memory..."
  ```
- **Exception**: None
- **Validation**: Simulate failure and test recovery
- **Status**: âœ… Implemented

---

## Rule #16: Never Load Daily Notes at Startup
- **Root Cause**: Loading all memory files at heartbeat instead of on-demand
- **Consequence**: ~20K tokens consumed at startup, leaving insufficient context for actual work
- **Guard**: Daily notes are archives. Load only `MEMORY.md` + `projects.md` at heartbeat. Load daily notes only when the user asks about specific past work.
- **Check**: Startup context must stay under ~4K tokens
- **Implementation**:
  ```
  # âœ… DO: Smart loading
  Read memory/projects.md       # ~1K tokens
  Read MEMORY.md                # ~3K tokens
  # Total: ~4K tokens at startup
  
  # Load on-demand only:
  # memory/YYYY-MM-DD.md    â†’ when asked about past work
  # Vector DB search        â†’ when a specific past-work question comes up
  
  # âŒ DON'T: Load everything
  # Read all memory/*.md files at startup  # Blows token budget
  ```
- **Exception**: None
- **Validation**: Monitor token usage at heartbeat; flag if startup exceeds 5K tokens
- **Status**: âœ… Implemented

---

## Rule #17: Vector DB Must Stay in Sync With Memory Files
- **Origin Failure**: Semantic search returning stale results after MEMORY.md rewrite (2026-03-06)
- **Root Cause**: memory_flush.py not run after curation, so embeddings reflected old content
- **Consequence**: Vector search results contradicted current MEMORY.md, causing agent confusion
- **Guard**: Always run `memory_flush.py` after any write to MEMORY.md or daily notes. Also run at every heartbeat (idempotent â€” `total_stored = 0` means nothing to do).
- **Check**: After any memory write, verify flush completes without error
- **Implementation**:
  ```python
  # âœ… DO: Flush after every memory write
  python3 ~/.openclaw/workspace/skills/vector-memory/scripts/memory_flush.py
  # total_stored = 0 is fine â€” means files unchanged since last flush
  
  # âœ… DO: Flush in heartbeat sequence (step 3 of every heartbeat)
  
  # âŒ DON'T: Skip flush after auto-curation rewrites MEMORY.md
  # âŒ DON'T: Assume vector DB is current without flushing
  ```
- **Exception**: Can skip flush for writes to heartbeat-state.json (non-memory metadata)
- **Validation**: Run a semantic search after flush and verify results match current MEMORY.md
- **Status**: âœ… Implemented

---

## Rule #18: projects.md Must Stay Under 180 Lines
- **Origin Failure**: projects.md bloated with stale entries, heartbeat token cost crept up (2026-03-06)
- **Root Cause**: Entries added over time with no trim policy
- **Consequence**: File that should cost ~1K tokens started costing 3K+, defeating smart loading
- **Guard**: Cap projects.md at 80 lines. On every auto-curation run, prune completed/dead projects to an archive section or remove them entirely.
- **Check**: `(Get-Content memory/projects.md).Count` â€” alert if > 80
- **Implementation**:
  ```powershell
  # âœ… DO: Check line count before adding entry
  $lines = (Get-Content "memory/projects.md").Count
  if ($lines -gt 75) { 
    # Prune stale entries first, then add
  }
  
  # âŒ DON'T: Keep appending without trimming
  ```
- **Exception**: Can temporarily exceed 80 lines during curation rewrite; must be under by end of run
- **Validation**: Check line count after every curation cron run
- **Status**: âœ… Implemented

---

## Rule #101: The Deadlock Reset
- **Origin Failure**: Agent entered apology loop instead of completing task
- **Root Cause**: Model over-indexed on refusal/limitation language under ambiguous instructions
- **Consequence**: Task not completed, user received unhelpful non-answer
- **Guard**: If output contains the phrase "I am truly and utterly sorry" or "limitations," do not send. Re-roll using a simplified Safe-Mode prompt and flag for manual review.
- **Check**: Scan outgoing message text before delivery
- **Exception**: None
- **Status**: âœ… Implemented

---


## Rule #19: Pre-approve WhatsApp Monthly Reminders
- **Root Cause**: Manual intervention required for monthly reminders (Jnr, Hughie, Janet)
- **Consequence**: Reminders may be missed if agent not proactive
- **Guard**: Create automated cron jobs for monthly reminders with pre-approved messages
- **Implementation**:
  - Jnr: 1st of month, 10am UK time - "Hey Jnr, just checking in. How's everything going?"
  - Hughie: 21st of month, 10am UK time - "Greetings, just reminding you..."
  - Janet: Fridays 8:30pm Ghana time - Weekly check-in with warm, playful tone
- **Status**: Proposed

## Rule #20: Specify Delivery Channel for Multi-Channel Cron Jobs
- **Root Cause**: Cron jobs failing with "Channel is required when multiple channels are configured: telegram, whatsapp"
- **Consequence**: Health logs, business check-ins, family contact automation failing
- **Guard**: Always specify delivery.channel parameter in cron job configuration when multiple channels are enabled
- **Implementation**:
  `json
  "cron": {
    "jobs": {
      "health-log-afternoon": {
        "delivery": {
          "channel": "telegram",
          "target": "3620024352",
          "thread": "50"
        }
      }
    }
  }
  `
- **Status**: Immediate action required

---
## Rule #25: WhatsApp Gateway 499 Errors Must Be Monitored and Escalated
- **Origin Failure**: WhatsApp Gateway error codes 499 persist (from 2026-03-28), causing 60-second disconnect cycles.
- **Root Cause**: Lack of systematic monitoring and escalation for error threshold.
- **Consequence**: Service disruption, degraded performance, potential data loss.
- **Guard**: Monitor WhatsApp Gateway error counts per hour; escalate if threshold of 10 errors per hour exceeded.
- **Check**: Track error code 499 occurrences with timestamps; alert when threshold exceeded.
- **Implementation**: Create monitoring script that logs error codes, counts per hour, and triggers escalation via #urgent topic.
- **Exception**: None for critical error patterns.
- **Validation**: Simulate error spike and verify escalation triggers.
- **Status**: Proposed (from 2026-03-29 consolidation).

---

## Rule #26: Telegram Bot Membership Must Be Verified Before Enabling Telegram Channel
- **Origin Failure**: Telegram bot not member of authorized group -1003620024352, resulting in unauthorized routing attempts and webhook errors.
- **Root Cause**: Missing verification step before enabling Telegram channel.
- **Consequence**: All outbound Telegram messages blocked, configuration errors persist, unauthorized routing attempts logged.
- **Guard**: Verify bot membership in authorized group before enabling Telegram channel; run `openclaw channels status` daily to confirm.
- **Check**: Daily verification that bot can send messages to group -1003620024352 and authorized topics.
- **Implementation**: Add verification step to startup; ensure bot is added to group as administrator with permission to send messages.
- **Exception**: None for authorized groups.
- **Validation**: Test sending test message to group after membership confirmed.
- **Status**: Proposed (from 2026-03-29 consolidation).

---

## Rule #27: Daily Learning Capture Must Include Rule Proposals for Each Failure Documented
- **Origin Failure**: Daily learning capture did not include rule proposals for failures documented.
- **Root Cause**: Learning capture template missing rule proposal section.
- **Consequence**: Failures not translated into actionable guards.
- **Guard**: Include rule proposals for each failure documented in daily learning entries.
- **Check**: Verify each failure has a corresponding rule proposal.
- **Implementation**: Add rule proposal section to daily learning template (e.g., "Rule Proposals": list under "What Failed Today").
- **Exception**: None for daily learning capture.
- **Validation**: Review daily learning entries for rule proposals.
- **Status**: Proposed (from 2026-03-29 consolidation).

---

## Rule #28: Daily Learning Entries Must Be Created Proactively During Sessions
- **Origin Failure**: Daily learning entries only created by cron job, missing proactive capture during sessions.
- **Root Cause**: No proactive learning capture process integrated into session workflow.
- **Consequence**: Learning opportunities missed, reactive capture leads to incomplete lessons.
- **Guard**: Create daily learning entries during sessions, not just at cron-triggered afterthoughts.
- **Check**: Review session logs for proactive learning entries (e.g., immediate documentation of insights).
- **Implementation**: Add learning capture step to session completion checklist.
- **Exception**: None for daily learning capture.
- **Validation**: Check daily memory files for proactive entries.
- **Status**: Proposed (from 2026-03-31 consolidation).

---

## Rule #29: When Referencing Templates, Extract and Bookmark Specific Sections for Faster Future Access
- **Origin Failure**: Template reference delay due to searching through LEARNING_SYSTEM.md.
- **Root Cause**: No quick access to template sections; manual search required.
- **Consequence**: Time wasted searching, potential errors in template usage.
- **Guard**: Extract and bookmark template sections for faster future access.
- **Check**: Verify template sections are bookmarked in documentation.
- **Implementation**: Create index of template sections with line numbers or quick links.
- **Exception**: None for templates.
- **Validation**: Test template referencing speed improvement.
- **Status**: Proposed (from 2026-03-31 consolidation).

---

## Rule #30: All Daily Memory Files Should Contain Both System Status AND Learning Sections
- **Origin Failure**: Daily memory file had only health check, missing learning section.
- **Root Cause**: Memory file template missing learning section.
- **Consequence**: Learning content not captured in daily memory.
- **Guard**: Include both system status and learning sections in daily memory files.
- **Check**: Verify each daily memory file has both sections.
- **Implementation**: Update daily memory template to include learning section.
- **Exception**: None for daily memory files.
- **Validation**: Review daily memory files for completeness.
- **Status**: Proposed (from 2026-03-31 consolidation).

---
##  Rule #31: Addproperly, not as a spam append
-Before appending to any system file, check the last 20 lines for today's date or identical content. If found, STOP. Never append without a uniqueness check.

---

## Adding New Rules

When a failure occurs:

1. **Document immediately**: What happened? Why?
2. **Identify root cause**: Was it a code bug? Missing check? Assumption?
3. **Create guard**: How do we prevent this?
4. **Test the guard**: Does it actually prevent the failure?
5. **Add to RULES.md**: Include origin, consequence, implementation
6. **Monitor**: Track false positives
7. **Update docs**: Educate the system about the new rule

---

**Total Rules**: 18 (+ Rule #101)
**Status**: Active and monitored
**Last Updated**: 2026-03-06
**Next Review**: Weekly (Monday 9am)




























































































































