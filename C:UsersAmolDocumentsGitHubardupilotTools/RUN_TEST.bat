@echo off
title EP-Pilot Engineering Test
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo [FAIL] Test environment is not installed.
    echo Please run INSTALL.bat first.
    echo.
    pause
    exit /b 1
)

.venv\Scripts\python.exe run_test.py

echo.
pause