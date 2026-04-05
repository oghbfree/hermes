$content = Get-Content "C:\OpenClaw\.openclaw\workspace\tasks-queue.md" -Raw
$pendingEntry = @'
## Pending

### [2026-03-28 22:10] - Pending
- **Source**: Cron Job (nightly-consolidation)
- **Instruction**: Resolve critical system issues identified today
- **Action**: Add bot to group -1003620024352 as administrator, resolve webhook 404 errors, monitor WhatsApp Gateway for 499 error recurrence, document error pattern baseline (428, 408, 499), follow up on John's Facebook ads response, follow up on spray paint coordination with John, monitor Akoma credentials file, review cron job target configurations, document recovery process for WhatsApp Gateway issues
- **Target**: System configuration, WhatsApp Gateway, Telegram bot
- **Channel**: Internal, WhatsApp
- **Result**: Pending - action items for tomorrow
- **Notes**: Critical actions required to restore full system functionality
'@
$content =  -replace '(?s)## Pending.*?## Completed Today',  + "
## Completed Today"
$content | Set-Content "C:\OpenClaw\.openclaw\workspace\tasks-queue.md" -Encoding UTF8
Write-Host "Updated pending section"
