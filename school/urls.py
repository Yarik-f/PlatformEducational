from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views
from school import views

router = DefaultRouter()
router.register(r'teachers', views.TeacherViewSet, basename='teachers')
urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.home_view, name='home'),
    path('teacher/', views.teacher_view, name='teacher'),
    path('teacher/<int:teacher_id>/', views.teacher_detail_view, name='teacher_detail'),
    path('school_life/<str:category>/', views.school_life_view, name='school_life'),
    path('school_life/blog/<int:blog_id>/', views.school_life_detail_view, name='blog_detail'),
    path('contacts/', views.contacts_view, name='contacts'),
    path('forms/', views.forms_view, name='forms'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('password_change/', views.custom_password_change, name='password_change'),

    path('profile/', views.profile_view, name='profile'),
    # path('profile/document/', views.document_view, name='document')
    path('document/', views.upload_file, name='upload_file'),
    path('document/archive/', views.archive_files, name='archive_files'),
    path('admissions/', views.admission_requests_list, name='admission_requests_list'),
    path('admissions/<int:pk>/', views.admission_request_detail, name='admission_request_detail'),
    path('download/<int:file_id>/', views.download_file, name='download_file'),
]
