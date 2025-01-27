from django.urls import path, include
from rest_framework.routers import DefaultRouter
from school import views

router = DefaultRouter()
router.register(r'teachers', views.TeacherViewSet, basename='teachers')
router.register(r'schedule', views.ScheduleViewSet, basename='schedule')
router.register(r'activities', views.AdditionalActivityViewSet, basename='activity')
router.register(r'registrations', views.AdditionalActivityRegistrationViewSet, basename='registration')
urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.home_view, name='home'),
    path('teacher/', views.teacher_view, name='teacher'),
    path('teacher/<int:teacher_id>/', views.teacher_detail_view, name='teacher_detail'),
    path('school_life/schedule/', views.schedule, name='schedule'),
    path('school_life/schedule/<int:class_id>/', views.schedule_class, name='schedule_class'),
    path('school_life/<str:category>/', views.school_life_view, name='school_life'),
    path('school_life/blog/<int:blog_id>/', views.school_life_detail_view, name='blog_detail'),

    path('about_school/contacts/', views.contacts_view, name='contacts'),
    path('about_school/facility/', views.facility_list, name='facility'),
    path('about_school/document_all/', views.document_list, name='document_list'),
    path('about_school/paid-services/', views.paid_services, name='paid_services'),
    path('about_school/paid-services/<int:pk>/', views.paid_service_detail, name='paid_service_detail'),
    path('about_school/awards-and-licenses/', views.awards_and_licenses, name='awards_and_licenses'),
    path('register_activity/', views.register_activity, name='register_activity'),
    path('forms/', views.forms_view, name='forms'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('password_change/', views.custom_password_change, name='password_change'),

    path('profile/', views.profile_view, name='profile'),
    path('document/', views.upload_file, name='upload_file'),
    path('document/archive/', views.archive_files, name='archive_files'),
    path('admissions/', views.admission_requests_list, name='admission_requests_list'),
    path('admissions/<int:pk>/', views.admission_request_detail, name='admission_request_detail'),
    path('download/archive/<int:archive_id>/', views.download_archive, name='download_archive'),
    path('download/file/<int:file_id>/', views.download_files, name='download_file'),
    path('classroom/', views.classroom_list, name='classroom_list'),
    path('classroom/<int:class_id>/', views.classroom_detail, name='classroom_detail'),
    path('files/', views.unified_view, name='director_file'),
]
