"""
Simple in-memory rate limiting middleware using a sliding window counter.

Note: For production use, a distributed rate limiter (e.g., Redis) is recommended.
"""

import time
from collections import defaultdict, deque
from typing import Callable, Deque, Dict

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse




class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    A basic rate limiting middleware applying a per-key limit over a time window.
    """

    def __init__(
        self,
        app,
        requests: int,
        window_seconds: int,
        key_func: Callable[[dict], str],
    ):
        super().__init__(app)
        self.requests = requests
        self.window = window_seconds
        self.key_func = key_func
        self.buckets: Dict[str, Deque[float]] = defaultdict(deque)

    async def dispatch(self, request: Request, call_next):
        key = self.key_func(request.scope)
        now = time.time()

        bucket = self.buckets[key]
        # Remove timestamps older than window
        while bucket and now - bucket[0] > self.window:
            bucket.popleft()

        if len(bucket) >= self.requests:
            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded", "code": "rate_limited"},
            )

        bucket.append(now)
        response = await call_next(request)
        # Could add headers with rate limit info; guard against responses without headers (e.g., StreamingResponse closed)
        try:
            response.headers["X-RateLimit-Limit"] = str(self.requests)
            response.headers["X-RateLimit-Remaining"] = str(max(0, self.requests - len(bucket)))
            response.headers["X-RateLimit-Window"] = str(self.window)
        except Exception:
            # Do not fail the request if headers cannot be set
            pass
        return response
