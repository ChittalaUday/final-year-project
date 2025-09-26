@echo off
echo Setting up Python environment for CLIP API...

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    exit /b 1
)

REM Create virtual environment
echo Creating Python virtual environment...
if exist python-env (
    echo Removing existing environment...
    rmdir /s /q python-env
)

python -m venv python-env
if %errorlevel% neq 0 (
    echo ERROR: Failed to create virtual environment
    exit /b 1
)

REM Activate environment and install dependencies
echo Activating environment and installing dependencies...
call python-env\Scripts\activate.bat

REM Upgrade pip first
python -m pip install --upgrade pip

REM Install requirements
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install Python dependencies
    exit /b 1
)

echo.
echo ✅ Python environment setup complete!
echo.
echo To activate the environment manually:
echo   python-env\Scripts\activate.bat
echo.
echo To test the setup:
echo   npm run python:test
echo.
pause