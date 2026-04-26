$date = "2026-04-18"
$file = "C:\Users\User\.openclaw\workspace\memory\insights\INTEGRATED_INSIGHTS_$date.md"
# Health summary
$healthSummary = if (Select-String -Path "C:\Users\User\.openclaw\workspace\memory\health\LOG-2026-04.md" -Pattern $date) { "Health logs recorded today." } else { "No health logs recorded today." }
# Business pulse
$businessEntries = Select-String -Path "C:\Users\User\.openclaw\workspace\memory\business\BUSINESS_CHECKINS_2026-04.md" -Pattern $date
if ($businessEntries) {
    $businessSummary = "WhatsApp channel offline causing failed morning check-ins. Need to login to WhatsApp account 233204252252."
} else {
    $businessSummary = "No business check-ins today."
}
# Learning capture
$keyInsight = "WhatsApp connectivity is a single point of failure for business communications; need robust monitoring and fallback."
$worked = "Security audits passed, workspace integrity scan okay, no credential exposure detected."
$failed = "WhatsApp channel offline, morning check-ins failed, gateway unresponsive."
$proposedRule = "Rule #37: Verify WhatsApp channel connectivity before sending critical messages, with fallback to Telegram or alert."
# Action items
$actionItems = @"
1. Login to WhatsApp channel via openclaw channels login.
2. Implement automatic connectivity check before sending critical messages.
3. Review Telegram bot membership for group -1003620024352.
"@
# Write file
$content = @"
# 🧠 DAILY INTEGRATED SYNTHESIS | $date

## 🩺 HEALTH & VITALS
$healthSummary

## 📈 DAILY LEARNING CAPTURE
- **Key Insight**: $keyInsight
- **Worked**: $worked
- **Failed**: $failed
- **Proposed Rule**: $proposedRule

## 📊 BUSINESS PULSE
$businessSummary

## 🎯 ACTION ITEMS FOR TOMORROW
$actionItems
"@
$content | Out-File -FilePath $file -Encoding utf8
Write-Output "File created: $file"
