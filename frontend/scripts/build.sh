#!/bin/bash

# Production Build Script for ReelRanker Frontend

set -e

echo "🚀 Starting production build..."

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: package.json not found. Please run this script from the frontend directory."
    exit 1
fi

# Clean previous build
echo "🧹 Cleaning previous build..."
rm -rf build/
rm -rf node_modules/

# Install dependencies
echo "📦 Installing dependencies..."
npm ci --only=production

# Set production environment
export NODE_ENV=production
export REACT_APP_ENVIRONMENT=production

# Build the application
echo "🔨 Building application..."
npm run build

# Check if build was successful
if [ ! -d "build" ]; then
    echo "❌ Build failed! build directory not found."
    exit 1
fi

# Optimize build
echo "⚡ Optimizing build..."
find build -name "*.js" -exec gzip -9 {} \;
find build -name "*.css" -exec gzip -9 {} \;

# Create build info
echo "📝 Creating build info..."
echo "Build completed at: $(date)" > build/build-info.txt
echo "Version: $(node -p "require('./package.json').version")" >> build/build-info.txt
echo "Environment: production" >> build/build-info.txt

echo "✅ Production build completed successfully!"
echo "📁 Build directory: $(pwd)/build"
echo "📊 Build size: $(du -sh build | cut -f1)"

# Optional: Run tests
if [ "$1" = "--test" ]; then
    echo "🧪 Running tests..."
    npm test -- --watchAll=false --passWithNoTests
fi
