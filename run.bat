@echo off
echo ========================================
echo BerkleyCore Loss Analysis Platform
echo ========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    echo Make sure to check "Add to PATH" during installation
    pause
    exit /b 1
)

:: Check if dependencies are installed
echo Checking dependencies...
pip show streamlit >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

echo.
echo Starting BerkleyCore...
echo Your browser will open to http://localhost:8501
echo Press Ctrl+C in this window to stop the server
echo.

streamlit run app.py

pause
