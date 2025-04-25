# CampusMart urls.py

from django.urls import path

from . import views

app_name = 'CampusMart'

urlpatterns = [
    path('', views.index, name='index'),
    path('listing/create/', views.create_listing, name='create_listing'),
    path('listings/mylistings/', views.my_listings, name='my_listings'),
    path('listing/<int:product_id>/update/', views.update_listing, name='update_listing'),
    path('listing/<int:product_id>/delete/', views.delete_listing, name='delete_listing'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),    
    path('logout/', views.logout_view, name='logout'),
]