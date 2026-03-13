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
  # ✅ DO: Use environment variables
  $apiKey = $env:OPENROUTER_API_KEY
  
  # ❌ DON'T: Store in config
  # "apiKey": "sk-or-v1-..."
  ```
- **Exception**: None for critical credentials
- **Validation**: Automated key detection before any output
- **Status**: ✅ Implemented

---

## Rule #2: Always Validate File Paths Before Operations
- **Root Cause**: Assuming directory exists without checking
- **Consequence**: Task failed silently, no error handling
- **Guard**: Check path.exists() and create if needed
- **Check**: `if (!(Test-Path $path)) { mkdir $path -Force }`
- **Implementation**:
  ```powershell
  # ✅ DO: Validate and create
  $dir = "C:\Users\User\.openclaw\workspace\memory"
  if (!(Test-Path $dir)) { mkdir $dir -Force }
  
  # ❌ DON'T: Assume it exists
  # Write-Host "Writing to $dir..." # Error if dir missing
  ```
- **Exception**: Can create parent directories with `-Force` flag
- **Validation**: Test with missing paths
- **Status**: ✅ Implemented

---

## Rule #3: Memory Writes Must Be Atomic
- **Root Cause**: Process interrupted during file write
- **Consequence**: Lost all cron jobs, unrecoverable data
- **Guard**: Write to temp file, then atomic rename
- **Check**: Always use temp + rename pattern for important files
- **Implementation**:
  ```powershell
  # ✅ DO: Atomic write pattern
  $temp = "$path.tmp"
  $content | Set-Content $temp
  Move-Item $temp $path -Force
  
  # ❌ DON'T: Direct write
  # $content | Set-Content $path
  ```
- **Exception**: None for data files; safe for logs
- **Validation**: Simulate power failure during write
- **Status**: ✅ Implemented

---

## Rule #4: Never Block on External APIs
- **Root Cause**: No timeout on HTTP request to Telegram
- **Consequence**: System unresponsive for 30+ seconds
- **Guard**: Set timeouts on ALL external calls, use async
- **Check**: Every API call must have timeout < 5 seconds
- **Implementation**:
  ```javascript
  // ✅ DO: Async with timeout
  const timeout = new Promise((_, r) => 
    setTimeout(() => r(new Error('timeout')), 5000)
  );
  const result = await Promise.race([apiCall(), timeout]);
  
  // ❌ DON'T: Blocking wait
  // const result = await apiCall(); // No timeout
  ```
- **Exception**: Can retry up to 3x with exponential backoff
- **Validation**: Test with slow/unreachable API
- **Status**: ✅ Implemented

---

## Rule #5: Always Validate User Input Before Processing
- **Root Cause**: No input sanitization or bounds checking
- **Consequence**: Bot stopped responding, manual restart needed
- **Guard**: Sanitize and validate all inputs
- **Check**: Type checking, bounds validation, length limits
- **Implementation**:
  ```javascript
  // ✅ DO: Validate input
  if (!message || typeof message !== 'string' || message.length > 4096) {
    throw new Error('Invalid message');
  }
  
  // ❌ DON'T: Trust user input
  // processMessage(message); // No validation
  ```
- **Exception**: None for security-critical inputs
- **Validation**: Fuzz test with random/extreme inputs
- **Status**: ✅ Implemented

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
- **Status**: ✅ Implemented

---

## Rule #7: Test Migrations Before Deployment
- **Root Cause**: Migrated live data without testing first
- **Consequence**: Lost session context, hours of recovery
- **Guard**: ALWAYS backup before migrations
- **Check**: Verify data integrity after migration
- **Implementation**:
  ```powershell
  # ✅ DO: Backup before migration
  Copy-Item "memory.json" "memory.json.backup"
  # ... run migration ...
  # Verify backup exists and is valid
  
  # ❌ DON'T: Skip backup
  # ... migrate directly ...
  ```
- **Exception**: Small data sets under 1MB don't need backup (still test)
- **Validation**: Test migration on backup data first
- **Status**: ✅ Implemented

---

## Rule #8: Config Validation Must Happen Before Startup
- **Root Cause**: Syntax error in config file undetected
- **Consequence**: Agents couldn't read their role definitions
- **Guard**: Run validation on every config change
- **Check**: `openclaw doctor` before `openclaw restart`
- **Implementation**:
  ```powershell
  # ✅ DO: Always validate
  openclaw doctor
  if ($LASTEXITCODE -ne 0) { exit 1 }
  openclaw restart
  
  # ❌ DON'T: Skip validation
  # openclaw restart # May fail mysteriously
  ```
- **Exception**: None
- **Validation**: Introduce syntax errors and catch with doctor
- **Status**: ✅ Implemented

---

## Rule #9: Memory Directory Must Exist and Be Writable
- **Root Cause**: Memory directory didn't exist
- **Consequence**: No learning capture, system state lost
- **Guard**: Create and verify memory directory on startup
- **Check**: Test write permissions before relying on directory
- **Implementation**:
  ```powershell
  # ✅ DO: Ensure directory exists
  $memDir = "C:\Users\User\.openclaw\workspace\memory"
  if (!(Test-Path $memDir)) { mkdir $memDir -Force }
  
  # Test write permission
  "test" | Out-File "$memDir/test.txt" -Force
  Remove-Item "$memDir/test.txt"
  ```
- **Exception**: None for critical memory system
- **Validation**: Test after creating directory
- **Status**: ✅ Implemented

---

## Rule #10: Never Assume External Services Are Available
- **Root Cause**: No fallback when external service down
- **Consequence**: Messages silently lost, no user notification
- **Guard**: Implement fallback for all external services
- **Check**: Queue messages when service unavailable, retry later
- **Implementation**:
  ```javascript
  // ✅ DO: Fallback to queue
  try {
    const result = await sendViaAPI(message);
    return result;
  } catch (e) {
    queueMessage(message);
    return { queued: true };
  }
  
  // ❌ DON'T: Fail if service unavailable
  // const result = await sendViaAPI(message); // Throws if API down
  ```
- **Exception**: None
- **Validation**: Test with API unavailable
- **Status**: ✅ Implemented

---

## Rule #11: Learning Capture Must Be Automated
- **Root Cause**: Relying on manual discipline
- **Consequence**: Only 40% of learnings captured, patterns missed
- **Guard**: Automate learning capture with scheduled tasks
- **Check**: Verify cron job runs and creates daily log
- **Implementation**:
  ```powershell
  # ✅ DO: Schedule daily capture
  Register-ScheduledTask -TaskName "Daily-Learning" `
    -Trigger (New-ScheduledTaskTrigger -Daily -At 21:00)
  
  # ❌ DON'T: Manual reminder
  # Reminder: "Remember to log what you learned"
  ```
