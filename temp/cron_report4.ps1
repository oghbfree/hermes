$jobsPath = "C:\Users\User\.openclaw\cron\jobs.json"
$jobs = Get-Content $jobsPath -Raw | ConvertFrom-Json
$currentMs = [DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()
$twentyFourHoursAgo = $currentMs - (24 * 60 * 60 * 1000)

# Group jobs by name, pick the most relevant entry (prefer enabled, then most recent)
$jobMap = @{}
foreach ($job in $jobs.jobs) {
    $name = $job.name
    if (-not $jobMap.ContainsKey($name)) {
        $jobMap[$name] = @()
    }
    $jobMap[$name] += $job
}
# For each name, select one job to represent
$selectedJobs = @()
foreach ($name in $jobMap.Keys) {
    $candidates = $jobMap[$name]
    # Prefer enabled jobs
    $enabled = $candidates | Where-Object { $_.enabled -eq $true }
    if ($enabled) { $candidates = $enabled }
    # Prefer the one with most recent lastRunAtMs
    $selected = $candidates | Sort-Object { $_.state.lastRunAtMs } -Descending | Select-Object -First 1
    $selectedJobs += $selected
}

$reportRows = @()
$anyFailedOrMissed = $false
$countFailed = 0
$countMissed = 0
$countRan = 0

foreach ($job in $selectedJobs) {
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

    # Determine if job ran in last 24h
    $ranRecently = $lastRunAtMs -ge $twentyFourHoursAgo
    # Determine if missed
    $missed = $false
    if ($nextRunAtMs -and $nextRunAtMs -lt $currentMs -and $lastRunAtMs -lt $nextRunAtMs) {
        $missed = $true
    }
    
    # Decide inclusion: include if ran recently, or missed, or failure (even if older)
    $include = $false
    if ($ranRecently -or $missed) {
        $include = $true
    } elseif ($lastRunStatus -eq "error") {
        # Include failures even if older, but only if enabled? maybe include all failures
        $include = $true
    }
    if (-not $include) { continue }
    
    # Determine status
    $status = "ran"
    $notes = ""
    
    if ($lastRunStatus -eq "error") {
        $status = "failed"
        $anyFailedOrMissed = $true
        $countFailed++
        $notes = $lastError
    } elseif ($missed) {
        $status = "missed"
        $anyFailedOrMissed = $true
        $countMissed++
        $notes = "Next run was at $(Get-Date -Date (Get-Date "1970-01-01 00:00:00Z").AddMilliseconds($nextRunAtMs) -Format 'yyyy-MM-dd HH:mm')"
    } elseif ($consecutiveErrors -gt 0) {
        $status = "failed"
        $anyFailedOrMissed = $true
        $countFailed++
        $notes = "Consecutive errors: $consecutiveErrors"
    } else {
        $status = "ran"
        $countRan++
    }
    
    # Scheduled column: show cron expression
    $scheduled = $scheduleExpr
    if ($scheduleTz) { $scheduled += " ($scheduleTz)" }
    
    # Truncate notes if too long
    if ($notes.Length -gt 100) {
        $notes = $notes.Substring(0, 97) + "..."
    }
    
    # Add row
    $reportRows += [PSCustomObject]@{
        Name = $name
        Scheduled = $scheduled
        Status = $status
        Notes = $notes
    }
}

# Sort rows: failed first, missed, then ran
$statusOrder = @{"failed"=1; "missed"=2; "ran"=3}
$sortedRows = $reportRows | Sort-Object { $statusOrder[$_.Status] }, { $_.Name }

# Generate report
$dateStr = Get-Date -Format "yyyy-MM-dd"
$timeStr = Get-Date -Format "HH:mm"
$report = "# ?Y>???? DAILY CRON STATUS REPORT | $dateStr`n"
$report += "Generated at $timeStr UTC`n`n"
if ($anyFailedOrMissed) {
    $report = "?Ys? **ATTENTION REQUIRED: SYSTEM FRICTION DETECTED**`n`n" + $report
}
$report += "**Summary:** Total jobs: $($selectedJobs.Count) | Failed: $countFailed | Missed: $countMissed | Ran: $countRan`n`n"
$report += "| Cron Name | Scheduled | Status | Notes |`n"
$report += "| :--- | :--- | :--- | :--- |`n"
foreach ($row in $sortedRows) {
    $report += "| $($row.Name) | $($row.Scheduled) | $($row.Status) | $($row.Notes) |`n"
}
$report += "`n*All other crons are inactive or not scheduled.*"
$report
