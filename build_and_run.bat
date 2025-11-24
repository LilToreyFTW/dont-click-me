@echo off
echo ================================================
echo    RealLife AI Tools - Complete Build & Run
echo ================================================
echo.

echo Building complete system...
python build_all.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ Build failed! Please check the errors above.
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ Build completed successfully!
echo.

echo Launching unified system (GUI + Web Server)...
python unified_launcher.py

echo.
echo System shutdown complete.
pause
