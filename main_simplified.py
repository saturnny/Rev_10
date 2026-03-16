"""
Simplified main.py for Vercel deployment
"""
import os
from fastapi import FastAPI, Depends, HTTPException, status, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional

# Database setup
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import NullPool
import ssl

# Load environment
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not configured")

# SSL context
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Engine with NullPool for serverless
engine = create_engine(
    DATABASE_URL,
    connect_args={"ssl_context": ssl_context},
    poolclass=NullPool,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# App setup
app = FastAPI(title="Time Tracking System", docs_url=None, redoc_url=None)

# Static files
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app.mount("/static", StaticFiles(directory=os.path.join(project_root, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(project_root, "templates"))

# Basic routes
@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login_new.html", {"request": request})

@app.get("/api")
async def api_info():
    return {"message": "Time Tracking System API", "version": "1.0.0"}

@app.post("/token", response_class=HTMLResponse)
async def login_for_access_token(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        # Simple authentication check
        if username == "adm@teste.com" and password == "adm123":
            response = RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
            response.set_cookie("access_token", "test-token", httponly=True)
            return response
        else:
            return templates.TemplateResponse("login_new.html", {
                "request": request,
                "error": "Usuário ou senha incorretos"
            })
    except Exception as e:
        return templates.TemplateResponse("login_new.html", {
            "request": request,
            "error": f"Erro: {str(e)}"
        })

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard_improved.html", {"request": request})

@app.post("/logout")
async def logout():
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("access_token")
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
