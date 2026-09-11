@echo off
title EP-Pilot Test Installation
cd /d "%~dp0"

echo ==================================================
echo        EP-PILOT TEST ENVIRONMENT INSTALLER
echo ==================================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo [FAIL] Python is not installed or not in PATH.
    echo Install Python 3 and try again.
    pause
    exit /b 1
)

echo [PASS] Python found.

if not exist ".venv" (
    echo [INFO] Creating Python virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo [FAIL] Could not create virtual environment.
        pause
        exit /b 1
    )
)

echo [INFO] Installing required Python packages...
call .venv\Scripts\python.exe -m pip install --upgrade pip
call .venv\Scripts\python.exe -m pip install -r requirements.txt

if errorlevel 1 (
    echo [FAIL] Package installation failed.
    pause
    exit /b 1
)

echo.
echo [PASS] EP-Pilot test environment installed successfully.
echo.
echo You can now run RUN_TEST.bat
echo.
pause