@echo off
setlocal EnableDelayedExpansion

echo ============================================================
echo      InstaReelTranscriber - Starting Application
echo ============================================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo [ERROR] Virtual environment not found!
    echo Please run setup_and_download.bat first.
    pause
    exit /b 1
)

REM Check if frontend node_modules exists
if not exist "frontend\node_modules" (
    echo [WARNING] Frontend dependencies not installed!
    echo Running: cd frontend ^&^& npm install
    cd frontend
    npm install
    cd ..
)

echo [INFO] Starting Backend API server...
start "InstaTranscriber Backend" cmd /k "venv\Scripts\activate && uvicorn src.api:app --reload --port 8000"

echo [INFO] Waiting for backend to start...
timeout /t 3 /nobreak >nul

echo [INFO] Starting Frontend development server...
start "InstaTranscriber Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ============================================================
echo   Servers are starting...
echo.
echo   Backend:  http://localhost:8000
echo   Frontend: http://localhost:3000
echo.
echo   Opening browser in 5 seconds...
echo ============================================================

timeout /t 5 /nobreak >nul
start http://localhost:3000

echo.
echo [INFO] Application is running!
echo [INFO] Close the terminal windows to stop the servers.
echo.

endlocal
