"""
SharePoint Sync Service
Handles bidirectional synchronization between local database and SharePoint lists
"""
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from sqlalchemy.orm import Session

from .sharepoint import sharepoint_client, SharePointConfig
from . import models, crud

class SharePointSyncService:
    """Service for synchronizing data with SharePoint"""
    
    def __init__(self, db: Session):
        self.db = db
        self.client = sharepoint_client
        self.site_id = None
        self.users_list_id = None
        self.lancamentos_list_id = None
        
    def _initialize(self) -> bool:
        """Initialize connection and get list IDs"""
        if not SharePointConfig.is_configured():
            print("SharePoint not configured")
            return False
            
        self.site_id = self.client.get_site_id()
        if not self.site_id:
            print("Could not get SharePoint site ID")
            return False
            
        self.users_list_id = self.client.get_list_id(self.site_id, SharePointConfig.USERS_LIST_NAME)
        self.lancamentos_list_id = self.client.get_list_id(self.site_id, SharePointConfig.LANCAMENTOS_LIST_NAME)
        
        return True
    
    # ============== USER SYNC ==============
    
    def sync_users_from_sharepoint(self) -> Tuple[int, int, int]:
        """
        Import users from SharePoint to local database
        Returns: (created, updated, errors)
        """
        if not self._initialize():
            return 0, 0, 1
            
        if not self.users_list_id:
            print(f"Users list '{SharePointConfig.USERS_LIST_NAME}' not found in SharePoint")
            return 0, 0, 1
        
        created = 0
        updated = 0
        errors = 0
        
        # Get users from SharePoint
        sp_users = self.client.get_list_items(self.site_id, self.users_list_id)
        
        for sp_user in sp_users:
            try:
                fields = sp_user.get("fields", {})
                email = fields.get("Email") or fields.get("email") or fields.get("E_mail")
                nome = fields.get("Nome") or fields.get("nome") or fields.get("Title")
                
                if not email or not nome:
                    continue
                
                # Check if user exists locally
                local_user = crud.get_user_by_email(self.db, email)
                
                if local_user:
                    # Update existing user
                    user_data = {
                        "nome": nome,
                        "gestao": fields.get("Gestao") or fields.get("gestao"),
                        "area": fields.get("Area") or fields.get("area"),
                        "equipe": fields.get("Equipe") or fields.get("equipe"),
                        "especialidade": fields.get("Especialidade") or fields.get("especialidade"),
                        "tipo_usuario": fields.get("TipoUsuario") or fields.get("tipo_usuario") or "Usuario"
                    }
                    crud.update_user(self.db, local_user.id, user_data)
                    updated += 1
                else:
                    # Create new user
                    from .schemas import UserCreate
                    user_data = UserCreate(
                        nome=nome,
                        email=email,
                        senha="changeme123",  # Default password, user should change
                        tipo_usuario=fields.get("TipoUsuario") or fields.get("tipo_usuario") or "Usuario",
                        gestao=fields.get("Gestao") or fields.get("gestao"),
                        area=fields.get("Area") or fields.get("area"),
                        equipe=fields.get("Equipe") or fields.get("equipe"),
                        especialidade=fields.get("Especialidade") or fields.get("especialidade")
                    )
                    crud.create_user(self.db, user_data)
                    created += 1
                    
            except Exception as e:
                print(f"Error syncing user: {e}")
                errors += 1
        
        return created, updated, errors
    
    def sync_users_to_sharepoint(self) -> Tuple[int, int, int]:
        """
        Export users from local database to SharePoint
        Returns: (created, updated, errors)
        """
        if not self._initialize():
            return 0, 0, 1
            
        if not self.users_list_id:
            print(f"Users list '{SharePointConfig.USERS_LIST_NAME}' not found")
            return 0, 0, 1
        
        created = 0
        updated = 0
        errors = 0
        
        # Get all local users
        local_users = crud.get_users(self.db)
        
        # Get existing SharePoint users to check for updates
        sp_users = self.client.get_list_items(self.site_id, self.users_list_id)
        sp_users_by_email = {}
        for sp_user in sp_users:
            fields = sp_user.get("fields", {})
            email = fields.get("Email") or fields.get("email") or fields.get("E_mail")
            if email:
                sp_users_by_email[email.lower()] = {
                    "id": sp_user.get("id"),
                    "fields": fields
                }
        
        for local_user in local_users:
            try:
                fields = {
                    "Title": local_user.nome,
                    "Nome": local_user.nome,
                    "Email": local_user.email,
                    "E_mail": local_user.email,
                    "Gestao": local_user.gestao or "",
                    "Area": local_user.area or "",
                    "Equipe": local_user.equipe or "",
                    "Especialidade": local_user.especialidade or "",
                    "TipoUsuario": local_user.tipo_usuario or "Usuario"
                }
                
                if local_user.email.lower() in sp_users_by_email:
                    # Update existing
                    sp_user = sp_users_by_email[local_user.email.lower()]
                    self.client.update_list_item(
                        self.site_id, 
                        self.users_list_id, 
                        sp_user["id"], 
                        fields
                    )
                    updated += 1
                else:
                    # Create new
                    self.client.create_list_item(
                        self.site_id, 
                        self.users_list_id, 
                        fields
                    )
                    created += 1
                    
            except Exception as e:
                print(f"Error exporting user {local_user.email}: {e}")
                errors += 1
        
        return created, updated, errors
    
    # ============== LANCAMENTOS SYNC ==============
    
    def sync_lancamentos_to_sharepoint(self, start_date: Optional[datetime] = None, 
                                       end_date: Optional[datetime] = None) -> Tuple[int, int, int]:
        """
        Export lançamentos from local database to SharePoint
        Returns: (created, updated, errors)
        """
        if not self._initialize():
            return 0, 0, 1
            
        if not self.lancamentos_list_id:
            print(f"Lançamentos list '{SharePointConfig.LANCAMENTOS_LIST_NAME}' not found")
            return 0, 0, 1
        
        created = 0
        updated = 0
        errors = 0
        
        # Get lançamentos from database
        if not start_date:
            start_date = datetime.now() - timedelta(days=30)
        if not end_date:
            end_date = datetime.now()
            
        lançamentos = self.db.query(models.Lancamento).filter(
            models.Lancamento.data >= start_date.date(),
            models.Lancamento.data <= end_date.date()
        ).all()
        
        # Get existing SharePoint lançamentos
        sp_items = self.client.get_list_items(self.site_id, self.lancamentos_list_id)
        sp_items_by_id = {}
        for item in sp_items:
            fields = item.get("fields", {})
            local_id = fields.get("LocalID") or fields.get("local_id")
            if local_id:
                sp_items_by_id[str(local_id)] = item.get("id")
        
        for lanc in lançamentos:
            try:
                # Calculate duration
                from datetime import datetime
                inicio = datetime.combine(lanc.data, lanc.hora_inicio)
                fim = datetime.combine(lanc.data, lanc.hora_fim)
                duracao_horas = (fim - inicio).total_seconds() / 3600
                
                fields = {
                    "Title": f"{lanc.usuario.nome} - {lanc.data}",
                    "LocalID": str(lanc.id),
                    "Usuario": lanc.usuario.nome,
                    "UsuarioEmail": lanc.usuario.email,
                    "Data": lanc.data.isoformat(),
                    "HoraInicio": lanc.hora_inicio.strftime("%H:%M"),
                    "HoraFim": lanc.hora_fim.strftime("%H:%M"),
                    "Atividade": lanc.atividade.nome if lanc.atividade else "",
                    "Categoria": lanc.atividade.categoria.nome if lanc.atividade and lanc.atividade.categoria else "",
                    "Observacao": lanc.observacao or "",
                    "DuracaoHoras": round(duracao_horas, 2)
                }
                
                if str(lanc.id) in sp_items_by_id:
                    # Update existing
                    self.client.update_list_item(
                        self.site_id,
                        self.lancamentos_list_id,
                        sp_items_by_id[str(lanc.id)],
                        fields
                    )
                    updated += 1
                else:
                    # Create new
                    self.client.create_list_item(
                        self.site_id,
                        self.lancamentos_list_id,
                        fields
                    )
                    created += 1
                    
            except Exception as e:
                print(f"Error exporting lançamento {lanc.id}: {e}")
                errors += 1
        
        return created, updated, errors
    
    def get_sync_status(self) -> Dict:
        """Get current sync configuration status"""
        return {
            "configured": SharePointConfig.is_configured(),
            "site_url": SharePointConfig.SITE_URL,
            "users_list": SharePointConfig.USERS_LIST_NAME,
            "lancamentos_list": SharePointConfig.LANCAMENTOS_LIST_NAME,
            "sync_interval": SharePointConfig.SYNC_INTERVAL
        }

# Convenience function for running sync
def run_full_sync(db: Session, direction: str = "both") -> Dict:
    """
    Run full synchronization
    direction: 'import', 'export', or 'both'
    """
    service = SharePointSyncService(db)
    results = {
        "users": {"created": 0, "updated": 0, "errors": 0},
        "lancamentos": {"created": 0, "updated": 0, "errors": 0},
        "timestamp": datetime.now().isoformat()
    }
    
    if direction in ["import", "both"]:
        # Import users from SharePoint
        c, u, e = service.sync_users_from_sharepoint()
        results["users_import"] = {"created": c, "updated": u, "errors": e}
    
    if direction in ["export", "both"]:
        # Export users to SharePoint
        c, u, e = service.sync_users_to_sharepoint()
        results["users_export"] = {"created": c, "updated": u, "errors": e}
        
        # Export lançamentos to SharePoint
        c, u, e = service.sync_lancamentos_to_sharepoint()
        results["lancamentos_export"] = {"created": c, "updated": u, "errors": e}
    
    return results
