from django import forms

from .models import Question, AdmissionRequest, UploadedFile, AdditionalActivity, AdditionalActivityRegistration


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

class ActivityRegistrationForm(forms.ModelForm):
    class Meta:
        model = AdditionalActivityRegistration
        fields = ['name', 'email', 'phone', 'activity', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Добавьте комментарий (необязательно)'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Ваш номер телефона'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Ваш email'}),
            'name': forms.TextInput(attrs={'placeholder': 'Ваше имя'}),
        }
        labels = {
            'name': 'Ваше имя',
            'email': 'Ваш email',
            'phone': 'Ваш телефон',
            'activity': 'Выберите услугу',
            'notes': 'Примечания',
        }

class SingleFileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']


class FileUploadForm(forms.ModelForm):
    activity = forms.ModelChoiceField(
        queryset=AdditionalActivity.objects.all(),
        required=False,
        label="Услуга (необязательно)"
    )
    name_file = forms.CharField(
        required=False,
        label="Название документа",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название файла (необязательно)'})
    )

    class Meta:
        model = UploadedFile
        fields = ['file', 'name_file', 'file_type', 'access_level']
        widgets = {
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'file_type': forms.Select(attrs={'class': 'form-control'}),
            'access_level': forms.Select(attrs={'class': 'form-control'}),
        }


class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField(required=True)

    def clean_excel_file(self):
        excel_file = self.cleaned_data.get('excel_file')
        if not excel_file.name.endswith('.xlsx'):
            raise forms.ValidationError("Пожалуйста, загрузите файл формата .xlsx.")
        return excel_file
