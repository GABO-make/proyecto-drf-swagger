from rest_framework import serializers
from .models import Producto, Categoria

class CategoriaSerializer(serializers.ModelSerializer):
    producto_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion', 'fecha_creacion', 'activo', 'producto_count']
        read_only_fields = ['id', 'fecha_creacion', 'producto_count']
    
    def get_producto_count(self, obj):
        return obj.productos.count()

class ProductoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    
    class Meta:
        model = Producto
        fields = [
            'id', 'nombre', 'descripcion', 'precio', 'stock',
            'categoria', 'categoria_nombre', 'fecha_creacion',
            'fecha_actualizacion', 'activo'
        ]
        read_only_fields = ['id', 'fecha_creacion', 'fecha_actualizacion', 'categoria_nombre']
    
    def validate_precio(self, value):
        if value <= 0:
            raise serializers.ValidationError("El precio debe ser mayor a cero")
        return value
    
    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("El stock no puede ser negativo")
        return value