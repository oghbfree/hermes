$json = Get-Content -Raw "C:\Users\User\.openclaw\cron\jobs.json" | ConvertFrom-Json
$nowMs = [int64]((Get-Date).ToUniversalTime() - (Get-Date "1970-01-01")).TotalMilliseconds
$oneDayMs = 24 * 3600 * 1000
$cutoff = $nowMs - $oneDayMs
$hasFailOrMissed = $false
$output = @()
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
    $statusEmoji = "�s���?"
    if ($lastRunStatus -eq "ok") { $status = "OK"; $statusEmoji = "�o." }
    elseif ($lastRunStatus -eq "error") { $status = "FAIL"; $statusEmoji = "�?O" }
    # Check if missed
    if ($nextRunAtMs -and $nextRunAtMs -lt $nowMs -and $lastRunAtMs -lt $nextRunAtMs) {
        $status = "MISSED"; $statusEmoji = "�s���?"
    }
    if ($status -eq "FAIL" -or $status -eq "MISSED") { $hasFailOrMissed = $true }
    # Build notes
    $notes = ""
    if ($lastError) { $notes = $lastError }
    if ($consecutiveErrors -gt 0) { $notes += " (Consecutive errors: $consecutiveErrors)" }
    if (-not $enabled) { $notes += " [DISABLED]" }
    # Trim
    $notes = $notes.Trim()
    $output += [PSCustomObject]@{
        Name = $name
        Scheduled = $scheduled
        Status = "$statusEmoji $status"
        Notes = $notes
    }
}
# Build report
$dateStr = Get-Date -Format "yyyy-MM-dd"
$report = "# �Y>���? DAILY CRON STATUS REPORT | $dateStr`n`n"
$report += "| Cron Name | Scheduled | Status | Notes |`n"
$report += "| :--- | :--- | :--- | :--- |`n"
foreach ($row in $output) {
    $report += "| $($row.Name) | $($row.Scheduled) | $($row.Status) | $($row.Notes) |`n"
}
if ($hasFailOrMissed) {
    $report = "�Ys� **ATTENTION REQUIRED: SYSTEM FRICTION DETECTED**`n`n" + $report
}
Write-Output $report
