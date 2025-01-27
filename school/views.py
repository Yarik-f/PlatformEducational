import os
import zipfile
from mimetypes import guess_type

import openpyxl
from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect, Http404, FileResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.encoding import smart_str
from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from school.forms import QuestionForm, AdmissionRequestForm, SingleFileUploadForm, FileUploadForm, ExcelUploadForm, \
    ActivityRegistrationForm
from school.models import *
from school.serializers import TeacherSerializer, ScheduleSerializer, AdditionalActivitySerializer, \
    AdditionalActivityRegistrationSerializer
from school.utils import export_schedule_to_excel, import_schedule_from_excel_with_update


def access_role(request):
    if request.user.groups.filter(name='Teachers').exists():
        profile = Teacher.objects.get(user=request.user)
        role = 'Teacher'
    elif request.user.groups.filter(name='Directors').exists():
        profile = Teacher.objects.get(user=request.user)
        role = 'Director'
    elif request.user.groups.filter(name='Students').exists():
        profile = Student.objects.get(user=request.user)
        role = 'Student'
    else:
        profile = AdmissionRequest.objects.get(user=request.user)
        role = 'Guest'
    return profile, role


def home_view(request):
    positions = Teacher.POSITION_CHOICES
    director = Teacher.objects.filter(position='director')
    director_positions = dict(positions).get('director')
    news = Blog.objects.filter(category='news')
    announce = Blog.objects.filter(category='announce')
    school_contact = SchoolContactInfo.objects.all()
    return render(request, 'home_page/home.html',
                  {
                      'news': news,
                      'announces': announce,
                      'director': director,
                      'director_positions': director_positions,
                      'school_contact': school_contact
                  })


def school_life_view(request, category=None):
    categories = Blog.CATEGORY_CHOICES
    if category:
        blogs = Blog.objects.filter(category=category)
        current_category = dict(categories).get(category)
    else:
        blogs = Blog.objects.all()
        current_category = None
    return render(request, 'school_life/school_life.html', {
        'categories': categories,
        'blogs': blogs,
        'current_category': current_category,
    })


def school_life_detail_view(request, blog_id):
    categories = Blog.CATEGORY_CHOICES
    blog = get_object_or_404(Blog, id=blog_id)
    return render(request, 'school_life/blog.html', {
        'categories': categories,
        'blog': blog,
    })


def schedule(request):
    classes = Class.objects.all()
    return render(request, 'schedule/schedule.html', {
        'classes': classes,
    })


def schedule_class(request, class_id):
    school_class = Class.objects.get(id=class_id)
    if request.method == 'POST':
        if 'export_schedule' in request.POST:
            return export_schedule_to_excel(school_class)
    schedule = Schedule.objects.filter(school_class=school_class).order_by('day_of_week', 'lesson_number')
    return render(request, 'schedule/schedule_class.html', {
        'school_class': school_class,
        'schedule': schedule
    })


def teacher_view(request):
    teachers = Teacher.objects.all()
    return render(request, 'about_school/teacher_page/teacher_card.html', {'teachers': teachers})


