from rest_framework import permissions


class IsCurrentUserOrAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (obj.id == request.user
                or request.user.is_superuser)
