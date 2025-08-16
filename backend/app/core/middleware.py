import time
import uuid
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
import redis
import json
from collections import defaultdict
import asyncio

from app.core.config import settings
from app.core.logging import log_request, get_logger

logger = get_logger(__name__)

class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware using Redis"""
    
    def __init__(self, app, redis_client: redis.Redis = None):
        super().__init__(app)
        self.redis_client = redis_client
        self.rate_limits = {
            "per_minute": settings.RATE_LIMIT_PER_MINUTE,
            "per_hour": settings.RATE_LIMIT_PER_HOUR,
            "burst": settings.RATE_LIMIT_BURST
        }
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Get client IP
        client_ip = self._get_client_ip(request)
        
        # Check rate limits
        if not await self._check_rate_limit(client_ip):
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "retry_after": 60
                }
            )
        
        # Continue with request
        response = await call_next(request)
        return response
    
    def _get_client_ip(self, request: Request) -> str:
        """Get client IP address"""
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return request.client.host
    
    async def _check_rate_limit(self, client_ip: str) -> bool:
        """Check if client has exceeded rate limits"""
        if not self.redis_client:
            return True  # Skip rate limiting if Redis is not available
        
        try:
            current_time = int(time.time())
            
            # Check per-minute limit
            minute_key = f"rate_limit:{client_ip}:minute:{current_time // 60}"
            minute_count = self.redis_client.get(minute_key)
            
            if minute_count and int(minute_count) >= self.rate_limits["per_minute"]:
                return False
            
            # Check per-hour limit
            hour_key = f"rate_limit:{client_ip}:hour:{current_time // 3600}"
            hour_count = self.redis_client.get(hour_key)
            
            if hour_count and int(hour_count) >= self.rate_limits["per_hour"]:
                return False
            
            # Increment counters
            pipe = self.redis_client.pipeline()
            pipe.incr(minute_key)
            pipe.expire(minute_key, 60)
            pipe.incr(hour_key)
            pipe.expire(hour_key, 3600)
            pipe.execute()
            
            return True
            
        except Exception as e:
            logger.error(f"Rate limiting error: {e}")
            return True  # Allow request if rate limiting fails

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging HTTP requests"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Generate request ID
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        # Add request ID to headers
        request.headers.__dict__["_list"].append(
            (b"x-request-id", request_id.encode())
        )
        
        # Start timing
        start_time = time.time()
        
        # Process request
        response = await call_next(request)
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Log request
        log_request(
            request_id=request_id,
            method=request.method,
            path=str(request.url.path),
            status_code=response.status_code,
            duration=duration
        )
        
        # Add request ID to response headers
        response.headers["X-Request-ID"] = request_id
        
        return response

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware for adding security headers"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)
        
        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        # Add CSP header in production
        if settings.ENVIRONMENT == "production":
            response.headers["Content-Security-Policy"] = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline'; "
                "style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data: https:; "
                "font-src 'self'; "
                "connect-src 'self';"
            )
        
        return response

class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Middleware for handling errors gracefully"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            logger.error(f"Unhandled exception in middleware: {e}", exc_info=True)
            
            # Return generic error response
            return JSONResponse(
                status_code=500,
                content={
                    "error": "Internal server error",
                    "request_id": getattr(request.state, "request_id", "unknown")
                }
            )

class HealthCheckMiddleware(BaseHTTPMiddleware):
    """Middleware to handle health check requests efficiently"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Fast path for health checks
        if request.url.path == "/health":
            return JSONResponse(
                status_code=200,
                content={
                    "status": "healthy",
                    "timestamp": time.time(),
                    "version": settings.VERSION
                }
            )
        
        return await call_next(request)
