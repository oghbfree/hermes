$json = Get-Content -Raw "C:\Users\User\.openclaw\cron\jobs.json" | ConvertFrom-Json
$nowMs = [int64]((Get-Date).ToUniversalTime() - (Get-Date "1970-01-01")).TotalMilliseconds
$oneDayMs = 24 * 3600 * 1000
$cutoff = $nowMs - $oneDayMs
$hasFailOrMissed = $false
$enabledJobs = @()
$disabledJobs = @()
foreach ($job in $json.jobs) {
    $name = $job.name
    $enabled = $job.enabled
    $lastRunAtMs = $job.state.lastRunAtMs
    $lastRunStatus = $job.state.lastRunStatus
    $consecutiveErrors = $job.state.consecutiveErrors
    $nextRunAtMs = $job.state.nextRunAtMs
    $lastError = $job.state.lastError
    $scheduled = "N/A"
    if ($job.schedule.kind -eq "cron") { $scheduled = $job.schedule.expr }
    # Determine status
    $status = "UNKNOWN"
    if ($lastRunStatus -eq "ok") { $status = "OK" }
    elseif ($lastRunStatus -eq "error") { $status = "FAIL" }
    # Check if missed
    if ($nextRunAtMs -and $nextRunAtMs -lt $nowMs -and $lastRunAtMs -lt $nextRunAtMs) {
        $status = "MISSED"
    }
    if ($status -eq "FAIL" -or $status -eq "MISSED") { $hasFailOrMissed = $true }
    # Build notes
    $notes = ""
    if ($lastError) { $notes = $lastError }
    if ($consecutiveErrors -gt 0) { $notes += " (Consecutive errors: $consecutiveErrors)" }
    $obj = [PSCustomObject]@{
        Name = $name
        Scheduled = $scheduled
        Status = $status
        Notes = $notes
        Enabled = $enabled
    }
    if ($enabled) { $enabledJobs += $obj } else { $disabledJobs += $obj }
}
$dateStr = Get-Date -Format "yyyy-MM-dd"
$report = "# DAILY CRON STATUS REPORT | $dateStr`n`n"
if ($hasFailOrMissed) {
    $report = "ATTENTION REQUIRED: SYSTEM FRICTION DETECTED`n`n" + $report
}
$report += "## Enabled Jobs ($($enabledJobs.Count))`n"
$report += "| Cron Name | Scheduled | Status | Notes |`n"
$report += "| :--- | :--- | :--- | :--- |`n"
foreach ($job in $enabledJobs) {
    $report += "| $($job.Name) | $($job.Scheduled) | $($job.Status) | $($job.Notes) |`n"
}
$report += "`n## Disabled Jobs ($($disabledJobs.Count))`n"
$report += "| Cron Name | Scheduled | Status | Notes |`n"
$report += "| :--- | :--- | :--- | :--- |`n"
foreach ($job in $disabledJobs) {
    $report += "| $($job.Name) | $($job.Scheduled) | $($job.Status) | $($job.Notes) |`n"
}
Write-Output $report
