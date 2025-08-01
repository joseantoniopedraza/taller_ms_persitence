from django.urls import path

from . import views

app_name = "clients"
urlpatterns = [
    path('', views.clients_list, name='clients_list'),
     path('interests/', views.interests_list, name='interests_list'),
    path('create/', views.create_client_with_interests, name='create_client_with_interests'),
]