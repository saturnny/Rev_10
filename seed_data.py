from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Base, User, Categoria, Atividade
from app.auth import get_password_hash
from datetime import datetime

def seed_database():
    # Criar tabelas
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Verificar se já existem dados
        if db.query(User).first():
            print("Database already seeded!")
            return
        
        # Criar categorias
        categorias_data = [
            {"nome": "Reunião"},
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
        
        # Criar atividades
        atividades_data = [
            {"nome": "Reunião semanal", "categoria_id": categorias[0].id},
            {"nome": "Reunião planejamento", "categoria_id": categorias[0].id},
            {"nome": "Auditoria campo", "categoria_id": categorias[1].id},
            {"nome": "Inspeção campo", "categoria_id": categorias[1].id},
            {"nome": "Elaboração relatório", "categoria_id": categorias[2].id}
        ]
        
        atividades = []
        for atv_data in atividades_data:
            atividade = Atividade(**atv_data)
            db.add(atividade)
            atividades.append(atividade)
        
        db.commit()
        
        # Criar usuários
        usuarios_data = [
            {
                "nome": "Administrador",
                "email": "admin@empresa.com",
                "senha": get_password_hash("admin123"),
                "tipo_usuario": "Admin",
                "gestao": "TI",
                "area": "Tecnologia",
                "equipe": "Desenvolvimento",
                "especialidade": "Sistemas"
            },
            {
                "nome": "Usuário Teste",
                "email": "usuario@empresa.com",
                "senha": get_password_hash("123456"),
                "tipo_usuario": "Usuário",
                "gestao": "Operações",
                "area": "Campo",
                "equipe": "Auditoria",
                "especialidade": "Inspeção"
            },
            {
                "nome": "João Silva",
                "email": "joao@empresa.com",
                "senha": get_password_hash("123456"),
                "tipo_usuario": "Usuário",
                "gestao": "Operações",
                "area": "Campo",
                "equipe": "Auditoria",
                "especialidade": "Auditoria"
            },
            {
                "nome": "Paulo Santos",
                "email": "paulo@empresa.com",
                "senha": get_password_hash("123456"),
                "tipo_usuario": "Usuário",
                "gestao": "Operações",
                "area": "Campo",
                "equipe": "Inspeção",
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
