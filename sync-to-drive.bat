@echo off
REM Die-namic System Sync Script
REM Mirrors GitHub repo to Google Drive
REM Run after pushing to GitHub

echo Syncing die-namic-system to Google Drive...
echo.

REM One-way mirror: GitHub -> Drive
REM /MIR = Mirror (make destination match source exactly)
REM /XD = Exclude directories (.git, node_modules)
REM /XF = Exclude files (desktop.ini)
REM /NFL /NDL = No file/directory list (cleaner output)
REM /NJH /NJS = No job header/summary
REM /NC /NS = No class/size info

robocopy "C:\Users\Sean\Documents\GitHub\die-namic-system" "G:\My Drive\Die-namic-System-v1.42" /MIR /XD .git node_modules /XF desktop.ini /R:3 /W:5

if %ERRORLEVEL% LEQ 3 (
    echo.
    echo Sync complete.
) else (
    echo.
    echo Sync encountered errors. Check output above.
)

pause
