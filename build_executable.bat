@echo off
REM Batch script to create executable using pyinstaller

REM Check if virtual environment is activated
if not defined VIRTUAL_ENV (
    echo Please activate your virtual environment before running this script.
    pause
    exit /b
)

REM Create executable with pyinstaller
pyinstaller --onefile --windowed app.py

pause
