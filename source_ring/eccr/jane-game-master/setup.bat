@echo off
echo.
echo ========================================
echo Jane Die-namic Delta Setup
echo ========================================
echo.

REM Check if .env exists
if exist .env (
    echo [OK] .env file found
) else (
    echo [!] Creating .env from template...
    copy .env.template .env
    echo.
    echo IMPORTANT: Edit .env and add your Gemini API key!
    echo Get your key from: https://makersuite.google.com/app/apikey
    echo.
    pause
)

echo.
echo Installing dependencies...
call npm install

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Edit .env and add your GEMINI_API_KEY
echo 2. Run: node mock-server/jane-delta-server.js
echo 3. In another terminal: npm run dev
echo.
echo See DELTA_README.md for full documentation
echo.
pause
