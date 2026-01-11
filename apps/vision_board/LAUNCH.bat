@echo off
TITLE Vision Board
COLOR 0E

echo ==================================================
echo      VISION BOARD - Local Server
echo ==================================================
echo.
echo Starting server at http://localhost:8080
echo.
echo NOTE: To load local images from categories.json,
echo       you may need to use "Quick Import Folder" instead,
echo       or run Chrome with --allow-file-access-from-files
echo.

start "" "http://localhost:8080"
python -m http.server 8080

PAUSE
