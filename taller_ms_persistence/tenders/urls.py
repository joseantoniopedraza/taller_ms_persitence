from django.urls import path
from . import views

app_name = "tenders"
urlpatterns = [
    path('tenders/', views.tenders_list, name='tenders_list'),
]
