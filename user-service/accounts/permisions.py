from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.has_admin_permission()

class IsManagerUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.has_manager_permission()
