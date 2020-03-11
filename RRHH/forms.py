from django import forms
from RRHH.models import HrCompany


class CompanyForm(forms.ModelForm):
    class Meta:
        model = HrCompany
        exclude = ['date_joined']
