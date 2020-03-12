import django_filters
from django.shortcuts import render

# Create your views here.

from django_filters import rest_framework as filters
from RRHH.filters import JobFilter, ApplicantFilter, CompanyFilter
from rest_framework import viewsets, generics, permissions, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from RRHH.models import HrJob, HrCompany, HrApplicant
from RRHH.permissions import IsNotLimitExceeded
from RRHH.serializers import JobSerializer, CompanySerializer, PasswordSerializer, CompanyCreateSerializer, \
    ApplicantSerializer, ApplicantProfileSerializer


class JobViewSet(viewsets.ViewSetMixin, mixins.RetrieveModelMixin, generics.ListAPIView):
    queryset = HrJob.objects.all()
    serializer_class = JobSerializer
    filterset_class = JobFilter


class CompanyViewSet(viewsets.ViewSetMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, generics.ListAPIView):
    queryset = HrCompany.objects.filter(is_active=True, is_superuser=False, is_staff=False)
    permission_classes = [permissions.IsAdminUser]
    filterset_class = CompanyFilter
    serializer_class = CompanySerializer

    def create(self, request, *args, **kwargs):
        self.serializer_class = CompanyCreateSerializer
        return super(CompanyViewSet, self).create(self, request, *args, **kwargs)

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

    def list(self, request, *args, **kwargs):
        self.serializer_class = ApplicantSerializer
        return super(ApplicantViewSet, self).list(self, request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = ApplicantProfileSerializer
        return super(ApplicantViewSet, self).retrieve(self, request, *args, **kwargs)
