import os
from fastapi import FastAPI, Depends, HTTPException, status, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional

from .database import get_db, engine
from .models import Base, User
from .schemas import UserLogin, Token, UserCreate, CategoriaCreate, AtividadeCreate, AtividadeUpdate, LancamentoCreate, LancamentoUpdate
from .crud import (
    get_user_by_email, create_user, get_users, update_user,
    get_categorias, create_categoria, delete_categoria,
    get_atividades, get_atividade, create_atividade, update_atividade, delete_atividade,
    get_lancamentos, get_lancamento, create_lancamento, update_lancamento, delete_lancamento, get_lancamentos_admin
)
from .auth import (
    authenticate_user, create_access_token, get_current_user, get_current_active_user, 
    require_admin, ACCESS_TOKEN_EXPIRE_MINUTES
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Time Tracking System", description="Sistema de controle de ponto e atividades", docs_url=None, redoc_url=None)

# Get the absolute path to the project root
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app.mount("/static", StaticFiles(directory=os.path.join(project_root, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(project_root, "templates"))

@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login_new.html", {"request": request})

@app.get("/api", response_class=HTMLResponse)
async def api_info():
    return {"message": "Time Tracking System API", "version": "1.0.0"}

@app.post("/token", response_class=HTMLResponse)
async def login_for_access_token(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, username, password)
    if not user:
        return templates.TemplateResponse("login_new.html", {
            "request": request,
            "error": "Usuário ou senha incorretos"
        })
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    
    response = RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=1800,
        expires=1800,
    )
    return response

@app.get("/lancamentos-teste-simples", response_class=HTMLResponse)
async def lancamentos_teste_simples(request: Request, current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    atividades = get_atividades(db)
    lancamentos = get_lancamentos(db, user_id=current_user.id)
    
    return templates.TemplateResponse("lancamentos_teste_simples.html", {
        "request": request,
        "user": current_user,
        "lancamentos": lancamentos,
        "atividades": atividades
    })

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    atividades = get_atividades(db)
    lancamentos = get_lancamentos(db, user_id=current_user.id, limit=10)
    return templates.TemplateResponse("dashboard_improved.html", {
        "request": request,
        "user": current_user,
        "lancamentos": lancamentos,
        "atividades": atividades
    })

@app.get("/lancamentos", response_class=HTMLResponse)
async def meus_lancamentos(request: Request, current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    atividades = get_atividades(db)
    lancamentos = get_lancamentos(db, user_id=current_user.id)
    
    # Função para verificar se pode editar/apagar lançamento (só hoje e ontem)
    def can_edit_lancamento(data_lancamento):
        hoje = datetime.now().date()
        ontem = hoje - timedelta(days=1)
        return data_lancamento.date() >= ontem
    
    return templates.TemplateResponse("lancamentos.html", {
        "request": request,
        "user": current_user,
        "lancamentos": lancamentos,
        "atividades": atividades,
        "can_edit_lancamento": can_edit_lancamento
    })

@app.get("/lancamentos-minimal", response_class=HTMLResponse)
async def lancamentos_minimal(request: Request, current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    atividades = get_atividades(db)
    lancamentos = get_lancamentos(db, user_id=current_user.id)
    
    return templates.TemplateResponse("lancamentos_minimal.html", {
        "request": request,
        "user": current_user,
        "lancamentos": lancamentos,
        "atividades": atividades
    })

@app.get("/lancamentos-final", response_class=HTMLResponse)
async def lancamentos_final(request: Request, current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    atividades = get_atividades(db)
    lancamentos = get_lancamentos(db, user_id=current_user.id)
    
    # Função para verificar se pode editar/apagar lançamento (só hoje e ontem)
    def can_edit_lancamento(data_lancamento):
        hoje = datetime.now().date()
        ontem = hoje - timedelta(days=1)
        return data_lancamento.date() >= ontem
    
    return templates.TemplateResponse("lancamentos_final.html", {
        "request": request,
        "user": current_user,
        "lancamentos": lancamentos,
        "atividades": atividades,
        "can_edit_lancamento": can_edit_lancamento
    })

@app.get("/lancamentos-simple", response_class=HTMLResponse)
async def lancamentos_simple(request: Request, current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    atividades = get_atividades(db)
    lancamentos = get_lancamentos(db, user_id=current_user.id)
    
    return templates.TemplateResponse("lancamentos_simple.html", {
        "request": request,
        "user": current_user,
        "lancamentos": lancamentos,
        "atividades": atividades
    })

@app.get("/lancamentos-test", response_class=HTMLResponse)
async def lancamentos_test(request: Request, current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    atividades = get_atividades(db)
    lancamentos = get_lancamentos(db, user_id=current_user.id)
    
    return templates.TemplateResponse("lancamentos_test.html", {
        "request": request,
        "user": current_user,
        "lancamentos": lancamentos,
        "atividades": atividades
    })

@app.get("/lancamentos", response_class=HTMLResponse)
async def meus_lancamentos(request: Request, current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    atividades = get_atividades(db)
    lancamentos = get_lancamentos(db, user_id=current_user.id)
    
    # Função para verificar se pode editar/apagar lançamento (só hoje e ontem)
    def can_edit_lancamento(data_lancamento):
        hoje = datetime.now().date()
        ontem = hoje - timedelta(days=1)
        return data_lancamento.date() >= ontem
    
    return templates.TemplateResponse("lancamentos_fixed.html", {
        "request": request,
        "user": current_user,
        "lancamentos": lancamentos,
        "atividades": atividades,
        "can_edit_lancamento": can_edit_lancamento
    })

@app.get("/api/lancamento/{lancamento_id}", response_class=JSONResponse)
async def get_lancamento_api(lancamento_id: int, current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    lancamento = get_lancamento(db, lancamento_id, user_id=current_user.id)
    if not lancamento:
        raise HTTPException(status_code=404, detail="Lançamento não encontrado")
    
    return {
        "id": lancamento.id,
        "data": lancamento.data.strftime('%Y-%m-%d'),
        "hora_inicio": lancamento.hora_inicio.strftime('%H:%M'),
        "hora_fim": lancamento.hora_fim.strftime('%H:%M'),
        "atividade_id": lancamento.atividade_id,
        "observacao": lancamento.observacao
    }

@app.get("/novo-lancamento", response_class=HTMLResponse)
async def novo_lancamento_page(request: Request, current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    atividades = get_atividades(db)
    lancamentos = get_lancamentos(db, user_id=current_user.id, limit=5)
    return templates.TemplateResponse("novo_lancamento_bootstrap.html", {
        "request": request,
        "user": current_user,
        "atividades": atividades,
        "lancamentos": lancamentos
    })

@app.post("/novo-lancamento", response_class=HTMLResponse)
async def criar_lancamento(
    request: Request,
    data: str = Form(...),
    hora_inicio: str = Form(...),
    hora_fim: str = Form(...),
    atividade_id: int = Form(...),
    observacao: Optional[str] = Form(None),
    return_url: Optional[str] = Form(None),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    from datetime import date, time, datetime
    
    lancamento_data = LancamentoCreate(
        data=datetime.strptime(data, "%Y-%m-%d").date(),
        hora_inicio=datetime.strptime(hora_inicio, "%H:%M").time(),
        hora_fim=datetime.strptime(hora_fim, "%H:%M").time(),
        atividade_id=atividade_id,
        observacao=observacao
    )
    
    create_lancamento(db, lancamento_data, current_user.id)
    
    # Redirecionar para return_url se fornecido, senão para /lancamentos
    redirect_url = return_url if return_url else "/lancamentos"
    return RedirectResponse(url=redirect_url, status_code=status.HTTP_303_SEE_OTHER)

@app.get("/editar-lancamento/{lancamento_id}", response_class=HTMLResponse)
async def editar_lancamento_page(
    lancamento_id: int,
    request: Request, 
    current_user: User = Depends(get_current_active_user), 
    db: Session = Depends(get_db)
):
    lancamento = get_lancamento(db, lancamento_id)
    if not lancamento or lancamento.usuario_id != current_user.id:
        raise HTTPException(status_code=404, detail="Lançamento não encontrado")
    
    atividades = get_atividades(db)
    return templates.TemplateResponse("editar_lancamento_bootstrap.html", {
        "request": request,
        "user": current_user,
        "lancamento": lancamento,
        "atividades": atividades
    })

@app.post("/editar-lancamento/{lancamento_id}", response_class=HTMLResponse)
async def atualizar_lancamento(
    request: Request,
    lancamento_id: int,
    data: str = Form(...),
    hora_inicio: str = Form(...),
    hora_fim: str = Form(...),
    atividade_id: int = Form(...),
    observacao: Optional[str] = Form(None),
    return_url: Optional[str] = Form(None),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    from datetime import date, time, datetime
    
    lancamento = get_lancamento(db, lancamento_id)
    if not lancamento or lancamento.usuario_id != current_user.id:
        raise HTTPException(status_code=404, detail="Lançamento não encontrado")
    
    lancamento_data = LancamentoUpdate(
        data=datetime.strptime(data, "%Y-%m-%d").date(),
        hora_inicio=datetime.strptime(hora_inicio, "%H:%M").time(),
        hora_fim=datetime.strptime(hora_fim, "%H:%M").time(),
        atividade_id=atividade_id,
        observacao=observacao
    )
    
    update_lancamento(db, lancamento_id, lancamento_data)
    
    # Redirecionar para return_url se fornecido, senão para /lancamentos
    redirect_url = return_url if return_url else "/lancamentos"
    return RedirectResponse(url=redirect_url, status_code=status.HTTP_303_SEE_OTHER)

@app.post("/excluir-lancamento/{lancamento_id}", response_class=HTMLResponse)
async def excluir_lancamento(
    lancamento_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    lancamento = get_lancamento(db, lancamento_id)
    if not lancamento or lancamento.usuario_id != current_user.id:
        raise HTTPException(status_code=404, detail="Lançamento não encontrado")
    
    delete_lancamento(db, lancamento_id)
    return RedirectResponse(url="/lancamentos", status_code=status.HTTP_303_SEE_OTHER)

# Admin routes
@app.get("/admin/lancamentos", response_class=HTMLResponse)
async def admin_lancamentos(
    request: Request,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
    user_id: Optional[int] = None,
    data: Optional[str] = None
):
    lancamentos = get_lancamentos_admin(db, user_id=user_id, data=data)
    usuarios = get_users(db)
    return templates.TemplateResponse("admin/lancamentos.html", {
        "request": request,
        "user": current_user,
        "lancamentos": lancamentos,
        "usuarios": usuarios,
        "filtro_user_id": user_id,
        "filtro_data": data
    })

@app.post("/logout")
async def logout():
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("access_token")
    return response

@app.get("/perfil", response_class=HTMLResponse)
async def perfil_page(request: Request, current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    return templates.TemplateResponse("perfil_view.html", {
        "request": request,
        "user": current_user
    })

@app.post("/perfil", response_class=HTMLResponse)
async def atualizar_perfil(
    request: Request,
    senha_atual: str = Form(...),
    nova_senha: str = Form(...),
    confirmar_senha: str = Form(...),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Verificar se a senha atual está correta
    if not verify_password(senha_atual, current_user.senha):
        return templates.TemplateResponse("perfil_view.html", {
            "request": request,
            "user": current_user,
            "error": "Senha atual incorreta"
        })
    
    # Verificar se as novas senhas coincidem
    if nova_senha != confirmar_senha:
        return templates.TemplateResponse("perfil_view.html", {
            "request": request,
            "user": current_user,
            "error": "A nova senha e a confirmação não coincidem"
        })
    
    # Verificar tamanho mínimo da nova senha
    if len(nova_senha) < 6:
        return templates.TemplateResponse("perfil_view.html", {
            "request": request,
            "user": current_user,
            "error": "A nova senha deve ter pelo menos 6 caracteres"
        })
    
    # Atualizar a senha
    hashed_password = get_password_hash(nova_senha)
    current_user.senha = hashed_password
    db.commit()
    
    return templates.TemplateResponse("perfil_view.html", {
        "request": request,
        "user": current_user,
        "message": "Senha alterada com sucesso!"
    })

@app.post("/alterar-senha", response_class=HTMLResponse)
async def alterar_senha(
    request: Request,
    senha_atual: str = Form(...),
    nova_senha: str = Form(...),
    confirmar_senha: str = Form(...),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if nova_senha != confirmar_senha:
        return templates.TemplateResponse("perfil_new.html", {
            "request": request,
            "user": current_user,
            "error": "As novas senhas não coincidem"
        })
    
    if not verify_password(senha_atual, current_user.senha):
        return templates.TemplateResponse("perfil_new.html", {
            "request": request,
            "user": current_user,
            "error": "Senha atual incorreta"
        })
    
    # Update password
    current_user.senha = get_password_hash(nova_senha)
    db.commit()
    
    return RedirectResponse(url="/perfil", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/admin/usuarios", response_class=HTMLResponse)
async def admin_usuarios(request: Request, current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    usuarios = get_users(db)
    return templates.TemplateResponse("admin/usuarios_bootstrap.html", {
        "request": request,
        "user": current_user,
        "usuarios": usuarios
    })

@app.get("/admin/atividades", response_class=HTMLResponse)
async def admin_atividades(request: Request, current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    atividades = get_atividades(db)
    categorias = get_categorias(db)
    return templates.TemplateResponse("admin/atividades.html", {
        "request": request,
        "user": current_user,
        "atividades": atividades,
        "categorias": categorias
    })

@app.post("/admin/atividades", response_class=HTMLResponse)
async def criar_atividade(
    request: Request,
    nome: str = Form(...),
    categoria_id: int = Form(...),
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    atividade_data = AtividadeCreate(nome=nome, categoria_id=categoria_id)
    create_atividade(db, atividade_data)
    return RedirectResponse(url="/admin/atividades", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/admin/atividades/{atividade_id}/editar", response_class=HTMLResponse)
async def editar_atividade(
    request: Request,
    atividade_id: int,
    nome: str = Form(...),
    categoria_id: int = Form(...),
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    atividade_data = AtividadeUpdate(nome=nome, categoria_id=categoria_id)
    update_atividade(db, atividade_id, atividade_data)
    return RedirectResponse(url="/admin/atividades", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/admin/atividades/{atividade_id}/excluir", response_class=HTMLResponse)
async def excluir_atividade(
    atividade_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    delete_atividade(db, atividade_id)
    return RedirectResponse(url="/admin/atividades", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/admin/categorias", response_class=HTMLResponse)
async def admin_categorias(request: Request, current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    categorias = get_categorias(db)
    return templates.TemplateResponse("admin/categorias.html", {
        "request": request,
        "user": current_user,
        "categorias": categorias
    })

@app.post("/admin/categorias", response_class=HTMLResponse)
async def criar_categoria(
    request: Request,
    nome: str = Form(...),
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    categoria_data = CategoriaCreate(nome=nome)
    create_categoria(db, categoria_data)
    return RedirectResponse(url="/admin/categorias", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/admin/categorias/{categoria_id}/excluir", response_class=HTMLResponse)
async def excluir_categoria(
    categoria_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    delete_categoria(db, categoria_id)
    return RedirectResponse(url="/admin/categorias", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie(key="access_token")
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
