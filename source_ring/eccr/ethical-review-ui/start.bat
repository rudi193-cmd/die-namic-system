@echo off
REM ECCR Ethical Review UI - Quick Start Script (Windows)

echo.
echo ∞Δ═══════════════════════════════════════════════════════════════∞Δ
echo.
echo    🌊 ECCR Ethical Review UI - Quick Start
echo    Sandcastle Sequence v0.3 ^| ESC-1 Protocol
echo.
echo ∞Δ═══════════════════════════════════════════════════════════════∞Δ
echo.

REM Check if node_modules exists
if not exist "node_modules\" (
  echo 📦 Installing dependencies...
  call npm install
  echo.
)

echo 🚀 Starting services...
echo.
echo    You need TWO command prompt windows:
echo    Terminal 1: Mock Server ^(port 5550^)
echo    Terminal 2: React App ^(port 5173^)
echo.
echo    Would you like to:
echo    1^) Start Mock Server only
echo    2^) Start React App only
echo    3^) Get manual instructions
echo.

set /p choice="   Enter choice (1-3): "

if "%choice%"=="1" (
  echo.
  echo    Starting Mock Server on http://localhost:5550...
  echo.
  call npm run mock-server
) else if "%choice%"=="2" (
  echo.
  echo    Starting React App on http://localhost:5173...
  echo.
  call npm run dev
) else if "%choice%"=="3" (
  echo.
  echo    Manual Instructions:
  echo    ────────────────────
  echo.
  echo    Terminal 1:
  echo    $ cd %CD%
  echo    $ npm run mock-server
  echo.
  echo    Terminal 2:
  echo    $ cd %CD%
  echo    $ npm run dev
  echo.
  echo    Then open: http://localhost:5173
  echo.
) else (
  echo    Invalid choice. Run 'start.bat' again.
)

echo.
pause
