$json = Get-Content 'C:\OpenClaw\.openclaw\workspace\cron\jobs.json' -Raw | ConvertFrom-Json
foreach ($job in $json.jobs) {
    Write-Output "$($job.name): $($job.schedule.expr)"
}
