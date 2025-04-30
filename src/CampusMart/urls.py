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
    path('listing/all/', views.view_all, name='view_all'),
    path('inbox/', views.inbox, name='inbox'),
    path('messaging/<int:product_id>/', views.messaging, name='messaging'),
    path('purchase/', views.purchase_listings, name='purchase_listings'),
    path('chat/<int:product_id>/<int:user_id>/', views.chat_with_user, name='chat_with_user'),
]