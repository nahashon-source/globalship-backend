"""
Rate limiting middleware using Redis.
"""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import logging

from app.core.config import settings
from app.services.redis_service import redis_service

logger = logging.getLogger(__name__)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware using Redis."""
    
    def __init__(self, app):
        super().__init__(app)
        self.rate_limit = settings.RATE_LIMIT_PER_MINUTE
        self.window = 60  # 60 seconds
    
    async def dispatch(self, request: Request, call_next):
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/api/v1/docs", "/api/v1/openapi.json"]:
            return await call_next(request)
        
        # Get client IP
        client_ip = request.client.host
        
        # Create rate limit key
        key = f"rate_limit:{client_ip}"
        
        try:
            # Get current count from Redis
            current_count = redis_service.get(key) or 0
            
            if isinstance(current_count, dict):
                current_count = 0
            
            current_count = int(current_count)
            
            if current_count >= self.rate_limit:
                logger.warning(f"Rate limit exceeded for IP: {client_ip}")
                return JSONResponse(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    content={
                        "detail": "Too many requests. Please try again later.",
                        "retry_after": 60
                    }
                )
            
            # Increment counter
            new_count = redis_service.increment(key)
            
            # Set expiry if first request
            if current_count == 0 and redis_service.redis_client:
                redis_service.redis_client.expire(key, self.window)
            
            response = await call_next(request)
            
            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.rate_limit)
            response.headers["X-RateLimit-Remaining"] = str(max(0, self.rate_limit - new_count))
            response.headers["X-RateLimit-Reset"] = str(self.window)
            
            return response
            
        except Exception as e:
            logger.error(f"Rate limiting error: {e}")
            # Don't block requests if Redis is down
            return await call_next(request)
