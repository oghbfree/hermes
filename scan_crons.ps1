$cutoffMs = 1774647044670
$files = Get-ChildItem "cron\runs\*.jsonl"
$results = @()
foreach ($file in $files) {
    $lines = Get-Content $file.FullName
    foreach ($line in $lines) {
        try {
            $json = $line | ConvertFrom-Json
            if ($json.runAtMs -and $json.runAtMs -gt $cutoffMs) {
                $results += [PSCustomObject]@{
                    File = $file.Name
                    JobId = $json.jobId
                    Action = $json.action
                    Status = $json.status
                    RunAtMs = $json.runAtMs
                    RunAt = ([DateTimeOffset]::FromUnixTimeMilliseconds($json.runAtMs)).DateTime
                }
            }
        } catch {
            # ignore parse errors
        }
    }
}
$results | Sort-Object RunAtMs | Format-Table -AutoSize
