from rest_framework.permissions import BasePermission

class IsProductManager(BasePermission):
    #only product manager
    def has_permission(self, request, view):
        return getattr(request.user, "role", None) == "product_manager"