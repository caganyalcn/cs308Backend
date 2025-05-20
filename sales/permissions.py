from rest_framework.permissions import BasePermission

class IsSalesManager(BasePermission):
    def has_permission(self, request, view):
        return (
            hasattr(request, "user")
            and getattr(request.user, "role", None) == "sales_manager"
        )
