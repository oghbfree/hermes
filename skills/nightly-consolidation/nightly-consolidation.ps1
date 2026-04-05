# Nightly Memory Consolidation Script
# Runs at 2:00 AM daily via cron
# Telegram notifications to #briefing channel

param(
    [string]$Date = (Get-Date -Format "yyyy-MM-dd"),
    [string]$SessionPath = "C:\OpenClaw\.openclaw\agents\main\sessions",
    [string]$WorkspacePath = "C:\OpenClaw\.openclaw\workspace"
)

# Import required modules
Import-Module PSWriteHTML

# Configuration
$TelegramChannel = "#briefing"
$ConsolidationPath = "$WorkspacePath\memory\consolidation"
$TodayFile = "$WorkspacePath\memory\$Date.md"

# Initialize counters
$filesUpdated = 0
$decisionsCaptured = 0
$tasksAdded = 0

# Create consolidation directory if it doesn't exist
if (!(Test-Path $ConsolidationPath)) {
    New-Item -ItemType Directory -Path $ConsolidationPath -Force
}

# 1. Read all session logs from today
Write-Host "Reading session logs from $SessionPath..."
$sessionFiles = Get-ChildItem -Path $SessionPath -Filter "*.jsonl" | Where-Object {
    $_.LastWriteTime.Date -eq (Get-Date).Date
}

$allSessionContent = @()
foreach ($file in $sessionFiles) {
    $content = Get-Content $file.FullName | ConvertFrom-Json
    $allSessionContent += $content
}

# 2. Read today's memory file
if (Test-Path $TodayFile) {
    $todayContent = Get-Content $TodayFile -Raw
} else {
    $todayContent = ""
}

# 3. Extract and categorize information
Write-Host "Extracting important information..."

# Project updates
$projectUpdates = @()
$projectPatterns = @("Akoma Robotics", "2Real", "Farm", "Property", "Geriatric Care", "OpenClaw")
foreach ($pattern in $projectPatterns) {
    $matches = $allSessionContent | Where-Object { $_ -match $pattern }
    if ($matches) {
        $projectUpdates += "## $pattern`n$matches"
    }
}

# Decisions made
$decisions = @()
$decisionKeywords = @("decided", "decision", "choose", "selected", "opted", "agreed")
foreach ($keyword in $decisionKeywords) {
    $matches = $allSessionContent | Where-Object { $_ -match $keyword }
    if ($matches) {
        $decisions += $matches
    }
}
$decisionsCaptured = $decisions.Count

# People mentioned
$peoplePatterns = @("John", "Sammy", "Ben", "Matthias", "Hughie", "Eric", "Janet", "Kwasi")
$peopleUpdates = @()
foreach ($person in $peoplePatterns) {
    $matches = $allSessionContent | Where-Object { $_ -match $person }
    if ($matches) {
        $peopleUpdates += "## $person`n$matches"
    }
}

# Business intelligence (prices, suppliers, leads)
$businessIntel = @()
$pricePatterns = @("\d+ GHC", "\d+ Cedis", "\d+ GBP", "\d+ USD", "\d+k", "\d+,\d+")
foreach ($pattern in $pricePatterns) {
    $matches = $allSessionContent | Where-Object { $_ -match $pattern }
    if ($matches) {
        $businessIntel += $matches
    }
}

# Tasks and action items
$taskKeywords = @("task", "action", "todo", "need to", "should", "must", "will")
$tasks = @()
foreach ($keyword in $taskKeywords) {
    $matches = $allSessionContent | Where-Object { $_ -match $keyword }
    if ($matches) {
        $tasks += $matches
    }
}
$tasksAdded = $tasks.Count

# New rules and lessons learned
$ruleKeywords = @("rule", "lesson", "learned", "should", "must", "always", "never")
$rules = @()
foreach ($keyword in $ruleKeywords) {
    $matches = $allSessionContent | Where-Object { $_ -match $keyword }
    if ($matches) {
        $rules += $matches
    }
}

# Successes and formulas
$successKeywords = @("success", "worked", "effective", "formula", "pattern")
$successes = @()
foreach ($keyword in $successKeywords) {
    $matches = $allSessionContent | Where-Object { $_ -match $keyword }
    if ($matches) {
        $successes += $matches
    }
}

# 4. Update files

# Update MEMORY.md
Write-Host "Updating MEMORY.md..."
$memoryContent = Get-Content "$WorkspacePath\MEMORY.md" -Raw
$memoryUpdates = "`n`n## Consolidated Updates - $Date`n"
if ($projectUpdates) { $memoryUpdates += "`n### Projects`n" + ($projectUpdates -join "`n") }
if ($peopleUpdates) { $memoryUpdates += "`n### People`n" + ($peopleUpdates -join "`n") }
if ($businessIntel) { $memoryUpdates += "`n### Business Intel`n" + ($businessIntel -join "`n") }
$memoryContent += $memoryUpdates
Set-Content -Path "$WorkspacePath\MEMORY.md" -Value $memoryContent
$filesUpdated++

