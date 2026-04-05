$now = [DateTimeOffset]::UtcNow
$nowMs = $now.ToUnixTimeMilliseconds()
Write-Output $nowMs
