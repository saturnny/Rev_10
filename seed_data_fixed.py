from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Base, User, Categoria, Atividade, Lancamento
from app.auth import get_password_hash
from datetime import datetime

def seed_database():
    # Criar tabelas
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Limpar dados existentes para evitar conflitos
        db.query(Lancamento).delete()
        db.query(Atividade).delete()
        db.query(Categoria).delete()
        db.query(User).delete()
        db.commit()
        
        # Criar categorias
        categorias_data = [
            {"nome": "Reuniao"},
            {"nome": "Trabalhando"},
            {"nome": "Administrativo"}
        ]
        
        categorias = []
        for cat_data in categorias_data:
            categoria = Categoria(**cat_data)
            db.add(categoria)
            categorias.append(categoria)
        
        db.commit()
        
        # Refresh para obter IDs
        for categoria in categorias:
            db.refresh(categoria)
        
        print(f"Categorias criadas: {[c.nome for c in categorias]}")
        
        # Criar atividades
        atividades_data = [
            {"nome": "Reuniao semanal", "categoria_id": categorias[0].id},
            {"nome": "Reuniao planejamento", "categoria_id": categorias[0].id},
            {"nome": "Auditoria campo", "categoria_id": categorias[1].id},
            {"nome": "Inspecao campo", "categoria_id": categorias[1].id},
            {"nome": "Elaboracao relatorio", "categoria_id": categorias[2].id}
        ]
        
        atividades = []
        for atv_data in atividades_data:
            atividade = Atividade(**atv_data)
            db.add(atividade)
            atividades.append(atividade)
        
        db.commit()
        
        # Refresh para obter IDs
        for atividade in atividades:
            db.refresh(atividade)
        
        print(f"Atividades criadas: {[a.nome for a in atividades]}")
        
        # Criar usuários
        usuarios_data = [
            {
                "nome": "Administrador",
                "email": "admin@empresa.com",
                "senha": get_password_hash("admin123")[:72],
                "tipo_usuario": "Admin",
                "gestao": "TI",
                "area": "Tecnologia",
                "equipe": "Desenvolvimento",
                "especialidade": "Sistemas"
            },
            {
                "nome": "Usuario Teste",
                "email": "usuario@empresa.com",
                "senha": get_password_hash("123456")[:72],
                "tipo_usuario": "Usuario",
                "gestao": "Operacoes",
                "area": "Campo",
                "equipe": "Auditoria",
                "especialidade": "Inspecao"
            },
            {
                "nome": "Joao Silva",
                "email": "joao@empresa.com",
                "senha": get_password_hash("123456")[:72],
                "tipo_usuario": "Usuario",
                "gestao": "Operacoes",
                "area": "Campo",
                "equipe": "Auditoria",
                "especialidade": "Auditoria"
            },
            {
                "nome": "Paulo Santos",
                "email": "paulo@empresa.com",
                "senha": get_password_hash("123456")[:72],
                "tipo_usuario": "Usuario",
                "gestao": "Operacoes",
                "area": "Campo",
                "equipe": "Inspecao",
                "especialidade": "Campo"
            }
        ]
        
        usuarios = []
        for user_data in usuarios_data:
            usuario = User(**user_data)
            db.add(usuario)
            usuarios.append(usuario)
        
        db.commit()
        
        # Refresh para obter IDs
        for usuario in usuarios:
            db.refresh(usuario)
        
        print("Database seeded successfully!")
        print("\nUsuários criados:")
        for usuario in usuarios:
            print(f"- {usuario.nome} ({usuario.tipo_usuario}): {usuario.email}")
        
        print("\nCredenciais de acesso:")
        print("Admin - admin@empresa.com / admin123")
        print("Usuário - usuario@empresa.com / 123456")
        print("João - joao@empresa.com / 123456")
        print("Paulo - paulo@empresa.com / 123456")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
