# Generated by Django 4.2.18 on 2025-01-24 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0025_remove_documentarchive_archive_admission'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadedfile',
            name='file_type',
            field=models.CharField(choices=[('admission', 'Поступление'), ('student', 'Студентам'), ('teacher', 'Учителям')], max_length=10, null=True, verbose_name='Тип документа'),
        ),
        migrations.AlterField(
            model_name='admissionrequest',
            name='is_approved',
            field=models.CharField(choices=[('no', 'Нет'), ('yes', 'Да')], max_length=10, verbose_name='Подтверждение'),
        ),
    ]
