@echo off
:: Request Admin elevation
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Requesting Administrator privileges...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

echo Starting Eyes Security Setup (Administrator)...
echo.
powershell -ExecutionPolicy Bypass -NoExit -File "%~dp0SETUP_RESTRICTIONS.ps1"
pause
