from rest_framework.permissions import BasePermission


class IsNotLimitExceeded(BasePermission):

    def has_permission(self, request, view):
        if view.action == "list":
            return True

        return bool(not request.user.limit_exceeded)
