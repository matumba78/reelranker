#!/usr/bin/env python3
"""
Script to create the .env file with proper database configuration
"""

env_content = """# API Configuration
API_V1_STR=/api/v1
PROJECT_NAME=ReelRanker API
VERSION=1.0.0
DESCRIPTION=AI-powered viral content analysis and generation API

# Remote Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=reelranker
DB_USER=reelranker
DB_PASSWORD=reelranker123
DB_SSL_MODE=prefer

# YouTube API Configuration
YOUTUBE_API_KEY="AIzaSyBRSkOPkEEaXr207xEsUYjeckQpVPxIs2Y"

# AI/ML Configuration
GOOGLE_AI_API_KEY="AIzaSyA-mAocqk6ZoJo33p5hz65KsTSr50LCwhw"
AI_PROVIDER=google
MODEL_NAME=gemini-1.5-flash

# Redis Configuration
REDIS_URL=redis://localhost:6379

# Security Configuration
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Rate Limiting
RATE_LIMIT_PER_MINUTE=100

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=logs/app.log

# CORS Configuration
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:8080"]

# Environment
ENVIRONMENT=development
DEBUG=true
"""

def create_env_file():
    """Create the .env file"""
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ .env file created successfully!")
        print("📝 Please update the database configuration with your actual values:")
        print("   - DB_HOST: Your database host")
        print("   - DB_PORT: Your database port (usually 5432)")
        print("   - DB_NAME: Your database name")
        print("   - DB_USER: Your database username")
        print("   - DB_PASSWORD: Your database password")
        print("   - DB_SSL_MODE: SSL mode (prefer, require, disable)")
        print("   - YOUTUBE_API_KEY: Your YouTube API key")
        print("   - GOOGLE_AI_API_KEY: Your Google AI API key")
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")

if __name__ == "__main__":
    create_env_file()
