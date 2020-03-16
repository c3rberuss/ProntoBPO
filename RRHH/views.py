import django_filters
from django.dispatch import receiver
from django.shortcuts import render

# Create your views here.

from RRHH.filters import JobFilter, ApplicantFilter, CompanyFilter
from rest_framework import viewsets, generics, permissions, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from RRHH.models import HrJob, HrCompany, HrApplicant, HrApplicantViewCount, HrCompanyPlan, HrDepartment, HrRecruitmentDegree
from RRHH.permissions import IsNotLimitExceeded, IsYourSelfOrAdmin
from RRHH.serializers import JobSerializer, CompanySerializer, PasswordSerializer, CompanyCreateSerializer, \
    ApplicantSerializer, ApplicantProfileSerializer, PlanSerializer, DepartmentSerializer, DegreeSerializer
from RRHH.signals import count_view


class JobViewSet(viewsets.ViewSetMixin, mixins.RetrieveModelMixin, generics.ListAPIView):
    queryset = HrJob.objects.all()
    serializer_class = JobSerializer
    filterset_class = JobFilter


class CompanyViewSet(viewsets.ViewSetMixin, mixins.RetrieveModelMixin, generics.ListCreateAPIView,
                     mixins.UpdateModelMixin):
    queryset = HrCompany.objects.filter(is_active=True)
    permission_classes = [IsYourSelfOrAdmin]
    filterset_class = CompanyFilter
    serializer_class = CompanySerializer

    def update(self, request, *args, **kwargs):
        self.serializer_class = CompanySerializer
        return super(CompanyViewSet, self).update(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        self.serializer_class = CompanyCreateSerializer
        return super(CompanyViewSet, self).create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        self.serializer_class = CompanySerializer
        return super(CompanyViewSet, self).list(self, request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = CompanySerializer
        return super(CompanyViewSet, self).retrieve(self, request, *args, **kwargs)

    @action(methods=['patch'], detail=True)
    def set_password(self, request, pk=None):

        company = HrCompany.objects.get(pk=pk)
        serializer = PasswordSerializer(data=request.data)

        if serializer.is_valid():
            company.set_password(serializer.data['password'])
            company.save()
            return Response({'message': 'password changed'})
        else:
            return Response(serializer.errors)

    @action(methods=['patch'], detail=True)
    def renew_plan(self, request, pk=None):
        company = HrCompany.objects.get(pk=pk)
        company.limit_exceeded = False
        company.save()

        return Response({"message": "The plan has been renew"})


class ApplicantViewSet(viewsets.ViewSetMixin, mixins.RetrieveModelMixin, generics.ListAPIView):
    queryset = HrApplicant.objects.all()
    serializer_class = ApplicantSerializer
    filterset_class = ApplicantFilter
    permission_classes = [IsNotLimitExceeded]
    ordering_fields = ['priority']
    ordering = ['-priority']

    def list(self, request, *args, **kwargs):
        self.serializer_class = ApplicantSerializer
        return super(ApplicantViewSet, self).list(self, request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = ApplicantProfileSerializer
        count_view.send(sender=request.user, applicant=self.get_object())
        return super(ApplicantViewSet, self).retrieve(self, request, *args, **kwargs)


class CompanyPlanViewSet(viewsets.ViewSetMixin, generics.ListAPIView):
    queryset = HrCompanyPlan.objects.all()
    serializer_class = PlanSerializer


class DepartmentViewSet(viewsets.ViewSetMixin, generics.ListAPIView):
    queryset = HrDepartment.objects.filter(active=True)
    serializer_class = DepartmentSerializer


class DegreeViewSet(viewsets.ViewSetMixin, generics.ListAPIView):
    queryset = HrRecruitmentDegree.objects.all()
    serializer_class = DegreeSerializer


# Receiver
@receiver(count_view)
def on_count_view(sender, **kwargs):
    applicant = kwargs['applicant']
    count_views = HrApplicantViewCount.objects.filter(company=sender).count()
    limit = sender.plan.no_of_views

    if count_views <= limit and not sender.is_superuser:
        HrApplicantViewCount.objects.get_or_create(company=sender, applicant=applicant)