def teacher_detail_view(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    return render(request, 'about_school/teacher_page/teacher_detail.html', {'teacher': teacher})


def about_school_view(request):
    school_contact = SchoolContactInfo.objects.all()
    for i in school_contact:
        print(type(i.longitude))
    return render(request, 'about_school/about_school.html', {'school_contact': school_contact})


def contacts_view(request):
    school_contact = SchoolContactInfo.objects.all()
    for i in school_contact:
        print(type(i.longitude))
    return render(request, 'about_school/contacts/contacts.html', {'school_contact': school_contact})


def facility_list(request):
    facilities = Facility.objects.all()
    return render(request, 'about_school/facility/facility.html', {'facilities': facilities})


def forms_view(request):
    success_message = None
    admission_form = AdmissionRequestForm()
    question_form = QuestionForm()
    if request.method == "POST":
        form_type = request.POST.get("form_type")
        if form_type == "admission_form":
            admission_form = AdmissionRequestForm(request.POST, request.FILES)
            question_form = QuestionForm()
            if admission_form.is_valid():
                admission_form.save()
                success_message = "Заявка на поступление успешно отправлена!"
                admission_form = AdmissionRequestForm()
        elif form_type == "question_form":
            question_form = QuestionForm(request.POST)
            admission_form = AdmissionRequestForm()
            if question_form.is_valid():
                question_form.save()
                success_message = "Ваш вопрос успешно отправлен!"
                question_form = QuestionForm()
    else:
        admission_form = AdmissionRequestForm()
        question_form = QuestionForm()

    return render(request, "form/forms_page.html",
                  {
                      "admission_form": admission_form,
                      "question_form": question_form,
                      "success_message": success_message
                  })


def login_view(request):
    error = None
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            error = "Неверное имя пользователя или пароль"
    else:
        form = AuthenticationForm()

    return render(request, 'auth/login.html', {'form': form, 'error': error})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def profile_view(request):
    user = request.user
    profile = access_role(request)[0]
    role = access_role(request)[1]

    context = {
        'user': user,
        'profile': profile,
        'role': role
    }
    return render(request, 'profile/profile.html', context)


@login_required
def upload_file(request):
    role = access_role(request)[1]

    if request.method == "POST":
        form = SingleFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)
            uploaded_file.user = request.user
            uploaded_file.file_type = 'admission'
            uploaded_file.save()
            return redirect('upload_file')
    else:
        form = SingleFileUploadForm()

    user_files = UploadedFile.objects.filter(user=request.user, file_type='admission')
    user_archive = DocumentArchive.objects.filter(user=request.user)

    return render(request, 'profile/profile_documents.html',
                  {
                      'form': form,
                      'user_files': user_files,
                      'user_archive': user_archive,
                      'role': role
                  })


@login_required
def archive_files(request):
    if request.method == "POST":
        user_files = UploadedFile.objects.filter(user=request.user)

        if not user_files.exists():
            return HttpResponseRedirect(reverse('upload_file'))

        first_name = translit(request.user.first_name, 'ru', reversed=True).lower()
        last_name = translit(request.user.last_name, 'ru', reversed=True).lower()

        archive_name = f"{last_name}_{first_name}_documents.zip"
        archive_path = os.path.join("media/archives", archive_name)

        with zipfile.ZipFile(archive_path, 'w') as zipf:
            for user_file in user_files:
                file_path = user_file.file.path
                zipf.write(file_path, os.path.basename(file_path))

        DocumentArchive.objects.create(user=request.user, archive=f"archives/{archive_name}")

        for user_file in user_files:
            file_path = user_file.file.path
            if os.path.exists(file_path):
                os.remove(file_path)
            user_file.delete()

        return HttpResponseRedirect(reverse('upload_file'))

    return HttpResponseRedirect(reverse('upload_file'))


@login_required
def admission_requests_list(request):
    role = access_role(request)[1]
    admission_requests = AdmissionRequest.objects.all()
    return render(request, 'profile/admission_requests_list.html',
                  {'admission_requests': admission_requests, 'role': role})


