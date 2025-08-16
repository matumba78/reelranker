#!/bin/bash

# Production Deployment Script for ReelRanker Frontend

echo "🚀 Starting production deployment..."

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: package.json not found. Please run this script from the frontend directory."
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
npm ci --only=production

# Run linting
echo "🔍 Running linting..."
npm run lint

# Build the application
echo "🏗️ Building production bundle..."
npm run build

# Check if build was successful
if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
    echo "📊 Bundle size analysis:"
    echo "   - Main bundle: $(du -h build/static/js/main.*.js | cut -f1)"
    echo "   - CSS bundle: $(du -h build/static/css/main.*.css | cut -f1)"
    echo ""
    echo "🌐 Your application is ready for deployment!"
    echo "   - Build folder: ./build"
    echo "   - Serve locally: npx serve -s build"
    echo "   - Deploy to: Netlify, Vercel, or any static hosting service"
else
    echo "❌ Build failed!"
    exit 1
fi
