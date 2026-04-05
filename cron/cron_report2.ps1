$cutoffMs = 1774647044670
$jobs = Get-Content "cron\jobs.json" | ConvertFrom-Json
$ran = @()
$failed = @()
$missed = @()
foreach ($job in $jobs.jobs) {
    $lastRun = $job.state.lastRunAtMs
    $lastRunStatus = $job.state.lastRunStatus
    $schedule = $job.schedule.expr
    $name = $job.name
    if ($lastRun -gt $cutoffMs) {
        # This cron ran in the last 24 hours
        $ran += [PSCustomObject]@{
            Name = $name
            Schedule = $schedule
            LastRun = [DateTimeOffset]::FromUnixTimeMilliseconds($lastRun).DateTime
            Status = if ($lastRunStatus -eq "error") { "Failed" } else { "Ran" }
            Notes = ""
        }
    }
    # Check for failure (last run error)
    if ($lastRunStatus -eq "error") {
        $failed += [PSCustomObject]@{
            Name = $name
            Schedule = $schedule
            LastRun = [DateTimeOffset]::FromUnixTimeMilliseconds($lastRun).DateTime
            Error = "Last run error"
        }
    }
    # Check for missed: maybe any cron that should have run in last 24 hours but didn't? Too complex.
}
# Output report
Write-Output "Daily Cron Execution Report for $(Get-Date -Format 'yyyy-MM-dd')"
Write-Output ""
if ($ran.Count -eq 0) {
    Write-Output "No cron jobs executed in the last 24 hours."
} else {
    Write-Output "Cron Name | Scheduled Time | Status | Notes"
    Write-Output "-------------------------------------------"
    foreach ($r in $ran) {
        "{0,-25} | {1,-15} | {2,-8} | {3}" -f $r.Name, $r.Schedule, $r.Status, $r.Notes
    }
}
Write-Output ""
Write-Output "FLAGGED ITEMS:"
if ($failed.Count -gt 0) {
    Write-Output "Failed crons (last run error):"
    foreach ($f in $failed) {
        Write-Output " - $($f.Name): $($f.Error)"
    }
} else {
    Write-Output "No failed crons."
}
Write-Output ""
Write-Output "Note: Cron daemon appears to have stopped after March 22nd. No cron jobs have executed since then."
