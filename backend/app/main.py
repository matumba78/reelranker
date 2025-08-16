import time
import signal
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import uvicorn
import redis

from app.core.config import settings
from app.core.logging import logger, get_logger
from app.db.connection import init_db, check_db_health, close_db_connections
from app.core.middleware import (
    RateLimitMiddleware,
    RequestLoggingMiddleware,
    SecurityHeadersMiddleware,
    ErrorHandlingMiddleware,
    HealthCheckMiddleware
)

# Import API routers
from app.api.v1 import shorts, topics, trends, score, generate

# Global variables for cleanup
redis_client = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("Starting ReelRanker API...")
    
    # Initialize Redis
    global redis_client
    try:
        redis_client = redis.from_url(
            settings.REDIS_URL,
            password=settings.REDIS_PASSWORD,
            db=settings.REDIS_DB,
            decode_responses=True
        )
        redis_client.ping()
        logger.info("Redis connection established")
    except Exception as e:
        logger.warning(f"Redis connection failed: {e}")
        redis_client = None
    
    # Initialize database
    try:
        if init_db():
            logger.info("Database initialized successfully")
        else:
            logger.warning("Database initialization failed - using mock data")
    except Exception as e:
        logger.warning(f"Database initialization error: {e}")
    
    logger.info("ReelRanker API started successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down ReelRanker API...")
    
    # Close database connections
    close_db_connections()
    
    # Close Redis connection
    if redis_client:
        redis_client.close()
        logger.info("Redis connection closed")
    
    logger.info("ReelRanker API shutdown complete")

# Create FastAPI app with lifespan
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan
)

# Add middleware in order (last added = first executed)
if settings.ENVIRONMENT == "production":
    # Trusted host middleware for production
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*"]  # Configure with your domain in production
    )

# Add custom middleware
app.add_middleware(ErrorHandlingMiddleware)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(HealthCheckMiddleware)

# Add rate limiting middleware
if redis_client:
    app.add_middleware(RateLimitMiddleware, redis_client=redis_client)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(shorts.router, prefix=settings.API_V1_STR, tags=["shorts"])
app.include_router(topics.router, prefix=settings.API_V1_STR, tags=["topics"])
app.include_router(trends.router, prefix=settings.API_V1_STR, tags=["trends"])
app.include_router(score.router, prefix=settings.API_V1_STR, tags=["score"])
app.include_router(generate.router, prefix=settings.API_V1_STR, tags=["generate"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to ReelRanker API",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "docs": "/docs" if settings.DEBUG else None,
        "health": "/health"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    health_status = {
        "status": "healthy",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "timestamp": time.time(),
        "services": {}
    }
    
    # Check database health
    try:
        db_healthy = check_db_health()
        health_status["services"]["database"] = "healthy" if db_healthy else "unhealthy"
    except Exception as e:
        health_status["services"]["database"] = "error"
        logger.error(f"Database health check failed: {e}")
    
    # Check Redis health
    try:
        if redis_client:
            redis_client.ping()
            health_status["services"]["redis"] = "healthy"
        else:
            health_status["services"]["redis"] = "not_configured"
    except Exception as e:
        health_status["services"]["redis"] = "unhealthy"
        logger.error(f"Redis health check failed: {e}")
    
    # Determine overall health
    overall_healthy = all(
        status in ["healthy", "not_configured"] 
        for status in health_status["services"].values()
    )
    
    status_code = 200 if overall_healthy else 503
    health_status["status"] = "healthy" if overall_healthy else "unhealthy"
    
    return JSONResponse(
        status_code=status_code,
        content=health_status
    )

@app.get("/ready")
async def readiness_check():
    """Readiness check endpoint for Kubernetes"""
    # Check if all required services are ready
    db_ready = check_db_health()
    
    if not db_ready:
        return JSONResponse(
            status_code=503,
            content={"status": "not_ready", "reason": "database_unavailable"}
        )
    
    return {"status": "ready"}

@app.get("/metrics")
async def metrics():
    """Basic metrics endpoint"""
    if not settings.ENABLE_METRICS:
        raise HTTPException(status_code=404, detail="Metrics not enabled")
    
    # Basic application metrics
    metrics_data = {
        "app": {
            "version": settings.VERSION,
            "environment": settings.ENVIRONMENT,
            "uptime": time.time()  # You'd want to track actual uptime
        },
        "database": {
            "connected": check_db_health()
        },
        "redis": {
            "connected": redis_client is not None and redis_client.ping()
        }
    }
    
    return metrics_data

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Global HTTP exception handler"""
    request_id = getattr(request.state, "request_id", "unknown")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "request_id": request_id
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    request_id = getattr(request.state, "request_id", "unknown")
    
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error" if not settings.DEBUG else str(exc),
            "status_code": 500,
            "request_id": request_id
        }
    )

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    logger.info(f"Received signal {signum}, shutting down gracefully...")
    sys.exit(0)

# Register signal handlers
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        workers=settings.WORKERS if settings.ENVIRONMENT == "production" else 1,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
        access_log=True
    )
