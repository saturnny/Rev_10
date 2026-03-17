"""
Vercel Serverless Function - FastAPI Integration
Uses FastAPI to serve templates properly
"""
import json
import sys
import os
from http.server import BaseHTTPRequestHandler
from io import BytesIO
from urllib.parse import parse_qs

# Load environment variables
try:
    from dotenv import load_dotenv
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    load_dotenv(os.path.join(project_root, '.env'))
    load_dotenv(os.path.join(project_root, '.env.vercel'))
except ImportError:
    pass

# Add project root to Python path
sys.path.insert(0, project_root)

class handler(BaseHTTPRequestHandler):
    """Time Tracking API handler with FastAPI template serving"""
    
    def do_GET(self):
        """Handle GET requests"""
        try:
            path = self.path
            
            # Serve static files directly
            if path.startswith('/static/'):
                self.serve_static_file(path)
                return
            
            # API endpoints
            if path.startswith('/api/'):
                self.handle_api_request()
                return
            
            # Check authentication for protected routes
            auth_result = self.check_authentication()
            
            # Serve login page for root and unauthenticated users
            if path == "/" or path == "/login":
                if auth_result['authenticated']:
                    # User is logged in, redirect to dashboard
                    self.send_response(302)
                    self.send_header('Location', '/dashboard')
                    self.end_headers()
                else:
                    # User not logged in, show login page
                    self.serve_login_page()
                return
            
            # Protected routes - require authentication
            if not auth_result['authenticated']:
                # Redirect to login
                self.send_response(302)
                self.send_header('Location', '/login')
                self.end_headers()
                return
            
            # Serve protected pages
            if path == "/dashboard":
                self.serve_dashboard()
                return
            elif path.startswith('/admin'):
                self.serve_admin_page(path)
                return
            elif path.startswith('/lancamentos'):
                self.serve_lancamentos_page()
                return
            elif path == "/perfil":
                self.serve_perfil_page()
                return
            
            # Default to login
            self.send_response(302)
            self.send_header('Location', '/login')
            self.end_headers()
            
        except Exception as e:
            error_data = {
                "error": "Internal Server Error",
                "message": str(e),
                "type": type(e).__name__
            }
            
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(error_data).encode('utf-8'))
    
    def do_POST(self):
        """Handle POST requests"""
        try:
            path = self.path
            
            # Login endpoint
            if path == "/token":
                self.handle_login()
                return
            
            # Logout endpoint
            elif path == "/logout":
                self.handle_logout()
                return
            
            # API endpoints
            elif path.startswith('/api/'):
                self.handle_api_request()
                return
            
            # Default
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not Found"}).encode('utf-8'))
            
        except Exception as e:
            error_data = {
                "error": "Internal Server Error",
                "message": str(e),
                "type": type(e).__name__
            }
            
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(error_data).encode('utf-8'))
    
    def check_authentication(self):
        """Check if user is authenticated via cookie"""
        try:
            # Get cookies from headers
            cookie_header = self.headers.get('Cookie', '')
            cookies = {}
            
            if cookie_header:
                for cookie in cookie_header.split(';'):
                    if '=' in cookie:
                        key, value = cookie.strip().split('=', 1)
                        cookies[key] = value
            
            # Check for access_token
            access_token = cookies.get('access_token')
            
            if not access_token:
                return {'authenticated': False}
            
            # TODO: Validate JWT token here
            # For now, just check if token exists
            return {'authenticated': True, 'token': access_token}
            
        except Exception as e:
            return {'authenticated': False, 'error': str(e)}
    
    def serve_login_page(self):
        """Serve the login page"""
        try:
            # Read login template
            login_template_path = os.path.join(project_root, 'templates', 'login_new.html')
            
            if os.path.exists(login_template_path):
                with open(login_template_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
            else:
                # Simple fallback
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(b"""
<!DOCTYPE html>
<html>
<head><title>Login</title></head>
<body>
<h2>Time Tracking Login</h2>
<form method="post" action="/token">
    <input type="email" name="username" placeholder="Email" required><br><br>
    <input type="password" name="password" placeholder="Senha" required><br><br>
    <button type="submit">Entrar</button>
</form>
<p>Admin: adm@teste.com / adm123</p>
<p>User: user@teste.com / user123</p>
</body>
</html>
                """)
                
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(f"<h1>Error</h1><p>{str(e)}</p>".encode('utf-8'))
    
    def serve_dashboard(self):
        """Serve the dashboard page"""
        try:
            # Read dashboard template
            dashboard_template_path = os.path.join(project_root, 'templates', 'dashboard_improved.html')
            
            if os.path.exists(dashboard_template_path):
                with open(dashboard_template_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
            else:
                # Simple fallback
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(b"""
<!DOCTYPE html>
<html>
<head><title>Dashboard</title></head>
<body>
<h1>Time Tracking Dashboard</h1>
<p>Bem-vindo!</p>
<a href="/logout">Sair</a>
<br><br>
<a href="/lancamentos">Meus Lançamentos</a><br>
<a href="/admin/usuarios">Admin Usuários</a><br>
<a href="/admin/categorias">Admin Categorias</a><br>
<a href="/admin/atividades">Admin Atividades</a><br>
<a href="/admin/lancamentos">Admin Lançamentos</a>
</body>
</html>
                """)
                
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(f"<h1>Error</h1><p>{str(e)}</p>".encode('utf-8'))
    
    def serve_admin_page(self, path):
        """Serve admin pages"""
        try:
            # Map admin paths to templates
            template_map = {
                '/admin/usuarios': 'admin/usuarios_bootstrap.html',
                '/admin/categorias': 'admin/categorias_bootstrap.html',
                '/admin/atividades': 'admin/atividades_bootstrap.html',
                '/admin/lancamentos': 'admin/lancamentos.html'
            }
            
            template_name = template_map.get(path)
            if template_name:
                template_path = os.path.join(project_root, 'templates', template_name)
                if os.path.exists(template_path):
                    with open(template_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(content.encode('utf-8'))
                    return
            
            # Fallback
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(f"<h1>Admin Page: {path}</h1><p>Template not found</p>".encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(f"<h1>Error</h1><p>{str(e)}</p>".encode('utf-8'))
    
    def serve_lancamentos_page(self):
        """Serve lancamentos page"""
        try:
            template_path = os.path.join(project_root, 'templates', 'lancamentos.html')
            
            if os.path.exists(template_path):
                with open(template_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
            else:
                # Fallback
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(b"<h1>Meus Lançamentos</h1><p>Page under construction</p>")
                
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(f"<h1>Error</h1><p>{str(e)}</p>".encode('utf-8'))
    
    def serve_perfil_page(self):
        """Serve perfil page"""
        try:
            template_path = os.path.join(project_root, 'templates', 'perfil_view.html')
            
            if os.path.exists(template_path):
                with open(template_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
            else:
                # Fallback
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(b"<h1>Meu Perfil</h1><p>Page under construction</p>")
                
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(f"<h1>Error</h1><p>{str(e)}</p>".encode('utf-8'))
    
    def serve_static_file(self, path):
        """Serve static files"""
        try:
            static_path = os.path.join(project_root, path.lstrip('/'))
            
            if os.path.exists(static_path) and os.path.isfile(static_path):
                with open(static_path, 'rb') as f:
                    content = f.read()
                
                # Determine content type
                if path.endswith('.css'):
                    content_type = 'text/css'
                elif path.endswith('.js'):
                    content_type = 'application/javascript'
                elif path.endswith('.png'):
                    content_type = 'image/png'
                elif path.endswith('.jpg') or path.endswith('.jpeg'):
                    content_type = 'image/jpeg'
                else:
                    content_type = 'application/octet-stream'
                
                self.send_response(200)
                self.send_header('Content-type', content_type)
                self.end_headers()
                self.wfile.write(content)
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'File not found')
                
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode('utf-8'))
    
    def handle_login(self):
        """Handle login POST request"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            # Parse form data
            form_data = parse_qs(post_data.decode('utf-8'))
            username = form_data.get('username', [''])[0]
            password = form_data.get('password', [''])[0]
            
            # Simple authentication check
            if username == "adm@teste.com" and password == "adm123":
                # Set cookie and redirect to dashboard
                self.send_response(302)
                self.send_header('Location', '/dashboard')
                self.send_header('Set-Cookie', 'access_token=test-admin-token; Path=/; HttpOnly')
                self.end_headers()
            elif username == "user@teste.com" and password == "user123":
                # Set cookie and redirect to dashboard
                self.send_response(302)
                self.send_header('Location', '/dashboard')
                self.send_header('Set-Cookie', 'access_token=test-user-token; Path=/; HttpOnly')
                self.end_headers()
            else:
                # Invalid credentials - redirect back to login
                self.send_response(302)
                self.send_header('Location', '/login?error=invalid')
                self.end_headers()
                
        except Exception as e:
            self.send_response(302)
            self.send_header('Location', '/login?error=server')
            self.end_headers()
    
    def handle_logout(self):
        """Handle logout"""
        self.send_response(302)
        self.send_header('Location', '/login')
        self.send_header('Set-Cookie', 'access_token=; Path=/; HttpOnly; Max-Age=0')
        self.end_headers()
    
    def handle_api_request(self):
        """Handle API requests"""
        path = self.path
        
        if path == "/api/health":
            response_data = {
                "status": "ok",
                "service": "time-tracking",
                "environment": "vercel"
            }
        else:
            response_data = {
                "error": "API endpoint not found",
                "path": path
            }
        
        self.send_response(200 if not path.startswith('/api/error') else 404)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(response_data).encode('utf-8'))
    
    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

# Export for Vercel
__all__ = ["handler"]
