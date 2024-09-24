
from rest_framework.permissions import BasePermission

class UserListPermissions(BasePermission):
   
    def has_permission(self, request, view):
        # Allow read-only access for all users
        if request.method in ['GET', 'HEAD','PUT', 'OPTIONS']:
            return True

        # Check if the user is an admin
        return request.user.is_superuser

class SellerListPermissions(BasePermission):
   
    def has_permission(self, request, view):
        # Allow read-only access for all users
        if request.method in ['GET', 'HEAD','PUT','DELETE', 'OPTIONS']:
            return True
      

        # Check if the user is an admin
        return request.user.is_superuser