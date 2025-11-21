# Sistema de Inventario API - Documentación

## Descripción
API RESTful para gestión de inventario construida con Django REST Framework y documentada con Swagger.

## Características
- Gestión completa de productos y categorías
- Control de stock con endpoints personalizados
- Documentación automática con Swagger UI
- Panel de administración Django
- Filtros y búsqueda en endpoints

## Instalación y Configuración

### Prerrequisitos
- Python 3.8+
- pip

### Pasos de instalación
1. Clonar el repositorio
2. Crear entorno virtual: `python -m venv venv`
3. Activar entorno virtual: `venv\Scripts\activate` (Windows) o `source venv/bin/activate` (Linux/Mac)
4. Instalar dependencias: `pip install -r requirements.txt`
5. Aplicar migraciones: `python manage.py migrate`
6. Crear superusuario: `python manage.py createsuperuser`
7. Ejecutar servidor: `python manage.py runserver`

## Documentación de la API

### URLs de Documentación
- **Swagger UI**: http://localhost:8000/swagger/
- **ReDoc**: http://localhost:8000/redoc/
- **Admin Django**: http://localhost:8000/admin/

### Endpoints Principales

#### Productos
- `GET /api/productos/` - Listar todos los productos
- `POST /api/productos/` - Crear nuevo producto
- `GET /api/productos/{id}/` - Obtener producto específico
- `PUT /api/productos/{id}/` - Actualizar producto
- `DELETE /api/productos/{id}/` - Eliminar producto
- `POST /api/productos/{id}/actualizar-stock/` - Actualizar stock
- `GET /api/productos/stock-bajo/` - Productos con stock bajo

#### Categorías
- `GET /api/categorias/` - Listar categorías
- `POST /api/categorias/` - Crear categoría
- `GET /api/categorias/{id}/` - Obtener categoría específica

### Ejemplos de Uso

#### Listar productos con filtros
```http
GET /api/productos/?search=laptop&min_precio=500&max_precio=1500