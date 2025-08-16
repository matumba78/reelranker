# 🚀 Render Deployment Guide

## Quick Deploy (Recommended)

### Option 1: Static Site Deployment
1. Go to [render.com](https://render.com)
2. Click "New +" → "Static Site"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `reelranker-frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `build`
   - **Node Version**: `18`

### Environment Variables
Set these in Render dashboard:
```
REACT_APP_API_URL=https://reel-ranker.onrender.com
REACT_APP_ENVIRONMENT=production
NODE_ENV=production
GENERATE_SOURCEMAP=false
```

## Troubleshooting

### If you get "Application exited early":

1. **Check Build Logs**: Look for specific error messages
2. **Verify Environment Variables**: All must be set correctly
3. **Node Version**: Ensure Node 18+ is selected
4. **Build Command**: Should be `npm install && npm run build`
5. **Publish Directory**: Must be `build`

### Common Issues:
- ❌ Missing environment variables
- ❌ Wrong Node version
- ❌ Build command errors
- ❌ Missing dependencies

### ✅ Success Indicators:
- Build completes without errors
- Static files generated in `build/` directory
- Application accessible at Render URL

## Manual Deployment Steps

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Fix Render deployment"
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

## Files Created for Render:
- ✅ `render.yaml` - Blueprint configuration
- ✅ `.nvmrc` - Node version specification
- ✅ `.render-buildpacks` - Buildpack specification
- ✅ `public/_redirects` - SPA routing
- ✅ `scripts/build-render.sh` - Custom build script
