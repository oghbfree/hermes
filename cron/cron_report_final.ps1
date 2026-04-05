$cutoffMs = 1774647044670
$nowMs = 1774733557089
$jobs = Get-Content "cron\jobs.json" | ConvertFrom-Json

# Function to convert cron expression to human-readable schedule
function Convert-CronToHuman($expr) {
    $parts = $expr -split '\s+'
    if ($parts.Count -lt 5) { return $expr }
    $min = $parts[0]
    $hour = $parts[1]
    $dom = $parts[2]
    $mon = $parts[3]
    $dow = $parts[4]
    
    # Daily at time
    if ($min -match '^\d+$' -and $hour -match '^\d+$' -and $dom -eq '*' -and $mon -eq '*' -and $dow -eq '*') {
        return "Daily at ${hour}:${min.PadLeft(2,'0')}"
    }
    # Weekly on specific day
    if ($min -match '^\d+$' -and $hour -match '^\d+$' -and $dom -eq '*' -and $mon -eq '*' -and $dow -match '^\d+$') {
        $dayNames = @('Sun','Mon','Tue','Wed','Thu','Fri','Sat')
        $dayName = $dayNames[[int]$dow]
        return "Weekly on $dayName at ${hour}:${min.PadLeft(2,'0')}"
    }
    # Monthly on day
    if ($min -match '^\d+$' -and $hour -match '^\d+$' -and $dom -match '^\d+$' -and $mon -eq '*' -and $dow -eq '*') {
        return "Monthly on day $dom at ${hour}:${min.PadLeft(2,'0')}"
    }
    # Hourly
    if ($min -eq '0' -and $hour -eq '*' -and $dom -eq '*' -and $mon -eq '*' -and $dow -eq '*') {
        return "Hourly at minute 0"
    }
    # Custom
    return $expr
}

$report = @()
foreach ($job in $jobs.jobs) {
    $name = $job.name
    $expr = $job.schedule.expr
    $schedule = Convert-CronToHuman $expr
    $lastRun = $job.state.lastRunAtMs
    $lastRunStatus = $job.state.lastRunStatus
    $nextRun = $job.state.nextRunAtMs
    
    $status = "Missed"
    $notes = ""
    if ($lastRun -gt $cutoffMs) {
        $status = "Ran"
        if ($lastRunStatus -eq "error") { $status = "Failed" }
    } elseif ($lastRunStatus -eq "error") {
        $status = "Failed"
        $notes = "Last run error"
    } elseif ($nextRun -lt $nowMs) {
        $status = "Missed"
        $notes = "Next run overdue"
    } else {
        $status = "Scheduled"
        $nextRunDt = [DateTimeOffset]::FromUnixTimeMilliseconds($nextRun).DateTime
        $notes = "Next run: $nextRunDt"
    }
    
    $report += [PSCustomObject]@{
        Name = $name
        Schedule = $schedule
        Status = $status
        Notes = $notes
    }
}

# Output table
Write-Output "Daily Cron Execution Report for $(Get-Date -Format 'yyyy-MM-dd')"
Write-Output ""
Write-Output "Cron Name | Scheduled Time | Status | Notes"
Write-Output "-------------------------------------------"
foreach ($r in $report) {
    "{0,-25} | {1,-20} | {2,-10} | {3}" -f $r.Name, $r.Schedule, $r.Status, $r.Notes
}

# Flag any crons that failed or were missed
$failed = $report | Where-Object { $_.Status -eq "Failed" }
$missed = $report | Where-Object { $_.Status -eq "Missed" }
Write-Output ""
Write-Output "FLAGGED ITEMS:"
if ($failed) {
    Write-Output "Failed crons:"
    foreach ($f in $failed) {
        Write-Output " - $($f.Name): $($f.Notes)"
    }
}
if ($missed) {
    Write-Output "Missed crons:"
    foreach ($m in $missed) {
        Write-Output " - $($m.Name): $($m.Schedule)"
    }
}
if (!$failed -and !$missed) {
    Write-Output "No failed or missed crons."
}
