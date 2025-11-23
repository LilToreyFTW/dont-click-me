# RealLife AI Tools Setup and Launcher
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "   RealLife AI Tools Setup and Launcher" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ from https://python.org" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Installing required packages..." -ForegroundColor Yellow
try {
    pip install -r requirements.txt
    Write-Host "Requirements installed successfully!" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Failed to install requirements" -ForegroundColor Red
    Write-Host "Try running: pip install --user -r requirements.txt" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "   Setup Complete! Starting the system..." -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "The system will:" -ForegroundColor White
Write-Host "- Start the email server on http://localhost:5000" -ForegroundColor White
Write-Host "- Open the email web interface in your browser" -ForegroundColor White
Write-Host "- Launch the GUI application" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C to stop all services" -ForegroundColor Yellow
Write-Host ""

try {
    python run_system.py
} catch {
    Write-Host ""
    Write-Host "System stopped or encountered an error." -ForegroundColor Yellow
} finally {
    Write-Host ""
    Read-Host "Press Enter to exit"
}
