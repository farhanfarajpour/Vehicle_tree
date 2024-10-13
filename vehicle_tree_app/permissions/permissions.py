from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


# permission_classes = [IsSuperUserOrAdmin, ]
class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if bool(request.user.is_authenticated):
            return True
        raise PermissionDenied("You are not authorized to access this resource.")


class IsSuperUserOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and (request.user.is_superuser and request.user.is_staff):
            return True
        raise PermissionDenied("You are not authorized to access this resource.")


class IsUser(BasePermission):

    def has_permission(self, request, view):
        if bool (request.user and request.user.is_authenticated):
            raise PermissionDenied("You are not authorized to access this resource.")
        return True
    def has_object_permission(self, request, view, obj):
        return obj == request.user
