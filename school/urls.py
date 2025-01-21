from django.urls import path

from school import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('teacher/', views.teacher_view, name='teacher'),
    path('teacher/<int:teacher_id>/', views.teacher_detail_view, name='teacher_detail'),
    path('school_life/', views.school_life_view, name='school_life'),
    path('school_life/<str:category>/', views.school_life_view, name='school_life_category'),
    path('school_life/blog/<int:blog_id>/', views.school_life_detail_view, name='blog_detail'),
    path('contacts/', views.contacts_view, name='contacts'),
    path('forms/', views.forms_view, name='forms'),

]
