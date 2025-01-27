from django.conf.global_settings import DEFAULT_FROM_EMAIL
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string
from transliterate import translit


class Blog(models.Model):
    CATEGORY_CHOICES = [
        ('news', 'Новости'),
        ('announce', 'Объявления'),
        ('event', 'Мероприятия'),
    ]
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='blog')
    title = models.CharField(max_length=100)
    description = models.TextField()
    pub_date = models.DateField('date published')
    image = models.ImageField(upload_to='images/blog', blank=True, null=True)

    def __str__(self):
        return self.title


class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class AdditionalActivity(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена", null=True)
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE, related_name='activities',
                                verbose_name="Учитель", null=True)
    documents = models.ForeignKey(
        'UploadedFile', on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="related_activities",
        verbose_name="Документы"
    )

    def __str__(self):
            return self.name

from django.db import models

class AdditionalActivityRegistration(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=15, verbose_name="Телефон")
    activity = models.ForeignKey(
        'AdditionalActivity',
        on_delete=models.CASCADE,
        related_name='registrations',
        verbose_name="Платная услуга"
    )
    date_registered = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")
    notes = models.TextField(blank=True, null=True, verbose_name="Примечания")

    def __str__(self):
        return f"{self.name} - {self.activity.name}"


class Teacher(models.Model):
    POSITION_CHOICES = [
        ('director', 'Директор'),
        ('management', 'Руководство'),
        ('teacher', 'Учитель'),
    ]

    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    patronymic = models.CharField(max_length=50, verbose_name="Отчество")
    position = models.CharField(max_length=50, choices=POSITION_CHOICES, verbose_name="Должность")
    education = models.TextField(verbose_name="Уровень образования")
    qualification = models.CharField(max_length=255, verbose_name="Квалификация")
    academic_degree = models.CharField(max_length=255, blank=True, null=True, verbose_name="Ученая степень")
    academic_title = models.CharField(max_length=255, blank=True, null=True, verbose_name="Ученое звание")
    qualification_improvement = models.TextField(blank=True, null=True, verbose_name="Повышение квалификации")
    professional_retraining = models.TextField(blank=True, null=True, verbose_name="Профессиональная переподготовка")
    experience_years = models.PositiveIntegerField(verbose_name="Опыт работы (лет)")
    phone = models.CharField(max_length=20, verbose_name="Контактный телефон")
    email = models.EmailField(verbose_name="Адрес электронной почты")
    branch = models.CharField(max_length=255, verbose_name="Филиал")
    educational_programs = models.TextField(blank=True, null=True, verbose_name="Образовательные программы")
    subjects_taught = models.ManyToManyField(Subject, related_name="teachers", verbose_name="Преподаваемые дисциплины")
    image = models.ImageField(upload_to='images/teacher', blank=True, null=True, verbose_name="Фото преподавателя")
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Пользователь")

    def __str__(self):
        return f"{self.last_name} {self.first_name} - {self.position}"


@receiver(post_save, sender=Teacher)
def create_user_for_teacher(sender, instance, created, **kwargs):
    if created and not instance.user:

        first_name_translit = translit(instance.first_name, 'ru', reversed=True).lower()
        last_name_translit = translit(instance.last_name, 'ru', reversed=True).lower()

        username = f"{first_name_translit}.{last_name_translit}"
        if User.objects.filter(username=username).exists():
            username += get_random_string(length=4)

        password = get_random_string(length=8)

        user = User.objects.create_user(
            username=username,
            email=instance.email,
            password=password
        )
        user.first_name = instance.first_name
        user.last_name = instance.last_name

        if instance.position == 'director':
            group, _ = Group.objects.get_or_create(name='Directors')
        elif instance.position == 'management':
            group, _ = Group.objects.get_or_create(name='Managements')
        else:
            group, _ = Group.objects.get_or_create(name='Teachers')
        user.groups.add(group)
        user.save()

        instance.user = user
        instance.save()

        subject = 'Ваша учетная запись создана'
        message = (
            f"Здравствуйте, {instance.first_name} {instance.last_name}!\n\n"
            f"Для вас была создана учетная запись в системе.\n"
            f"Ваши данные для входа:\n"
            f"Логин: {username}\n"
            f"Пароль: {password}\n\n"
            f"Рекомендуем сменить пароль после первого входа.\n\n"
            f"С уважением,\nАдминистрация школы."
        )
        send_mail(
            subject,
            message,
            DEFAULT_FROM_EMAIL,
            [instance.email],
            fail_silently=False,
        )


