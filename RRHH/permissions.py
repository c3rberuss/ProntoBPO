from rest_framework.permissions import BasePermission
from RRHH.models import HrApplicantViewCount


class IsNotLimitExceeded(BasePermission):

    def has_permission(self, request, view):
        if view.action == "list":
            return True

        count_views = HrApplicantViewCount.objects.filter(company=request.user).count()
        limit = request.user.plan.no_of_views

        if count_views >= limit and not request.user.is_superuser:
            HrApplicantViewCount.objects.filter(company=request.user).delete()
            request.user.limit_exceeded = True
            request.user.save()

        return bool(not request.user.limit_exceeded)
