from rest_framework.permissions import BasePermission


class IsNotLimitExceeded(BasePermission):

    def has_permission(self, request, view):
        return bool(not request.user.limit_exceeded)
