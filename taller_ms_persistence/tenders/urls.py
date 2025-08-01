from django.urls import path
from . import views

app_name = "tenders"
urlpatterns = [
    path('', views.tenders_list, name='tenders_list'),
    path('create/', views.create_tender, name='create_tender'),
]
