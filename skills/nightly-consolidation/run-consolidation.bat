@echo off
echo Running Nightly Memory Consolidation...
powershell -ExecutionPolicy Bypass -File "C:\OpenClaw\.openclaw\workspace\skills\nightly-consolidation\nightly-consolidation.ps1"
echo Consolidation complete.
