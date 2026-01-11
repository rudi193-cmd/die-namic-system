@echo off
TITLE Vision Board - Image Categorizer
COLOR 0E

echo ==================================================
echo      VISION BOARD - AI Image Categorizer
echo ==================================================
echo.

if "%~1"=="" (
    echo Usage: CATEGORIZE.bat [folder_path]
    echo.
    echo Example: CATEGORIZE.bat "C:\Users\You\Pictures\Goals"
    echo.
    set /p FOLDER="Enter folder path (or drag folder here): "
) else (
    set FOLDER=%~1
)

echo.
echo Categorizing images in: %FOLDER%
echo Using PORTABLE mode (images embedded in JSON)
echo.

python categorize.py "%FOLDER%" --portable

echo.
echo ==================================================
echo Done! Now import categories.json into the Vision Board.
echo ==================================================
echo.

PAUSE
