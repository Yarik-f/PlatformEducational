# Generated by Django 4.2.18 on 2025-01-20 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdditionalActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('blog', 'Новости'), ('announce', 'Объявления'), ('event', 'Мероприятия'), ('schedule', 'Расписание')], default='blog', max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('pub_date', models.DateField(verbose_name='date published')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=50, verbose_name='Фамилия')),
                ('first_name', models.CharField(max_length=50, verbose_name='Имя')),
                ('patronymic', models.CharField(max_length=50, verbose_name='Отчество')),
                ('position', models.CharField(choices=[('director', 'Директор'), ('teacher', 'Учитель')], max_length=50, verbose_name='Должность')),
                ('education', models.TextField(verbose_name='Уровень образования')),
                ('qualification', models.CharField(max_length=255, verbose_name='Квалификация')),
                ('academic_degree', models.CharField(blank=True, max_length=255, null=True, verbose_name='Ученая степень')),
                ('academic_title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Ученое звание')),
                ('qualification_improvement', models.TextField(blank=True, null=True, verbose_name='Повышение квалификации')),
                ('professional_retraining', models.TextField(blank=True, null=True, verbose_name='Профессиональная переподготовка')),
                ('experience_years', models.PositiveIntegerField(verbose_name='Опыт работы (лет)')),
                ('phone', models.CharField(max_length=20, verbose_name='Контактный телефон')),
                ('email', models.EmailField(max_length=254, verbose_name='Адрес электронной почты')),
                ('branch', models.CharField(max_length=255, verbose_name='Филиал')),
                ('educational_programs', models.TextField(blank=True, null=True, verbose_name='Образовательные программы')),
                ('additional_taught', models.ManyToManyField(related_name='teachers', to='school.additionalactivity', verbose_name='Дополнительные услуги')),
                ('subjects_taught', models.ManyToManyField(related_name='teachers', to='school.subject', verbose_name='Преподаваемые дисциплины')),
            ],
        ),
    ]
