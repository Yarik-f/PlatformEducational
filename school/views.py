from django.shortcuts import render, get_object_or_404

from school.forms import QuestionForm, AdmissionRequestForm
from school.models import *


def home_view(request):
    news = Blog.objects.filter(category='news')
    announce = Blog.objects.filter(category='announce')
    return render(request, 'home_page/home.html', {'news': news, 'announces': announce})


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
        elif form_type == "question_form":
            question_form = QuestionForm(request.POST)
            admission_form = AdmissionRequestForm()
            if question_form.is_valid():
                question_form.save()
                success_message = "Ваш вопрос успешно отправлен!"
    else:
        admission_form = AdmissionRequestForm()
        question_form = QuestionForm()

    return render(request, "form/forms_page.html",
                  {
                      "admission_form": admission_form,
                      "question_form": question_form,
                      "success_message": success_message
                  })
