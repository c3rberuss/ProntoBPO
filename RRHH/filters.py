import django_filters
from django.db.models import Q
from RRHH.models import HrJob, HrApplicant, HrApplicantCategory, HrCompany


class JobFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', method='search_by_name', label='Name')
    department = django_filters.CharFilter(field_name='department__name', lookup_expr='iexact', label='Department')

    def search_by_name(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value)
        )

    class Meta:
        model = HrJob
        fields = []  # ['name', 'department__name']


class ApplicantFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='partner_name', method='search_by_name', label='Name')
    department = django_filters.CharFilter(field_name='department__name', lookup_expr='iexact', label='Department')
    subject = django_filters.CharFilter(field_name='name', lookup_expr='iexact', label='Subject')
    tags = django_filters.ModelChoiceFilter(queryset=HrApplicantCategory.objects.all(), field_name='categories')
    salary = django_filters.NumberFilter(field_name='salary_expected', label='Salary')
    priority = django_filters.NumberFilter(field_name='priority', label='Priority')
    job = django_filters.CharFilter(field_name='job__name', lookup_expr='iexact', label='Job')

    def search_by_name(self, queryset, name, value):
        return queryset.filter(
            Q(partner_name__icontains=value)
        )

    class Meta:
        model = HrApplicant
        fields = []  # ['partner_name', 'priority', 'categories', 'name', 'salary_expected', 'department__name', 'job']


class CompanyFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='iexact', label='Name')
    email = django_filters.CharFilter(field_name='email', lookup_expr='iexact', label='Email')
    plan = django_filters.CharFilter(field_name='plan__name', lookup_expr='iexact', label='Plan')
    limit = django_filters.BooleanFilter(field_name='limit_exceeded', label='Limit exceeded')

    class Meta:
        model = HrCompany
        fields = []  # ['name', 'email', 'plan__name', 'limit_exceeded']
