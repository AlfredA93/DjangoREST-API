from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Only allow users to edit profile fields if they are the owner"""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
