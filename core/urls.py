from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Configuración de Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Sistema de Inventario API",
        default_version='v1',
        description="""
        Documentación completa de la API del Sistema de Inventario.
        
        ## Características principales:
        - Gestión de productos
        - Administración de categorías
        - Control de stock e inventario
        - Reportes de productos con stock bajo
        
        ## Autenticación
        La API actualmente no requiere autenticación para fines de demostración.
        """,
        terms_of_service="https://www.miempresa.com/terminos/",
        contact=openapi.Contact(email="soporte@miempresa.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Admin Django
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/', include('api.urls')),
    
    # Swagger URLs
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', 
            schema_view.without_ui(cache_timeout=0), 
            name='schema-json'),
    path('swagger/', 
         schema_view.with_ui('swagger', cache_timeout=0), 
         name='schema-swagger-ui'),
    path('redoc/', 
         schema_view.with_ui('redoc', cache_timeout=0), 
         name='schema-redoc'),
    
    # Redirección raíz a la documentación
    path('', schema_view.with_ui('redoc', cache_timeout=0)),
]