class Question(models.Model):
    full_name = models.CharField(max_length=255, verbose_name="ФИО")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Телефон", blank=True, null=True)
    question_text = models.TextField(verbose_name="Вопрос")
    submission_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата подачи")

    def __str__(self):
        return f"Вопрос от {self.full_name} ({self.email})"


class AdmissionRequest(models.Model):
    APPROVED_CHOICES = [
        ('no', 'Нет'),
        ('yes', 'Да'),
    ]
    parent_full_name = models.CharField(max_length=255, verbose_name="ФИО родителя")
    parent_passport = models.CharField(
        max_length=50,
        verbose_name="Паспорт родителя",
        blank=True,
        null=True
    )
    parent_id_number = models.CharField(
        max_length=50,
        verbose_name="ИН родителя",
        blank=True,
        null=True
    )
    parent_email = models.EmailField(verbose_name="Email родителя или ученика", null=True)
    last_name = models.CharField(max_length=255, verbose_name="Фамилия ученика", null=True)
    first_name = models.CharField(max_length=255, verbose_name="Имя ученика", null=True)
    patronymic = models.CharField(max_length=255, verbose_name="Отчество ученика", null=True)
    student_passport = models.CharField(
        max_length=50,
        verbose_name="Паспорт ученика",
        blank=True,
        null=True
    )
    student_id_number = models.CharField(
        max_length=50,
        verbose_name="ИН ученика",
        blank=True,
        null=True
    )
    grade_applied = models.CharField(max_length=10, verbose_name="Класс для поступления")
    submission_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата подачи")
    is_approved = models.CharField(max_length=10, choices=APPROVED_CHOICES, verbose_name="Подтверждение")
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Пользователь")


@receiver(post_save, sender=AdmissionRequest)
def create_user_for_student(sender, instance, created, **kwargs):
    if created and not instance.user:

        first_name_translit = translit(instance.first_name, 'ru', reversed=True).lower()
        last_name_translit = translit(instance.last_name, 'ru', reversed=True).lower()

        username = f"{first_name_translit}.{last_name_translit}"
        if User.objects.filter(username=username).exists():
            username += get_random_string(length=4)

        password = get_random_string(length=8)

        user = User.objects.create_user(
            username=username,
            email=instance.parent_email,
            password=password
        )
        user.first_name = instance.first_name
        user.last_name = instance.last_name

        group, _ = Group.objects.get_or_create(name='Guest')
        user.groups.add(group)
        user.save()

        instance.user = user
        instance.save()

        subject = "Ваши данные для входа"
        message = f"""
                Здравствуйте, {instance.parent_full_name}!

                Ваша заявка на поступление была успешно отправлена.
                В профиле нужно загрузить фотографии паспорта как родителя так и Вас.
                После загрузки документов ожидайте подтверждение.
                Ваши данные для входа:

                Логин: {username}
                Пароль: {password}

                Пожалуйста, используйте эти данные для входа в систему.
                """
        send_mail(
            subject,
            message,
            DEFAULT_FROM_EMAIL,
            [instance.parent_email],
            fail_silently=False,
        )


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="student", null=True)
    last_name = models.CharField(max_length=255, verbose_name="Фамилия ученика", null=True)
    first_name = models.CharField(max_length=255, verbose_name="Имя ученика", null=True)
    patronymic = models.CharField(max_length=255, verbose_name="Отчество ученика", null=True)
    parent_email = models.EmailField(verbose_name="Email родителя или ученика", null=True)
    student_passport = models.CharField(max_length=50, verbose_name="Номер паспорт")
    student_id = models.CharField(max_length=50, verbose_name="ИН паспорта")
    address = models.TextField(verbose_name="Адрес", blank=True, null=True)
    classroom = models.ForeignKey('Class', on_delete=models.SET_NULL, verbose_name="Класс", null=True,
                                  related_name="students")

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.classroom.name}"


