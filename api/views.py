from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Producto, Categoria
from .serializers import ProductoSerializer, CategoriaSerializer

class CategoriaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar categorías de productos.
    
    Proporciona operaciones CRUD completas para las categorías
    del sistema de inventario.
    """
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    
    @swagger_auto_schema(
        operation_description="Obtiene la lista de todas las categorías",
        responses={
            200: CategoriaSerializer(many=True),
            400: "Error en la solicitud"
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Crea una nueva categoría",
        request_body=CategoriaSerializer,
        responses={
            201: CategoriaSerializer,
            400: "Datos de entrada inválidos"
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class ProductoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar productos del inventario.
    
    Permite realizar operaciones CRUD completas sobre los productos,
    incluyendo búsqueda, filtrado y gestión de stock.
    """
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    
    @swagger_auto_schema(
        operation_description="""
        Obtiene la lista completa de productos.
        
        Puede ser filtrada por parámetros de búsqueda en el query string.
        """,
        manual_parameters=[
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description="Buscar productos por nombre",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'categoria',
                openapi.IN_QUERY,
                description="Filtrar por categoría ID",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'min_precio',
                openapi.IN_QUERY,
                description="Filtrar por precio mínimo",
                type=openapi.TYPE_NUMBER
            ),
            openapi.Parameter(
                'max_precio',
                openapi.IN_QUERY,
                description="Filtrar por precio máximo",
                type=openapi.TYPE_NUMBER
            ),
            openapi.Parameter(
                'activo',
                openapi.IN_QUERY,
                description="Filtrar por estado activo",
                type=openapi.TYPE_BOOLEAN
            )
        ],
        responses={200: ProductoSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Crea un nuevo producto en el inventario",
        request_body=ProductoSerializer,
        responses={
            201: ProductoSerializer,
            400: "Datos de entrada inválidos"
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Obtiene los detalles de un producto específico",
        responses={
            200: ProductoSerializer,
            404: "Producto no encontrado"
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        method='post',
        operation_description="""
        Actualiza el stock de un producto.
        
        Permite incrementar o decrementar la cantidad disponible
        en el inventario.
        """,
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['cantidad'],
            properties={
                'cantidad': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="Cantidad a agregar (positivo) o quitar (negativo)"
                ),
                'motivo': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Motivo del ajuste de inventario"
                )
            }
        ),
        responses={
            200: openapi.Response(
                description="Stock actualizado exitosamente",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'producto': openapi.Schema(type=openapi.TYPE_STRING),
                        'nuevo_stock': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'mensaje': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            ),
            400: "Cantidad inválida o insuficiente stock",
            404: "Producto no encontrado"
        }
    )
    @action(detail=True, methods=['post'], url_path='actualizar-stock')
    def actualizar_stock(self, request, pk=None):
        """
        Endpoint personalizado para actualizar el stock de un producto.
        """
        producto = self.get_object()
        cantidad = request.data.get('cantidad')
        motivo = request.data.get('motivo', 'Ajuste de inventario')
        
        if cantidad is None:
            return Response(
                {'error': 'La cantidad es requerida'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            cantidad = int(cantidad)
            nuevo_stock = producto.actualizar_stock(cantidad)
            
            return Response({
                'producto': producto.nombre,
                'nuevo_stock': nuevo_stock,
                'mensaje': f'Stock actualizado: {cantidad} unidades. Motivo: {motivo}'
            })
            
        except ValueError as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @swagger_auto_schema(
        method='get',
        operation_description="Obtiene productos con stock bajo (menos de 10 unidades)",
        responses={200: ProductoSerializer(many=True)}
    )
    @action(detail=False, methods=['get'], url_path='stock-bajo')
    def stock_bajo(self, request):
        """
        Endpoint para obtener productos con stock bajo.
        """
        productos_bajo_stock = Producto.objects.filter(stock__lt=10, activo=True)
        serializer = self.get_serializer(productos_bajo_stock, many=True)
        return Response(serializer.data)
