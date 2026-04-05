$lines = Get-Content 'C:\OpenClaw\.openclaw\workspace\tasks-queue.md'
$idx = -1
for ($i=0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match 'No pending tasks') {
        $idx = $i
        break
    }
}
if ($idx -eq -1) { Write-Error 'Not found'; exit 1 }
$newLines = @()
for ($i=0; $i -lt $lines.Count; $i++) {
    if ($i -eq $idx) {
        $newLines += '### [2026-03-28 22:10] - Pending'
        $newLines += '- **Source**: Cron Job (nightly-consolidation)'
        $newLines += '- **Instruction**: Resolve critical system issues identified today'
        $newLines += '- **Action**: Add bot to group -1003620024352 as administrator, resolve webhook 404 errors, monitor WhatsApp Gateway for 499 error recurrence, document error pattern baseline (428, 408, 499), follow up on John''s Facebook ads response, follow up on spray paint coordination with John, monitor Akoma credentials file, review cron job target configurations, document recovery process for WhatsApp Gateway issues'
        $newLines += '- **Target**: System configuration, WhatsApp Gateway, Telegram bot'
        $newLines += '- **Channel**: Internal, WhatsApp'
        $newLines += '- **Result**: Pending - action items for tomorrow'
        $newLines += '- **Notes**: Critical actions required to restore full system functionality'
    } else {
        $newLines += $lines[$i]
    }
}
$newLines | Set-Content 'C:\OpenClaw\.openclaw\workspace\tasks-queue.md' -Encoding UTF8
Write-Host 'Updated'
