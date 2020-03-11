from django.contrib import admin
from RRHH.models import HrJob, HrApplicant, HrCompany, HrCompanyPlan
from RRHH.forms import CompanyForm


class CompanyAdmin(admin.ModelAdmin):
    fields = ('name', 'email', 'password', 'plan', 'limit_exceeded', 'is_staff', 'is_superuser', 'is_active')
    exclude = ('date_joined',)
    readonly_fields = []
    form = CompanyForm

    def get_readonly_fields(self, request, obj=None):
        if obj is not None:
            self.readonly_fields.append('password')

        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        if 'password' not in self.readonly_fields:
            obj.set_password(obj.password)

        super().save_model(request, obj, form, change)


# Register your models here.

admin.site.register(HrJob)
admin.site.register(HrApplicant)
admin.site.register(HrCompany, CompanyAdmin)
admin.site.register(HrCompanyPlan)
