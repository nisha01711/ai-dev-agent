@echo off
echo ====================================
echo AI Software Engineer Agent - Backend
echo ====================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate
echo.

REM Check if .env exists
if not exist ".env" (
    echo WARNING: .env file not found!
    echo Please copy .env.example to .env and configure your API keys
    echo.
    pause
    exit /b 1
)

REM Install/upgrade dependencies
echo Installing dependencies...
pip install -r requirements.txt
echo.

REM Create necessary directories
if not exist "data\chroma_db" mkdir data\chroma_db
if not exist "data\projects" mkdir data\projects
if not exist "logs" mkdir logs

REM Run the application
echo Starting Flask application...
echo Server will be available at http://localhost:5000
echo Press Ctrl+C to stop
echo.
python app.py

pause
