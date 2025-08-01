# accounts/permissions.py
from rest_framework.permissions import BasePermission
from rest_framework import permissions

class IsAdminRole(permissions.BasePermission):
    def has_permission(self, request, view):
        # Define your permission logic here
        return request.user and request.user.is_staff

class IsUserRole(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_regular_user