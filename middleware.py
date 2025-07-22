from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import status
from fastapi.responses import JSONResponse
import time

PERIOD = 10 #counts in seconds
LIMIT = 5
REQUEST_COUNT = { }

class ratelimit(BaseHTTPMiddleware):
    
    async def dispatch(self, request, call_next):
        client_ip = request.client.host
        now = time.time()  
        window_start = now - PERIOD
        
        if client_ip not in REQUEST_COUNT: 
            REQUEST_COUNT [client_ip] = []

        REQUEST_COUNT [client_ip] = [t for t in REQUEST_COUNT [client_ip] if t > window_start ]
        
        if len(REQUEST_COUNT[client_ip]) >= LIMIT:
            return JSONResponse(content={"detail": "rate limit execeded"},status_code=status.HTTP_429_TOO_MANY_REQUESTS)
        REQUEST_COUNT[client_ip].append(now)
        response = await call_next(request)
        return response 