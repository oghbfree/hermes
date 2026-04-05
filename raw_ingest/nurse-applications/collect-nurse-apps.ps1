# Nurse Application Collector
# Run this script to collect new nurse applications from Google Forms

$WORKSPACE = "C:\OpenClaw\.openclaw\workspace"
$SCRIPT_DIR = "$WORKSPACE\raw_ingest\nurse-applications"
$OUTPUT_DIR = "$SCRIPT_DIR\processed"

# Ensure directories exist
New-Item -ItemType Directory -Force -Path $OUTPUT_DIR | Out-Null

# Log timestamp
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Write-Host "=== Nurse Application Collector ===" -ForegroundColor Cyan
Write-Host "Time: $timestamp" -ForegroundColor Gray
Write-Host "Form: https://forms.gle/n83KW2FoG5ffYSJL8" -ForegroundColor Gray

# Check for credentials
if (Test-Path "$SCRIPT_DIR\credentials.json") {
    Write-Host "✓ Google credentials found" -ForegroundColor Green
    
    # Run the Python processor
    try {
        python "$SCRIPT_DIR\nurse_applications.py"
        
        # Create completion marker
        $marker = @{
            collected_at = $timestamp
            form_url = "https://forms.gle/n83KW2FoG5ffYSJL8"
            status = "success"
        } | ConvertTo-Json
        $marker | Out-File "$OUTPUT_DIR\last_collection.json" -Encoding UTF8
        
        Write-Host "`n✓ Collection complete" -ForegroundColor Green
    }
    catch {
        Write-Host "✗ Error: $_" -ForegroundColor Red
    }
}
else {
    Write-Host "⚠ No Google credentials found" -ForegroundColor Yellow
    Write-Host "  Follow setup instructions in README.md" -ForegroundColor Yellow
}

Write-Host "`nNext steps:" -ForegroundColor Cyan
Write-Host "  1. Review new applications in: $OUTPUT_DIR" -ForegroundColor Gray
Write-Host "  2. Share form link via WhatsApp to potential nurses" -ForegroundColor Gray
Write-Host "  3. Run daily to stay on top of applications" -ForegroundColor Gray