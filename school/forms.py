from django import forms

from .models import Question, AdmissionRequest, UploadedFile


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["full_name", "email", "phone", "question_text"]
        widgets = {
            "question_text": forms.Textarea(attrs={"placeholder": "Введите ваш вопрос"}),
        }

class AdmissionRequestForm(forms.ModelForm):
    class Meta:
        model = AdmissionRequest
        fields = [
            "parent_full_name",
            "parent_passport",
            "parent_id_number",
            "parent_email",
            "last_name",
            "first_name",
            "patronymic",
            "student_passport",
            "student_id_number",
            "grade_applied",
        ]
        widgets = {
            "parent_passport": forms.TextInput(attrs={"placeholder": "Серия и номер паспорта"}),
            "parent_id_number": forms.TextInput(attrs={"placeholder": "ИН паспорта"}),
            "student_passport": forms.TextInput(attrs={"placeholder": "Серия и номер паспорта"}),
            "student_id_number": forms.TextInput(attrs={"placeholder": "ИН паспорта"}),
            "grade_applied": forms.TextInput(attrs={"placeholder": "Например, 10 класс"}),
        }

class SingleFileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']