# Generated by Django 4.2.18 on 2025-01-23 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0011_alter_schedule_day_of_week'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='admissionrequest',
            name='attached_files',
        ),
        migrations.AlterField(
            model_name='admissionrequest',
            name='student_address',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Адрес ученика'),
        ),
        migrations.DeleteModel(
            name='AdmissionFile',
        ),
    ]
