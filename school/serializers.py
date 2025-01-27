from rest_framework import serializers
from school.models import *

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = [
            'lesson_number',
            'school_class',
            'day_of_week',
            'subject',
            'office',
            'teacher',
            'start_time',
            'end_time'
        ]

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = [
            'id',
            'first_name',
            'last_name',
            'patronymic',
            'email',
            'phone',
        ]

class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ['id', 'file', 'file_type', 'uploaded_at']

class AdditionalActivitySerializer(serializers.ModelSerializer):
    documents = UploadedFileSerializer(many=True)
    teacher = TeacherSerializer()

    class Meta:
        model = AdditionalActivity
        fields = ['id', 'name', 'description', 'price', 'documents', 'teacher']