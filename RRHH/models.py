from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User, PermissionsMixin, AbstractUser
from django.db import models
from django.utils import timezone

from RRHH.managers import CustomUserManager

colors = ('ribbon-two-primary', 'ribbon-two-secondary', 'ribbon-two-info', 'ribbon-two-danger', 'ribbon-two-warning',
          'ribbon-two-success', 'ribbon-two-pink', 'ribbon-two-purple', 'ribbon-two-dark')


class HrApplicantCategory(models.Model):
    name = models.CharField(unique=True, max_length=100)
    color = models.IntegerField(blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    write_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'hr_applicant_category'


class HrApplicant(models.Model):
    email_cc = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100)
    active = models.BooleanField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    email_from = models.CharField(max_length=128, blank=True, null=True)
    probability = models.FloatField(blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    date_closed = models.DateTimeField(blank=True, null=True)
    date_open = models.DateTimeField(blank=True, null=True)
    date_last_stage_update = models.DateTimeField(blank=True, null=True)
    priority = models.CharField(max_length=100, blank=True, null=True)
    job = models.ForeignKey('HrJob', models.DO_NOTHING, blank=True, null=True)
    salary_proposed_extra = models.CharField(max_length=100, blank=True, null=True)
    salary_expected_extra = models.CharField(max_length=100, blank=True, null=True)
    salary_proposed = models.FloatField(blank=True, null=True)
    salary_expected = models.FloatField(blank=True, null=True)
    availability = models.DateField(blank=True, null=True)
    partner_name = models.CharField(max_length=100, blank=True, null=True)
    partner_phone = models.CharField(max_length=32, blank=True, null=True)
    partner_mobile = models.CharField(max_length=32, blank=True, null=True)
    type = models.ForeignKey('HrRecruitmentDegree', models.DO_NOTHING, blank=True, null=True)
    department = models.ForeignKey('HrDepartment', models.DO_NOTHING, blank=True, null=True)
    delay_close = models.FloatField(blank=True, null=True)
    color = models.IntegerField(blank=True, null=True)
    emp = models.ForeignKey('HrEmployee', models.DO_NOTHING, blank=True, null=True)
    kanban_state = models.CharField(max_length=100)
    write_date = models.DateTimeField(blank=True, null=True)
    categories = models.ManyToManyField(HrApplicantCategory,
                                        through="HrApplicantHrApplicantCategoryRel",
                                        through_fields=('hr_applicant', 'hr_applicant_category'))

    def __str__(self):
        return self.partner_name

    class Meta:
        verbose_name = "Applicant"
        verbose_name_plural = "Applicants"
        managed = False
        db_table = 'hr_applicant'


class HrApplicantHrApplicantCategoryRel(models.Model):
    hr_applicant = models.ForeignKey(HrApplicant, models.DO_NOTHING)
    hr_applicant_category = models.ForeignKey(HrApplicantCategory, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'hr_applicant_hr_applicant_category_rel'


class HrDepartment(models.Model):
    name = models.CharField(max_length=100)
    complete_name = models.CharField(max_length=100, blank=True, null=True)
    active = models.BooleanField(blank=True, null=True)
    parent = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    manager = models.ForeignKey('HrEmployee', models.DO_NOTHING, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    color = models.IntegerField(blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    write_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hr_department'

    def __str__(self):
        return self.name


class HrDepartmentMailChannelRel(models.Model):
    hr_department = models.ForeignKey(HrDepartment, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'hr_department_mail_channel_rel'


class HrDepartureWizard(models.Model):
    departure_reason = models.CharField(max_length=100, blank=True, null=True)
    departure_description = models.TextField(blank=True, null=True)
    plan = models.ForeignKey('HrPlan', models.DO_NOTHING, blank=True, null=True)
    employee = models.ForeignKey('HrEmployee', models.DO_NOTHING)
    create_date = models.DateTimeField(blank=True, null=True)
    write_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hr_departure_wizard'


class HrEmployee(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    active = models.BooleanField(blank=True, null=True)
    gender = models.CharField(max_length=100, blank=True, null=True)
    marital = models.CharField(max_length=100, blank=True, null=True)
    spouse_complete_name = models.CharField(max_length=100, blank=True, null=True)
    spouse_birthdate = models.DateField(blank=True, null=True)
    children = models.IntegerField(blank=True, null=True)
    place_of_birth = models.CharField(max_length=100, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    ssnid = models.CharField(max_length=100, blank=True, null=True)
    sinid = models.CharField(max_length=100, blank=True, null=True)
    identification_id = models.CharField(max_length=100, blank=True, null=True)
    passport_id = models.CharField(max_length=100, blank=True, null=True)
    permit_no = models.CharField(max_length=100, blank=True, null=True)
    visa_no = models.CharField(max_length=100, blank=True, null=True)
    visa_expire = models.DateField(blank=True, null=True)
    additional_note = models.TextField(blank=True, null=True)
    certificate = models.CharField(max_length=100, blank=True, null=True)
    study_field = models.CharField(max_length=100, blank=True, null=True)
    study_school = models.CharField(max_length=100, blank=True, null=True)
    emergency_contact = models.CharField(max_length=100, blank=True, null=True)
    emergency_phone = models.CharField(max_length=100, blank=True, null=True)
    km_home_work = models.IntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    color = models.IntegerField(blank=True, null=True)
    barcode = models.CharField(unique=True, max_length=100, blank=True, null=True)
    pin = models.CharField(max_length=100, blank=True, null=True)
    departure_reason = models.CharField(max_length=100, blank=True, null=True)
    departure_description = models.TextField(blank=True, null=True)
    department = models.ForeignKey(HrDepartment, models.DO_NOTHING, blank=True, null=True)
    job = models.ForeignKey('HrJob', models.DO_NOTHING, blank=True, null=True)
    job_title = models.CharField(max_length=100, blank=True, null=True)
    work_phone = models.CharField(max_length=100, blank=True, null=True)
    mobile_phone = models.CharField(max_length=100, blank=True, null=True)
    work_email = models.CharField(max_length=100, blank=True, null=True)
    work_location = models.CharField(max_length=100, blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    write_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hr_employee'

    def __str__(self):
        return self.name


class HrEmployeeCategory(models.Model):
    name = models.CharField(unique=True, max_length=100)
    color = models.IntegerField(blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    write_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hr_employee_category'


class HrJob(models.Model):
    name = models.CharField(max_length=100)
    expected_employees = models.IntegerField(blank=True, null=True)
    no_of_employee = models.IntegerField(blank=True, null=True)
    no_of_recruitment = models.IntegerField(blank=True, null=True)
    no_of_hired_employee = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    requirements = models.TextField(blank=True, null=True)
    department = models.ForeignKey(HrDepartment, models.DO_NOTHING, blank=True, null=True)
    state = models.CharField(max_length=100)
    create_date = models.DateTimeField(blank=True, null=True)
    write_date = models.DateTimeField(blank=True, null=True)
    manager = models.ForeignKey(HrEmployee, models.DO_NOTHING, blank=True, null=True)
    color = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def color_class(self):
        index = self.color if self.color is not None else 0
        class_color = colors[index] if len(colors) > index else colors[0]
        return "ribbon-two " + class_color

    class Meta:
        verbose_name = "Job"
        verbose_name_plural = "Jobs"
        managed = False
        db_table = 'hr_job'


class HrJobHrRecruitmentStageRel(models.Model):
    hr_recruitment_stage = models.ForeignKey('HrRecruitmentStage', models.DO_NOTHING)
    hr_job = models.ForeignKey(HrJob, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'hr_job_hr_recruitment_stage_rel'


class HrPlan(models.Model):
    name = models.CharField(max_length=100)
    active = models.BooleanField(blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    write_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hr_plan'


class HrPlanActivityType(models.Model):
    summary = models.CharField(max_length=100, blank=True, null=True)
    responsible = models.CharField(max_length=100)
    note = models.TextField(blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    write_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hr_plan_activity_type'


class HrPlanHrPlanActivityTypeRel(models.Model):
    hr_plan = models.ForeignKey(HrPlan, models.DO_NOTHING)
    hr_plan_activity_type = models.ForeignKey(HrPlanActivityType, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'hr_plan_hr_plan_activity_type_rel'


class HrPlanWizard(models.Model):
    plan = models.ForeignKey(HrPlan, models.DO_NOTHING, blank=True, null=True)
    employee = models.ForeignKey(HrEmployee, models.DO_NOTHING)
    create_date = models.DateTimeField(blank=True, null=True)
    write_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hr_plan_wizard'


class HrRecruitmentDegree(models.Model):
    name = models.CharField(unique=True, max_length=100)
    sequence = models.IntegerField(blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    write_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hr_recruitment_degree'

    def __str__(self):
        return self.name


class HrRecruitmentSource(models.Model):
    job = models.ForeignKey(HrJob, models.DO_NOTHING, blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    write_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hr_recruitment_source'


class HrRecruitmentStage(models.Model):
    name = models.CharField(max_length=100)
    sequence = models.IntegerField(blank=True, null=True)
    requirements = models.TextField(blank=True, null=True)
    fold = models.BooleanField(blank=True, null=True)
    legend_blocked = models.CharField(max_length=100)
    legend_done = models.CharField(max_length=100)
    legend_normal = models.CharField(max_length=100)
    create_date = models.DateTimeField(blank=True, null=True)
    write_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hr_recruitment_stage'


class HrCompanyPlan(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    no_of_views = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Plan"
        verbose_name_plural = "Plans"
        db_table = 'hr_company_plan'


class HrCompany(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=175)
    plan = models.ForeignKey(HrCompanyPlan, on_delete=models.CASCADE, null=True)
    limit_exceeded = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', ]

    @property
    def no_views(self):
        return HrApplicantViewCount.objects.filter(company=self).count()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        db_table = 'hr_company'


class HrApplicantViewCount(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(HrCompany, on_delete=models.CASCADE, null=False)
    applicant = models.ForeignKey(HrApplicant, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'hr_applicant_view'
