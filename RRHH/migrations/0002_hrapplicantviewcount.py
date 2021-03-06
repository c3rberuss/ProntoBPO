# Generated by Django 3.0.4 on 2020-03-13 04:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('RRHH', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HrApplicantViewCount',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('applicant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='RRHH.HrApplicant')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'hr_applicant_view',
            },
        ),
    ]
