import django_filters
from rest_framework import serializers
from RRHH.models import HrJob, HrCompany, HrApplicant


class JobSerializer(serializers.HyperlinkedModelSerializer):
    department = serializers.StringRelatedField(many=False)

    class Meta:
        model = HrJob
        fields = ['id', 'name', 'department', 'description', 'requirements', 'state', 'color_class']


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


class ApplicantSerializer(serializers.ModelSerializer):
    categories = serializers.StringRelatedField(many=True, )
    priority = serializers.IntegerField()

    class Meta:
        model = HrApplicant
        fields = ['id', 'partner_name', 'priority', 'categories']


class ApplicantProfileSerializer(serializers.ModelSerializer):
    categories = serializers.StringRelatedField(many=True, )
    priority = serializers.IntegerField()
    job = serializers.StringRelatedField(many=False)
    type = serializers.StringRelatedField(many=False)
    department = serializers.StringRelatedField(many=False)

    class Meta:
        model = HrApplicant
        fields = ['id', 'partner_name', 'priority', 'categories', 'partner_phone', 'partner_mobile', 'name',
                  'description', 'email_from', 'salary_expected', 'type', 'department', 'job']


class PasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = HrCompany
        fields = ['password']
