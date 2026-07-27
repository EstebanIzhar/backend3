from rest_framework.permissions import BasePermission, SAFE_METHODS

def is_in_group(user, group_name):
    return user.is_authenticated and user.groups.filter(name=group_name).exists()

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return is_in_group(request.user, 'ADMIN') or request.user.is_superuser

class BookPermission(BasePermission):
    """
    Reglas de Negocio:
    - Ver libros (GET): ADMIN, BIBLIOTECARIO, CLIENTE (Cualquier autenticado).
    - Crear libros (POST): ADMIN, BIBLIOTECARIO.
    - Editar libros (PUT/PATCH): ADMIN, BIBLIOTECARIO.
    - Eliminar libros (DELETE): Solo ADMIN.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        # Ver libros (Métodos de lectura seguros: GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS:
            return True

        # Crear o editar libros
        if request.method in ['POST', 'PUT', 'PATCH']:
            return (
                is_in_group(request.user, 'ADMIN') or 
                is_in_group(request.user, 'BIBLIOTECARIO') or 
                request.user.is_superuser
            )

        # Eliminar libros
        if request.method == 'DELETE':
            return is_in_group(request.user, 'ADMIN') or request.user.is_superuser

        return False