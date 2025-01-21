from django import forms

from .models import Question, AdmissionRequest

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
            "student_full_name",
            "student_passport",
            "grade_applied",
            "attached_files"
        ]
        widgets = {
            "parent_passport": forms.TextInput(attrs={"placeholder": "Серия и номер паспорта"}),
            "student_passport": forms.TextInput(attrs={"placeholder": "Серия и номер паспорта"}),
            "grade_applied": forms.TextInput(attrs={"placeholder": "Например, 10 класс"}),
        }