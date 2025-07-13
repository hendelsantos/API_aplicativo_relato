"""
Sistema de Relatório de Manutenção - URLs Principais
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API de Autenticação JWT
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # APIs das aplicações
    path('api/auth/', include('authentication.urls')),
    path('api/parts/', include('parts.urls')),
    path('api/locations/', include('locations.urls')),
    path('api/activities/', include('activities.urls')),
]

# Configuração para servir arquivos de media em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
