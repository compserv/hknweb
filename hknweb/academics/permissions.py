from rest_framework import permissions


class HasPermissionOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        # !TODO Check if user has permissions
        return request.user.is_authenticated
