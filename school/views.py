import os
import zipfile
from mimetypes import guess_type

from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.contrib.auth import views as auth_views
from django.utils.encoding import smart_str
from rest_framework import viewsets

from school.forms import QuestionForm, AdmissionRequestForm, SingleFileUploadForm
from school.models import *
from school.serializers import TeacherSerializer


def home_view(request):
    positions = Teacher.POSITION_CHOICES
    director = Teacher.objects.filter(position='director')
    director_positions = dict(positions).get('director')
    news = Blog.objects.filter(category='news')
    announce = Blog.objects.filter(category='announce')
    return render(request, 'home_page/home.html',
                  {
                      'news': news,
                      'announces': announce,
                      'director': director,
                      'director_positions': director_positions,
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


def teacher_view(request):
    teachers = Teacher.objects.all()
    return render(request, 'teacher_page/teacher_card.html', {'teachers': teachers})


def teacher_detail_view(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    return render(request, 'teacher_page/teacher_detail.html', {'teacher': teacher})


def contacts_view(request):
    return render(request, 'contacts/contacts.html')


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

    if user.groups.filter(name='Teachers').exists():
        profile = Teacher.objects.get(user=user)
        role = 'Teacher'
    elif user.groups.filter(name='Directors').exists():
        profile = Teacher.objects.get(user=user)
        role = 'Director'
    elif user.groups.filter(name='Students').exists():
        profile = Student.objects.get(user=user)
        role = 'Student'
    else:
        profile = AdmissionRequest.objects.get(user=user)
        role = 'Guest'

    context = {
        'user': user,
        'profile': profile,
        'role': role
    }
    return render(request, 'auth/profile.html', context)


@login_required
def upload_file(request):
    if request.user.groups.filter(name='Students').exists():
        role = 'Student'
    else:
        role = 'Guest'

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

    return render(request, 'auth/profile_documents.html',
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
    role = 'Director'
    admission_requests = AdmissionRequest.objects.all()
    return render(request, 'auth/admission_requests_list.html',
                  {'admission_requests': admission_requests, 'role': role})


@login_required
def admission_request_detail(request, pk):
    role = 'Director'
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

    return render(request, 'auth/admission_request_detail.html', {
        'admission_request': admission_request,
        'uploaded_files': uploaded_files,
        'role': role
    })


@login_required
def download_file(request, file_id):
    document = get_object_or_404(DocumentArchive, id=file_id)

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
def custom_password_change(request):

    if request.user.groups.filter(name='Teachers').exists():
        role = 'Teacher'
    elif request.user.groups.filter(name='Directors').exists():
        role = 'Director'
    elif request.user.groups.filter(name='Students').exists():
        role = 'Student'
    else:
        role = 'Guest'

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

    return render(request, 'auth/password_change.html', {
        'form': form,
        'role': role,
    })

class TeacherViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
