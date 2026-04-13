$file = "C:\Users\User\.openclaw\workspace\health\mum\2026-04-13.md"
$content = Get-Content $file -Raw
$evening = @"


## Evening Check

- **Dinner:** 
- **Drink:** 
- **Medication taken:** 
- **Mobility:** 
- **Mood:** 
- **Symptoms:** 
- **Severity:** 
- **Notes:** 

---

READY FOR CONSOLIDATION

"@
$placeholder = "*Awaiting carer input from Telegram #health-log-mum (Topic 51)*"
$newContent = $content -replace [regex]::Escape($placeholder), ($evening + "`r`n" + $placeholder)
Set-Content -Path $file -Value $newContent -NoNewline
