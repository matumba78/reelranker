#!/bin/bash
set -e

echo "🐳 Docker Deployment Script for ReelRanker Frontend"
echo "=================================================="

# Configuration
DOCKER_USERNAME="your-dockerhub-username"
IMAGE_NAME="reelranker-frontend"
TAG="latest"

# Build the image
echo "🔨 Building Docker image..."
docker build -t $IMAGE_NAME .

# Tag for Docker Hub
echo "🏷️  Tagging image for Docker Hub..."
docker tag $IMAGE_NAME $DOCKER_USERNAME/$IMAGE_NAME:$TAG

# Push to Docker Hub
echo "📤 Pushing to Docker Hub..."
docker push $DOCKER_USERNAME/$IMAGE_NAME:$TAG

echo "✅ Docker image deployed successfully!"
echo "🔗 Image: $DOCKER_USERNAME/$IMAGE_NAME:$TAG"
echo ""
echo "🚀 Next steps:"
echo "1. Update render.yaml with your Docker Hub image"
echo "2. Deploy on Render using Docker registry"
