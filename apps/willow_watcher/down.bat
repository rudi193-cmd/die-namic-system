@echo off
:: Stop willow watcher
taskkill /IM python.exe /FI "WINDOWTITLE eq *watcher*" 2>nul
if %errorlevel%==0 (
    echo Watcher down.
) else (
    echo Watcher not running or already stopped.
)
