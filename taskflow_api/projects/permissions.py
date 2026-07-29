from rest_framework import permissions

class IsOwnerOrMember(permissions.BasePermission):
    """
    Permite el acceso solo al dueño del proyecto o a los miembros asignados.
    """
    def has_object_permission(self, request, view, obj):
        # Permiso a nivel de objeto para Project
        if hasattr(obj, 'owner') and hasattr(obj, 'members'):
            return request.user == obj.owner or request.user in obj.members.all()
        return False

class IsTaskAssigneeOrProjectOwner(permissions.BasePermission):
    """
    Permite ver/modificar la tarea al dueño del proyecto o al usuario asignado.
    """
    def has_object_permission(self, request, view, obj):
        return request.user == obj.project.owner or request.user == obj.assigned_to