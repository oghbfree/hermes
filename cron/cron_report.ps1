$cutoffMs = 1774647044670
$jobs = Get-Content "cron\jobs.json" | ConvertFrom-Json
$report = @()
foreach ($job in $jobs.jobs) {
    $lastRun = $job.state.lastRunAtMs
    $lastRunStatus = $job.state.lastRunStatus
    $schedule = $job.schedule.expr
    $enabled = $job.enabled
    $name = $job.name
    $lastRunTime = if ($lastRun -gt 0) { [DateTimeOffset]::FromUnixTimeMilliseconds($lastRun).DateTime } else { "Never" }
    $status = if ($lastRun -gt $cutoffMs) { "Ran" } elseif ($lastRunStatus -eq "error") { "Failed" } else { "Missed" }
    $notes = ""
    if (-not $enabled) { $notes = "Disabled" }
    if ($lastRunStatus -eq "error") { $notes += " Last run error" }
    $report += [PSCustomObject]@{
        Name = $name
        Schedule = $schedule
        LastRun = $lastRunTime
        Status = $status
        Notes = $notes
    }
}
# Output plain text table
$line = "Cron Name | Scheduled Time | Status | Notes"
$divider = "-" * 80
Write-Output $line
Write-Output $divider
foreach ($r in $report) {
    "{0,-20} | {1,-20} | {2,-10} | {3,-30}" -f $r.Name, $r.Schedule, $r.Status, $r.Notes
}
# Flag any crons that failed or were missed
$failed = $report | Where-Object { $_.Notes -match "error" }
$missed = $report | Where-Object { $_.Status -eq "Missed" }
if ($failed) {
    Write-Output ""
    Write-Output "FLAGGED FAILED CRONS:"
    $failed | ForEach-Object { Write-Output " - $($_.Name): $($_.Notes)" }
}
if ($missed) {
    Write-Output ""
    Write-Output "FLAGGED MISSED CRONS:"
    $missed | ForEach-Object { Write-Output " - $($_.Name): Last run $($_.LastRun)" }
}
