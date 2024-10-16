from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAutorOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS or request.user == obj.author)
