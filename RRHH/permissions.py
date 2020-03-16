from rest_framework.permissions import BasePermission
from RRHH.models import HrApplicantViewCount, HrCompany
from RRHH.serializers import CompanySerializer


class IsNotLimitExceeded(BasePermission):

    def has_permission(self, request, view):
        if view.action == "list":
            return True

        count_views = HrApplicantViewCount.objects.filter(company=request.user).count()

        if request.user.plan is not None:
            limit = request.user.plan.no_of_views
        else:
            return bool(False or request.user.is_superuser)

        if count_views >= limit and not request.user.is_superuser:
            HrApplicantViewCount.objects.filter(company=request.user).delete()
            request.user.limit_exceeded = True
            request.user.save()

        return bool(not request.user.limit_exceeded or request.user.is_superuser)


class IsYourSelfOrAdmin(BasePermission):

    def has_permission(self, request, view):
        user = request.user

        try:
            company = HrCompany.objects.get(pk=view.kwargs['pk'])
        except:
            return bool(False or user.is_superuser)

        return bool(user.is_superuser or company.id == user.id)
