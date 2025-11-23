@echo off
echo ================================================
echo    RealLife AI Tools Setup and Launcher
echo ================================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo Python found. Checking pip...
pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip is not available
    pause
    exit /b 1
)

echo.
echo Installing required packages...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install requirements
    echo Try running: pip install --user -r requirements.txt
    pause
    exit /b 1
)

echo.
echo ================================================
echo    Setup Complete! Starting the system...
echo ================================================
echo.
echo The system will:
echo - Start the email server on http://localhost:5000
echo - Open the email web interface in your browser
echo - Launch the GUI application
echo.
echo Press Ctrl+C to stop all services
echo.

python run_system.py

echo.
echo System stopped. Press any key to exit.
pause >nul
