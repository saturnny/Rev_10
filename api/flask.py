"""
Flask Vercel Serverless Function
Alternative to FastAPI - simpler and more compatible
"""
import json
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({
        "message": "Time Tracking API with Flask",
        "status": "healthy",
        "framework": "Flask"
    })

@app.route('/api/health')
def health():
    return jsonify({
        "status": "ok",
        "service": "time-tracking",
        "environment": "vercel",
        "framework": "Flask"
    })

@app.route('/api/test')
def test():
    return jsonify({
        "test": "success",
        "message": "Flask serverless working",
        "method": request.method,
        "headers": dict(request.headers)
    })

# Vercel handler
def handler(environ, start_response):
    return app(environ, start_response)