- **Exception**: None for critical learning system
- **Validation**: Check daily logs exist every morning
- **Status**: ✅ Implemented

---

## Rule #12: File Size Limits Prevent Transcription Failures
- **Root Cause**: No file size validation before processing
- **Consequence**: Task hung for 5 minutes, then failed
- **Guard**: Validate file size before transcription
- **Check**: Max 50MB for fast models, 100MB for larger models
- **Implementation**:
  ```powershell
  # ✅ DO: Check file size
  $file = Get-Item "audio.mp3"
  if ($file.Length -gt 50MB) { 
    Write-Error "File too large"
    exit 1
  }
  
  # ❌ DON'T: Assume file is reasonable
  # whisper "audio.mp3" # May timeout on large file
  ```
- **Exception**: Can compress or split large files
- **Validation**: Test with various file sizes
- **Status**: ✅ Implemented

---

## Rule #13: Concurrency Requires Locking
- **Root Cause**: No file locking mechanism
- **Consequence**: Data corruption, partial writes
- **Guard**: Use file locking for shared resources
- **Check**: Lock before write, release after
- **Implementation**:
  ```javascript
  // ✅ DO: File locking
  const lockFile = file + '.lock';
  fs.writeFileSync(lockFile, JSON.stringify({pid: process.pid}));
  try {
    // ... write file ...
  } finally {
    fs.unlinkSync(lockFile);
  }
  
  // ❌ DON'T: Direct writes
  // fs.writeFileSync(file, data); // No locking
  ```
- **Exception**: None for shared data
- **Validation**: Simulate concurrent writes
- **Status**: ✅ Implemented

---

## Rule #14: Config Keys Must Be Consistent
- **Root Cause**: Manual config editing with inconsistent formatting
- **Consequence**: Agent couldn't read role definition
- **Guard**: Use schema validation for config files
- **Check**: Validate against schema before loading
- **Implementation**:
  ```javascript
  // ✅ DO: Schema validation
  const schema = {
    agents: {
      defaults: {
        model: { type: 'object', required: true },
        workspace: { type: 'string', required: true }
      }
    }
  };
  validateConfig(config, schema);
  
  // ❌ DON'T: Assume config is correct
  // const model = config.agents.defaults.model; // May be undefined
  ```
- **Exception**: None for critical configs
- **Validation**: Test with broken configs
- **Status**: ⏳ In Progress

---

