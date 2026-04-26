$jobsPath = "C:\Users\User\.openclaw\cron\jobs.json"
$jobs = Get-Content $jobsPath -Raw | ConvertFrom-Json
$currentMs = [DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()
$twentyFourHoursAgo = $currentMs - (24 * 60 * 60 * 1000)

$reportRows = @()
$anyFailedOrMissed = $false

foreach ($job in $jobs.jobs) {
    $name = $job.name
    $enabled = $job.enabled
    $lastRunAtMs = $job.state.lastRunAtMs
    $lastRunStatus = $job.state.lastRunStatus
    $consecutiveErrors = $job.state.consecutiveErrors
    $lastError = $job.state.lastError
    $nextRunAtMs = $job.state.nextRunAtMs
    $scheduleExpr = $job.schedule.expr
    $scheduleTz = $job.schedule.tz
    $scheduleKind = $job.schedule.kind

    # Determine if job should be included in report
    $include = $false
    if ($enabled -eq $true) {
        # Include enabled jobs that have run in last 24h, or have errors, or missed
        if ($lastRunAtMs -ge $twentyFourHoursAgo) { $include = $true }
        if ($lastRunStatus -eq "error") { $include = $true }
        if ($consecutiveErrors -gt 0) { $include = $true }
        if ($nextRunAtMs -and $nextRunAtMs -lt $currentMs -and $lastRunAtMs -lt $nextRunAtMs) { $include = $true }
    } else {
        # Include disabled jobs only if they have errors (maybe leftover)
        if ($lastRunStatus -eq "error") { $include = $true }
    }
    
    if (-not $include) { continue }
    
    # Determine status
    $status = "OK"
    $notes = ""
    
    if ($lastRunStatus -eq "error") {
        $status = "FAIL"
        $anyFailedOrMissed = $true
        $notes = $lastError
    } elseif ($consecutiveErrors -gt 0) {
        $status = "CRITICAL"
        $anyFailedOrMissed = $true
        $notes = "Consecutive errors: $consecutiveErrors"
    } elseif ($nextRunAtMs -and $nextRunAtMs -lt $currentMs -and $lastRunAtMs -lt $nextRunAtMs) {
        $status = "MISSED"
        $anyFailedOrMissed = $true
        $notes = "Next run was at $(Get-Date -Date (Get-Date "1970-01-01 00:00:00Z").AddMilliseconds($nextRunAtMs) -Format 'yyyy-MM-dd HH:mm')"
    } elseif ($lastRunAtMs -ge $twentyFourHoursAgo) {
        $status = "OK"
    } else {
        $status = "INACTIVE"
    }
    
    # Scheduled column: show cron expression
    $scheduled = $scheduleExpr
    if ($scheduleTz) { $scheduled += " ($scheduleTz)" }
    
    # Add row
    $reportRows += [PSCustomObject]@{
        Name = $name
        Scheduled = $scheduled
        Status = $status
        Notes = $notes
        Enabled = $enabled
    }
}

# Generate report
$dateStr = Get-Date -Format "yyyy-MM-dd"
$report = "# ?Y>???? DAILY CRON STATUS REPORT | $dateStr`n`n"
if ($anyFailedOrMissed) {
    $report = "?Ys? **ATTENTION REQUIRED: SYSTEM FRICTION DETECTED**`n`n" + $report
}
$report += "| Cron Name | Scheduled | Status | Notes |`n"
$report += "| :--- | :--- | :--- | :--- |`n"
foreach ($row in $reportRows) {
    $report += "| $($row.Name) | $($row.Scheduled) | $($row.Status) | $($row.Notes) |`n"
}
$report
