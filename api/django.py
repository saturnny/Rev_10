"""
Django Vercel Serverless Function
Alternative approach with Django
"""
import json
import os
import sys

# Add Django to path
sys.path.append(os.path.dirname(__file__))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vercel_settings')

try:
    from django.core.wsgi import get_wsgi_application
    from django.http import JsonResponse
    
    app = get_wsgi_application()
    
    def django_handler(request):
        """Django handler for Vercel"""
        try:
            # Convert Vercel request to Django format
            method = request.get('method', 'GET')
            path = request.get('path', '/')
            
            if path == '/':
                return JsonResponse({
                    'message': 'Time Tracking API with Django',
                    'status': 'healthy',
                    'framework': 'Django'
                })
            
            elif path == '/api/health':
                return JsonResponse({
                    'status': 'ok',
                    'service': 'time-tracking',
                    'environment': 'vercel',
                    'framework': 'Django'
                })
                
            else:
                return JsonResponse({
                    'error': 'Not Found',
                    'message': f'Path {path} not found',
                    'available_paths': ['/', '/api/health']
                }, status=404)
                
        except Exception as e:
            return JsonResponse({
                'error': 'Internal Server Error',
                'message': str(e),
                'framework': 'Django'
            }, status=500)
    
    # Export handler
    handler = django_handler
    
except ImportError:
    # Fallback if Django not available
    def handler(request):
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'error': 'Django not available',
                'message': 'Django framework not installed'
            })
        }
