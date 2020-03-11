from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, generics, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from RRHH.models import HrJob, HrCompany
from RRHH.serializers import JobSerializer, CompanySerializer, PasswordSerializer, CompanyCreateSerializer


class JobViewSet(viewsets.ViewSetMixin, generics.ListAPIView):
    queryset = HrJob.objects.all()
    serializer_class = JobSerializer


class JobRetrieve(generics.RetrieveAPIView):
    queryset = HrJob.objects.all()
    serializer_class = JobSerializer


class CompanyListCreate(viewsets.ViewSetMixin, generics.ListCreateAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = HrCompany.objects.all()
    serializer_class = CompanySerializer


class CompanyViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAdminUser]

    def create(self, request):
        serializer = CompanyCreateSerializer(data=request.data)

        if serializer.is_valid():

            if HrCompany.objects.get(email=serializer.data['email']) is None:

                company = HrCompany()
                company.set_password(serializer.data['password'])
                company.name = serializer.data['name']
                company.email = serializer.data['email']
                company.plan_id = serializer.data['plan']

                company.save()

                return Response({"message": "Company has been created"})

            else:
                return Response({"message": "Already exists a Company with this email"})

        else:
            return Response(serializer.errors)

    def list(self, request):
        queryset = HrCompany.objects.filter(is_active=True, is_superuser=False, is_staff=False)
        serializer = CompanySerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            queryset = HrCompany.objects.get(pk=pk, is_superuser=False, is_staff=False)

            if queryset is not None:
                serializer = CompanySerializer(queryset)
                return Response(serializer.data)
        except Exception:
            return Response({"error": "Company does not exists"})

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
