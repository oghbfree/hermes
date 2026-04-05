# Mission Control Launcher

Write-Host "Starting Mission Control Dashboard..." -ForegroundColor Green
Write-Host "URL: http://localhost:3000" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow

cd "C:\Users\User\.openclaw\workspace\mission-control"
node server.js
