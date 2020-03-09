from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from RRHH.models import HrJob
from RRHH.serializers import JobSerializer


class JobViewSet(viewsets.ModelViewSet):
    queryset = HrJob.objects.all()
    serializer_class = JobSerializer
