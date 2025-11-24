# RealLife AI Tools - Complete Build & Run Script
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "   RealLife AI Tools - Complete Build & Run" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "🔨 Building complete system..." -ForegroundColor Yellow
try {
    $buildResult = python build_all.py 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Build failed!" -ForegroundColor Red
        Write-Host "Error details:" -ForegroundColor Red
        Write-Host $buildResult -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
    Write-Host "✅ Build completed successfully!" -ForegroundColor Green
} catch {
    Write-Host "❌ Build error: $($_.Exception.Message)" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "🚀 Launching unified system (GUI + Web Server)..." -ForegroundColor Cyan
try {
    python unified_launcher.py
} catch {
    Write-Host "❌ System error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "System shutdown complete." -ForegroundColor Yellow
Read-Host "Press Enter to exit"
