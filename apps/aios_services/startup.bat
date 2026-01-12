@echo off
:: AIOS Background Services Startup
:: GOVERNANCE: Human must invoke this. AI cannot.

echo Starting AIOS background services...
echo.

:: Start Eyes (screen capture)
echo [1/2] Starting Eyes...
start "eyes_events" /MIN pythonw "%~dp0..\eyes\eyes_events.py" --no-consent
timeout /t 2 /nobreak >nul

:: Start Willow Watcher (inbox monitor)
echo [2/2] Starting Willow Watcher...
start "willow_watcher" /MIN pythonw "%~dp0..\willow_watcher\watcher.py" --no-consent
timeout /t 2 /nobreak >nul

echo.
echo Services started:
echo   - Eyes (screen capture)
echo   - Willow Watcher (inbox monitor)
echo.
echo Check logs:
echo   - Eyes: C:\Users\Sean\.eyes\audit.log
echo   - Watcher: C:\Users\Sean\.willow\events.log
echo.
pause
