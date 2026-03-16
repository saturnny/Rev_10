"""
SharePoint Integration Module
Handles authentication and data synchronization with Microsoft SharePoint
"""
import os
import requests
from typing import List, Dict, Optional, Any
from datetime import datetime
from msal import ConfidentialClientApplication
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SharePointConfig:
    """Configuration for SharePoint integration"""
    TENANT_ID = os.getenv("SHAREPOINT_TENANT_ID", "")
    CLIENT_ID = os.getenv("SHAREPOINT_CLIENT_ID", "")
    CLIENT_SECRET = os.getenv("SHAREPOINT_CLIENT_SECRET", "")
    SITE_URL = os.getenv("SHAREPOINT_SITE_URL", "")
    USERS_LIST_NAME = os.getenv("SHAREPOINT_USERS_LIST_NAME", "Funcionarios")
    LANCAMENTOS_LIST_NAME = os.getenv("SHAREPOINT_LANCAMENTOS_LIST_NAME", "Lancamentos")
    SYNC_INTERVAL = int(os.getenv("SHAREPOINT_SYNC_INTERVAL_MINUTES", "60"))
    
    @classmethod
    def is_configured(cls) -> bool:
        """Check if all required configuration is present"""
        return all([
            cls.TENANT_ID,
            cls.CLIENT_ID,
            cls.CLIENT_SECRET,
            cls.SITE_URL
        ])

class SharePointClient:
    """Client for SharePoint REST API operations"""
    
    def __init__(self):
        self.config = SharePointConfig()
        self.access_token = None
        self.app = None
        
        if self.config.is_configured():
            self.app = ConfidentialClientApplication(
                client_id=self.config.CLIENT_ID,
                client_credential=self.config.CLIENT_SECRET,
                authority=f"https://login.microsoftonline.com/{self.config.TENANT_ID}"
            )
    
    def _get_access_token(self) -> Optional[str]:
        """Get access token for Microsoft Graph API"""
        if not self.app:
            return None
            
        # Try to get token silently first
        accounts = self.app.get_accounts()
        if accounts:
            result = self.app.acquire_token_silent(
                scopes=["https://graph.microsoft.com/.default"],
                account=accounts[0]
            )
            if result and "access_token" in result:
                return result["access_token"]
        
        # Acquire new token
        result = self.app.acquire_token_for_client(
            scopes=["https://graph.microsoft.com/.default"]
        )
        
        if "access_token" in result:
            return result["access_token"]
        else:
            print(f"Error acquiring token: {result.get('error_description', 'Unknown error')}")
            return None
    
    def _make_request(self, endpoint: str, method: str = "GET", data: Dict = None) -> Optional[Dict]:
        """Make authenticated request to SharePoint API"""
        token = self._get_access_token()
        if not token:
            return None
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        url = f"https://graph.microsoft.com/v1.0{endpoint}"
        
        try:
            if method == "GET":
                response = requests.get(url, headers=headers)
            elif method == "POST":
                response = requests.post(url, headers=headers, json=data)
            elif method == "PATCH":
                response = requests.patch(url, headers=headers, json=data)
            elif method == "DELETE":
                response = requests.delete(url, headers=headers)
            else:
                return None
            
            response.raise_for_status()
            return response.json() if response.content else {}
            
        except requests.exceptions.RequestException as e:
            print(f"SharePoint API Error: {e}")
            return None
    
    def get_site_id(self) -> Optional[str]:
        """Get SharePoint site ID from URL"""
        # Extract site path from URL
        site_url = self.config.SITE_URL
        if not site_url:
            return None
            
        # Parse site URL to get hostname and site path
        from urllib.parse import urlparse
        parsed = urlparse(site_url)
        hostname = parsed.netloc
        site_path = parsed.path.strip('/')
        
        endpoint = f"/sites/{hostname}:/{site_path}"
        result = self._make_request(endpoint)
        
        if result and "id" in result:
            return result["id"]
        return None
    
    def get_list_id(self, site_id: str, list_name: str) -> Optional[str]:
        """Get list ID by name"""
        endpoint = f"/sites/{site_id}/lists"
        result = self._make_request(endpoint)
        
        if result and "value" in result:
            for list_item in result["value"]:
                if list_item.get("displayName") == list_name:
                    return list_item.get("id")
        return None
    
    def get_list_items(self, site_id: str, list_id: str, filter_query: str = None) -> List[Dict]:
        """Get all items from a SharePoint list"""
        endpoint = f"/sites/{site_id}/lists/{list_id}/items?expand=fields"
        
        if filter_query:
            endpoint += f"&filter={filter_query}"
        
        result = self._make_request(endpoint)
        
        if result and "value" in result:
            return result["value"]
        return []
    
    def create_list_item(self, site_id: str, list_id: str, fields: Dict) -> Optional[Dict]:
        """Create a new item in SharePoint list"""
        endpoint = f"/sites/{site_id}/lists/{list_id}/items"
        data = {
            "fields": fields
        }
        return self._make_request(endpoint, method="POST", data=data)
    
    def update_list_item(self, site_id: str, list_id: str, item_id: str, fields: Dict) -> Optional[Dict]:
        """Update an existing item in SharePoint list"""
        endpoint = f"/sites/{site_id}/lists/{list_id}/items/{item_id}"
        data = {
            "fields": fields
        }
        return self._make_request(endpoint, method="PATCH", data=data)
    
    def delete_list_item(self, site_id: str, list_id: str, item_id: str) -> bool:
        """Delete an item from SharePoint list"""
        endpoint = f"/sites/{site_id}/lists/{list_id}/items/{item_id}"
        result = self._make_request(endpoint, method="DELETE")
        return result is not None

# Global client instance
sharepoint_client = SharePointClient()
