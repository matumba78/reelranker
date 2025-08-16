# 🚀 Render Deployment Guide (Node 22 Compatible)

## ✅ Node.js Version Fix Applied

**Issue**: Render uses Node 22.16.0 by default, but your app was configured for Node 18
**Solution**: Updated configuration to be compatible with Node 22

## Quick Deploy (Recommended)

### Option 1: Static Site Deployment
1. Go to [render.com](https://render.com)
2. Click "New +" → "Static Site"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `reelranker-frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `build`
   - **Node Version**: `22` (Render default)

### Environment Variables
Set these in Render dashboard:
```
REACT_APP_API_URL=https://reel-ranker.onrender.com
REACT_APP_ENVIRONMENT=production
NODE_ENV=production
GENERATE_SOURCEMAP=false
```

## Key Changes Made

### ✅ Node.js Compatibility
- Updated `.nvmrc` to Node 22
- Added `engines` field in package.json
- Updated react-scripts to latest version

### ✅ Build Configuration
- Simplified build command
- Removed problematic prebuild scripts
- Added proper environment variables

### ✅ Render-Specific Files
- `render.yaml` - Blueprint configuration
- `.nvmrc` - Node version specification
- `public/_redirects` - SPA routing

## Troubleshooting

### If you still get "Application exited early":

1. **Check Node Version**: Ensure Render is using Node 22
2. **Verify Build Logs**: Look for specific error messages
3. **Environment Variables**: All must be set correctly
4. **Build Command**: Should be `npm install && npm run build`

### Common Issues:
- ❌ Node version mismatch (fixed)
- ❌ Missing environment variables
- ❌ Build command errors
- ❌ Missing dependencies

## Manual Deployment Steps

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Fix Node 22 compatibility for Render"
   git push
   ```

2. **Deploy on Render**:
   - Use Static Site deployment
   - Set environment variables
   - Monitor build logs

3. **Verify Deployment**:
   - Check application loads
   - Test API connections
   - Verify routing works

## Files Updated for Node 22:
- ✅ `.nvmrc` - Updated to Node 22
- ✅ `package.json` - Added engines field
- ✅ `render.yaml` - Simplified configuration
- ✅ `react-scripts` - Updated to latest version
