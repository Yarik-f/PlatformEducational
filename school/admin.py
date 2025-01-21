from django.contrib import admin
from django.utils.safestring import mark_safe

from school.models import *


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('category', 'title', 'pub_date')

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(AdditionalActivity)
class AdditionalActivityAdmin(admin.ModelAdmin):
    pass

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email']
    search_fields = ['first_name', 'last_name', 'email']
    filter_horizontal = ['subjects_taught', 'additional_taught']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'question_text']

@admin.register(AdmissionRequest)
class AdmissionRequestAdmin(admin.ModelAdmin):
    list_display = ['parent_full_name', 'student_full_name', 'grade_applied', 'file_link']

    def file_link(self, obj):
        if obj.attached_files:
            return mark_safe(f'<a href="{obj.attached_files.url}" download>Скачать</a>')
        return "Нет файла"
    file_link.allow_tags = True
    file_link.short_description = "Скачать файл"