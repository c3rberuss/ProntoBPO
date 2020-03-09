from rest_framework import serializers
from RRHH.models import HrJob


class JobSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = HrJob
        fields = ['id', 'name', 'department_id', 'description', 'requirements', 'state']