## Rule #15: Recovery Must Be Faster Than Prevention
- **Root Cause**: No backup or recovery procedure
- **Consequence**: Lost time, lost data
- **Guard**: Automatic backups with easy recovery
- **Check**: Test recovery procedure monthly
- **Implementation**:
  ```powershell
  # ✅ DO: Automatic backup
  Copy-Item "jobs.json" "jobs.json.bak"
  
  # ✅ DO: Easy recovery
  Copy-Item "jobs.json.bak" "jobs.json"
  
  # ❌ DON'T: Manual recovery
  # "Manually reconstruct from memory..."
  ```
- **Exception**: None
- **Validation**: Simulate failure and test recovery
- **Status**: ✅ Implemented

---

## Rule #16: Never Load Daily Notes at Startup
- **Root Cause**: Loading all memory files at heartbeat instead of on-demand
- **Consequence**: ~20K tokens consumed at startup, leaving insufficient context for actual work
- **Guard**: Daily notes are archives. Load only `MEMORY.md` + `projects.md` at heartbeat. Load daily notes only when the user asks about specific past work.
- **Check**: Startup context must stay under ~4K tokens
- **Implementation**:
  ```
  # ✅ DO: Smart loading
  Read memory/projects.md       # ~1K tokens
  Read MEMORY.md                # ~3K tokens
  # Total: ~4K tokens at startup
  
  # Load on-demand only:
  # memory/YYYY-MM-DD.md    → when asked about past work
  # Vector DB search        → when a specific past-work question comes up
  
  # ❌ DON'T: Load everything
  # Read all memory/*.md files at startup  # Blows token budget
  ```
- **Exception**: None
- **Validation**: Monitor token usage at heartbeat; flag if startup exceeds 5K tokens
- **Status**: ✅ Implemented

---

## Rule #17: Vector DB Must Stay in Sync With Memory Files
- **Origin Failure**: Semantic search returning stale results after MEMORY.md rewrite (2026-03-06)
- **Root Cause**: memory_flush.py not run after curation, so embeddings reflected old content
- **Consequence**: Vector search results contradicted current MEMORY.md, causing agent confusion
- **Guard**: Always run `memory_flush.py` after any write to MEMORY.md or daily notes. Also run at every heartbeat (idempotent — `total_stored = 0` means nothing to do).
- **Check**: After any memory write, verify flush completes without error
- **Implementation**:
  ```python
  # ✅ DO: Flush after every memory write
  python3 ~/.openclaw/workspace/skills/vector-memory/scripts/memory_flush.py
  # total_stored = 0 is fine — means files unchanged since last flush
  
  # ✅ DO: Flush in heartbeat sequence (step 3 of every heartbeat)
  
  # ❌ DON'T: Skip flush after auto-curation rewrites MEMORY.md
  # ❌ DON'T: Assume vector DB is current without flushing
  ```
- **Exception**: Can skip flush for writes to heartbeat-state.json (non-memory metadata)
- **Validation**: Run a semantic search after flush and verify results match current MEMORY.md
- **Status**: ✅ Implemented

---

## Rule #18: projects.md Must Stay Under 180 Lines
- **Origin Failure**: projects.md bloated with stale entries, heartbeat token cost crept up (2026-03-06)
- **Root Cause**: Entries added over time with no trim policy
- **Consequence**: File that should cost ~1K tokens started costing 3K+, defeating smart loading
- **Guard**: Cap projects.md at 80 lines. On every auto-curation run, prune completed/dead projects to an archive section or remove them entirely.
- **Check**: `(Get-Content memory/projects.md).Count` — alert if > 80
- **Implementation**:
  ```powershell
  # ✅ DO: Check line count before adding entry
  $lines = (Get-Content "memory/projects.md").Count
  if ($lines -gt 75) { 
    # Prune stale entries first, then add
  }
  
  # ❌ DON'T: Keep appending without trimming
  ```
- **Exception**: Can temporarily exceed 80 lines during curation rewrite; must be under by end of run
- **Validation**: Check line count after every curation cron run
- **Status**: ✅ Implemented

---

## Rule #101: The Deadlock Reset
- **Origin Failure**: Agent entered apology loop instead of completing task
- **Root Cause**: Model over-indexed on refusal/limitation language under ambiguous instructions
- **Consequence**: Task not completed, user received unhelpful non-answer
- **Guard**: If output contains the phrase "I am truly and utterly sorry" or "limitations," do not send. Re-roll using a simplified Safe-Mode prompt and flag for manual review.
- **Check**: Scan outgoing message text before delivery
- **Exception**: None
- **Status**: ✅ Implemented

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
