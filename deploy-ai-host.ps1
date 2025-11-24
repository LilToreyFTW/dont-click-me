# Mega Enhanced AI Host Deployment Script
# Advanced AI-powered Cloudflare Workers deployment

param(
    [switch]$Dev,
    [switch]$Test,
    [switch]$Analytics,
    [switch]$SetupAI,
    [switch]$SetupD1,
    [string]$GatewayId
)

Write-Host "🤖 Mega Enhanced AI Host Deployment" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

# Check if wrangler is installed
try {
    $wranglerVersion = & wrangler --version 2>$null
    Write-Host "✅ Wrangler CLI: $wranglerVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Wrangler CLI not found. Installing..." -ForegroundColor Yellow
    npm install -g wrangler
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to install Wrangler. Please install Node.js first." -ForegroundColor Red
        exit 1
    }
}

# Setup AI Gateway if requested
if ($SetupAI) {
    Write-Host "🧠 Setting up AI Gateway..." -ForegroundColor Yellow
    try {
        $gatewayResult = & wrangler ai create-gateway 2>&1
        Write-Host "✅ AI Gateway created:" -ForegroundColor Green
        Write-Host $gatewayResult -ForegroundColor White

        # Extract gateway ID and update wrangler.toml
        $gatewayId = ($gatewayResult | Select-String -Pattern "gateway-id: (.+)").Matches.Groups[1].Value
        if ($gatewayId) {
            Write-Host "🔧 Updating wrangler.toml with gateway ID: $gatewayId" -ForegroundColor Yellow
            (Get-Content wrangler.toml) -replace 'gateway_id = "your-ai-gateway-id"', "gateway_id = `"$gatewayId`"" | Set-Content wrangler.toml
        }
    } catch {
        Write-Host "❌ Failed to create AI Gateway: $($_.Exception.Message)" -ForegroundColor Red
    }
    exit 0
}

# Setup D1 Database if requested
if ($SetupD1) {
    Write-Host "🗄️ Setting up D1 Analytics Database..." -ForegroundColor Yellow
    try {
        $dbResult = & wrangler d1 create ai-host-analytics 2>&1
        Write-Host "✅ D1 Database created:" -ForegroundColor Green
        Write-Host $dbResult -ForegroundColor White
    } catch {
        Write-Host "❌ Failed to create D1 Database: $($_.Exception.Message)" -ForegroundColor Red
    }
    exit 0
}

# Check authentication
Write-Host "🔐 Checking Cloudflare authentication..." -ForegroundColor Yellow
try {
    $authResult = & wrangler whoami 2>$null
    Write-Host "✅ Authenticated as: $($authResult -split "`n" | Select-Object -First 1)" -ForegroundColor Green
} catch {
    Write-Host "❌ Not authenticated. Please run: wrangler auth login" -ForegroundColor Red
    exit 1
}

# Validate configuration
Write-Host "🔍 Validating configuration..." -ForegroundColor Yellow
if (!(Test-Path "wrangler.toml")) {
    Write-Host "❌ wrangler.toml not found!" -ForegroundColor Red
    exit 1
}

if (!(Test-Path "workers/ai-host.js")) {
    Write-Host "❌ workers/ai-host.js not found!" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Configuration validated" -ForegroundColor Green

# Development mode
if ($Dev) {
    Write-Host "🚀 Starting development server..." -ForegroundColor Cyan
    Write-Host "🌐 Local development URL: http://localhost:8787" -ForegroundColor White
    Write-Host "📊 Analytics will be available at: http://localhost:8787/analytics" -ForegroundColor White
    Write-Host "🧠 AI Insights at: http://localhost:8787/ai-insights" -ForegroundColor White
    Write-Host "💚 Health check at: http://localhost:8787/health" -ForegroundColor White
    Write-Host ""
    Write-Host "Press Ctrl+C to stop the development server" -ForegroundColor Yellow
    Write-Host ""

    & wrangler dev --port 8787
    exit 0
}

# Test mode
if ($Test) {
    Write-Host "🧪 Running AI Host tests..." -ForegroundColor Yellow
    & wrangler dev --test-scheduled
    exit 0
}

# Analytics mode
if ($Analytics) {
    Write-Host "📊 Starting analytics monitoring..." -ForegroundColor Cyan
    Write-Host "Press Ctrl+C to stop monitoring" -ForegroundColor Yellow
    & wrangler tail --format=pretty
    exit 0
}

# Production deployment
Write-Host "🚀 Deploying Mega Enhanced AI Host to production..." -ForegroundColor Cyan
Write-Host ""

try {
    $deployResult = & wrangler deploy 2>&1

    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Deployment successful!" -ForegroundColor Green
        Write-Host ""

        # Extract the deployed URL
        $deployedUrl = ($deployResult | Select-String -Pattern "https://.+\.workers\.dev").Matches.Value
        if ($deployedUrl) {
            Write-Host "🌐 Your AI Host is live at: $deployedUrl" -ForegroundColor Cyan
            Write-Host ""
            Write-Host "📋 Important URLs:" -ForegroundColor Yellow
            Write-Host "🏠 Homepage: $deployedUrl" -ForegroundColor White
            Write-Host "💚 Health Check: $deployedUrl/health" -ForegroundColor White
            Write-Host "📊 Analytics: $deployedUrl/analytics" -ForegroundColor White
            Write-Host "🧠 AI Insights: $deployedUrl/ai-insights" -ForegroundColor White
            Write-Host "📧 Email API: $deployedUrl/api/email/send" -ForegroundColor White
            Write-Host "🎮 Discord API: $deployedUrl/api/discord/analyze" -ForegroundColor White
        }

        Write-Host ""
        Write-Host "🎯 AI Host Features Activated:" -ForegroundColor Cyan
        Write-Host "• 🤖 AI-powered request analysis and optimization" -ForegroundColor White
        Write-Host "• 🔒 Advanced security with threat detection" -ForegroundColor White
        Write-Host "• 📊 Real-time analytics and performance monitoring" -ForegroundColor White
        Write-Host "• ⚡ Intelligent caching and content optimization" -ForegroundColor White
        Write-Host "• 🌐 Global edge computing with AI routing" -ForegroundColor White
        Write-Host "• 🔮 Predictive performance and scaling" -ForegroundColor White
        Write-Host "• 🛡️ Automated security responses" -ForegroundColor White

        Write-Host ""
        Write-Host "📈 Monitoring & Management:" -ForegroundColor Yellow
        Write-Host "• Run '.\deploy-ai-host.ps1 -Analytics' to monitor logs" -ForegroundColor White
        Write-Host "• Visit analytics endpoints for AI insights" -ForegroundColor White
        Write-Host "• Automatic performance optimization active" -ForegroundColor White

    } else {
        Write-Host "❌ Deployment failed!" -ForegroundColor Red
        Write-Host "Error output:" -ForegroundColor Red
        Write-Host $deployResult -ForegroundColor Red
        exit 1
    }

} catch {
    Write-Host "❌ Deployment error: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🎉 Mega Enhanced AI Host is now live and learning!" -ForegroundColor Green
Write-Host "🤖 The AI will continuously optimize performance and security" -ForegroundColor Cyan