@login_required
def admission_request_detail(request, pk):
    role = access_role(request)[1]
    admission_request = get_object_or_404(AdmissionRequest, pk=pk)
    uploaded_files = DocumentArchive.objects.filter(user=admission_request.user)

    if request.method == 'POST':
        decision = request.POST.get('is_approved')

        if decision == 'yes':
            grade = admission_request.grade_applied
            available_classes = Class.objects.filter(name__startswith=grade).annotate(student_count=Count('students'))

            class_to_assign = None

            for classroom in available_classes:
                if classroom.student_count < 25:
                    class_to_assign = classroom
                    break

            if not class_to_assign:
                next_suffix = chr(65 + available_classes.count())
                new_class_name = f"{grade}{next_suffix}"
                class_to_assign = Class.objects.create(name=new_class_name)

            student = Student.objects.create(
                user=admission_request.user,
                last_name=admission_request.last_name,
                first_name=admission_request.first_name,
                patronymic=admission_request.patronymic,
                parent_email=admission_request.parent_email,
                student_passport=admission_request.student_passport,
                student_id=admission_request.student_id_number,
                address="",
                classroom=class_to_assign,
            )
            student.save()

            group = Group.objects.get(name='Students')
            admission_request.user.groups.clear()
            admission_request.user.groups.add(group)

            admission_request.is_approved = 'yes'
            admission_request.delete()

            send_mail(
                'Поздравляем с поступлением!',
                f'Уважаемый {admission_request.last_name} {admission_request.first_name}, '
                f'вы зачислены в класс {class_to_assign.name}.',
                DEFAULT_FROM_EMAIL,
                [admission_request.user.email],
                fail_silently=False,
            )

            return redirect('admission_requests_list')

        elif decision == 'no':
            send_mail(
                'Решение о поступлении',
                f'Уважаемый {admission_request.last_name} {admission_request.first_name}, '
                f'к сожалению, вы не поступили.',
                DEFAULT_FROM_EMAIL,
                [admission_request.user.email],
                fail_silently=False,
            )

            admission_request.is_approved = 'no'
            admission_request.delete()
            return redirect('admission_requests_list')

    return render(request, 'profile/admission_request_detail.html', {
        'admission_request': admission_request,
        'uploaded_files': uploaded_files,
        'role': role
    })


@login_required
def classroom_list(request):
    role = access_role(request)[1]
    classrooms = Class.objects.all()
    return render(request, 'profile/classroom_list.html',
                  {'classrooms': classrooms, 'role': role})


@login_required
def classroom_detail(request, class_id):
    role = access_role(request)[1]
    classroom = get_object_or_404(Class, id=class_id)
    students = Student.objects.filter(classroom=classroom)
    teachers = Teacher.objects.all()

    if request.method == 'POST':
        teacher_id = request.POST.get('teacher')
        if teacher_id:
            teacher = Teacher.objects.get(id=teacher_id)
            classroom.teacher = teacher
            classroom.save()

    return render(request, 'profile/classroom_detail.html', {
        'classroom': classroom,
        'students': students,
        'teachers': teachers,
        'role': role
    })


@login_required
def download_archive(request, archive_id):
    document = get_object_or_404(DocumentArchive, id=archive_id)

    if document.user != request.user and not request.user.groups.filter(name='Directors').exists():
        return HttpResponse("У вас нет доступа к этому файлу.", status=403)

    file_path = document.archive.path
    file_name = document.archive.name.split('/')[-1]
    mime_type, _ = guess_type(file_path)

    try:
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type=mime_type or "application/octet-stream")
            response['Content-Disposition'] = f'attachment; filename="{smart_str(file_name)}"'
            return response
    except FileNotFoundError:
        raise Http404("Файл не найден.")


@login_required
def download_files(request, file_id):

    file_instance = get_object_or_404(UploadedFile, id=file_id)

    if file_instance.file_type == "management" and not request.user.is_staff:
        raise Http404("У вас нет доступа к этому файлу.")
    if file_instance.file_type == "teacher" and not request.user.groups.filter(
            name__in=["Teachers", "Directors"]).exists():
        raise Http404("У вас нет доступа к этому файлу.")
    if file_instance.file_type == "student" and not request.user.is_authenticated:
        raise Http404("Только зарегистрированные пользователи могут скачать этот файл.")

    response = FileResponse(file_instance.file.open(), as_attachment=True)
    response['Content-Disposition'] = f'attachment; filename="{file_instance.file.name}"'
    return response


@login_required
def custom_password_change(request):
    role = access_role(request)[1]
    print(role)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Вы успешно сменили пароль!")
            return redirect('profile')
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки.")
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'profile/password_change.html', {
        'form': form,
        'role': role,
    })


