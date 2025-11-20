from rest_framework import permissions


class IsModer(permissions.BasePermission):
    """Класс для модераторов"""

    def has_permission(self, request, view):
        return request.user.groups.filter(name="Модераторы").exists()


class IsOwner(permissions.BasePermission):
    """Класс для владельцев"""

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False
