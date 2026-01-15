@echo off
:: =========================================================
:: SAFE DRIVE SYNC — No Deletions, No Destruction
::
:: GOVERNANCE: This script COPIES only. Never deletes.
:: Uses /XO (exclude older) to avoid overwriting newer files.
:: =========================================================

setlocal EnableDelayedExpansion

:: CONFIGURATION
set "SOURCE=C:\Users\Sean\Documents\GitHub\die-namic-system"
set "DEST=G:\My Drive\Willow_Backup"
set "LOGFILE=%~dp0sync_log.txt"
set "DRY_RUN=0"

:: Parse arguments
if "%1"=="--dry-run" set "DRY_RUN=1"
if "%1"=="--help" goto :help

:: =========================================================
:: SAFETY CHECKS
:: =========================================================

:: 1. Check source exists
if not exist "%SOURCE%" (
    echo [ERROR] Source not found: %SOURCE%
    echo [ERROR] Source not found: %SOURCE% >> "%LOGFILE%"
    exit /b 1
)

:: 2. Check Drive is mounted
if not exist "G:\My Drive" (
    echo [ERROR] Google Drive G: not mounted.
    echo [ERROR] Google Drive G: not mounted. >> "%LOGFILE%"
    exit /b 1
)

:: 3. Create dest if needed (SAFE - just creates folder)
if not exist "%DEST%" (
    echo [INFO] Creating backup folder: %DEST%
    mkdir "%DEST%"
)

:: =========================================================
:: THE SYNC (SAFE MODE)
:: =========================================================
::
:: Flags used:
::   /E     = Copy subdirectories (including empty)
::   /XO    = Exclude Older (don't overwrite newer files in dest)
::   /R:3   = Retry 3 times if locked
::   /W:2   = Wait 2 seconds between retries
::   /NP    = No Progress (cleaner logs)
::   /NDL   = No Directory List
::   /NJH   = No Job Header
::   /NJS   = No Job Summary (we'll make our own)
::   /XD    = Exclude directories
::
:: NOT USED (UNSAFE):
::   /MIR   = DANGEROUS - deletes files in dest not in source
::   /PURGE = DANGEROUS - deletes files in dest not in source
::
:: =========================================================

echo.
echo ========================================
echo   SAFE DRIVE SYNC
echo   %DATE% %TIME%
echo ========================================
echo.
echo Source: %SOURCE%
echo Dest:   %DEST%
echo.

echo [%DATE% %TIME%] Starting SAFE sync... >> "%LOGFILE%"

if "%DRY_RUN%"=="1" (
    echo [DRY RUN MODE - No files will be copied]
    echo.
    robocopy "%SOURCE%" "%DEST%" /E /XO /R:3 /W:2 /NP /L /XD .git .claude node_modules __pycache__ .mypy_cache
    echo.
    echo [DRY RUN COMPLETE - Run without --dry-run to execute]
) else (
    robocopy "%SOURCE%" "%DEST%" /E /XO /R:3 /W:2 /NP /NDL /XD .git .claude node_modules __pycache__ .mypy_cache /LOG+:"%LOGFILE%" /TEE
)

echo.
echo [%DATE% %TIME%] Sync complete. >> "%LOGFILE%"
echo ========================================
echo   SYNC COMPLETE
echo   Log: %LOGFILE%
echo ========================================

exit /b 0

:: =========================================================
:help
:: =========================================================
echo.
echo SAFE DRIVE SYNC
echo.
echo Usage: drive_sync.bat [options]
echo.
echo Options:
echo   --dry-run    Show what would be copied without copying
echo   --help       Show this help message
echo.
echo SAFE GUARANTEES:
echo   - Never deletes files in destination
echo   - Never overwrites newer files
echo   - Excludes .git, .claude, node_modules, __pycache__
echo.
exit /b 0
