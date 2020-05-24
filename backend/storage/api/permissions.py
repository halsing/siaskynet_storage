from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit and see it.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user == "AnonymousUser":
            return False
        return bool(obj.owner == user)
