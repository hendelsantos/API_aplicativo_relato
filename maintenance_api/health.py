from django.http import JsonResponse
from django.views import View
from django.db import connection
from django.conf import settings
import datetime

class HealthCheckView(View):
    """
    Endpoint de verificação de saúde da aplicação.
    Usado para monitoramento e load balancers.
    """
    
    def get(self, request):
        """Verificar saúde da aplicação"""
        try:
            # Verificar conexão com banco de dados
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                db_status = "ok"
        except Exception as e:
            db_status = f"error: {str(e)}"
        
        # Informações do sistema
        health_data = {
            "status": "ok" if db_status == "ok" else "error",
            "timestamp": datetime.datetime.now().isoformat(),
            "version": "1.0.0",
            "environment": "development" if settings.DEBUG else "production",
            "database": db_status,
            "services": {
                "api": "ok",
                "database": db_status,
            }
        }
        
        status_code = 200 if health_data["status"] == "ok" else 503
        
        return JsonResponse(health_data, status=status_code)
