"""ProntoBPO URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token
from rest_framework import routers
from RRHH.views import JobViewSet, CompanyViewSet, ApplicantViewSet, CompanyPlanViewSet, DepartmentViewSet, \
    DegreeViewSet
from ProntoBPO.settings import DEBUG

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()

router.register('companies', CompanyViewSet, basename='Companies')
router.register('jobs', JobViewSet, basename='Jobs')
router.register('applicants', ApplicantViewSet, basename='Applicants')
router.register('plans', CompanyPlanViewSet, basename='Plans')
router.register('departments', DepartmentViewSet, basename='Departments')
router.register('degrees', DegreeViewSet, basename='Degrees')

urlpatterns = [
    path('api/auth/', obtain_jwt_token),
    path('api/', include(router.urls)),
    path('api/verify/', verify_jwt_token)
]

if DEBUG:
    urlpatterns.append(path('admin/', admin.site.urls))
