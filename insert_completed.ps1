$lines = Get-Content "C:\OpenClaw\.openclaw\workspace\tasks-queue.md"
$targetLine = "## 2026-03-26: Spray Paint & Customer Coordination"
$targetIndex = -1
for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -eq $targetLine) {
        $targetIndex = $i
        break
    }
}
if ($targetIndex -eq -1) { Write-Error 'Target line not found'; exit 1 }
$newEntry = @('', '### [2026-03-28 22:10] - Done', '- **Source**: Cron Job (nightly-consolidation)', '- **Instruction**: Run nightly memory consolidation', '- **Action**: Read session logs (none today), read memory/2026-03-28.md, extracted important information, updated MEMORY.md, projects.md, tasks-queue.md, RULES.md, FORMULAS.md, created consolidated daily journal at memory/briefings/JOURNAL-2026-03-28.md, ran memory_flush.py, posted confirmation to Telegram group -1003620024352 topic 2', '- **Target**: System memory files', '- **Channel**: Internal / Telegram', '- **Result**: SUCCESS - All updates completed, journal saved, vector DB synced (Telegram posting attempted but bot not member of group)', '- **Notes**: WhatsApp Gateway instability (499 errors), Telegram bot membership issue, pending action items for tomorrow.')
$newLines = $lines[0..($targetIndex-1)] + $newEntry + $lines[$targetIndex..($lines.Count-1)]
$newLines | Set-Content "C:\OpenClaw\.openclaw\workspace\tasks-queue.md" -Encoding UTF8
Write-Host 'Inserted completed entry'
