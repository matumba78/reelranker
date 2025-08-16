from pydantic_settings import BaseSettings
from typing import Optional, List
import os
import secrets

class Settings(BaseSettings):
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "ReelRanker API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "AI-powered viral content analysis and generation API"
    
    # Database Configuration
    # Remote PostgreSQL Configuration
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "reelranker"
    DB_USER: str = "reelranker"
    DB_PASSWORD: str = "reelranker123"
    DB_SSL_MODE: str = "prefer"  # Options: disable, allow, prefer, require, verify-ca, verify-full
    
    # Construct DATABASE_URL from components
    @property
    def DATABASE_URL(self) -> str:
        """Construct database URL from components"""
        # Validate required database components
        if not self.DB_HOST:
            raise ValueError("DB_HOST is required but not set")
        if not self.DB_PORT:
            raise ValueError("DB_PORT is required but not set")
        if not self.DB_NAME:
            raise ValueError("DB_NAME is required but not set")
        if not self.DB_USER:
            raise ValueError("DB_USER is required but not set")
        if not self.DB_PASSWORD:
            raise ValueError("DB_PASSWORD is required but not set")
        
        # Ensure port is an integer
        try:
            port = int(self.DB_PORT)
        except (ValueError, TypeError):
            raise ValueError(f"DB_PORT must be a valid integer, got: {self.DB_PORT}")
        
        if self.DB_SSL_MODE and self.DB_SSL_MODE != "disable":
            return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{port}/{self.DB_NAME}?sslmode={self.DB_SSL_MODE}"
        else:
            return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{port}/{self.DB_NAME}"
    
    # Database Connection Pool Configuration
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 30
    DATABASE_POOL_TIMEOUT: int = 30
    DATABASE_POOL_RECYCLE: int = 3600
    
    # YouTube API Configuration
    YOUTUBE_API_KEY: Optional[str] = None
    
    # AI/ML Configuration
    GOOGLE_AI_API_KEY: Optional[str] = None
    MODEL_NAME: str = "gemini-1.5-flash"
    AI_PROVIDER: str = "google"
    
    # Redis Configuration
    REDIS_URL: str = "redis://localhost:6379"
    REDIS_PASSWORD: Optional[str] = None
    REDIS_DB: int = 0
    
    # Security Configuration
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 100
    RATE_LIMIT_PER_HOUR: int = 1000
    RATE_LIMIT_BURST: int = 50
    
    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_MAX_SIZE: int = 10 * 1024 * 1024  # 10MB
    LOG_BACKUP_COUNT: int = 5
    
    # CORS Configuration
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 1
    
    # Health Check
    HEALTH_CHECK_INTERVAL: int = 30
    
    # Cache Configuration
    CACHE_TTL: int = 3600  # 1 hour
    CACHE_MAX_SIZE: int = 1000
    
    # Monitoring
    ENABLE_METRICS: bool = False
    METRICS_PORT: int = 9090
    
    # File Upload
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_FILE_TYPES: List[str] = ["image/jpeg", "image/png", "image/gif", "video/mp4"]
    
    # External API Timeouts
    REQUEST_TIMEOUT: int = 30
    YOUTUBE_API_TIMEOUT: int = 10
    AI_API_TIMEOUT: int = 60
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings()

# Environment-specific overrides
if settings.ENVIRONMENT == "production":
    settings.DEBUG = False
    settings.LOG_LEVEL = "WARNING"
    settings.WORKERS = 4
    settings.ENABLE_METRICS = True
    # Ensure secure defaults for production
    if settings.SECRET_KEY == "your-secret-key-here":
        settings.SECRET_KEY = secrets.token_urlsafe(32)
    if not settings.BACKEND_CORS_ORIGINS or settings.BACKEND_CORS_ORIGINS == ["http://localhost:3000", "http://localhost:8080"]:
        settings.BACKEND_CORS_ORIGINS = []  # Should be set via environment variable in production
