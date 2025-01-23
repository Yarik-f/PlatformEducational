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
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='auth/password_change.html'),
         name='password_change'),

    path('profile/', views.profile_view, name='profile')
]
