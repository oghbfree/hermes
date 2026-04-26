$json = Get-Content -Raw "C:\Users\User\.openclaw\cron\jobs.json" | ConvertFrom-Json
$nowMs = [int64]((Get-Date).ToUniversalTime() - (Get-Date "1970-01-01")).TotalMilliseconds
$oneDayMs = 24 * 3600 * 1000
$cutoff = $nowMs - $oneDayMs
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
    # Check if critical
    $critical = $consecutiveErrors -gt 0
    # Last run within 24h?
    $recent = $lastRunAtMs -and $lastRunAtMs -gt $cutoff
    # Build notes
    $notes = ""
    if ($lastError) { $notes = $lastError }
    if ($critical) { $notes += " (Consecutive errors: $consecutiveErrors)" }
    if (-not $enabled) { $notes += " [DISABLED]" }
    Write-Output "$name | $scheduled | $status | $notes"
}
