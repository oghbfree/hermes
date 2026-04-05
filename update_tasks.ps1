$lines = Get-Content "C:\OpenClaw\.openclaw\workspace\tasks-queue.md"
# Find line index of "_(No pending tasks)_"
$pendingIndex = -1
for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match "No pending tasks") {
        $pendingIndex = $i
        break
    }
}
Write-Host "Pending index: $pendingIndex"
# Replace that line with pending tasks
$pendingTasks = @(
    "### [2026-03-28 22:10] - Pending",
    "- **Source**: Cron Job (nightly-consolidation)",
    "- **Instruction**: Resolve critical system issues identified today",
    "- **Action**: Add bot to group -1003620024352 as administrator, resolve webhook 404 errors, monitor WhatsApp Gateway for 499 error recurrence, document error pattern baseline (428, 408, 499), follow up on John's Facebook ads response, follow up on spray paint coordination with John, monitor Akoma credentials file, review cron job target configurations, document recovery process for WhatsApp Gateway issues",
    "- **Target**: System configuration, WhatsApp Gateway, Telegram bot",
    "- **Channel**: Internal, WhatsApp",
    "- **Result**: Pending - action items for tomorrow",
    "- **Notes**: Critical actions required to restore full system functionality"
)
$newLines = @()
for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($i -eq $pendingIndex) {
        $newLines += 
    } else {
        $newLines += $lines[$i]
    }
}
# Find the last line of "Completed Today" section (before the blank line before "## 2026-03-26")
$completedIndex = -1
for ($i = 0; $i -lt $newLines.Count; $i++) {
    if ($newLines[$i] -match "## 2026-03-26") {
        $completedIndex = $i
        break
    }
}
Write-Host "Completed heading index: $completedIndex"
# Insert new completed entry before that heading (maybe before the blank line)
$newEntry = @('', "### [2026-03-28 22:10] - Done", "- **Source**: Cron Job (nightly-consolidation)", "- **Instruction**: Run nightly memory consolidation", "- **Action**: Read session logs (none today), read memory/2026-03-28.md, extracted important information, updated MEMORY.md, projects.md, tasks-queue.md, RULES.md, FORMULAS.md, created consolidated daily journal at memory/briefings/JOURNAL-2026-03-28.md, ran memory_flush.py, posted confirmation to Telegram group -1003620024352 topic 2", "- **Target**: System memory files", "- **Channel**: Internal / Telegram", "- **Result**: SUCCESS - All updates completed, journal saved, vector DB synced (Telegram posting attempted but bot not member of group)", "- **Notes**: WhatsApp Gateway instability (499 errors), Telegram bot membership issue, pending action items for tomorrow.")
$newLines = [0..($completedIndex-1)] + $newEntry + $newLines[$completedIndex..($newLines.Count-1)]
# Write back
$newLines | Set-Content "C:\OpenClaw\.openclaw\workspace\tasks-queue.md" -Encoding UTF8
Write-Host "tasks-queue.md updated"
