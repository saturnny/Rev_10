from sqlalchemy.orm import Session
from .models import User, Categoria, Atividade, Lancamento
from .schemas import UserCreate, UserUpdate, CategoriaCreate, AtividadeCreate, AtividadeUpdate, LancamentoCreate, LancamentoUpdate
from .auth import get_password_hash
from typing import Optional, List

# Users
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.senha)
    db_user = User(
        nome=user.nome,
        email=user.email,
        senha=hashed_password,
        gestao=user.gestao,
        area=user.area,
        equipe=user.equipe,
        especialidade=user.especialidade,
        tipo_usuario=user.tipo_usuario
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: UserUpdate):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        update_data = user.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)
        db.commit()
        db.refresh(db_user)
    return db_user

# Categorias
def get_categorias(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Categoria).offset(skip).limit(limit).all()

def get_categoria(db: Session, categoria_id: int):
    return db.query(Categoria).filter(Categoria.id == categoria_id).first()

def create_categoria(db: Session, categoria: CategoriaCreate):
    db_categoria = Categoria(nome=categoria.nome)
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

def delete_categoria(db: Session, categoria_id: int):
    db_categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if db_categoria:
        db.delete(db_categoria)
        db.commit()
    return db_categoria

# Atividades
def get_atividades(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Atividade).all()

def get_atividade(db: Session, atividade_id: int):
    return db.query(Atividade).filter(Atividade.id == atividade_id).first()

def create_atividade(db: Session, atividade: AtividadeCreate):
    db_atividade = Atividade(
        nome=atividade.nome,
        categoria_id=atividade.categoria_id
    )
    db.add(db_atividade)
    db.commit()
    db.refresh(db_atividade)
    return db_atividade

def update_atividade(db: Session, atividade_id: int, atividade: AtividadeUpdate):
    db_atividade = db.query(Atividade).filter(Atividade.id == atividade_id).first()
    if db_atividade:
        update_data = atividade.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_atividade, field, value)
        db.commit()
        db.refresh(db_atividade)
    return db_atividade

def delete_atividade(db: Session, atividade_id: int):
    db_atividade = db.query(Atividade).filter(Atividade.id == atividade_id).first()
    if db_atividade:
        db.delete(db_atividade)
        db.commit()
    return db_atividade

# Lancamentos
def get_lancamentos(db: Session, user_id: Optional[int] = None, skip: int = 0, limit: int = 100):
    query = db.query(Lancamento)
    if user_id:
        query = query.filter(Lancamento.usuario_id == user_id)
    return query.order_by(Lancamento.data.desc(), Lancamento.hora_inicio.desc()).offset(skip).limit(limit).all()

def get_lancamento(db: Session, lancamento_id: int):
    return db.query(Lancamento).filter(Lancamento.id == lancamento_id).first()

def create_lancamento(db: Session, lancamento: LancamentoCreate, user_id: int):
    db_lancamento = Lancamento(
        usuario_id=user_id,
        data=lancamento.data,
        hora_inicio=lancamento.hora_inicio,
        hora_fim=lancamento.hora_fim,
        atividade_id=lancamento.atividade_id,
        observacao=lancamento.observacao
    )
    db.add(db_lancamento)
    db.commit()
    db.refresh(db_lancamento)
    return db_lancamento

def update_lancamento(db: Session, lancamento_id: int, lancamento: LancamentoUpdate):
    db_lancamento = db.query(Lancamento).filter(Lancamento.id == lancamento_id).first()
    if db_lancamento:
        update_data = lancamento.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_lancamento, field, value)
        db.commit()
        db.refresh(db_lancamento)
    return db_lancamento

def delete_lancamento(db: Session, lancamento_id: int):
    db_lancamento = db.query(Lancamento).filter(Lancamento.id == lancamento_id).first()
    if db_lancamento:
        db.delete(db_lancamento)
        db.commit()
    return db_lancamento

def get_lancamentos_admin(db: Session, user_id: Optional[int] = None, data: Optional[str] = None):
    query = db.query(Lancamento)
    if user_id:
        query = query.filter(Lancamento.usuario_id == user_id)
    if data:
        query = query.filter(Lancamento.data == data)
    return query.order_by(Lancamento.data.desc(), Lancamento.hora_inicio.desc()).all()
