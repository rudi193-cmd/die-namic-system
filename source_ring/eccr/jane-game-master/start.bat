@echo off
echo.
echo ✨═══════════════════════════════════════════════════════════════✨
echo.
echo    🎲 Jane's Adventure - Quick Start
echo    Game Master Interface for Ages 9-12
echo.
echo ✨═══════════════════════════════════════════════════════════════✨
echo.

if not exist "node_modules\" (
  echo 📦 Installing dependencies...
  call npm install
  echo.
)

echo 🚀 Starting Jane's Adventure...
echo.
echo    You need TWO command prompt windows:
echo    Terminal 1: Jane's Server ^(port 5551^)
echo    Terminal 2: React App ^(port 3001^)
echo.
echo    Choose:
echo    1^) Start Jane's Server only
echo    2^) Start React App only
echo    3^) Manual instructions
echo.

set /p choice="   Enter choice (1-3): "

if "%choice%"=="1" (
  echo.
  echo    Starting Jane's Narrative Engine on http://localhost:5551...
  echo.
  call npm run mock-server
) else if "%choice%"=="2" (
  echo.
  echo    Starting Jane's Adventure on http://localhost:3001...
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
  echo    Then open: http://localhost:3001
  echo.
) else (
  echo    Invalid choice. Run 'start.bat' again.
)

echo.
pause
