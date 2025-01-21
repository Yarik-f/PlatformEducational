from django.db import models

class Blog(models.Model):
    CATEGORY_CHOICES = [
        ('news', 'Новости'),
        ('announce', 'Объявления'),
        ('event', 'Мероприятия'),
        ('schedule', 'Расписание'),
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

    def __str__(self):
        return self.name

class Teacher(models.Model):
    POSITION_CHOICES = [
        ('director', 'Директор'),
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
    additional_taught = models.ManyToManyField(AdditionalActivity, related_name="teachers", blank=True, null=True, verbose_name="Дополнительные услуги")
    image = models.ImageField(upload_to='images/teacher', blank=True, null=True, verbose_name="Фото преподавателя")

    def __str__(self):
        return f"{self.last_name} {self.first_name} - {self.position}"

class Question(models.Model):
    full_name = models.CharField(max_length=255, verbose_name="ФИО")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Телефон", blank=True, null=True)
    question_text = models.TextField(verbose_name="Вопрос")
    submission_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата подачи")

    def __str__(self):
        return f"Вопрос от {self.full_name} ({self.email})"


class AdmissionRequest(models.Model):
    parent_full_name = models.CharField(max_length=255, verbose_name="ФИО родителя")
    parent_passport = models.CharField(max_length=50, verbose_name="Паспортные данные родителя")
    student_full_name = models.CharField(max_length=255, verbose_name="ФИО ученика")
    student_passport = models.CharField(max_length=50, verbose_name="Паспортные данные ученика")
    grade_applied = models.CharField(max_length=10, verbose_name="Класс для поступления")
    attached_files = models.FileField(upload_to="admission_files/", verbose_name="Прикреплённые файлы", blank=True, null=True)
    submission_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата подачи")

    def __str__(self):
        return f"Поступление: {self.student_full_name} ({self.grade_applied})"

