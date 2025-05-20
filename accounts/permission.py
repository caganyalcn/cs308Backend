from rest_framework.permissions import BasePermission

class IsProductManager(BasePermission):

    def has_permission(self, request, view):
        return getattr(request.user, "role", None) == "product_manager"

class IsSalesManager(BasePermission):
    
   
    def has_permission(self, request, view):
        return getattr(request.user, "role", None) == "sales_manager"