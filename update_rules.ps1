$lines = Get-Content "C:\OpenClaw\.openclaw\workspace\RULES.md"
$targetLine = "When a failure occurs:"
$targetIndex = -1
for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -eq $targetLine) {
        $targetIndex = $i
        break
    }
}
if ($targetIndex -eq -1) { Write-Error "Target line not found"; exit 1 }
Write-Host "Target index: $targetIndex"
# Insert new rule before target line (maybe skip preceding blank lines)
$newRule = @('', '## Rule #24: Document All Error Code Patterns With Recovery Times', '- **Origin Failure**: WhatsApp Gateway error codes 428, 408, 499 observed throughout the day, but no baseline documented for comparison.', '- **Root Cause**: Lack of systematic tracking of error patterns and recovery times.', '- **Consequence**: Inability to detect deviations from normal behavior, delayed escalation, potential service disruption.', '- **Guard**: Document all error code patterns (428, 408, 499) with recovery times to establish baseline.', '- **Check**: After each error event, log error code, timestamp, recovery duration, and context.', '- **Implementation**: Create a dedicated section in daily memory logs for error pattern tracking. Include error code, timestamp, recovery time, and notes.', '- **Exception**: None for critical error patterns.', '- **Validation**: Verify that error pattern baseline is updated daily and deviations are flagged.', '- **Status**: Proposed.', '')
$newLines = $lines[0..($targetIndex-1)] + $newRule + $lines[$targetIndex..($lines.Count-1)]
# Update Total Rules line
for ($i = 0; $i -lt $newLines.Count; $i++) {
    if ($newLines[$i] -match 'Total Rules') {
        $newLines[$i] = '**Total Rules**: 24 (+ Rule #101)'
    }
    if ($newLines[$i] -match 'Last Updated') {
        $newLines[$i] = '**Last Updated**: 2026-03-28'
    }
}
$newLines | Set-Content "C:\OpenClaw\.openclaw\workspace\RULES.md" -Encoding UTF8
Write-Host "RULES.md updated"
