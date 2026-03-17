"""
Starlette Vercel Serverless Function
Minimal ASGI framework - lighter than FastAPI
"""
import json
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

# Create Starlette app
app = Starlette(routes=[
    Route('/', lambda request: JSONResponse({
        "message": "Time Tracking API with Starlette",
        "status": "healthy",
        "framework": "Starlette"
    })),
    Route('/api/health', lambda request: JSONResponse({
        "status": "ok",
        "service": "time-tracking",
        "environment": "vercel",
        "framework": "Starlette"
    })),
    Route('/api/test', lambda request: JSONResponse({
        "test": "success",
        "message": "Starlette serverless working",
        "framework": "Starlette"
    }))
])

# Vercel ASGI handler
async def handler(scope, receive, send):
    await app(scope, receive, send)
