"""
Vercel Serverless Function - Teste Simples
Seguindo exatamente as recomendações do ChatGPT
"""
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"msg": "deploy funcionando"}

@app.get("/api/test")
def test():
    return {"msg": "deploy funcionando", "status": "ok"}

# Vercel precisa disso
handler = app
