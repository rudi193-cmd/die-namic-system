@echo off
echo Starting Eyes Security Setup...
echo.
powershell -ExecutionPolicy Bypass -NoExit -File "%~dp0SETUP_RESTRICTIONS.ps1"
pause