@login_required
def unified_view(request):
    active_tab = request.POST.get('tab', 'upload-tab')
    role = access_role(request)[1]

    if request.method == 'POST':
        if active_tab == 'upload-tab':
            form = FileUploadForm(request.POST, request.FILES)
            if form.is_valid():
                file_instance = form.save(commit=False)
                file_instance.user = request.user
                file_instance.save()

                if not file_instance.name_file:
                    file_instance.name_file = file_instance.file.name

                file_instance.save()

                activity = form.cleaned_data.get('activity')
                if activity:
                    activity.documents = file_instance
                    activity.save()

                messages.success(request, "Файл успешно загружен!")
                return redirect(f'{request.path}?tab=upload-tab')
            else:
                messages.error(request, "Ошибка при загрузке файла. Проверьте данные.")

        elif active_tab == 'schedule-tab':
            if 'excel_file' in request.FILES:
                excel_file = request.FILES['excel_file']
                success, message = import_schedule_from_excel_with_update(excel_file)
                if success:
                    messages.success(request, message)
                else:
                    messages.error(request, message)
                return redirect(f'{request.path}?tab=schedule-tab')
            elif 'export_schedule' in request.POST:
                return export_schedule_to_excel()

    file_form = FileUploadForm()
    schedule_form = ExcelUploadForm()
    activities = AdditionalActivity.objects.all()
    files = UploadedFile.objects.all()

    return render(request, 'profile/upload_files.html', {
        'active_tab': active_tab,
        'file_form': file_form,
        'schedule_form': schedule_form,
        'activities': activities,
        'files': files,
        'role': role
    })


def document_list(request):
    # Получение всех документов
    documents = UploadedFile.objects.all()

    # Фильтр по категории из GET-запроса
    category_filter = request.GET.get('category')
    if category_filter:
        documents = documents.filter(file_type=category_filter)

    user = request.user
    if not user.is_superuser:
        if user.groups.filter(name='students').exists():
            documents = documents.filter(access_level__in=['all', 'students'])
        elif user.groups.filter(name='teachers').exists():
            documents = documents.filter(access_level__in=['all', 'teachers'])
        elif user.groups.filter(name='management').exists():
            documents = documents.filter(access_level__in=['all', 'management'])
        else:
            documents = documents.filter(access_level='all')

    categories = UploadedFile.CATEGORY_CHOICES

    return render(request, 'about_school/document_list/document_list.html', {
        'documents': documents,
        'categories': categories,
    })


def paid_services(request):
    services = AdditionalActivity.objects.all()
    return render(request, 'about_school/paid_services/paid_services.html', {'services': services})


def paid_service_detail(request, pk):
    service = get_object_or_404(AdditionalActivity, pk=pk)
    return render(request, 'about_school/paid_services/paid_service_detail.html', {'service': service})

def awards_and_licenses(request):
    awards = Award.objects.all().order_by('-created_at')
    licenses = License.objects.all().order_by('-created_at')
    return render(request, 'about_school/awards_and_licenses/awards_and_licenses.html', {'awards': awards, 'licenses': licenses})

def register_activity(request):
    if request.method == 'POST':
        form = ActivityRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Вы успешно записались на услугу!")
            return redirect('register_activity')
        else:
            messages.error(request, "Ошибка при записи на услугу. Проверьте введённые данные.")
    else:
        form = ActivityRegistrationForm()

    activities = AdditionalActivity.objects.all()
    return render(request, 'activites/register_activity.html', {
        'form': form,
        'activities': activities
    })
class ScheduleViewSet(ReadOnlyModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        class_id = self.request.query_params.get('class_id')
        class_name = self.request.query_params.get('class_name')

        if not class_id and not class_name:
            raise ValidationError("Укажите параметр 'class_id' или 'class_name' для фильтрации.")

        if class_id:
            queryset = queryset.filter(school_class__id=class_id)
        elif class_name:
            queryset = queryset.filter(school_class__name=class_name)

        return queryset


class TeacherViewSet(ReadOnlyModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class AdditionalActivityViewSet(ReadOnlyModelViewSet):
    queryset = AdditionalActivity.objects.select_related('teacher').prefetch_related('documents')
    serializer_class = AdditionalActivitySerializer

class AdditionalActivityRegistrationViewSet(viewsets.ModelViewSet):
    queryset = AdditionalActivityRegistration.objects.all()
    serializer_class = AdditionalActivityRegistrationSerializer