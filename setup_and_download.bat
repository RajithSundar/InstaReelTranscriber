@echo off
setlocal EnableDelayedExpansion

echo ============================================================
echo   InstaTranscriber Setup & Pre-Download
echo ============================================================

REM 1. Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found! Please install Python 3.8+
    pause
    exit /b 1
)

REM 2. Create Virtual Environment if missing
if not exist "venv" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
)

REM 3. Activate Venv and Install Requirements
call venv\Scripts\activate.bat
echo [INFO] Installing/Updating dependencies...
python -m pip install --upgrade pip >nul
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)

REM 4. Pre-download Whisper Model (Robust)
echo.
echo [INFO] Pre-downloading Whisper model to avoid timeout errors...
python src/model_downloader.py --model base
if %errorlevel% neq 0 (
    echo [ERROR] Model download failed even with robust downloader.
    echo Please check your internet connection.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   Setup Complete! Model is ready.
echo ============================================================
echo.
echo You can now run the tool using:
echo python src/main.py "YOUR_INSTAGRAM_URL"
echo.

endlocal
