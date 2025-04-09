# CampusMart urls.py

from django.urls import path

from . import views

app_name = 'CampusMart'

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),    
    path('logout/', views.logout_view, name='logout'),
]