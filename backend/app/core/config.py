from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "ReelRanker API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "AI-powered viral content analysis and generation API"
    
    # Database Configuration
    DATABASE_URL: str = "postgresql://reelranker:reelranker123@localhost:5432/reelranker"
    
    # YouTube API Configuration
    YOUTUBE_API_KEY: Optional[str] = None
    
    # AI/ML Configuration
    OPENAI_API_KEY: Optional[str] = None
    MODEL_NAME: str = "gpt-3.5-turbo"
    
    # Redis Configuration
    REDIS_URL: str = "redis://localhost:6379"
    
    # Security Configuration
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 100
    
    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    
    # CORS Configuration
    BACKEND_CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:8080"]
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings()

# Environment-specific overrides
if settings.ENVIRONMENT == "production":
    settings.DEBUG = False
    settings.LOG_LEVEL = "WARNING"
