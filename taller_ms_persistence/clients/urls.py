from django.urls import path

from . import views

urlpatterns = [
    path('clients/', views.clients_list, name='clients_list'),
     path('interests/', views.interests_list, name='interests_list'),
    path("", views.index, name="index"),
]