class UploadedFile(models.Model):
    CATEGORY_CHOICES = [
        ('local_regulations', 'Локальные нормативные акты'),
        ('paid_service', 'Платные услуги'),
    ]

    ACCESS_CHOICES = [
        ('all', 'Все пользователи'),
        ('students', 'Только студенты'),
        ('teachers', 'Только учителя'),
        ('management', 'Только руководство'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="uploaded_files")
    name_file = models.CharField(max_length=50, verbose_name='Наименование', null=True)
    file = models.FileField(upload_to="uploads/documents/")
    file_type = models.CharField(max_length=50, choices=CATEGORY_CHOICES, verbose_name='Категория документа', null=True)
    access_level = models.CharField(max_length=15, choices=ACCESS_CHOICES, verbose_name='Доступ', default='all')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    activities = models.ManyToManyField(
        'AdditionalActivity',
        blank=True,
        related_name="associated_files",
        verbose_name="Платные услуги"
    )
    apply_to_all_services = models.BooleanField(
        default=False,
        verbose_name="Применить ко всем платным услугам"
    )

    def __str__(self):
        return f"{self.file.name}"


class DocumentArchive(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='Пользователь')
    archive = models.FileField(upload_to='archives/', verbose_name='Архив документов')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')


class Class(models.Model):
    name = models.CharField(max_length=10, verbose_name="Класс")
    teacher = models.ForeignKey(
        'Teacher', on_delete=models.SET_NULL, verbose_name="Классный руководитель", blank=True, null=True
    )
    max_students = models.PositiveIntegerField(default=25, verbose_name="Максимальное количество студентов")

    def __str__(self):
        return self.name


class Schedule(models.Model):
    DAY_OF_WEEK_CHOICES = [
        ('monday', 'Понедельник'),
        ('tuesday', 'Вторник'),
        ('wednesday', 'Среда'),
        ('thursday', 'Четверг'),
        ('friday', 'Пятница'),
        ('saturday', 'Суббота'),
    ]
    lesson_number = models.PositiveSmallIntegerField(verbose_name='Номер урока', null=True)
    school_class = models.ForeignKey(Class, on_delete=models.CASCADE, verbose_name="Класс")
    day_of_week = models.CharField(max_length=20, choices=DAY_OF_WEEK_CHOICES, verbose_name="День недели")
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, null=True,)
    office = models.PositiveIntegerField(verbose_name="Кабинет", null=True)
    teacher = models.ForeignKey(
        'Teacher', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Учитель"
    )
    start_time = models.TimeField(verbose_name="Время начала урока")
    end_time = models.TimeField(verbose_name="Время окончания урока")

    def __str__(self):
        return self.school_class

class Award(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название награды")
    description = models.TextField(blank=True, verbose_name="Описание награды")
    image = models.ImageField(upload_to='awards/', blank=True, null=True, verbose_name="Фото награды")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.title


class License(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название лицензии")
    description = models.TextField(blank=True, verbose_name="Описание лицензии")
    image = models.ImageField(upload_to='licenses/', blank=True, null=True, verbose_name="Фото лицензии")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.title

class SchoolContactInfo(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название школы")
    address = models.TextField(verbose_name="Адрес", blank=True)
    phone = models.CharField(max_length=20, verbose_name="Телефон", blank=True)
    email = models.EmailField(verbose_name="Электронная почта", blank=True)
    begin_time = models.TimeField(verbose_name='Начало рабочего дня', null=True, blank=True)
    end_time = models.TimeField(verbose_name='Конец рабочего дня', null=True)

    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name="Широта",
        blank=True,
        null=True,
        help_text="Координаты для отображения на карте"
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name="Долгота",
        blank=True,
        null=True,
        help_text="Координаты для отображения на карте"
    )

    def __str__(self):
        return self.name


class Equipment(models.Model):
    name = models.CharField(max_length=255, verbose_name="Наименование оборудования")

    def __str__(self):
        return self.name

class Facility(models.Model):
    FACILITY_CHOICES = [
        ('classroom', 'Кабинет'),
        ('practical_object', 'Объект для практических занятий'),
    ]
    facility_type = models.CharField(
        max_length=50,
        choices=FACILITY_CHOICES,
        verbose_name="Тип объекта",
        default='classroom'
    )
    school_contact = models.ForeignKey(SchoolContactInfo, on_delete=models.CASCADE, verbose_name="Адрес")
    name = models.CharField(max_length=255, verbose_name="Наименование кабинета")
    equipment = models.ManyToManyField(Equipment, verbose_name="Оснащенность кабинета")
    accessibility = models.CharField(
        max_length=255,
        choices=[("partial", "Частичная"), ("full", "Полная"), ("none", "Отсутствует")],
        verbose_name="Приспособленность для инвалидов",
        default="partial"
    )

    def __str__(self):
        return f"{self.name} ({self.school_contact})"
