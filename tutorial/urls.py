from django.urls import path
from . import views


urlpatterns = [
    path('', views.homepage, name='site-home'),
    path('register/', views.register, name='site-register'),
    path('profile/', views.profile, name='site-profile'),
    path('courses/', views.courses, name='site-courses'),
    path('registercourse/', views.register_for_course, name='register-course'),
    path('validate_register/', views.validate_chapter, name='validate-chapter'),
    # path('test/', views.testing, name="test"),
]
