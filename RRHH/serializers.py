from rest_framework import serializers
from RRHH.models import HrJob, HrCompany, HrCompanyPlan


class JobSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = HrJob
        fields = ['id', 'name', 'department_id', 'description', 'requirements', 'state', 'color_class']


class CompanySerializer(serializers.ModelSerializer):
    plan = serializers.StringRelatedField(many=False)

    class Meta:
        model = HrCompany
        fields = ['id', 'name', 'email', 'plan', 'limit_exceeded']


class CompanyCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    plan = serializers.IntegerField(required=True)
    password = serializers.CharField(required=True)
    name = serializers.CharField(required=True)

    class Meta:
        model = HrCompany
        exclude = ['groups', 'user_permissions']


class PasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = HrCompany
        fields = ['password']
