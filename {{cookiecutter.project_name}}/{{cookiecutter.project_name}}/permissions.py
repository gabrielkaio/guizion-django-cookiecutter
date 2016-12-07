from rest_framework import permissions


class IsCreationOrIsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated():
            if view.action == 'create':
                return True
            else:
                return False
        return True


class NoPermissionNeeded(permissions.BasePermission):
    def has_permission(self, request, view):
        return True


class IsAdminOrListNoPermissionNeeded(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'list':
            return True
        else:
            return request.user.is_superuser