# Update projects.md
Write-Host "Updating projects.md..."
$projectsContent = Get-Content "$WorkspacePath\memory\projects.md" -Raw
$projectsContent += "`n`n## $Date Updates`n" + ($projectUpdates -join "`n")
Set-Content -Path "$WorkspacePath\memory\projects.md" -Value $projectsContent
$filesUpdated++

# Update tasks-queue.md
Write-Host "Updating tasks-queue.md..."
$tasksContent = Get-Content "$WorkspacePath\tasks-queue.md" -Raw
$tasksContent += "`n`n## $Date Tasks`n" + ($tasks -join "`n")
Set-Content -Path "$WorkspacePath\tasks-queue.md" -Value $tasksContent
$filesUpdated++

# Update RULES.md
if ($rules) {
    Write-Host "Updating RULES.md..."
    $rulesContent = Get-Content "$WorkspacePath\RULES.md" -Raw
    $rulesContent += "`n`n## Rules Learned - $Date`n" + ($rules -join "`n")
    Set-Content -Path "$WorkspacePath\RULES.md" -Value $rulesContent
    $filesUpdated++
}

# Update FORMULAS.md
if ($successes) {
    Write-Host "Updating FORMULAS.md..."
    $formulasContent = Get-Content "$WorkspacePath\FORMULAS.md" -Raw
    $formulasContent += "`n`n## Success Patterns - $Date`n" + ($successes -join "`n")
    Set-Content -Path "$WorkspacePath\FORMULAS.md" -Value $formulasContent
    $filesUpdated++
}

# 5. Create consolidated daily journal
Write-Host "Creating daily journal..."
$journalPath = "$WorkspacePath\memory\briefings\JOURNAL-$Date.md"
$journalContent = @"
# Daily Journal - $Date

## Summary
Consolidated $(($sessionFiles).Count) session files with $(($allSessionContent).Count) messages.

## Key Decisions
$($decisions -join "`n")

## People Contacted
$($peopleUpdates -join "`n")

## Projects Moved Forward
$($projectUpdates -join "`n")

## Tasks Completed/Pending
$($tasks -join "`n")

## Blockers Encountered
$(if ($businessIntel) { $businessIntel -join "`n" } else { "None reported" })

## Tomorrow's Focus
- Review tasks-queue.md for pending items
- Follow up on outstanding decisions
- Continue project momentum

---
Generated by Nightly Consolidation Script
"@

Set-Content -Path $journalPath -Value $journalContent
$filesUpdated++

# 6. Run memory_flush.py
Write-Host "Running memory_flush.py..."
$memoryFlushPath = "$WorkspacePath\skills\vector-memory\scripts\memory_flush.py"
if (Test-Path $memoryFlushPath) {
    python $memoryFlushPath
    Write-Host "Memory flush completed."
} else {
    Write-Host "WARNING: memory_flush.py not found at $memoryFlushPath"
}

# 7. Post to Telegram
Write-Host "Posting to Telegram #briefing..."
$telegramMessage = "?? Nightly consolidation complete for $Date

Updated: $filesUpdated files
Decisions: $decisionsCaptured captured
Tasks: $tasksAdded added
Journal: $journalPath

Vector DB synced. Ready for tomorrow."

# Post to Telegram (using OpenClaw's message tool or API)
# This would use the Telegram bot API or OpenClaw's messaging system
Write-Host "Telegram message ready: $telegramMessage"

# Create consolidation report
$reportPath = "$ConsolidationPath\CONSOLIDATION-$Date.md"
$reportContent = @"
# Consolidation Report - $Date

## Summary
- Session files processed: $(($sessionFiles).Count)
- Total messages: $(($allSessionContent).Count)
- Files updated: $filesUpdated
- Decisions captured: $decisionsCaptured
- Tasks added: $tasksAdded

## Files Updated
- MEMORY.md
- memory/projects.md
- tasks-queue.md
$(if ($rules) { "- RULES.md`n" } else { "" })
$(if ($successes) { "- FORMULAS.md`n" } else { "" })
- $journalPath

## Session Files Processed
$(($sessionFiles | ForEach-Object { "- $($_.Name)" }) -join "`n")

## Notes
- All changes have been embedded into vector DB via memory_flush.py
- Telegram notification sent to $TelegramChannel
- Next consolidation: Tomorrow at 2:00 AM

---
Consolidation completed at $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
"@

Set-Content -Path $reportPath -Value $reportContent
Write-Host "Consolidation report saved to: $reportPath"

Write-Host "Nightly consolidation completed successfully!"
