$logDir = "C:\Users\User\.openclaw\logs"
$workspaceDir = "C:\Users\User\.openclaw\workspace"
$patterns = @(
    @{ Name = "OpenAI"; Pattern = 'sk-[a-zA-Z0-9]{48}' },
    @{ Name = "GitHub"; Pattern = 'ghp_[a-zA-Z0-9]{36}' },
    @{ Name = "TelegramBotToken"; Pattern = '\d+:[a-zA-Z0-9_-]{35}' },
    @{ Name = "OpenRouterAPIKey"; Pattern = 'sk-or-[a-zA-Z0-9]+' },
    @{ Name = "GenericToken32"; Pattern = '[A-Za-z0-9]{32,}' }
)
$redactions = @()
Get-ChildItem -Path $logDir -File -Recurse | ForEach-Object {
    $file = $_.FullName
    $content = Get-Content $file -Raw
    $changed = $false
    foreach ($p in $patterns) {
        $matches = [regex]::Matches($content, $p.Pattern)
        if ($matches.Count -gt 0) {
            foreach ($match in $matches) {
                $token = $match.Value
                # Skip if token is already redacted placeholder
                if ($token -eq '[REDACTED]') { continue }
                # Additional validation: token should not be part of normal words
                if ($token -match '^[A-Z]{2,}$') { continue } # likely acronym
                $content = $content -replace [regex]::Escape($token), '[REDACTED]'
                $redactions += [PSCustomObject]@{
                    File = $file
                    Pattern = $p.Name
                    Token = $token
                }
                $changed = $true
            }
        }
    }
    if ($changed) {
        Set-Content -Path $file -Value $content -NoNewline
        Write-Output "Redacted tokens in $file"
    }
}
$redactions | Format-Table -AutoSize
