#!/bin/bash
set -e

echo "🚀 Starting Render build process..."

# Set environment variables for Render
export NODE_ENV=production
export GENERATE_SOURCEMAP=false
export CI=false

echo "📦 Installing dependencies..."
npm install

echo "🔨 Building application..."
npm run build

echo "✅ Build completed successfully!"
echo "📁 Build directory contents:"
ls -la build/

echo "🎯 Render deployment ready!"
