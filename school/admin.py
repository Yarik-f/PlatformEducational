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
    list_display = ('name', 'price', 'teacher', 'description')
    list_filter = ('teacher',)

@admin.register(AdditionalActivityRegistration)
class AdditionalActivityRegistrationAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone']


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email']
    search_fields = ['first_name', 'last_name', 'email']
    filter_horizontal = ['subjects_taught']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'question_text']


@admin.register(AdmissionRequest)
class AdmissionRequestAdmin(admin.ModelAdmin):
    list_display = ['parent_full_name', 'last_name', 'first_name', 'grade_applied']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'classroom']


@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    pass


@admin.register(DocumentArchive)
class DocumentArchiveAdmin(admin.ModelAdmin):
    list_display = ['archive']


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    pass


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['school_class', 'day_of_week', 'subject', 'office', 'start_time', 'end_time']


@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'description')


@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'description')


@admin.register(SchoolContactInfo)
class SchoolContactInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'address']


@admin.register(Facility)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ("name", "school_contact", "facility_type", "accessibility")
    list_filter = ("accessibility",)
    search_fields = ("name", "equipment")
    filter_horizontal = ['equipment']


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ["name"]
