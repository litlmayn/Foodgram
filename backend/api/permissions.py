from rest_framework import permissions


class IsCurrentUserOrAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if (request.method in permissions.SAFE_METHODS
                and request.user.is_authenticated):
            return True
        return (obj.id == request.user
                or request.user.is_superuser)