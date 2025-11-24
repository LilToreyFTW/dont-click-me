#!/bin/bash

echo "🚀 Cloudflare Pages Deployment Script"
echo "====================================="
echo ""

# Check if wrangler is installed
if ! command -v wrangler &> /dev/null; then
    echo "❌ Wrangler CLI not found. Installing..."
    npm install -g wrangler
fi

# Check if logged in
echo "🔐 Checking Cloudflare authentication..."
wrangler auth login

# Deploy to Cloudflare Pages
echo "📦 Deploying to Cloudflare Pages..."
wrangler pages deploy ./static --project-name cores-email-ai-approval --compatibility-date 2024-01-01

echo ""
echo "✅ Deployment Complete!"
echo "🌐 Your site is now live at: https://cores-email-ai-approval.pages.dev"
echo ""
echo "📋 Next Steps:"
echo "1. Go to https://dash.cloudflare.com"
echo "2. Navigate to Pages"
echo "3. Find 'cores-email-ai-approval' project"
echo "4. Add custom domain if desired (paid feature)"
echo "5. Enable additional features like analytics"
echo ""
echo "💡 For backend functionality, consider:"
echo "- Vercel for full Flask app deployment"
echo "- Railway.app for free database hosting"
echo "- Render.com for free web service hosting"
