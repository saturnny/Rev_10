"""
Vercel Serverless Function - FastAPI Standard Entry Point
Following ChatGPT's recommendations for Vercel compatibility
"""
from app.main import app

# Vercel precisa disso - entrypoint padrão
handler = app

# Export para Vercel
__all__ = ["handler"]
