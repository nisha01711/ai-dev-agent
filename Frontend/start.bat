@echo off
echo ====================================
echo AI Dev Agent Frontend - Quick Setup
echo ====================================
echo.

echo Step 1: Installing dependencies...
call npm install

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to install dependencies!
    echo Please make sure Node.js is installed.
    pause
    exit /b 1
)

echo.
echo ====================================
echo Installation Complete! ✓
echo ====================================
echo.
echo Starting development server...
echo The app will open at http://localhost:3000
echo.
echo Press Ctrl+C to stop the server
echo ====================================
echo.

call npm run dev

pause
