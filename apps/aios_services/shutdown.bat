@echo off
:: AIOS Background Services Shutdown

echo Stopping AIOS background services...
echo.

:: Stop Eyes
taskkill /FI "WINDOWTITLE eq eyes_events*" /F 2>nul
if %errorlevel%==0 (echo   Eyes: stopped) else (echo   Eyes: not running)

:: Stop Willow Watcher
taskkill /FI "WINDOWTITLE eq willow_watcher*" /F 2>nul
if %errorlevel%==0 (echo   Watcher: stopped) else (echo   Watcher: not running)

echo.
echo Services stopped.
pause
