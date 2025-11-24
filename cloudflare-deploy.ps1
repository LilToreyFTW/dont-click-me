# Cloudflare Pages Deployment Script for Windows
Write-Host "🚀 Cloudflare Pages Deployment Script" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Check if wrangler is installed
try {
    $wranglerVersion = wrangler --version 2>$null
    Write-Host "✅ Wrangler CLI found: $wranglerVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Wrangler CLI not found. Installing..." -ForegroundColor Yellow
    npm install -g wrangler
}

# Check if logged in
Write-Host "🔐 Checking Cloudflare authentication..." -ForegroundColor Yellow
try {
    wrangler auth login
} catch {
    Write-Host "❌ Authentication failed. Please login manually: wrangler auth login" -ForegroundColor Red
    exit 1
}

# Deploy to Cloudflare Pages
Write-Host "📦 Deploying to Cloudflare Pages..." -ForegroundColor Yellow
try {
    wrangler pages deploy ./static --project-name cores-email-ai-approval --compatibility-date 2024-01-01
    Write-Host "" -ForegroundColor White
    Write-Host "✅ Deployment Complete!" -ForegroundColor Green
    Write-Host "🌐 Your site is now live at: https://cores-email-ai-approval.pages.dev" -ForegroundColor Cyan
    Write-Host "" -ForegroundColor White
    Write-Host "📋 Next Steps:" -ForegroundColor Yellow
    Write-Host "1. Go to https://dash.cloudflare.com" -ForegroundColor White
    Write-Host "2. Navigate to Pages" -ForegroundColor White
    Write-Host "3. Find 'cores-email-ai-approval' project" -ForegroundColor White
    Write-Host "4. Add custom domain if desired (paid feature)" -ForegroundColor White
    Write-Host "5. Enable additional features like analytics" -ForegroundColor White
    Write-Host "" -ForegroundColor White
    Write-Host "💡 For backend functionality, consider:" -ForegroundColor Cyan
    Write-Host "- Vercel for full Flask app deployment" -ForegroundColor White
    Write-Host "- Railway.app for free database hosting" -ForegroundColor White
    Write-Host "- Render.com for free web service hosting" -ForegroundColor White
} catch {
    Write-Host "❌ Deployment failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
